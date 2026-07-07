# 115-media-hub 二次开发文档

> Fork: Li-Qifeng/115-media-hub  
> 上游: xianer235/115-media-hub  
> 日期: 2026-07-07

---

## 一、项目总览

### 1.1 基本信息

| 属性 | 值 |
|------|------|
| 技术栈 | Python 3.12 + FastAPI + SQLite |
| 代码量 | 65 个 Python 文件，~41,660 行 |
| Web 模板 | 14 个 Jinja2 HTML 文件，Tailwind CSS |
| 包管理 | pip (`requirements.txt`) |
| 部署 | Docker (slim-bookworm, 单容器) |
| 默认端口 | 18080 (HTTP) |
| 默认凭证 | admin / admin123 |

### 1.2 目录结构

```
115-media-hub/
├── main.py                    # FastAPI 入口
├── requirements.txt           # 依赖：fastapi, uvicorn, requests, python-multipart, itsdangerous
├── Dockerfile                 # Python 3.12 slim
├── compose.yml                # Docker Compose 示例
├── app/
│   ├── main.py                # 路由注册
│   ├── core.py                # 核心：FastAPI app, 配置, 运行时状态 (~7065行)
│   ├── config_store.py        # JSON 配置持久化 (线程安全 + mtime 缓存)
│   ├── db.py                  # SQLite 数据库 (11张表 + 索引)
│   ├── background.py          # 后台任务循环 (独立 asyncio 线程)
│   ├── memory.py              # 内存释放工具
│   ├── http_utils.py          # HTTP 请求工具 (带代理/重试/SSL)
│   ├── runtime_files.py       # 文件路径操作, 日志管理
│   ├── startup.py             # 启动：后台调度器 (目录树/监控/订阅/签到/内存清理)
│   ├── versioning.py          # 版本检查
│   ├── resource_tg.py         # Telegram 频道爬虫 (~506行)
│   ├── resource_identity.py   # 资源去重/身份识别
│   ├── resource_linking.py    # 链接解析/分类/提取 ~501行)
│   ├── resource_store.py      # 资源数据库 CRUD
│   ├── resource_jobs.py       # 资源任务管理
│   ├── media_tags.py          # 媒体标签/质量识别
│   ├── share_selection.py     # 分享选择逻辑
│   ├── subscription_scoring.py# 订阅匹配评分
│   ├── providers/             # 6个云盘Provider + 注册表
│   │   ├── base.py            # CloudProvider ABC
│   │   ├── registry.py        # 注册表
│   │   ├── pan115.py          # 115 网盘
│   │   ├── quark.py           # 夸克网盘
│   │   ├── aliyun.py          # 阿里云盘
│   │   ├── pan123.py          # 123云盘
│   │   ├── tianyi.py          # 天翼云盘
│   │   ├── pansou.py          # PanSou 盘搜 (~516行)
│   │   ├── tmdb.py            # TMDB API
│   │   └── common.py          # 通用工具
│   ├── routes/                # 13个路由模块
│   │   ├── pages.py           # HTML 页面路由
│   │   ├── resource.py        # 资源中心 API (~1865行)
│   │   ├── monitor.py         # 文件夹监控 + Webhook
│   │   ├── subscription.py    # 订阅引擎 API
│   │   ├── settings.py        # 参数配置 API
│   │   ├── strm.py            # STRM 文件管理
│   │   ├── tree.py            # 目录树任务
│   │   ├── scraper.py         # 刮削管理
│   │   ├── tmdb.py            # TMDB 搜索/详情
│   │   ├── recommendation.py  # 资源推荐
│   │   ├── events.py          # 事件推送 (SSE)
│   │   └── ...
│   └── services/              # 后台服务
│       ├── resource.py        # 资源任务执行
│       ├── monitor.py         # 文件夹监控执行
│       ├── subscription*.py   # 订阅引擎 (7个文件串)
│       ├── tree.py            # 目录树→STRM
│       ├── scraper.py         # 刮削执行
│       ├── notify.py          # 企业微信通知
│       └── sign115.py         # 115 签到
├── templates/                 # Jinja2 模板
├── static/                    # 静态资源
└── tests/                     # 测试
```

