# SSE 通信性能优化设计

**日期：** 2026-05-02
**目标：** 在 2Mbps FRP 中转部署场景下，保证数据不丢失的同时，优化前后端通信延迟。

---

## 1. 问题诊断

| 问题 | 根因 | 影响 |
|------|------|------|
| 首页加载慢 | 137KB 单文件 index.js + 全流量走 2Mbps FRP | 白屏 4-8 秒 |
| 操作响应慢 | 每次操作完整 HTTP 往返 + FRP 延迟 | 点击后等 1-3 秒 |
| 状态更新延迟 | SSE 推送全量状态快照（6 模块），降级轮询时并发 5 请求争抢带宽 | 更新滞后、显示不一致 |
| SSE 断开恢复慢 | 固定 3 秒重连，降级轮询在 SSE 恢复后不立即停止 | 断开期间数据可能遗漏 |

**核心矛盾：** SSE 推送全量快照 → 数据量大 → 慢连接下容易断开 → 触发降级轮询 → 更多请求争抢带宽 → 恶性循环。

---

## 2. 改造范围

```
┌─────────────────────────────────────────────────┐
│  前端                                              │
│  ├─ JS 拆分：核心 35KB + 各 Tab 按需加载             │
│  ├─ SSE 增量消费：只更新变化的模块                    │
│  ├─ 降级轮询合并：1 个 /status-summary 请求替代 5 个  │
│  └─ 请求优先级：用户操作优先，轮询主动让路             │
├─────────────────────────────────────────────────┤
│  传输层                                            │
│  ├─ SSE 增量推送：只发变化模块 + 30s 全量保底补发     │
│  ├─ SSE 重连指数退避：1s → 2s → 4s → ... → 30s     │
│  └─ 静态资源版本化强缓存                              │
├─────────────────────────────────────────────────┤
│  后端                                              │
│  ├─ 增量推送对比：跟踪上次推送，标记变化模块           │
│  ├─ 新增合并降级接口：GET /status-summary            │
│  └─ 操作响应保持同步 + loading 指示                   │
└─────────────────────────────────────────────────┘
```

**不改什么：**
- 不换 WebSocket（FRP 配置更复杂，收益不明确）
- 不拆分后端微服务（瓶颈在带宽不在 CPU）
- 不做乐观更新 + 回滚（体验不好）

---

## 3. 改造点详解

### 3.1 前端 JS 拆分（首页加载优化）

**现状：** `static/js/index.js`（137KB）包含全部页面逻辑，浏览器必须完整下载后才能渲染。

**改造：**
- 抽离核心模块 `static/js/core.js`（~35KB）：导航、SSE 连接、状态管理、API 工具函数、任务中心 UI（main/树任务）
- 已有 Tab 模块保持不变：`modules/monitor/`、`modules/subscription/`、`modules/resource/` 等继续按需加载
- `index.js` 精简为：导入 core.js + 注册 Tab 切换时的模块加载回调
- 首页 HTML 只引用 `core.js`，打开即渲染任务中心

**文件改动：**
- `templates/index.html` — 修改 script 引用
- `static/js/index.js` — 拆分出核心代码
- 新建 `static/js/core.js` — 核心运行时

**预期效果：** 首页首次加载从 4-8s 降至 1-2s（35KB vs 137KB）。

### 3.2 SSE 增量推送

**现状：** `broadcast_ui_state()` 每 0.35s debounce 后推送全部 6 模块完整快照。日志新增一行也会触发全量重发。

**改造：**

后端（`app/core.py`）：
1. 新增 `_last_broadcast_snapshot` 字典，记录上次推送的每个模块的 hash
2. `build_ui_state_payload()` 改为按模块 hash 对比，只包含变化的模块
3. 增量推送时响应格式增加 `_changed: ["subscription"]` 字段标记变化模块
4. 每 30 秒（心跳 2 个周期）强制全量推送一次作为一致性保底
5. SSE 新建连接时首帧始终发全量快照

前端（`static/js/core.js`）：
1. SSE `state` 事件处理中，读取 `_changed` 数组
2. 只调用变化模块对应的 `apply*State()` 函数
3. `_changed` 不存在或为 null 时视为全量更新

**文件改动：**
- `app/core.py` — `build_ui_state_payload()`、`flush_ui_state_updates()`、`broadcast_ui_state()` 
- `app/routes/events.py` — 首帧标记
- `static/js/core.js` — SSE 增量消费逻辑

