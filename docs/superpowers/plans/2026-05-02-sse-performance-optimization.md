# SSE 通信性能优化 实施计划

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 在 2Mbps FRP 中转场景下优化前后端通信延迟，SSE 增量推送 + 降级轮询合并 + 请求优先级 + 静态资源缓存。

**Architecture:** 后端 SSE 推送改为增量模式（只推变化模块 + 30s 全量保底），新增 `/status-summary` 合并降级接口，静态资源加版本化强缓存。前端改造 SSE 消费端支持增量更新，降级轮询从 5 请求合并为 1 请求，SSE 重连使用指数退避，用户操作期间暂停后台轮询。

**Tech Stack:** Python FastAPI + asyncio SSE, Vanilla JS + jQuery, SQLite（不变）

**设计文档偏差说明：** 原设计中的「前端 JS 拆分」（index.js 137KB → core.js 35KB）因 index.js 是 2825 行单体 IIFE，抽取核心逻辑会造成大规模重构，风险高。改为所有改动在 index.js 内 inline 完成，功能收益等效。JS 拆分留待后续独立迭代。

---

## 文件结构

| 文件 | 改动 | 说明 |
|------|------|------|
| `app/routes/events.py` | 修改 | 新增 `/status-summary` 端点 |
| `app/core.py` | 修改 | SSE 增量推送 + 静态缓存中间件 |
| `app/routes/pages.py` | 修改 | 传递 asset_version 到模板 |
| `templates/index.html` | 修改 | script 引用加版本号 |
| `static/js/index.js` | 修改 | SSE 增量消费 + 降级合并 + 指数退避 + 请求优先级 |

**不改：** `static/js/modules/` 下所有文件、后端其他路由、SQLite 结构。

---

### Task 1: 新增 GET /status-summary 降级轮询合并接口

**Files:** `app/routes/events.py`

- [ ] **Step 1: 在 events.py 添加 /status-summary 路由**

`app/routes/events.py` 当前内容（37 行）：

```python
import asyncio
import json

from fastapi import APIRouter, Request
from fastapi.responses import StreamingResponse

from ..core import *  # noqa: F401,F403

router = APIRouter()


@router.get("/events")
async def stream_events(request: Request) -> StreamingResponse:
    queue: asyncio.Queue[str] = asyncio.Queue(maxsize=8)
    ui_event_subscribers.add(queue)
    cfg = get_config()
    queue.put_nowait(json.dumps(build_ui_state_payload(cfg), ensure_ascii=False))

    async def event_stream() -> AsyncIterator[str]:
        try:
            while True:
                if await request.is_disconnected():
                    break
                try:
                    payload = await asyncio.wait_for(queue.get(), timeout=UI_HEARTBEAT_SECONDS)
                except asyncio.TimeoutError:
                    yield ": keepalive\n\n"
                    continue
                yield f"retry: {UI_EVENT_RETRY_MS}\nevent: state\ndata: {payload}\n\n"
        finally:
            ui_event_subscribers.discard(queue)

    return StreamingResponse(
        event_stream(),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"},
    )
```

在文件末尾追加新端点（第 38 行之后）：

```python

@router.get("/status-summary")
async def get_status_summary(request: Request) -> Dict[str, Any]:
    cfg = get_config()
    return build_ui_state_payload(cfg)
```

- [ ] **Step 2: 验证 Python 语法**

```bash
PYTHONPYCACHEPREFIX=/tmp/115-media-hub-pycache .venv/bin/python -m compileall app/routes/events.py
```
Expected: Compile successful.

- [ ] **Step 3: 启动 dev server 测试端点**

```bash
.venv/bin/python -m uvicorn main:app --host 0.0.0.0 --port 18080 &
sleep 2
curl -s http://localhost:18080/status-summary | python3 -c "import sys,json; d=json.load(sys.stdin); print('Keys:', list(d.keys()))"
```
Expected: `Keys: ['main', 'monitor', 'subscription', 'sign115', 'cookie_health', 'resource_channel_sync']`

- [ ] **Step 4: 提交**

```bash
git add app/routes/events.py
git commit -m "feat: add /status-summary endpoint for merged fallback polling"
```

---

### Task 2: 后端 SSE 增量推送

**Files:** `app/core.py`

- [ ] **Step 1: 添加增量推送状态变量**

在 `app/core.py` 第 3182 行 `ui_event_subscribers: Set[asyncio.Queue[str]] = set()` 之后，第 3183 行之前插入：