---

## 二、核心架构

### 2.1 FastAPI 应用初始化 (app/core.py)

```
主流程:
1. FastAPI() 创建 app
2. SessionMiddleware (PBKDF2 密码)
3. CORS 中间件
4. GZip 中间件
5. 静态缓存中间件
6. 可选 Server-Timing 中间件
7. 加载配置 (JSON → JsonConfigStore)
8. 注册路由 (app/main.py)
9. 启动事件 → startup()
```

常量体系 (全部可被环境变量覆盖):
- `CONFIG_PATH` = `/app/config/settings.json`
- `DB_PATH` = `/app/config/data.db`
- `STRM_ROOT` = `/app/strm`
- `LOG_DIR` = `/app/logs`
- 搜索/订阅/监控的各类超时/限流常量

### 2.2 配置系统 (app/config_store.py)

`JsonConfigStore` — 线程安全的 JSON 配置文件管理:

```python
store = JsonConfigStore(
    path="/app/config/settings.json",
    default_factory=default_config,
    normalize=normalize_config,
    post_load=on_config_loaded,
    post_save=on_config_saved,
)

store.get()   # 读取 (mtime 缓存)
store.save()  # 写入 → post_save 回调
```

- 原子读写: `json.dump()` + `os.stat().st_mtime_ns` 缓存
- `post_save` 回调通知运行时刷新
- 所有配置修改统一走 `settings.json` 文件

### 2.3 数据库 (app/db.py)

**位置:** `/app/config/data.db`  
**连接:** `open_db()` → sqlite3 + WAL + busy_timeout=30s  
**重试:** `retry_sqlite_locked()` — 指数退避重试 SQLite 锁

#### 11 张数据表

| 表名 | 用途 | 关键字段 |
|------|------|---------|
| `resource_items` | 资源发现结果 | source_type, title, link_url, link_type, status |
| `resource_jobs` | 资源转存任务 | resource_id, savepath, status, monitor_task_name |
| `subscription_task_state` | 订阅任务状态 | task_name, media_type, last_episode, matched_resource_id |
| `subscription_matches` | 订阅匹配记录 | task_name, resource_id, score |
| `subscription_episode_ledger` | 剧集账本 | task_name, episode, status, best_score |
| `subscription_channel_search_watermarks` | 频道搜索水位线 | task_name, channel_id, last_post_cursor |
| `subscription_channel_support_stats` | 频道统计 | channel_id, matched_runs, error_runs |
| `share_entries_cache` | 分享条目缓存 | share_code, cid, payload_json |
| `monitor_files` | 监控文件记录 | task_name, local_rel_path, remote_rel_path |
| `monitor_dirs` | 监控目录记录 | task_name, dir_rel_path, needs_rescan |
| `local_files` | 本地文件跟踪 | path_hash, relative_path, scan_token |
| `scraper_jobs` | 刮削任务 | provider, status, options_json |
| `scraper_job_actions` | 刮削操作明细 | job_id, action_index, old/new paths |
| `recommendation_watchlist` | 推荐清单 | tmdb_id, media_type, title, status |
| `notification_dedupe` | 通知去重 | dedupe_key, scene, expires_at |

### 2.4 后台任务系统 (app/background.py)

```python
# 单例: 独立 asyncio 事件循环线程
background_runtime = BackgroundTaskRuntime()

# 提交任务
submit_background(func, *args, label="task-name")

# 生命周期
start_background_runtime()  # 启动线程 + 循环
stop_background_runtime()   # 停止循环
```

可同时运行同步和异步函数 (自动 await)。

### 2.5 启动流程 (app/startup.py)