**预期效果：** 日常推送体积减少 60%-80%（通常只有 1-2 个模块变化）。

### 3.3 降级轮询优化

**现状：** SSE 断开时每 15 秒发起 5 个独立请求，互相抢带宽。

**改造：**

后端：
1. 新增 `GET /status-summary` 路由（在 `app/routes/events.py` 或新建路由文件）
2. 返回与 SSE 全量快照相同格式的数据（复用 `build_ui_state_payload`）
3. 保持现有单独端点（`/logs`、`/monitor/status` 等）不变，供 Tab 模块独立刷新使用

前端：
1. SSE 断开后不使用独立的 5 请求轮询，改用单请求 `GET /status-summary`
2. SSE 重连指数退避：第 1 次 1 秒、第 2 次 2 秒、第 3 次 4 秒……最大 30 秒
3. SSE `onopen` 后立即停止降级轮询 timer
4. 降级轮询间隔保持 15 秒

**文件改动：**
- `app/routes/events.py` — 新增 `/status-summary` 端点
- `static/js/core.js` — 降级轮询逻辑重写

**预期效果：** SSE 断开期间请求数从 5 个降至 1 个，避免带宽争抢。

### 3.4 请求优先级

**现状：** 资源轮询（REST API 调用）和用户操作可能同时发起，共享 2Mbps 通道。

**改造：**

前端：
1. 用户操作（POST 保存/启动/停止等）发起前，暂停资源轮询 timer
2. 操作完成后恢复轮询（包括成功和失败两种情况）
3. 资源轮询在 `document.hidden` 时进一步降低频率（当前已有部分逻辑，补充完善）
4. 添加操作 Loading 状态指示（按钮禁用 + 文字提示"处理中..."）

**文件改动：**
- `static/js/core.js` — 请求队列优先级管理

### 3.5 静态资源缓存

**改造：**
1. 后端在 `main.py` / `core.py` 的 StaticFiles mount 上配置 `Cache-Control` 头（版本化静态资源 1 年缓存）
2. HTML 模板中的 JS 引用添加版本号 query：`core.js?v=0.3.7`
3. 版本号从 `version.json` 自动读取

**文件改动：**
- `app/core.py` — StaticFiles 缓存头配置
- `templates/index.html` — JS 引用加版本号

---

## 4. 数据流对比

### 改造前
```
SSE 连接: [main+monitor+subscription+sign115+cookie_health+channel_sync] ──→ 全量 6 模块
断开后: 并发 GET /logs, /monitor/status, /subscription/status, /sign115, /cookie_health
首页: 下载 137KB index.js
```

### 改造后
```
SSE 连接: [_changed: ["subscription"], subscription: {...}] ──→ 仅变化模块
断开后: 单请求 GET /status-summary
首页: 下载 35KB core.js，其他模块 Tab 切换时按需加载
30s 保底: 全量 6 模块快照，修正任何中间遗漏
```

---

## 5. 风险与对策

| 风险 | 对策 |
|------|------|
| 增量 hash 对比有开销 | hash 用 md5 对小 payload，每个模块 < 1ms |
| 增量推送丢数据导致前端状态不一致 | 30s 全量快照保底 + SSE 首帧全量 |
| JS 拆分后 Tab 切换首次有加载延迟 | 模块文件小（10-20KB），2Mbps 下 < 1s，浏览器缓存后再切秒开 |
| 旧浏览器缓存旧版本 JS | 版本号 query string 自动刷新 |
| `/status-summary` 返回数据比单个端点大 | GZip 压缩下差异不大，但合并请求减少 HTTP 开销和并发争抢 |

---

## 6. 不变更的部分

- SSE 端点路径保持 `/events`
- 现有 REST API 端点全部保留，供 Tab 模块独立使用
- `UI_PUSH_DEBOUNCE_SECONDS` 等环境变量配置项保留不变
- 后端 task/monitor/subscription 状态存储结构不变
- GZipMiddleware 保持不变

---

## 7. 验收标准

1. 首页 (core.js) 在 2Mbps 下首次加载 < 2 秒
2. SSE 日常推送 payload 体积减少 60% 以上
3. SSE 断开后降级轮询 30 秒内恢复页面一致性
4. SSE 重连期间不发生 5 请求并发
5. 用户操作期间不触发资源轮询请求
6. 30 秒内至少一次全量快照推送，确保最终一致性
7. 所有现有功能（任务中心、监控、订阅、资源导入、刮削、TMDB、设置）正常工作