```python
# SSE incremental broadcast state
_last_broadcast_hashes: Dict[str, str] = {}
_last_full_broadcast_ts: float = 0.0
UI_FULL_BROADCAST_INTERVAL_SECONDS = 30.0
```

- [ ] **Step 2: 改造 build_ui_state_payload 支持增量模式**

找到 `build_ui_state_payload` 函数（约 3773 行，当前签名为 `def build_ui_state_payload(cfg=None, log_limit=UI_STATUS_STREAM_LOG_TAIL_LIMIT)`）。

将整个函数替换为：

```python
def build_ui_state_payload(
    cfg: Optional[Dict[str, Any]] = None,
    log_limit: int = UI_STATUS_STREAM_LOG_TAIL_LIMIT,
    incremental: bool = False,
) -> Dict[str, Any]:
    active_cfg = cfg or get_config()
    full = {
        "main": build_main_status_payload(log_limit=log_limit),
        "monitor": build_monitor_status_payload(active_cfg, log_limit=log_limit),
        "subscription": build_subscription_status_payload(active_cfg, log_limit=log_limit),
        "sign115": build_sign115_status_payload(active_cfg),
        "cookie_health": build_cookie_health_payload(active_cfg),
        "resource_channel_sync": build_resource_channel_sync_payload(),
    }
    if not incremental:
        return full

    changed = []
    delta: Dict[str, Any] = {}
    for key, value in full.items():
        module_hash = hashlib.md5(
            json.dumps(value, ensure_ascii=False, sort_keys=True).encode("utf-8")
        ).hexdigest()
        if module_hash != _last_broadcast_hashes.get(key, ""):
            changed.append(key)
            delta[key] = value
            _last_broadcast_hashes[key] = module_hash

    delta["_changed"] = changed
    return delta
```

注意：`hashlib` 已在 core.py 第 3 行导入，`json` 已在第 4 行导入。无需添加导入。

- [ ] **Step 3: 改造 flush_ui_state_updates 支持增量推送 + 30s 全量保底**

找到 `flush_ui_state_updates` 函数（约 4225 行），将整个函数替换为：

```python
async def flush_ui_state_updates(delay: float) -> None:
    global ui_push_pending, ui_push_task, _last_full_broadcast_ts
    try:
        await asyncio.sleep(max(0.0, delay))
        while ui_push_pending:
            ui_push_pending = False
            now_ts = time.time()
            force_full = (now_ts - _last_full_broadcast_ts) >= UI_FULL_BROADCAST_INTERVAL_SECONDS
            cfg = get_config()
            payload_dict = build_ui_state_payload(
                cfg,
                incremental=not force_full,
            )
            if force_full:
                _last_full_broadcast_ts = now_ts
            payload = json.dumps(payload_dict, ensure_ascii=False)
            await broadcast_ui_state(payload)
            if ui_push_pending:
                await asyncio.sleep(UI_PUSH_DEBOUNCE_SECONDS)
    finally:
        ui_push_task = None
```

- [ ] **Step 4: 确认 SSE 首帧全量推送**

`app/routes/events.py` 第 17 行首帧推送 `build_ui_state_payload(cfg)` 默认 `incremental=False`，无需修改。

- [ ] **Step 5: 验证 Python 语法**

```bash
PYTHONPYCACHEPREFIX=/tmp/115-media-hub-pycache .venv/bin/python -m compileall app/core.py
```
Expected: Compile successful.

- [ ] **Step 6: 提交**

```bash
git add app/core.py
git commit -m "feat: add SSE incremental push with 30s full snapshot fallback"
```

---

### Task 3: 静态资源缓存

**Files:** `app/core.py`, `app/routes/pages.py`, `templates/index.html`

- [ ] **Step 1: 添加缓存中间件**

在 `app/core.py` 第 230 行 `app.add_middleware(GZipMiddleware, minimum_size=1024)` 之后插入：

```python
class _StaticCacheMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        response = await call_next(request)
        path = request.url.path.lower()
        if path.startswith("/static/") and any(
            path.endswith(ext) for ext in (".js", ".css", ".svg", ".ico", ".png", ".woff2")
        ):
            response.headers["Cache-Control"] = "public, max-age=31536000, immutable"
        return response

app.add_middleware(_StaticCacheMiddleware)
```

确认 `from starlette.middleware.base import BaseHTTPMiddleware` 已在 core.py 中存在（用于 GZipMiddleware 等）。如果没有则添加。

- [ ] **Step 2: 确认模板已有 asset_version 变量**