```
startup()
├── bind_ui_event_loop()        # SSE 事件推送通道
├── start_background_runtime()  # 后台线程
├── ensure_db()                 # 建表
├── 恢复 pending 资源任务
├── 刷新 115 签到状态
├── 5个异步调度器:
│   ├── scheduler()             # 目录树定时任务 (cron_hour)
│   ├── monitor_scheduler()     # 文件夹监控定时 (cron_minutes)
│   ├── subscription_scheduler() # 订阅调度 (时段+间隔)
│   ├── sign115_scheduler()     # 每日签到
│   └── memory_housekeeper()    # 内存清理
```

每个调度器 5 秒轮询一次。

---

## 三、Provider 系统 (核心可扩展点)

### 3.1 CloudProvider 抽象基类 (app/providers/base.py)

这是整个系统最关键的接口。所有网盘提供商继承它:

```python
class CloudProvider(ABC):
    name: str = ""           # 唯一标识, 如 "115", "quark"
    label: str = ""          # 显示名, 如 "115 网盘"
    link_type: str = ""      # 链接类型, 如 "115share"

    auth_type: str = "cookie" # cookie/password/refresh_token
    config_keys: List[str] = []

    # 能力声明 (布尔开关)
    supports_folder_browse: bool = True
    supports_share_receive: bool = True
    supports_subscription: bool = False
    supports_offline: bool = False
    supports_strm: bool = False
    supports_monitor: bool = False
    supports_rename/rename/move/copy/delete: bool = False

    # 核心抽象方法
    list_entries(cookie, cid) -> List[Dict]           # 列出目录
    create_folder(cookie, cid, name) -> Dict           # 创建目录
    resolve_folder_id_by_path(cookie, path) -> str     # 路径→ID
    ensure_folder_id_by_path(cookie, path) -> str      # 确保路径存在
    resolve_share_payload(cookie, url, ...) -> Dict    # 解析分享
    list_share_entries(cookie, payload, cid, ...) -> Dict
    prepare_share_receive(cookie, payload, cid) -> Dict
    submit_share_receive(cookie, payload, files) -> Dict
    probe_connectivity(cookie) -> bool                # 连通性检测
    resolve_download_url(cookie, file_id) -> str       # 直链

    # 限流
    rate_limit_seconds: float
    throttle()  # 自动限流
```

### 3.2 注册表 (app/providers/registry.py)

```python
register(provider)          # 注册 Provider
get(name) -> CloudProvider  # 按名称获取
get_or_none(name)           # 安全获取
get_by_link_type(type)      # 按链接类型匹配
list_all() -> List          # 全部
list_enabled(cfg) -> List   # 已启用的
get_all_capabilities(cfg)   # 能力清单
```

### 3.3 现有 6 个 Provider

| Provider | name | auth_type | link_type | 能力 |
|----------|------|-----------|-----------|------|
| 115 | `115` | cookie | `115share` | 全部支持 |
| 夸克 | `quark` | cookie | `quark` | 目录浏览+分享接收+订阅 |
| 阿里云盘 | `aliyun` | refresh_token | `aliyun` | 目录浏览+分享接收 |
| 123云盘 | `pan123` | cookie | `123pan` | 目录浏览+分享接收 |
| 天翼云盘 | `tianyi` | cookie | `tianyi` | 目录浏览+分享接收 |
| PanSou | `pansou` | password | — | 搜索 (非网盘) |

### 3.4 你要加的: DiscoveryProvider

原项目没有独立的"资源发现"Provider 接口。当前的发现逻辑分散在:
- `resource_tg.py`: TG 频道爬虫 (硬编码, 不是 Provider)
- `providers/pansou.py`: PanSou 盘搜 (是 CloudProvider, 但只用于搜索)
- `routes/resource.py`: 手动导入 (无 Provider 封装)

**你需要定义新的接口:**

```python
# app/providers/discovery_base.py (新增)
class DiscoveryProvider(ABC):
    name: str                     # 唯一标识, 如 "my_telegram"
    label: str                    # 显示名
    
    def search(self, query: str, **kwargs) -> List[ResourceItem]: ...
    def validate(self) -> bool: ...    # 检测配置是否有效
```

---

## 四、资源发现模块分析

### 4.1 TG 频道爬虫 (app/resource_tg.py)

核心流程:

```
fetch_telegram_channel_posts_page(cfg, source, limit, before, query)
├── build_tg_proxy_url(cfg)        # 代理配置
├── build_telegram_channel_page_url()  # 构建 t.me/s/频道?before=xxx
├── http_request_text_with_final_url() # HTTP 请求
├── parse_telegram_posts_page()        # 解析 HTML
│   ├── TG_WIDGET_POST_REGEX       # 匹配帖子widget
│   ├── extract_resource_links()    # 提取链接
│   ├── detect_resource_link_type() # 识别链接类型
│   ├── pick_resource_title()       # 提取标题
│   ├── guess_resource_quality()    # 质量猜测
│   └── return → posts[]
└── 翻页: TG_PREV_BEFORE_REGEX
```

关键常量:
- `TG_SEARCH_MAX_PAGES` = 3 (每频道最多翻 3 页)
- `TG_SEARCH_MATCH_LIMIT_PER_CHANNEL` = 12 (每频道最多匹配 12 条)
- `TG_CHANNEL_THREADS_DEFAULT` = 6 (同步线程数)
- 全部可环境变量覆盖

### 4.2 链接解析体系 (app/resource_linking.py)

支持的链接类型 (13种):

```
magnet, 115share, quark, aliyun, baidu, xunlei, uc,
123pan, tianyi, pikpak, lanzou, google_drive, onedrive, mega
```

核心函数:
- `extract_resource_links(raw_text)` → 从文本中提取所有链接
- `detect_resource_link_type(url)` → 识别链接类型
- `choose_resource_link(links)` → 按优先级选最佳链接 (magnet > 115share > quark > ...)
- `parse_115_share_payload(url, text, code)` → 解析 115 分享链接+提取码
- `extract_resource_candidates(text, ...)` → 完整解析一条资源消息
- `guess_resource_quality(text)` → 从文本猜测画质 (4K/HDR/1080p...)

### 4.3 资源去重 (app/resource_identity.py)

- `build_resource_item_identity(item)` → 基于 link_url/title/时间构建指纹
- `dedupe_resource_item_dicts(items)` → 去重
- `resource_item_matches_search(item, keywords)` → 关键词匹配

---

## 五、订阅引擎分析

### 5.1 整体架构

订阅引擎由 **7 个文件** 协同工作:

```
services/
├── subscription.py               # 主逻辑: 任务编排/集数视图
├── subscription_runner.py        # 单次运行入口 (queue → run)
├── subscription_task_runner.py   # 实际执行搜索+评分+导入
├── subscription_share_selection.py # 分享候选筛选
├── subscription_share_runtime.py # 分享运行时状态
├── subscription_episode.py       # 剧集账本管理
├── subscription_state.py         # 任务状态持久化
```

### 5.2 订阅运行流程

```
queue_subscription_job(task_name, trigger)
  └→ start_next_subscription_job()
      └→ run_subscription_task()
          ├── 1. 准备阶段: 加载任务配置, 获取 Cookie
          ├── 2. 搜索阶段:
          │   ├── TG 频道并行搜索 (多线程)
          │   ├── PanSou 盘搜 (可选)
          │   ├── 本地数据库匹配 (resource_items)
          │   └── 汇总 → 候选列表
          ├── 3. 目录校准: 按评分/质量/剧集筛选
          ├── 4. 候选导入: 创建 resource_jobs → 自动转存
          └── 5. 收口: 触发文件夹监控 → STRM 刷新
```

### 5.3 质量优先级