查看 `app/routes/pages.py` 中渲染 index 的路由，搜索 `asset_version`：

```bash
grep -n "asset_version\|TemplateResponse" app/routes/pages.py
```

如果尚未传递 `asset_version`，在渲染 index 的路由函数中添加版本读取：

```python
import json as _json

version_path = os.path.join(BASE_DIR, "version.json")
asset_version = "0"
try:
    with open(version_path, "r") as f:
        ver_data = _json.load(f)
        asset_version = str(ver_data.get("version", "0")).strip() or "0"
except Exception:
    pass
```

然后在 `TemplateResponse` 的 context 中添加 `"asset_version": asset_version`。

- [ ] **Step 3: 更新 index.html script 引用**

检查 `templates/index.html` 第 233-244 行，所有 script 标签已使用 `?v={{ asset_version }}`。确认 CSS 引用（第 14 行）也已使用。

如果 `asset_version` 之前由其他机制提供，确保所有 `<script src="...">` 和 `<link href="...">` 末尾带有 `?v={{ asset_version }}`。

- [ ] **Step 4: 验证 Python 语法**

```bash
PYTHONPYCACHEPREFIX=/tmp/115-media-hub-pycache .venv/bin/python -m compileall app/core.py app/routes/pages.py
```

- [ ] **Step 5: 验证缓存头**

```bash
.venv/bin/python -m uvicorn main:app --host 0.0.0.0 --port 18080 &
sleep 2
curl -sI http://localhost:18080/static/js/index.js?v=0.3.7 | grep -i cache-control
```
Expected: `cache-control: public, max-age=31536000, immutable`

- [ ] **Step 6: 提交**

```bash
git add app/core.py app/routes/pages.py templates/index.html
git commit -m "feat: add static resource cache headers with versioned URLs"
```

---

### Task 4: 前端 SSE 增量消费

**Files:** `static/js/index.js`

- [ ] **Step 1: 改造 connectStatusStream 中 state 事件处理**

`static/js/index.js` 找到 `connectStatusStream` 函数（约 1672 行）。

将第 1682-1694 行的 `addEventListener('state', ...)` 代码块：

```javascript
            statusEventSource.addEventListener('state', (event) => {
                try {
                    const payload = JSON.parse(event.data || '{}');
                    stopStatusFallbackPolling();
                    applyMainState(payload.main);
                    applyMonitorState(payload.monitor);
                    applySubscriptionState(payload.subscription);
                    applySign115State(payload.sign115);
                    applyCookieHealthState(payload.cookie_health);
                    applyResourceChannelSyncState(payload.resource_channel_sync);
                } catch (err) {
                    console.warn('Status stream parse failed', err);
                }
            });
```

替换为：

```javascript
            statusEventSource.addEventListener('state', (event) => {
                try {
                    const payload = JSON.parse(event.data || '{}');
                    stopStatusFallbackPolling();
                    const changed = Array.isArray(payload._changed) ? payload._changed : null;
                    if (changed) {
                        if (changed.includes('main') && payload.main) applyMainState(payload.main);
                        if (changed.includes('monitor') && payload.monitor) applyMonitorState(payload.monitor);
                        if (changed.includes('subscription') && payload.subscription) applySubscriptionState(payload.subscription);
                        if (changed.includes('sign115') && payload.sign115) applySign115State(payload.sign115);
                        if (changed.includes('cookie_health') && payload.cookie_health) applyCookieHealthState(payload.cookie_health);
                        if (changed.includes('resource_channel_sync') && payload.resource_channel_sync) applyResourceChannelSyncState(payload.resource_channel_sync);
                    } else {
                        if (payload.main) applyMainState(payload.main);
                        if (payload.monitor) applyMonitorState(payload.monitor);
                        if (payload.subscription) applySubscriptionState(payload.subscription);
                        if (payload.sign115) applySign115State(payload.sign115);
                        if (payload.cookie_health) applyCookieHealthState(payload.cookie_health);
                        if (payload.resource_channel_sync) applyResourceChannelSyncState(payload.resource_channel_sync);
                    }
                } catch (err) {
                    console.warn('Status stream parse failed', err);
                }
            });
```

- [ ] **Step 2: 提交**

```bash
git add static/js/index.js
git commit -m "feat: add incremental SSE consumption in frontend"
```

---

### Task 5: 前端降级轮询合并为单请求

**Files:** `static/js/index.js`

- [ ] **Step 1: 重写 startStatusFallbackPolling**

`static/js/index.js` 第 1526-1535 行，替换整个函数：