```python
SUBSCRIPTION_QUALITY_PRIORITY_ORDERS = {
    "balanced": [1080, 720, 2160, 480, 360],
    "ultra":    [2160, 1080, 720, 480, 360],
    "fhd":      [1080, 2160, 720, 480, 360],
    "hd":       [720, 1080, 2160, 480, 360],
    "sd":       [480, 720, 1080, 2160, 360],
}
```

---

## 六、Route API 参考

### 6.1 路由总览

| 路由 | 模块 | 方法 | 说明 |
|------|------|------|------|
| `/api/settings` | settings | GET/POST | 配置读写 |
| `/api/tree/*` | tree | 多种 | 目录树管理 |
| `/api/resource/*` | resource | 多种 | 资源中心 CRUD |
| `/api/resource/item/*` | resource | GET/POST | 资源项操作 |
| `/api/resource/job/*` | resource | 多种 | 资源任务操作 |
| `/api/resource/search` | resource | POST | TG 频道搜索 |
| `/api/resource/pansou-search` | resource | POST | PanSou 搜索 |
| `/api/resource/channel/sync` | resource | POST | 同步 TG 频道 |
| `/api/subscription/*` | subscription | 多种 | 订阅管理 |
| `/api/monitor/*` | monitor | 多种 | 文件夹监控 |
| `/api/webhook/{name}` | monitor | POST | Webhook 入口 |
| `/api/scraper/*` | scraper | 多种 | 刮削管理 |
| `/api/strm/*` | strm | 多种 | STRM 文件 |
| `/api/tmdb/*` | tmdb | GET | TMDB 搜索 |
| `/api/events` | events | GET | SSE 事件流 |
| `/api/recommendation/*` | recommendation | 多种 | 推荐清单 |

### 6.2 关键 API 详情

**资源搜索:**
```http
POST /api/resource/search
{
  "keyword": "黑客帝国 4K",
  "channels": ["@dianying", "@movie"],
  "channels_blacklist": [],
  "pansou_enabled": true,
  "pansou_provider_filter": "115",
  "cancel_existing_search": true
}
→ { "items": [...], "search_id": "..." }
```

**PanSou 搜索:**
```http
POST /api/resource/pansou-search
{
  "keyword": "黑客帝国",
  "provider_filter": "115",
  "include_magnet_for_115": true
}
→ { "items": [...], "elapsed_ms": 1234 }
```

**触发订阅:**
```http
POST /api/subscription/{name}/trigger
→ { "status": "queued", ... }
```

**Webhook 转存+刷新:**
```http
POST /api/webhook/{任务名}
{
  "savepath": "/电影",
  "magnet": "magnet:?xt=urn:btih:xxx",
  "title": "示例电影",
  "delayTime": 10
}
→ { "status": "queued" }
```

---

## 七、配置文件结构

配置文件: `/app/config/settings.json`

核心字段:

```json
{
  "cookie_115": "xxx",
  "cookie_quark": "",
  "cookie_pan123": "",
  "cookie_tianyi": "",
  "aliyun_refresh_token": "",

  "strm_external_host": "http://192.168.2.123:18080",
  "strm_extensions": "mp4,mkv,avi,mov,ts",
  "scan_extensions": "mp4,mkv,avi,mov,ts",

  "tg_proxy_enabled": false,
  "tg_proxy_protocol": "http",
  "tg_proxy_host": "",
  "tg_proxy_port": "",
  "tg_channel_threads": 6,
  "tg_channel_sync_limit": 10,

  "pansou_base_url": "",
  "pansou_username": "",
  "pansou_password": "",
  "pansou_src": "all",
  "pansou_channels": "",
  "pansou_plugins": "",

  "resource_sources": [
    {"name": "电影频道", "channel_id": "@dianying", "type": "tg"}
  ],

  "subscription_tasks": [
    {
      "name": "黑客帝国4",
      "media_type": "movie",
      "keyword": "黑客帝国 4",
      "provider": "115",
      "savepath": "/电影",
      "quality": "ultra",
      "score": 60,
      "enabled": true,
      "schedule_weekdays": [],
      "schedule_start_time": "00:00",
      "schedule_end_time": "23:59",
      "schedule_interval_minutes": 120
    }
  ],

  "monitor_tasks": [
    {
      "name": "电影监控",
      "scan_path": "/电影",
      "cron_minutes": 60,
      "webhook_enabled": false,
      "delay_seconds": 10,
      "enabled": true
    }
  ],

  "cron_hour": 0,
  "sign115_enabled": false,
  "sign115_cron_time": "09:00",
  "provider_enabled": { "115": true, "quark": false },

  "webhook_secret": "",
  "tmdb_api_key": "",
  "notify_webhook_url": "",
  "notify_corpid": "",
  "notify_corpsecret": "",
  "notify_agentid": ""
}
```