```javascript
        function startStatusFallbackPolling() {
            if (statusFallbackTimer) return;
            statusFallbackTimer = window.setInterval(async () => {
                try {
                    const payload = await window.MediaHubApi.getJson('/status-summary');
                    applyMainState(payload.main);
                    applyMonitorState(payload.monitor);
                    applySubscriptionState(payload.subscription);
                    applySign115State(payload.sign115);
                    applyCookieHealthState(payload.cookie_health);
                    applyResourceChannelSyncState(payload.resource_channel_sync);
                } catch (e) {}
            }, STATUS_FALLBACK_INTERVAL);
        }
```

旧代码（需确认准确匹配再替换）：

```javascript
        function startStatusFallbackPolling() {
            if (statusFallbackTimer) return;
            statusFallbackTimer = window.setInterval(() => {
                refreshMainLogs({ compact: true });
                refreshMonitorState({ compact: true });
                refreshSubscriptionState({ compact: true });
                refreshSign115Status(false);
                refreshCookieHealthStatus(false);
            }, STATUS_FALLBACK_INTERVAL);
        }
```

- [ ] **Step 2: 确认 MediaHubApi.getJson 可用**

`static/js/modules/app/api.js` 中定义了 `window.MediaHubApi.getJson`，在 HTML 中 `api.js` 先于 `index.js` 加载，因此可用。

- [ ] **Step 3: 提交**

```bash
git add static/js/index.js
git commit -m "feat: merge fallback polling into single /status-summary request"
```

---

### Task 6: SSE 重连指数退避

**Files:** `static/js/index.js`

- [ ] **Step 1: 添加退避变量**

在 `static/js/index.js` 第 180 行 `let statusEventSource = null;` 之后插入：

```javascript
        let sseReconnectAttempt = 0;
        const SSE_RECONNECT_BASE_MS = 1000;
        const SSE_RECONNECT_MAX_MS = 30000;
```

- [ ] **Step 2: 重写 onerror 处理**

第 1701-1705 行，将：

```javascript
            statusEventSource.onerror = () => {
                statusStreamHealthy = false;
                startStatusFallbackPolling();
                scheduleResourcePolling(RESOURCE_POLL_ACTIVE_INTERVAL);
            };
```

替换为：

```javascript
            statusEventSource.onerror = () => {
                statusStreamHealthy = false;
                startStatusFallbackPolling();
                scheduleResourcePolling(RESOURCE_POLL_ACTIVE_INTERVAL);
                statusEventSource.close();
                sseReconnectAttempt += 1;
                const delay = Math.min(
                    SSE_RECONNECT_MAX_MS,
                    SSE_RECONNECT_BASE_MS * Math.pow(2, sseReconnectAttempt - 1)
                );
                window.setTimeout(() => {
                    connectStatusStream();
                }, delay);
            };
```

- [ ] **Step 3: onopen 重置计数**

第 1696-1699 行，将：

```javascript
            statusEventSource.onopen = () => {
                statusStreamHealthy = true;
                stopStatusFallbackPolling();
                scheduleResourcePolling();
            };
```

替换为：

```javascript
            statusEventSource.onopen = () => {
                statusStreamHealthy = true;
                sseReconnectAttempt = 0;
                stopStatusFallbackPolling();
                scheduleResourcePolling();
            };
```

- [ ] **Step 4: 提交**

```bash
git add static/js/index.js
git commit -m "feat: add exponential backoff for SSE reconnect"
```

---

### Task 7: 前端请求优先级管理

**Files:** `static/js/index.js`

- [ ] **Step 1: 添加暂停/恢复辅助函数**

在 `scheduleResourcePolling` 函数定义之前（约 1657 行 `function scheduleResourcePolling(...` 之前）插入：

```javascript
        let resourcePollingPaused = false;

        function pauseResourcePolling() {
            resourcePollingPaused = true;
            if (resourcePollTimer) {
                window.clearTimeout(resourcePollTimer);
                resourcePollTimer = null;
            }
        }

        function resumeResourcePolling(delay = 500) {
            resourcePollingPaused = false;
            scheduleResourcePolling(delay);
        }
```

- [ ] **Step 2: 修改 scheduleResourcePolling 检查暂停**

在 `scheduleResourcePolling` 函数体开头（第 1657 行附近）添加一行暂停检查。找到：

```javascript
        function scheduleResourcePolling(delayOverride = null) {
            if (resourcePollTimer) {
```

改为：