---

## 八、NAS 环境集成参考

### 8.1 小雅 Alist 凭证

| 项目 | 值 |
|------|-----|
| Alist API | `http://127.0.0.1:5678` |
| Alist Token | `alist-09ceb38a-f143-47f7-b255-c3eec819cd7b...` |
| Alist 密码 | `56965779` |
| Emby API | `http://127.0.0.1:6908` |
| Emby Key | `e825ed6f7f8f44ffa0563cddaddce14d` |

### 8.2 路径映射

Emby 文件路径 → Alist 文件路径:
```
/media/电影/xxx → /电影/xxx
/media/115/电影/xxx → /115/电影/xxx
```

STRM 文件内容格式:
```
http://xiaoya.host:5678/d/电影/蓝光5600部（115）/xxx.mkv
```

### 8.3 部署配置

115-media-hub 的 docker-compose 配置 (适配 NAS):

```yaml
services:
  115-media-hub:
    image: xianer235/115-media-hub:latest
    container_name: 115-media-hub
    restart: unless-stopped
    ports:
      - "18080:18080"
    volumes:
      - /vol1/1000/docker/115-media-hub/config:/app/config
      - /vol1/1000/docker/115-media-hub/logs:/app/logs
    environment:
      - TZ=Asia/Shanghai
      - TG_CHANNEL_THREADS_DEFAULT=6
      - PANSOU_SEARCH_TIMEOUT_SECONDS=15
```

---

## 九、二次开发计划

### 9.1 需要新增的功能

| 优先级 | 功能 | 实现方式 | 预估工作量 |
|--------|------|---------|-----------|
| P0 | **MCP Server** | 新增 `app/mcp_server.py`, 用 FastMCP 暴露工具 | ~0.5天 |
| P0 | **DiscoveryProvider 接口** | 新增 `app/providers/discovery_base.py`, 重构 TG/PanSou 为 Provider | ~1天 |
| P1 | **MCP 工具: discover_media** | 封装资源搜索+PanSou+TG 为 MCP 工具 | ~0.5天 |
| P1 | **MCP 工具: subscribe_media** | 封装订阅管理 | ~0.5天 |
| P1 | **MCP 工具: transfer_media** | 封装转存+Webhook | ~0.5天 |
| P2 | **自定义 Provider 示例** | 在 `app/providers/custom/` 下提供示例模板 | ~0.5天 |
| P2 | **MCP tool: get_status** | 系统状态查询 | ~0.5天 |

### 9.2 MCP Server 实现方案

用 FastMCP (Python SDK, `modelcontextprotocol/python-sdk`)：

```python
# app/mcp_server.py
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("115-media-hub")

@mcp.tool(description="搜索媒体资源，支持 TG 频道和 PanSou 多渠道")
async def discover_media(
    title: str = Field(description="片名"),
    year: int = Field(default=None, description="年份"),
    quality: str = Field(default="4K", description="画质偏好"),
    provider: str = Field(default="115", description="网盘提供商")
) -> str:
    """
    1. 调用 core 中的 resource_search 函数
    2. 聚合 TG + PanSou 结果
    3. 返回格式化结果
    """
    ...

@mcp.tool(description="订阅媒体，自动追更")
async def subscribe_media(
    title: str, media_type: str = "movie",
    quality: str = "4K", savepath: str = "/电影"
) -> str:
    """调用 subscription 模块创建订阅任务"""
    ...

@mcp.resource(uri="media://subscriptions", description="当前订阅列表")
def get_subscriptions() -> str:
    """返回当前所有订阅任务及其状态"""
    ...

@mcp.prompt()
def media_assistant() -> str:
    """预置提示词，指导 AI 如何使用媒体工具"""
    return "你是一个媒体助手..."
```