```javascript
        function scheduleResourcePolling(delayOverride = null) {
            if (resourcePollingPaused) return;
            if (resourcePollTimer) {
```

- [ ] **Step 3: 包装 MediaHubApi.postJson 自动暂停/恢复轮询**

最简洁的方式是在 `window.MediaHubApi.postJson` 上包装一层，无需修改每个操作函数。在 `connectStatusStream` 函数之后（约 1706 行之后，或任何 `window.MediaHubApi` 已初始化的位置之后）添加：

```javascript
        (function wrapPostJsonForRequestPriority() {
            if (!window.MediaHubApi || typeof window.MediaHubApi.postJson !== 'function') return;
            const originalPostJson = window.MediaHubApi.postJson.bind(window.MediaHubApi);
            window.MediaHubApi.postJson = async function (...args) {
                pauseResourcePolling();
                try {
                    return await originalPostJson(...args);
                } finally {
                    resumeResourcePolling();
                }
            };
        })();
```

这段代码使用 IIFE 模式：保存原始的 `postJson`，用新函数替换它，新函数在调用前后自动暂停/恢复轮询。所有通过 `window.MediaHubApi.postJson` 发起的操作（保存配置、启动/停止任务、清日志等）自动受益。

注意：这段代码必须在 `api.js` 加载之后执行。检查 HTML 中 `api.js`（第 233 行）早于 `index.js`（第 234 行），满足条件。

- [ ] **Step 4: 提交**

```bash
git add static/js/index.js
git commit -m "feat: add request priority - pause resource polling during user POST operations"
```

---

### Task 8: 全量验证与版本号更新

**Files:** `version.json`, `CHANGELOG.md`（如存在）

- [ ] **Step 1: 完整 Python 编译检查**

```bash
PYTHONPYCACHEPREFIX=/tmp/115-media-hub-pycache .venv/bin/python -m compileall app/ main.py
```
Expected: Compile successful, no errors.

- [ ] **Step 2: 启动 dev server 端到端测试**

```bash
.venv/bin/python -m uvicorn main:app --host 0.0.0.0 --port 18080 &
sleep 2
```

手动验证（浏览器打开 `http://localhost:18080`）：

| # | 验证项 | 方法 |
|---|--------|------|
| 1 | 首页正常加载 | 浏览器打开，确认页面渲染完整 |
| 2 | 缓存头生效 | DevTools → Network → `/static/js/index.js` → Response Headers 含 `Cache-Control: public, max-age=31536000, immutable` |
| 3 | SSE 连接正常 | Network → `/events` 显示 pending 状态，无错误 |
| 4 | `/status-summary` 可用 | Console: `await fetch('/status-summary').then(r=>r.json()).then(d=>console.log(Object.keys(d)))` 输出 6 个模块 key |
| 5 | SSE 增量推送 | 在任务页触发一个操作，查看 `/events` 的 EventStream 帧是否含 `_changed` 字段 |
| 6 | 30s 全量保底 | 等待 30 秒，确认至少一帧不含 `_changed`（全量推送） |
| 7 | Tab 切换正常 | 依次点击所有导航按钮，页面正常切换 |
| 8 | 降级轮询 | 停止服务器，浏览器 Console 查看到 `/status-summary` 请求；重新启动服务器，SSE 恢复 |
| 9 | SSE 退避重连 | 停止服务器，观察 Console 中 SSE 重连间隔是否递增（Network 面板可见 `/events` 请求间隔增大） |
| 10 | 请求优先级 | 点击"立即签到"按钮，Console 无报错，操作正常完成 |

- [ ] **Step 3: 更新版本号**

更新 `version.json`：

```json
{
  "version": "0.3.8",
  "buildDate": "2026-05-02T12:00:00+08:00",
  "notes": [
    "SSE 增量推送：日常推送体积减少60-80%",
    "降级轮询合并：SSE断开后单请求替代5请求",
    "SSE 重连指数退避：1s→2s→4s→...→30s",
    "静态资源版本化强缓存：二次访问秒开",
    "请求优先级：用户操作期间暂停后台轮询"
  ],
  "changelogUrl": "https://github.com/xianer235/115-media-hub/blob/main/CHANGELOG.md",
  "projectUrl": "https://github.com/xianer235/115-media-hub"
}
```

同步更新 CHANGELOG.md。

- [ ] **Step 4: 最终提交**

```bash
git add version.json CHANGELOG.md
git commit -m "chore: bump version to 0.3.8 for SSE performance optimization"

# 查看所有改动
git log --oneline -8
```