**集成方式:**
- AI Agent 通过 stdio 启动 `python -m app.mcp_server`
- 或者嵌入 FastAPI: 在 `startup()` 中启动 MCP 子进程
- 与原有 Web 管理后台共享配置和数据库

### 9.3 DiscoveryProvider 接口设计

```python
# app/providers/discovery_base.py
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import List, Optional

@dataclass
class DiscoveryResult:
    title: str
    link_url: str
    link_type: str  # 115share / magnet / quark / ...
    quality: str = ""
    year: str = ""
    source_name: str = ""
    extra: dict = field(default_factory=dict)

class DiscoveryProvider(ABC):
    name: str = ""
    label: str = ""

    @abstractmethod
    def search(self, keyword: str, **kwargs) -> List[DiscoveryResult]:
        """搜索资源，返回候选列表"""
        ...

    def validate(self) -> bool:
        """检测配置是否有效"""
        return True

    def config_fields(self) -> List[dict]:
        """返回配置表单字段定义，用于 Web UI 动态渲染"""
        return []
```

然后重构现有的 TG 搜索和 PanSou 搜索为 DiscoveryProvider 实现，并允许用户注册自定义 Provider:

```python
# app/providers/discovery_registry.py
_discovery_providers: Dict[str, DiscoveryProvider] = {}

def register_discovery(provider: DiscoveryProvider):
    _discovery_providers[provider.name] = provider

def search_all(keyword: str, **kwargs) -> List[DiscoveryResult]:
    """轮询所有已注册 Provider"""
    results = []
    for p in _discovery_providers.values():
        try:
            results.extend(p.search(keyword, **kwargs))
        except Exception as e:
            log.error(f"{p.name} search failed: {e}")
    return results
```

---

## 十、开发注意事项

### 10.1 代码风格

- 项目使用 `*` 通配导入 (`from ..core import *`)
- 大量使用 `max()` + `min()` 钳制常量
- 重试模式: `retry_sqlite_locked()` — 指数退避
- 所有超时/限制均可通过环境变量覆盖
- 使用 `submit_background()` 做异步任务，不是直接 `asyncio.create_task()`

### 10.2 测试

- 测试在 `tests/` 目录
- 使用 pytest
- 数据库测试可以直接操作 SQLite 文件

### 10.3 部署

- Docker 镜像: `xianer235/115-media-hub:latest`
- 默认监听 18080
- 挂载 `/app/config`, `/app/logs` 持久化
- 首次启动默认 admin/admin123

### 10.4 MCP 的 Python 生态

- 官方 SDK: `modelcontextprotocol/python-sdk` (953 commits, 最成熟)
- 高层 API: FastMCP (`mcp.server.fastmcp`)
- stdio 传输: Claude Desktop 可通过 `python -m app.mcp_server` 拉起
- HTTP 传输: 可内嵌到 FastAPI 中 (Streamable HTTP)

### 10.5 已有的可复用基础设施

- 配置系统 ✅ `JsonConfigStore`
- 数据库 ✅ `open_db()` + `ensure_db()`
- 后台任务 ✅ `submit_background()`
- HTTP 请求 ✅ `http_request_json()` + 代理支持
- 日志 ✅ `append_log_file()` + `read_log_tail()`
- Provider 注册表 ✅ `registry.py`
- 事件推送 ✅ `schedule_ui_state_push()` (SSE)