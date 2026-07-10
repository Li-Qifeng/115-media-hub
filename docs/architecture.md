# 架构设计：115 Media Hub 演进方案

> 阶段五产出：基于阶段四最佳实践提炼与阶段三横向对比矩阵，设计一个**新的、更优**的架构方案。
> 本方案不复制任何单一项目，而是结合 20 个调研项目的优秀实践，构成 115 Media Hub 的演进方向。
> 编写时间：2026-07
> 依据来源：
> - 最佳实践提炼：[`docs/best-practice.md`](./best-practice.md)（事实标准 10 / 优秀实践 14 / 应避免 13 / 未来方案 14）
> - 横向对比矩阵：[`docs/competitor-comparison.md`](./competitor-comparison.md)
> - 市场调研明细：[`docs/market-analysis.md`](./market-analysis.md)

---

## 1. 总体架构

### 1.1 设计理念

本方案以"**五位一体闭环 + 能力声明 + 事件驱动 + 配置即数据**"为核心理念，结合多个优秀项目的优点，规避其痛点：

| 设计取向 | 借鉴来源 | 演进点 |
|---------|---------|--------|
| Provider 抽象 + 能力声明 + UI 自动渲染 | [Radarr](https://github.com/Radarr/Radarr) Provider 体系 + [Alist](https://github.com/AlistGo/alist) Driver 接口 | Radarr 需编译发版，本方案运行时注册（对标 Alist `init()` 注册） |
| 事件驱动 + 多级缓存 | [MoviePilot](https://github.com/jxxghp/MoviePilot) `app/core/event.py` + `app/core/cache.py` | 叠加 Server-Timing 可观测性（[PanSou](https://github.com/fish2018/pansou) 思路延伸） |
| 增量同步 scan_token + mtime 比对 | [qmediasync](https://github.com/qicfan/qmediasync) | 规避 [Alist](https://github.com/AlistGo/alist) 缺增量导致 429 的反面 |
| 插件市场 + 热插拔 | [MoviePilot](https://github.com/jxxghp/MoviePilot) 300+ 插件 | 引入沙箱隔离与生命周期管理 |
| 豆瓣 + TMDB 双源 + 防封禁框架 | [jellyfin-plugin-metashark](https://github.com/cxfksword/jellyfin-plugin-metashark) | 工程化节流/代理/重试/缓存，填补生态空白 |
| 转存任务组 + 失效检查 + 新链挑选 | [quark-auto-save](https://github.com/Cp0204/quark-auto-save) | 跨网盘复用而非单盘 |
| 异步插件先返回再补充 + 二级缓存 | [PanSou](https://github.com/fish2018/pansou) | 用于 TG 频道搜索降首屏延迟 |
| MCP 协议端点 + AI Agent | [MoviePilot](https://github.com/jxxghp/MoviePilot) `/api/v1/mcp` + [PanSou](https://github.com/fish2018/pansou) | 面板能力被外部 LLM 复用 |
| WebAuthn Passkey 无密码登录 | [AutoBangumi](https://github.com/EstrellaXD/Auto_Bangumi) | 规避 [aliyundrive-subscribe](https://github.com/adminpass/aliyundrive-subscribe) admin/admin 弱口令 |
| Cookie 健康分层 + 加密存储 | [CloudSaver](https://github.com/jiangrui1994/CloudSaver) + [AutoBangumi](https://github.com/EstrellaXD/Auto_Bangumi) | 摒弃明文存储（应避免 3.3） |
| 配置热重载不中断连接 | [MediaMTX](https://github.com/bluenviron/mediamtx) | post_save 回调驱动 |
| 组织化运营 | [OpenList](https://github.com/OpenListTeam/OpenList) + [Seerr](https://github.com/seerr-team/seerr) | 规避 [Alist](https://github.com/AlistGo/alist)/[nas-tools](https://github.com/NAStool/nas-tools) 单点风险 |

**核心定位**：在"网盘媒体面板"细分赛道形成"多网盘（5+）+ STRM 生成 + TG 资源同步 + 影视订阅 + 刮削管理"五位一体闭环，填补 20 个调研项目中无人完整覆盖的生态空白（[对比矩阵 5.3](./competitor-comparison.md)）。

### 1.2 架构分层图

```
┌─────────────────────────────────────────────────────────────────────────┐
│  表现层 (Presentation)                                                    │
│  Vue3 SPA + Tailwind | Tailwind 暗色模式 | 移动端响应式 | SSE 实时状态     │
└──────────────────────────────┬──────────────────────────────────────────┘
                               │ HTTPS / SSE / WebSocket(MCP)
┌──────────────────────────────┴──────────────────────────────────────────┐
│  API 层 (API Layer)                                                       │
│  FastAPI Router | 请求校验(Pydantic) | 认证中间件 | 统一响应封装          │
│  路由分组: settings/resource/subscription/monitor/scraper/strm/tmdb/      │
│            events/recommendation/webhook/mcp                              │
└──────────────────────────────┬──────────────────────────────────────────┘
                               │ 调用
┌──────────────────────────────┴──────────────────────────────────────────┐
│  业务服务层 (Service Layer)                                                │
│  ResourceService | SubscriptionEngine | MonitorEngine | StrmEngine |      │
│  ScraperEngine | NotifyService | Scheduler | RecommendationService        │
│  ↓ 发布事件                                  ↑ 订阅事件                   │
└──────────────────────────────┬──────────────────────────────────────────┘
                               │ 事件总线 (Event Bus)
┌──────────────────────────────┴──────────────────────────────────────────┐
│  领域模型层 (Domain Layer)                                                 │
│  领域对象: Resource / Subscription / Episode / MonitorFile / StrmEntry / │
│            ScrapeJob / WatchItem                                          │
│  领域服务: 资源去重 / 链接解析 / 评分算法 / 集数账本 / 命名模板           │
└──────────────────────────────┬──────────────────────────────────────────┘
                               │ 依赖倒置 (DIP)
┌──────────────────────────────┴──────────────────────────────────────────┐
│  Provider 适配层 (Provider Layer) — 插件化 + 能力声明                       │
│  CloudProvider(5+) | DiscoveryProvider(TG/盘搜) | MetadataProvider       │
│  (TMDB/豆瓣) | NotifyProvider(微信/TG/Discord/Bark) | HookPlugin         │
│  └─ Registry 运行时注册 | Capability 布尔声明 | 配置字段定义自动渲染        │
└──────────────────────────────┬──────────────────────────────────────────┘
                               │
┌──────────────────────────────┴──────────────────────────────────────────┐
│  基础设施层 (Infrastructure)                                               │
│  SQLite WAL/PG | JsonConfigStore | EventBus(SSE) | Cache(LRU+磁盘) |     │
│  Logger(按任务会话) | HttpClient(代理/限流/重试) | Crypto(Fernet) |       │
│  WebDAV Server | MCP Server                                               │
└─────────────────────────────────────────────────────────────────────────┘
```

### 1.3 核心设计原则

1. **Provider 抽象 + 能力声明**（依据：优秀实践 2.1 + 2.2 + 未来方案 4.3）：所有异构组件（网盘/发现源/元数据/通知）统一抽象为 Provider，每个声明 `supports_*` 布尔能力开关，运行时按能力路由。新增 Provider 零侵入主流程（对标 [Alist](https://github.com/AlistGo/alist) `init()` 注册）。
2. **插件化**（依据：未来方案 4.5）：Provider、Discovery、Metadata、Notify、Hook 五类插件统一接口，支持热加载/卸载，沙箱隔离（对标 [MoviePilot](https://github.com/jxxghp/MoviePilot) 300+ 插件）。
3. **事件驱动**（依据：未来方案 4.4）：核心调度以事件总线驱动，模块订阅事件解耦，叠加多级缓存（对标 [MoviePilot](https://github.com/jxxghp/MoviePilot) `app/core/event.py`）。
4. **配置即数据**（依据：应避免 3.10）：默认值 → 环境变量 → 配置文件 → 运行时覆盖四层叠加，Web UI 表单化，摒弃 INI 单文件（规避 [aliyundrive-subscribe](https://github.com/adminpass/aliyundrive-subscribe) 反面）。
5. **单一职责 + 反巨石**（依据：应避免 3.2）：保持 `providers / routes / services / domain / infra` 五层清晰，警惕 `core.py` 膨胀（规避 [nas-tools](https://github.com/NAStool/nas-tools) 被重构反面）。
6. **增量优先**（依据：优秀实践 2.6 + 未来方案 4.7）：网盘同步一律 scan_token + mtime 增量，规避全量请求触发 429（规避 [Alist](https://github.com/AlistGo/alist) 反面）。
7. **安全合规**（依据：应避免 3.3）：Cookie/Token 加密存储，首启动强制改默认密码，WebAuthn Passkey，摒弃明文与弱口令。
8. **可观测性**（依据：未来方案 4.9）：Server-Timing 头暴露内部耗时，日志按任务会话分页，指标暴露 Prometheus。
9. **向后兼容**（依据：应避免 3.8）：提供迁移脚本 + 向后兼容期，schema 变更走版本化迁移（规避 [Alist](https://github.com/AlistGo/alist) v2→v3 反面）。

### 1.4 技术栈选型

| 层 | 选型 | 理由与最佳实践依据 |
|----|------|------------------|
| 语言 | Python 3.12 | 异步 IO 契合网盘高延迟场景；生态对网盘/刮削/PT 适配库最齐全（事实标准 1.1，[MoviePilot](https://github.com/jxxghp/MoviePilot)/[quark-auto-save](https://github.com/Cp0204/quark-auto-save) 同栈） |
| Web 框架 | FastAPI（异步） | 自带 OpenAPI/Swagger 降低 API 维护成本；异步原生契合网盘高延迟（事实标准 1.1）；摒弃 Flask 同步（应避免 3.1，规避 [nas-tools](https://github.com/NAStool/nas-tools)） |
| 前端 | Vue3 + Tailwind CSS | 编译期框架体积小；移动端响应式（事实标准 1.8，[MoviePilot](https://github.com/jxxghp/MoviePilot)/[AutoBangumi](https://github.com/EstrellaXD/Auto_Bangumi) 同栈） |
| 数据库 | SQLite 默认 + 可选 PostgreSQL | SQLite 零运维开箱即用；PG 应对多用户高并发（事实标准 1.3，[MoviePilot](https://github.com/jxxghp/MoviePilot)/[Seerr](https://github.com/seerr-team/seerr) 同模式） |
| ORM | SQLAlchemy 2.x + aiosqlite | 异步驱动；抽象层支持切换 PG（[AutoBangumi](https://github.com/EstrellaXD/Auto_Bangumi) aiosqlite） |
| 配置存储 | JSON 文件 + mtime 缓存 | 线程安全；mtime 比对避免重复 IO（优秀实践，已有 `JsonConfigStore`） |
| 任务调度 | 内置 APScheduler + cron | 统一调度器便于资源排队（事实标准 1.7） |
| 事件 | 自建 EventBus + SSE 推送 | 轻量状态 + 按需拉日志（优秀实践 2.3） |
| 加密 | cryptography Fernet | Cookie/Token 对称加密存储（优秀实践 2.7，应避免 3.3） |
| 认证 | Session + bcrypt + WebAuthn Passkey | 摒弃弱口令（未来方案 4.10，[AutoBangumi](https://github.com/EstrellaXD/Auto_Bangumi)） |
| 部署 | Docker 单容器 + 官方镜像 | NAS 用户门槛最低（事实标准 1.2） |
| 可观测性 | Server-Timing + structlog + Prometheus | 填补领域前瞻空白（未来方案 4.9） |
| AI 集成 | MCP 协议端点 + 可选 LLM Agent | 面板能力被外部 LLM 复用（未来方案 4.1/4.2） |

---

## 2. 模块设计

### 2.1 Provider 体系

**职责**：将网盘、发现源、元数据源等异构组件统一抽象，运行时注册，按能力声明路由。

**依赖**：基础设施层（HttpClient、Crypto、ConfigStore）。

**三类 Provider 抽象**：

```python
# app/providers/base.py
class CloudProvider(ABC):
    # 元数据
    name: str
    label: str
    link_type: str  # "115" / "quark" / "aliyun" / ...
    auth_type: str  # "cookie" / "refresh_token" / "oauth" / "password"

    # 能力声明（布尔开关，借鉴 Radarr）
    supports_folder_browse: bool = True
    supports_share_receive: bool = True
    supports_subscription: bool = False
    supports_offline: bool = False
    supports_strm: bool = False
    supports_monitor: bool = False
    supports_rename: bool = False
    supports_move: bool = False
    supports_copy: bool = False
    supports_delete: bool = False
    supports_incremental_sync: bool = False  # 新增：增量同步能力

    # 配置字段定义（UI 自动渲染表单，借鉴 Radarr）
    config_fields: List[ConfigField] = []

    # 核心 API（抽象方法）
    @abstractmethod
    def list_entries(self, cookie: str, cid: str = "0") -> List[Dict]: ...
    @abstractmethod
    def create_folder(self, cookie: str, cid: str, folder_name: str) -> Dict: ...
    @abstractmethod
    def resolve_share_payload(self, cookie: str, share_url: str, ...) -> Dict: ...
    @abstractmethod
    def submit_share_receive(self, cookie: str, receive_payload: Dict, files: List) -> Dict: ...
    @abstractmethod
    def probe_connectivity(self, cookie: str) -> bool: ...
    # 可选方法按能力覆写
    def resolve_download_url(self, cookie: str, file_id: str) -> str: ...
    def submit_offline_task(self, cookie: str, url: str, folder_id: str) -> Dict: ...
    # 增量同步（新增，借鉴 qmediasync）
    def list_entries_incremental(self, cookie: str, cid: str, scan_token: str) -> Tuple[List, str]: ...
```

```python
# app/providers/discovery_base.py
class DiscoveryProvider(ABC):
    name: str
    label: str
    supports_async_supplement: bool = False  # 先返回再补充，借鉴 PanSou
    supports_mcp: bool = False  # 是否暴露为 MCP 工具

    @abstractmethod
    def search(self, keyword: str, **opts) -> List[ResourceHit]: ...
    # 异步补充（借鉴 PanSou 二级缓存）
    async def search_supplement(self, keyword: str, initial: List) -> List: ...
```

```python
# app/providers/metadata_base.py
class MetadataProvider(ABC):
    name: str  # "tmdb" / "douban" / "tvdb"
    supports_movie: bool = True
    supports_tv: bool = True
    supports_chinese: bool = False
    rate_limit_qps: float = 0.0  # 节流，借鉴 metashark 防封禁

    @abstractmethod
    def search_by_title(self, title: str, year: str = "") -> List[MediaMeta]: ...
    @abstractmethod
    def get_detail(self, media_id: str, media_type: str = "movie") -> MediaMeta: ...
```

**能力声明驱动 UI**：前端通过 `GET /api/settings/providers` 获取所有已注册 Provider 及其 `config_fields` 定义，自动渲染配置表单（对标 [Radarr](https://github.com/Radarr/Radarr) UI 自动渲染）。

### 2.2 资源中心（Resource Center）

**职责**：发现资源、去重、链接解析、导入转存任务编排。

**依赖**：Provider 体系（Discovery + Cloud）、领域层（ResourceIdentity）、基础设施（DB、EventBus）。

**关键接口**：
- `discover(keyword)` → 聚合多 DiscoveryProvider，去重合并（按 normalized_title + link_url）
- `parse_link(raw_text)` → 解析分享链/磁力链，识别 link_type
- `dedupe(item)` → 基于 `resource_items.link_url` 唯一索引去重
- `create_import_job(resource_id, target_folder)` → 创建转存任务，入队

**去重策略**：`resource_items` 表对 `link_url` 建唯一索引（`WHERE link_url <> ''`），同链不重复入库；按 `normalized_title + source_name` 聚合展示。

### 2.3 订阅引擎（Subscription Engine）

**职责**：影视追更任务编排、搜索、评分、集数账本管理。

**依赖**：资源中心、Provider 体系、MetadataProvider（TMDB）、领域层（评分算法、集数账本）。

**关键模块**：
- `SubscriptionRunner`：周期调度，按 cron 拉取 DiscoveryProvider 增量
- `SubscriptionScoring`：评分算法（标题匹配度 + 分辨率 + 集数完整度）
- `EpisodeLedger`：集数账本，按 `(task_name, episode)` 主键记录最优命中，避免重复转存
- `ShareSelection`：分享链失效后从搜索结果挑选新链接力（借鉴 [quark-auto-save](https://github.com/Cp0204/quark-auto-save) 新链挑选）

### 2.4 监控引擎（Monitor Engine）

**职责**：网盘文件夹扫描、补扫、变更检测、STRM 增量更新。

**依赖**：Provider 体系（Cloud）、领域层（scan_token）、STRM 引擎、EventBus。

**关键能力**：
- 增量扫描：`scan_token` + mtime 比对，仅拉变更集（借鉴 [qmediasync](https://github.com/qicfan/qmediasync)，规避 [Alist](https://github.com/AlistGo/alist) 全量 429）
- 补扫机制：`monitor_dirs.needs_rescan` 标记需重扫目录，`missing_confirmations` 累计缺失确认
- Webhook 触发：文件变更后发布 `monitor.completed` 事件，触发 STRM/刮削

### 2.5 STRM 引擎（Strm Engine）

**职责**：STRM 文件生成、中继代理、302 直链适配。

**依赖**：Provider 体系（Cloud.resolve_download_url）、监控引擎、基础设施（HttpClient 代理）。

**关键能力**：
- STRM 生成：按监控目录映射本地 .strm 文件
- 302 代理（借鉴 [qmediasync](https://github.com/qicfan/qmediasync)）：内置下载链接代理改写 UA/注入鉴权头，解决部分客户端 UA 不能播放
- 增量更新：基于 monitor_files 变更集增量生成/删除，避免全量重建
- 中继服务：可选内置轻量 HTTP 代理端口

### 2.6 刮削引擎（Scraper Engine）

**职责**：TMDB/豆瓣识别、批量重命名、NFO 生成、元数据双向同步。

**依赖**：MetadataProvider（TMDB + 豆瓣双源）、Provider 体系（文件操作）、领域层（命名模板）。

**关键能力**：
- 双源刮削：TMDB（季集结构/海报）+ 豆瓣（中文剧情/评分），叠加节流/代理/重试/缓存防封禁（借鉴 [jellyfin-plugin-metashark](https://github.com/cxfksword/jellyfin-plugin-metashark)，规避应避免 3.9）
- 批量重命名：命名模板引擎（变量占位 + 正则捕获，借鉴 [tinyMediaManager](https://gitlab.com/tinyMediaManager/tinyMediaManager) JMTE + [aliyundrive-subscribe](https://github.com/adminpass/aliyundrive-subscribe) 智能模板）
- 元数据双向同步：NFO/海报回传网盘（借鉴 [qmediasync](https://github.com/qicfan/qmediasync)）
- 任务化：`scraper_jobs` + `scraper_job_actions` 记录可回滚操作

### 2.7 任务调度器（Scheduler）

**职责**：后台运行时、cron 调度、任务并发控制。

**依赖**：基础设施（APScheduler）、业务服务层。

**关键能力**：
- cron 表达式调度（事实标准 1.7）
- 任务并发限制：避免多任务并发触发风控
- 任务会话 ID：每个任务实例分配 session_id，日志按会话分页（未来方案 4.9）
- 失败重试与退避

### 2.8 配置中心（Config Center）

**职责**：JSON 配置存储、mtime 缓存、热重载、敏感字段脱敏。

**依赖**：基础设施（JsonConfigStore）。

**关键能力**：
- `JsonConfigStore`：线程安全 + mtime 比对缓存（已有实现，优秀实践）
- `post_save` 回调：配置变更触发热重载，不中断已有连接（借鉴 [MediaMTX](https://github.com/bluenviron/mediamtx)）
- 敏感字段：Cookie/Token 写入加密，读取脱敏返回/留空保持原值

### 2.9 事件总线（Event Bus）

**职责**：模块间解耦通信、SSE 实时推送。

**依赖**：基础设施（SSE）。

**关键能力**：
- 发布订阅模型
- SSE 推送轻量状态 + 按需拉日志（优秀实践 2.3）
- 节流去重：`UI_PUSH_DEBOUNCE` 合并高频事件

### 2.10 通知服务（Notify Service）

**职责**：多渠道通知推送、按事件路由、去重。

**依赖**：Provider 体系（NotifyProvider）、EventBus。

**关键能力**：
- 多渠道：企业微信/TG/Discord/Slack/Bark/ServerChan/钉钉/邮件（事实标准 1.9）
- 按事件类型路由
- 去重：`notification_dedupe` 表，按场景+任务+集数去重

### 2.11 认证与权限（Auth）

**职责**：登录鉴权、Session 管理、Webhook 鉴权、RBAC 扩展。

**依赖**：基础设施（bcrypt、WebAuthn）。

**关键能力**：
- Session + bcrypt（事实标准）
- WebAuthn Passkey 无密码（未来方案 4.10）
- 登录限流失败锁定（优秀实践）
- Webhook Token + HMAC 签名
- RBAC 多用户扩展（未来）

---

## 3. 目录结构

改进点：在现有 `app/providers/routes/services` 基础上，新增 `domain`（领域模型）、`infra`（基础设施）、`plugins`（插件目录），并将 `core.py` 拆解为各层职责，避免巨石文件（规避应避免 3.2）。

```
115-media-hub/
├── app/
│   ├── __init__.py
│   ├── main.py                    # FastAPI 应用入口（组装路由/中间件/生命周期）
│   ├── startup.py                 # 启动引导（DB 初始化/Provider 注册/调度器启动）
│   ├── background.py              # 后台运行时入口
│   │
│   ├── api/                       # API 层
│   │   ├── __init__.py
│   │   ├── deps.py                # 依赖注入（认证/配置/DB session）
│   │   ├── response.py            # 统一响应封装 {code,message,data}
│   │   ├── errors.py              # 统一异常处理（脱敏）
│   │   └── middleware.py          # 认证/CORS/Server-Timing/限流 中间件
│   │
│   ├── routes/                    # 路由分组（薄控制器，仅参数校验+调用 service）
│   │   ├── __init__.py
│   │   ├── settings.py            # /api/settings
│   │   ├── resource.py            # /api/resource
│   │   ├── subscription.py        # /api/subscription
│   │   ├── monitor.py             # /api/monitor
│   │   ├── scraper.py             # /api/scraper
│   │   ├── strm.py                # /api/strm
│   │   ├── tmdb.py                # /api/tmdb
│   │   ├── events.py              # /api/events (SSE)
│   │   ├── recommendation.py     # /api/recommendation
│   │   ├── webhook.py             # /webhook
│   │   ├── mcp.py                 # /api/v1/mcp (MCP 协议端点)
│   │   ├── auth.py                # /api/auth (登录/passkey)
│   │   └── pages.py               # 页面渲染路由
│   │
│   ├── services/                  # 业务服务层
│   │   ├── __init__.py
│   │   ├── resource.py            # 资源中心
│   │   ├── subscription.py         # 订阅引擎入口
│   │   ├── subscription_runner.py  # 订阅调度执行
│   │   ├── subscription_episode.py # 集数账本
│   │   ├── subscription_scoring.py # 评分算法
│   │   ├── subscription_share_selection.py # 新链挑选
│   │   ├── monitor.py             # 监控引擎
│   │   ├── strm_files.py          # STRM 引擎
│   │   ├── scraper.py             # 刮削引擎
│   │   ├── notify.py              # 通知服务
│   │   ├── scheduler.py           # 任务调度器
│   │   ├── recommendation.py      # 推荐清单
│   │   └── auth.py                # 认证与权限
│   │
│   ├── domain/                    # 领域模型层（纯逻辑，无 IO 依赖）
│   │   ├── __init__.py
│   │   ├── models.py              # 领域对象（Resource/Subscription/Episode...）
│   │   ├── resource_identity.py   # 资源去重/规范化
│   │   ├── link_parser.py         # 链接解析（分享链/磁力链）
│   │   ├── naming_template.py     # 命名模板引擎
│   │   ├── scoring.py             # 评分领域逻辑
│   │   └── episode_ledger.py      # 集数账本领域逻辑
│   │
│   ├── providers/                 # Provider 适配层（插件化）
│   │   ├── __init__.py
│   │   ├── base.py                # CloudProvider 抽象
│   │   ├── discovery_base.py      # DiscoveryProvider 抽象
│   │   ├── metadata_base.py       # MetadataProvider 抽象
│   │   ├── notify_base.py         # NotifyProvider 抽象
│   │   ├── registry.py            # 运行时注册表（init 注册 + 能力查询）
│   │   ├── common.py              # 共享工具
│   │   ├── pan115.py              # 115 网盘
│   │   ├── quark.py               # 夸克网盘
│   │   ├── aliyun.py              # 阿里云盘
│   │   ├── pan123.py              # 123 网盘
│   │   ├── tianyi.py              # 天翼云盘
│   │   ├── pansou.py              # 盘搜 DiscoveryProvider
│   │   ├── tg_discovery.py        # TG 频道 DiscoveryProvider
│   │   ├── tmdb.py                # TMDB MetadataProvider
│   │   ├── douban.py              # 豆瓣 MetadataProvider（防封禁框架）
│   │   └── notify/                # 通知 Provider
│   │       ├── wechat.py
│   │       ├── telegram.py
│   │       ├── discord.py
│   │       ├── bark.py
│   │       └── email.py
│   │
│   ├── plugins/                   # 插件体系（通用 Hook + 第三方扩展）
│   │   ├── __init__.py
│   │   ├── base.py                # Plugin 基类 + 生命周期
│   │   ├── manager.py             # 插件加载/卸载/沙箱
│   │   ├── manifest.py            # 插件清单（能力声明）
│   │   └── marketplace.py          # 插件市场（预留）
│   │
│   ├── infra/                     # 基础设施层
│   │   ├── __init__.py
│   │   ├── db.py                  # SQLite WAL/PG + 锁重试
│   │   ├── config_store.py        # JsonConfigStore（mtime 缓存）
│   │   ├── config_runtime.py      # 运行时配置覆盖
│   │   ├── event_bus.py           # 事件总线 + SSE
│   │   ├── cache.py               # 多级缓存（内存 LRU + 磁盘）
│   │   ├── http_client.py         # HTTP 客户端（代理/限流/重试）
│   │   ├── crypto.py              # 加密（Fernet）
│   │   ├── logger.py              # 结构化日志（按任务会话）
│   │   ├── webdav.py              # WebDAV 服务（预留）
│   │   └── metrics.py             # 指标（Server-Timing/Prometheus）
│   │
│   └── versioning.py              # schema 版本化迁移
│
├── plugins/                       # 外部插件目录（热加载扫描）
│   └── README.md
│
├── static/                        # 前端静态资源（Vue3 SPA 构建）
│   ├── css/
│   ├── js/
│   └── icons/
│
├── templates/                     # Jinja2 页面模板（首屏/登录）
│   ├── index.html
│   ├── login.html
│   └── partials/
│
├── tests/                         # 测试
│   ├── unit/
│   ├── integration/
│   ├── providers/                # Provider mock 测试
│   └── fixtures/
│
├── docs/                          # 文档（见第 12 章）
│   ├── market-analysis.md
│   ├── competitor-comparison.md
│   ├── best-practice.md
│   ├── architecture.md
│   ├── product-plan.md
│   ├── roadmap.md
│   └── DEVELOPMENT.md
│
├── Dockerfile
├── compose.yml
├── requirements.txt
├── main.py                        # CLI/启动入口
├── cli.py
└── README.md
```

**目录用途说明**：
- `app/api/`：API 层横切关注（中间件、依赖注入、统一响应、错误处理），与 `routes/` 分离让控制器更薄。
- `app/domain/`：纯领域逻辑，无 IO 依赖，便于单元测试（借鉴 DDD 分层）。
- `app/infra/`：基础设施实现，可替换（SQLite↔PG、本地缓存↔Redis）。
- `app/plugins/`：插件体系，与 `providers/`（内置 Provider）分离，`plugins/` 放第三方扩展。
- `plugins/`（根目录）：外部插件热加载扫描目录。

---

## 4. 插件体系

### 4.1 插件接口定义

五类插件统一接口，均继承 `Plugin` 基类：

```python
# app/plugins/base.py
class Plugin(ABC):
    plugin_id: str               # 唯一标识
    name: str                   # 显示名
    version: str
    author: str
    plugin_type: str            # "provider" / "discovery" / "metadata" / "notify" / "hook"
    capabilities: List[str]    # 能力声明
    config_fields: List[ConfigField] = []  # 配置字段（UI 自动渲染）

    @abstractmethod
    async def on_load(self, ctx: PluginContext) -> None: ...  # 加载
    async def on_enable(self) -> None: ...                     # 启用
    async def on_disable(self) -> None: ...                    # 禁用
    async def on_unload(self) -> None: ...                      # 卸载
```

**五类插件接口**：

| 插件类型 | 接口 | 能力声明示例 |
|---------|------|-------------|
| Provider 插件 | 实现 `CloudProvider` | `supports_strm`/`supports_share_receive`/`supports_incremental_sync` |
| Discovery 插件 | 实现 `DiscoveryProvider` | `supports_async_supplement`/`supports_mcp` |
| Metadata 插件 | 实现 `MetadataProvider` | `supports_movie`/`supports_tv`/`supports_chinese` |
| Notify 插件 | 实现 `NotifyProvider` | `supports_rich_text`/`supports_image` |
| 通用 Hook 插件 | 实现 `HookPlugin` | 订阅事件钩子（pre/post import、pre/post scrape） |

**ConfigField 定义**（UI 自动渲染依据，对标 [Radarr](https://github.com/Radarr/Radarr)）：

```python
@dataclass
class ConfigField:
    key: str
    label: str
    type: str  # "string" / "password" / "integer" / "boolean" / "select" / "text"
    required: bool = False
    default: Any = ""
    placeholder: str = ""
    options: List[str] = None  # select 枚举值
    sensitive: bool = False     # 敏感字段（脱敏返回）
    help: str = ""
```

### 4.2 插件生命周期

```
注册(Registry) → 加载(on_load) → 启用(on_enable) ⇄ 禁用(on_disable) → 卸载(on_unload)
      ↑                                              ↓
      └──────── 热重载（配置变更/手动刷新）──────────┘
```

- **注册**：插件入口点 `__init__.py` 调用 `registry.register(plugin_cls)`（借鉴 [Alist](https://github.com/AlistGo/alist) `init()` 注册）。
- **加载**：`on_load(ctx)` 注入配置、注册到对应 Provider 注册表。
- **启用/禁用**：运行时切换，不重启进程（对标 [MoviePilot](https://github.com/jxxghp/MoviePilot) 热插拔）。
- **卸载**：`on_unload()` 清理资源、注销。

### 4.3 插件加载机制

三种加载方式并存：

1. **入口点扫描**（内置 Provider）：`app/providers/` 各模块 `__init__` 注册，启动时 `startup.py` 统一加载。
2. **目录扫描**（外部插件）：扫描 `plugins/` 目录下符合 manifest 的插件包（借鉴 [aliyunpan](https://github.com/tickstep/aliyunpan) `~/.aliyunpan/plugins` 思路）。
3. **热加载**：运行时通过 `POST /api/settings/plugins/{id}/reload` 触发，不重启进程（对标 [MoviePilot](https://github.com/jxxghp/MoviePilot) 一键安装）。

```python
# app/plugins/manager.py
class PluginManager:
    def scan_directory(self, path: str) -> List[PluginManifest]: ...
    def load(self, manifest: PluginManifest) -> Plugin: ...
    def reload(self, plugin_id: str) -> None: ...  # 热重载
    def unload(self, plugin_id: str) -> None: ...
```

### 4.4 插件能力声明

借鉴 [Radarr](https://github.com/Radarr/Radarr) Provider 体系与 [Alist](https://github.com/AlistGo/alist) Driver 接口的布尔能力开关（优秀实践 2.1 + 未来方案 4.3）：

```python
class Capability(Enum):
    STRM = "strm"
    SHARE_RECEIVE = "share_receive"
    SUBSCRIPTION = "subscription"
    OFFLINE = "offline"
    MONITOR = "monitor"
    INCREMENTAL_SYNC = "incremental_sync"
    FILE_RENAME = "file_rename"
    ASYNC_SUPPLEMENT = "async_supplement"  # 先返回再补充
    MCP_EXPOSE = "mcp_expose"              # 暴露为 MCP 工具
```

UI 通过 `GET /api/settings/providers` 获取所有 Provider 及 `capabilities`，按能力自动展示对应配置面板与功能开关——新增 Provider 无需改前端代码（对标 [Radarr](https://github.com/Radarr/Radarr) UI 自动渲染表单）。

### 4.5 插件隔离与沙箱

- **进程内隔离**：插件运行于独立命名空间，注册表隔离，避免全局状态污染。
- **资源限制**：插件超时（`PLUGIN_TIMEOUT`，借鉴 [PanSou](https://github.com/fish2018/pansou)）、内存限额。
- **异常隔离**：插件异常不传播到主流程，降级返回空结果并记录告警。
- **配置隔离**：每个插件独立配置命名空间，互不干扰。
- **安全考量**：第三方插件默认禁用网络访问白名单外地址（防恶意外联）；敏感操作（文件删除/转存）需二次确认。

### 4.6 配置注入

插件配置通过 `PluginContext` 注入，遵循配置分层（见第 5 章）：

```python
@dataclass
class PluginContext:
    config: Dict[str, Any]      # 已规范化配置
    event_bus: EventBus          # 事件总线引用
    http_client: HttpClient      # 共享 HTTP 客户端（含代理/限流）
    logger: Logger               # 按插件 ID 分会话日志
    cache: Cache                 # 共享缓存
```

插件不直接读配置文件，统一通过 `ctx.config` 获取已脱敏、已规范化的配置值。

---

## 5. 配置体系

### 5.1 配置分层

四层叠加，优先级从低到高（规避 [aliyundrive-subscribe](https://github.com/adminpass/aliyundrive-subscribe) INI 单文件反面，应避免 3.10）：

```
默认值（代码内 DEFAULT_CONFIG）
    ↓ 被覆盖
环境变量（.env / Docker env，12-Factor）
    ↓ 被覆盖
配置文件（config/settings.json，JsonConfigStore 持久化）
    ↓ 被覆盖
运行时覆盖（Web UI 修改，POST /api/settings）
```

- **默认值**：代码内 `DEFAULT_CONFIG` 字典，保证开箱即用。
- **环境变量**：部署期注入（如 `SQLITE_LOCK_RETRY_ATTEMPTS`、`TZ`、`PUID/PGID`），符合 12-Factor（事实标准 1.2）。
- **配置文件**：`config/settings.json`，`JsonConfigStore` 持久化，Web UI 修改写入此层。
- **运行时覆盖**：临时覆盖不落盘，进程重启失效（用于调试）。

### 5.2 配置存储

采用已有 `JsonConfigStore`（优秀实践，mtime 缓存）：

- **线程安全**：`threading.Lock` 保护读写。
- **mtime 缓存**：`st_mtime_ns` 比对，未变更直接返回内存副本，避免重复 IO（`_cache_value` + `_cache_mtime_ns`）。
- **原子写入**：先写临时文件再 rename，避免写中断损坏。
- **规范化**：`normalize()` 回调统一补默认值、修正类型。
- **post_save 回调**：配置变更触发热重载（见 5.5）。

### 5.3 敏感字段处理

规避明文存储（应避免 3.3，借鉴 [CloudSaver](https://github.com/jiangrui1994/CloudSaver)/[AutoBangumi](https://github.com/EstrellaXD/Auto_Bangumi)）：

- **加密存储**：Cookie/Token/Password 写入前用 Fernet 对称加密，密钥派生自 `JWT_SECRET` 环境变量。
- **脱敏返回**：API 读取时敏感字段返回掩码（如 `****1234`）或留空，`ConfigField.sensitive=True` 标记。
- **留空保持原值**：前端提交空值时后端不覆盖原值（避免误清空）。

```python
def mask_sensitive(value: str) -> str:
    if not value or len(value) <= 4:
        return ""
    return value[:0] + "****" + value[-4:]
```

### 5.4 配置校验与规范化

- **Pydantic 模型校验**：每类配置定义 Pydantic `BaseModel`，类型/范围/必填校验。
- **normalize() 回调**：`JsonConfigStore` 加载后统一补默认值、修正非法值。
- **Provider 配置字段**：由 `config_fields` 声明，UI 自动渲染并前端校验。

### 5.5 热重载机制

借鉴 [MediaMTX](https://github.com/bluenviron/mediamtx) 配置热重载不中断连接（优秀实践 2.12）：

- `JsonConfigStore.save()` 后触发 `post_save(payload)` 回调。
- 回调内按变更字段分发：Provider 配置变更→重新初始化 Provider；调度周期变更→重设 cron；通知配置变更→重载 NotifyProvider。
- **不中断已有连接**：热重载仅影响新请求，已建立的 SSE/WebSocket 会话保持。

```python
def post_save(payload: Dict) -> None:
    changes = diff_config(old, payload)
    if "providers" in changes:
        registry.reload_providers(payload["providers"])
    if "scheduler" in changes:
        scheduler.reschedule(payload["scheduler"])
```

---

## 6. 权限体系

### 6.1 认证机制

- **Session + bcrypt**：登录成功后建立 Session（事实标准），密码 bcrypt 哈希存储，杜绝明文（应避免 3.3）。
- **WebAuthn Passkey**：未来方案 4.10，生物识别/安全密钥无密码登录，无密码落库（借鉴 [AutoBangumi](https://github.com/EstrellaXD/Auto_Bangumi)，规避 [aliyundrive-subscribe](https://github.com/adminpass/aliyundrive-subscribe) admin/admin 弱口令）。
- **首启动强制改密**：首次登录强制修改默认密码，规避默认弱口令被入侵（应避免 3.3）。
- **CSRF 防护**：表单提交校验 CSRF Token，Session 绑定。

### 6.2 登录限流

优秀实践（失败锁定）：

- 连续失败 N 次锁定账号 M 分钟（默认 N=5，M=15）。
- 按 IP + 账号双维度限流，防暴力破解。
- 锁定状态返回模糊错误（"账号或密码错误"），不泄露账号是否存在。

### 6.3 Webhook 鉴权

- **Token 校验**：每个 Webhook 配置独立 Token，请求头 `X-Webhook-Token` 比对。
- **HMAC 签名**：可选 HMAC-SHA256 签名（请求头 `X-Webhook-Signature`），`HMAC(secret, body)`，防篡改重放。
- **时间戳防重放**：携带 `X-Webhook-Timestamp`，超过容差拒绝。

### 6.4 API 认证中间件

```python
# app/api/middleware.py
class AuthMiddleware:
    EXEMPT_PATHS = {"/api/auth/login", "/api/auth/passkey/*", "/webhook", "/api/v1/mcp"}
    def __call__(self, request):
        if request.path in self.EXEMPT_PATHS:
            return  # 放行（webhook/mcp 单独鉴权）
        session = request.cookies.get("session")
        if not verify_session(session):
            raise HTTPException(401)
```

- Session 校验中间件覆盖所有 `/api/*`（除白名单）。
- MCP 端点单独 Token 鉴权（对标 [MoviePilot](https://github.com/jxxghp/MoviePilot) `/api/v1/mcp`）。
- API Key 模式（预留，供外部工具如 Requestrr/HomeAssistant 集成，事实标准 1.4）。

### 6.5 多用户与角色（未来扩展 RBAC）

当前单管理员，预留 RBAC 扩展（借鉴 [Seerr](https://github.com/seerr-team/seerr) 权限位 + [Alist](https://github.com/AlistGo/alist) 用户体系）：

- 角色：admin / user / guest。
- 权限位：`manage_settings` / `manage_subscription` / `manage_transfer` / `view_only`。
- 多用户配额（未来，对标 [Seerr](https://github.com/seerr-team/seerr)）。
- Override Rules：基于用户/标签的条件化默认值（优秀实践 2.14，对标 [Seerr](https://github.com/seerr-team/seerr)）。

### 6.6 CORS 策略

- 默认仅允许同源。
- 可配置允许的 Origin 白名单（`config.cors_origins`）。
- 凭证模式（Cookie）需显式白名单，禁用 `*` + `credentials`。

---

## 7. 数据模型

### 7.1 存储选型

**SQLite WAL + busy_timeout + 锁重试**（事实标准 1.3，已有 `app/infra/db.py` 实现）：

- `PRAGMA journal_mode = WAL`：读写并发，部分挂载文件系统不支持则降级。
- `PRAGMA busy_timeout = 30000`：写冲突等待 30s。
- `PRAGMA synchronous = NORMAL`：性能与可靠平衡。
- `PRAGMA temp_store = MEMORY`：临时表内存化。
- 锁重试：`retry_sqlite_locked` 指数退避（`SQLITE_LOCK_RETRY_ATTEMPTS=8`，`base=0.2s`，`max=2.5s`），规避应避免 3.12 长事务持锁。
- **可选 PostgreSQL**：通过 SQLAlchemy 抽象，多用户高并发场景切换（对标 [MoviePilot](https://github.com/jxxghp/MoviePilot)/[Seerr](https://github.com/seerr-team/seerr)）。

### 7.2 核心表设计

> 已有表沿用 `app/infra/db.py` 现有 schema，新增表标注【新增】，改进表标注【改进】。

#### 资源项 `resource_items`【沿用+改进】

```sql
CREATE TABLE resource_items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    source_type TEXT NOT NULL DEFAULT 'manual',      -- manual/tg/pansou/search
    source_name TEXT NOT NULL DEFAULT '',
    channel_name TEXT NOT NULL DEFAULT '',
    title TEXT NOT NULL,
    normalized_title TEXT NOT NULL DEFAULT '',       -- 去重用规范化标题
    raw_text TEXT NOT NULL DEFAULT '',
    link_url TEXT NOT NULL DEFAULT '',               -- 唯一索引去重
    link_type TEXT NOT NULL DEFAULT 'unknown',       -- 115/quark/aliyun/magnet
    message_url TEXT NOT NULL DEFAULT '',
    quality TEXT NOT NULL DEFAULT '',
    year TEXT NOT NULL DEFAULT '',
    status TEXT NOT NULL DEFAULT 'new',             -- new/imported/ignored
    created_at TEXT NOT NULL,
    published_at TEXT NOT NULL DEFAULT '',
    last_seen_at TEXT NOT NULL DEFAULT '',
    extra_json TEXT NOT NULL DEFAULT '{}'            -- cover_url/source_post_id/source_url
);
-- 索引：link_url 唯一、message_url、title_source、created_at、status
```

#### 资源转存任务 `resource_jobs`【沿用】

```sql
CREATE TABLE resource_jobs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    resource_id INTEGER NOT NULL,
    title TEXT NOT NULL DEFAULT '',
    link_url TEXT NOT NULL DEFAULT '',
    link_type TEXT NOT NULL DEFAULT '',
    folder_id TEXT NOT NULL DEFAULT '',
    savepath TEXT NOT NULL DEFAULT '',
    sharetitle TEXT NOT NULL DEFAULT '',
    monitor_task_name TEXT NOT NULL DEFAULT '',
    refresh_delay_seconds INTEGER NOT NULL DEFAULT 0,
    auto_refresh INTEGER NOT NULL DEFAULT 1,
    status TEXT NOT NULL DEFAULT 'pending',         -- pending/running/succeeded/failed
    status_detail TEXT NOT NULL DEFAULT '',
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    started_at TEXT NOT NULL DEFAULT '',
    finished_at TEXT NOT NULL DEFAULT '',
    last_triggered_at TEXT NOT NULL DEFAULT '',
    response_json TEXT NOT NULL DEFAULT '{}',
    extra_json TEXT NOT NULL DEFAULT '{}'
);
```

#### 订阅状态 `subscription_task_state`【沿用】

```sql
CREATE TABLE subscription_task_state (
    task_name TEXT PRIMARY KEY,
    media_type TEXT NOT NULL DEFAULT 'movie',       -- movie/tv/anime
    status TEXT NOT NULL DEFAULT 'idle',            -- idle/running/succeeded/failed
    progress INTEGER NOT NULL DEFAULT 0,
    detail TEXT NOT NULL DEFAULT '',
    last_run_at TEXT NOT NULL DEFAULT '',
    last_success_at TEXT NOT NULL DEFAULT '',
    last_error TEXT NOT NULL DEFAULT '',
    last_episode INTEGER NOT NULL DEFAULT 0,
    total_episodes INTEGER NOT NULL DEFAULT 0,
    matched_resource_id INTEGER NOT NULL DEFAULT 0,
    matched_resource_title TEXT NOT NULL DEFAULT '',
    matched_score INTEGER NOT NULL DEFAULT 0,
    queued_job_id INTEGER NOT NULL DEFAULT 0,
    stats_json TEXT NOT NULL DEFAULT '{}',
    updated_at TEXT NOT NULL
);
```

#### 订阅匹配 `subscription_matches`【沿用】

```sql
CREATE TABLE subscription_matches (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    task_name TEXT NOT NULL,
    resource_id INTEGER NOT NULL,
    job_id INTEGER NOT NULL DEFAULT 0,
    media_type TEXT NOT NULL DEFAULT 'movie',
    season INTEGER NOT NULL DEFAULT 0,
    episode INTEGER NOT NULL DEFAULT 0,
    total_episodes INTEGER NOT NULL DEFAULT 0,
    score INTEGER NOT NULL DEFAULT 0,
    matched_at TEXT NOT NULL,
    UNIQUE(task_name, resource_id)
);
```

#### 集数账本 `subscription_episode_ledger`【沿用】

```sql
CREATE TABLE subscription_episode_ledger (
    task_name TEXT NOT NULL,
    episode INTEGER NOT NULL,
    season INTEGER NOT NULL DEFAULT 0,
    media_type TEXT NOT NULL DEFAULT 'tv',
    best_score INTEGER NOT NULL DEFAULT 0,          -- 同集最优命中分数
    best_resolution INTEGER NOT NULL DEFAULT 0,
    source_fp TEXT NOT NULL DEFAULT '',              -- 来源指纹
    content_fp TEXT NOT NULL DEFAULT '',             -- 内容指纹
    link_type TEXT NOT NULL DEFAULT '',
    link_url TEXT NOT NULL DEFAULT '',
    resource_id INTEGER NOT NULL DEFAULT 0,
    job_id INTEGER NOT NULL DEFAULT 0,
    status TEXT NOT NULL DEFAULT 'active',           -- active/superseded
    first_seen_at TEXT NOT NULL DEFAULT '',
    updated_at TEXT NOT NULL DEFAULT '',
    PRIMARY KEY (task_name, episode)
);
```

#### 频道搜索水位 `subscription_channel_search_watermarks`【沿用】

```sql
CREATE TABLE subscription_channel_search_watermarks (
    task_name TEXT NOT NULL,
    channel_id TEXT NOT NULL,
    last_post_cursor INTEGER NOT NULL DEFAULT 0,    -- 增量游标
    last_published_at TEXT NOT NULL DEFAULT '',
    last_run_at TEXT NOT NULL DEFAULT '',
    updated_at TEXT NOT NULL DEFAULT '',
    PRIMARY KEY (task_name, channel_id)
);
```

#### 频道支持统计 `subscription_channel_support_stats`【沿用】

```sql
CREATE TABLE subscription_channel_support_stats (
    channel_id TEXT PRIMARY KEY,
    channel_name TEXT NOT NULL DEFAULT '',
    searched_runs INTEGER NOT NULL DEFAULT 0,
    matched_runs INTEGER NOT NULL DEFAULT 0,
    matched_items INTEGER NOT NULL DEFAULT 0,
    error_runs INTEGER NOT NULL DEFAULT 0,
    incremental_stop_hits INTEGER NOT NULL DEFAULT 0,
    pages_scanned INTEGER NOT NULL DEFAULT 0,
    last_task_name TEXT NOT NULL DEFAULT '',
    last_provider TEXT NOT NULL DEFAULT '',
    last_trigger TEXT NOT NULL DEFAULT '',
    last_error TEXT NOT NULL DEFAULT '',
    last_searched_at TEXT NOT NULL DEFAULT '',
    last_matched_at TEXT NOT NULL DEFAULT '',
    updated_at TEXT NOT NULL DEFAULT ''
);
```

#### 监控文件 `monitor_files`【沿用】

```sql
CREATE TABLE monitor_files (
    task_name TEXT NOT NULL,
    local_rel_path TEXT NOT NULL,
    remote_rel_path TEXT NOT NULL,
    remote_modified TEXT,                           -- mtime 比对
    file_size INTEGER DEFAULT 0,
    PRIMARY KEY (task_name, local_rel_path)
);
```

#### 监控目录 `monitor_dirs`【沿用】

```sql
CREATE TABLE monitor_dirs (
    task_name TEXT NOT NULL,
    dir_rel_path TEXT NOT NULL,
    remote_modified TEXT,
    needs_rescan INTEGER NOT NULL DEFAULT 0,        -- 补扫标记
    missing_confirmations INTEGER NOT NULL DEFAULT 0,
    PRIMARY KEY (task_name, dir_rel_path)
);
```

#### 本地文件 `local_files`【沿用】

```sql
CREATE TABLE local_files (
    path_hash TEXT PRIMARY KEY,
    relative_path TEXT,
    scan_token TEXT NOT NULL DEFAULT ''              -- 增量同步令牌（借鉴 qmediasync）
);
```

#### 刮削任务 `scraper_jobs`【沿用】

```sql
CREATE TABLE scraper_jobs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    provider TEXT NOT NULL DEFAULT '',
    status TEXT NOT NULL DEFAULT 'pending',
    status_detail TEXT NOT NULL DEFAULT '',
    total_actions INTEGER NOT NULL DEFAULT 0,
    succeeded_actions INTEGER NOT NULL DEFAULT 0,
    failed_actions INTEGER NOT NULL DEFAULT 0,
    rollback_succeeded_actions INTEGER NOT NULL DEFAULT 0,
    rollback_failed_actions INTEGER NOT NULL DEFAULT 0,
    created_at TEXT NOT NULL DEFAULT '',
    updated_at TEXT NOT NULL DEFAULT '',
    started_at TEXT NOT NULL DEFAULT '',
    finished_at TEXT NOT NULL DEFAULT '',
    options_json TEXT NOT NULL DEFAULT '{}',
    tmdb_json TEXT NOT NULL DEFAULT '{}',
    plan_json TEXT NOT NULL DEFAULT '{}'
);
```

#### 刮削动作 `scraper_job_actions`【沿用】

```sql
CREATE TABLE scraper_job_actions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    job_id INTEGER NOT NULL,
    action_index INTEGER NOT NULL DEFAULT 0,
    provider TEXT NOT NULL DEFAULT '',
    entry_id TEXT NOT NULL DEFAULT '',
    is_dir INTEGER NOT NULL DEFAULT 0,
    old_parent_id TEXT NOT NULL DEFAULT '',
    old_name TEXT NOT NULL DEFAULT '',
    old_path TEXT NOT NULL DEFAULT '',
    new_parent_id TEXT NOT NULL DEFAULT '',
    new_name TEXT NOT NULL DEFAULT '',
    new_path TEXT NOT NULL DEFAULT '',
    target_parent_path TEXT NOT NULL DEFAULT '',
    status TEXT NOT NULL DEFAULT 'pending',
    status_detail TEXT NOT NULL DEFAULT '',
    rollback_status TEXT NOT NULL DEFAULT '',
    rollback_detail TEXT NOT NULL DEFAULT '',
    created_at TEXT NOT NULL DEFAULT '',
    updated_at TEXT NOT NULL DEFAULT '',
    response_json TEXT NOT NULL DEFAULT '{}'
);
```

#### 推荐清单 `recommendation_watchlist`【沿用】

```sql
CREATE TABLE recommendation_watchlist (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    tmdb_id INTEGER NOT NULL,
    media_type TEXT NOT NULL DEFAULT 'movie',
    title TEXT NOT NULL,
    original_title TEXT DEFAULT '',
    year TEXT DEFAULT '',
    poster_url TEXT DEFAULT '',
    overview TEXT DEFAULT '',
    vote_average REAL DEFAULT 0,
    tmdb_detail_json TEXT DEFAULT '{}',
    status TEXT NOT NULL DEFAULT 'want',
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    UNIQUE(tmdb_id, media_type)
);
```

#### 通知去重 `notification_dedupe`【沿用】

```sql
CREATE TABLE notification_dedupe (
    dedupe_key TEXT PRIMARY KEY,
    scene TEXT NOT NULL DEFAULT '',
    task_name TEXT NOT NULL DEFAULT '',
    episode INTEGER NOT NULL DEFAULT 0,
    savepath TEXT NOT NULL DEFAULT '',
    created_at TEXT NOT NULL DEFAULT '',
    expires_at TEXT NOT NULL DEFAULT ''
);
```

#### 分享缓存 `share_entries_cache`【沿用】

```sql
CREATE TABLE share_entries_cache (
    cache_key TEXT PRIMARY KEY,
    share_code TEXT NOT NULL DEFAULT '',
    receive_code TEXT NOT NULL DEFAULT '',
    cid TEXT NOT NULL DEFAULT '0',
    payload_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL DEFAULT '',
    expires_at TEXT NOT NULL DEFAULT ''
);
```

#### 凭据存储 `credentials`【新增】

```sql
CREATE TABLE credentials (
    provider_name TEXT NOT NULL,
    credential_type TEXT NOT NULL DEFAULT 'cookie', -- cookie/refresh_token/oauth
    encrypted_value TEXT NOT NULL,                   -- Fernet 加密
    health_status TEXT NOT NULL DEFAULT 'unknown',   -- green/yellow/red
    last_probe_at TEXT NOT NULL DEFAULT '',
    last_probe_ok INTEGER NOT NULL DEFAULT 0,
    updated_at TEXT NOT NULL,
    PRIMARY KEY (provider_name, credential_type)
);
```

#### 用户 `users`【新增】

```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL DEFAULT '',           -- bcrypt，Passkey 用户为空
    role TEXT NOT NULL DEFAULT 'admin',
    permissions INTEGER NOT NULL DEFAULT 0,           -- 权限位
    must_change_password INTEGER NOT NULL DEFAULT 0,  -- 首启动强制改密
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);
```

#### WebAuthn 凭据 `webauthn_credentials`【新增】

```sql
CREATE TABLE webauthn_credentials (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    credential_id TEXT NOT NULL UNIQUE,               -- base64
    public_key BLOB NOT NULL,
    sign_count INTEGER NOT NULL DEFAULT 0,
    device_type TEXT NOT NULL DEFAULT '',
    created_at TEXT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id)
);
```

#### 任务会话 `task_sessions`【新增】

```sql
CREATE TABLE task_sessions (
    session_id TEXT PRIMARY KEY,                      -- UUID
    task_type TEXT NOT NULL,                          -- subscription/monitor/scraper/import
    task_name TEXT NOT NULL DEFAULT '',
    status TEXT NOT NULL DEFAULT 'running',
    started_at TEXT NOT NULL,
    finished_at TEXT NOT NULL DEFAULT '',
    log_path TEXT NOT NULL DEFAULT '',                -- 日志文件路径
    stats_json TEXT NOT NULL DEFAULT '{}'
);
```

#### 插件状态 `plugins_state`【新增】

```sql
CREATE TABLE plugins_state (
    plugin_id TEXT PRIMARY KEY,
    enabled INTEGER NOT NULL DEFAULT 0,
    config_json TEXT NOT NULL DEFAULT '{}',
    installed_at TEXT NOT NULL DEFAULT '',
    updated_at TEXT NOT NULL DEFAULT ''
);
```

### 7.3 索引策略

沿用现有索引（`idx_resource_items_*`、`idx_resource_jobs_*`、`idx_subscription_*` 等），新增：

```sql
CREATE INDEX idx_credentials_health ON credentials(health_status);
CREATE INDEX idx_users_username ON users(username);
CREATE INDEX idx_task_sessions_task ON task_sessions(task_type, status, started_at DESC);
CREATE INDEX idx_task_sessions_status ON task_sessions(status);
```

- 资源项：按 link_url 唯一、status、created_at、source_type+channel 复合索引，支撑列表过滤与去重。
- 订阅：按 task_name + matched_at 支撑追更历史查询。
- 集数账本：按 task_name + status 支撑活跃集数查询。
- 任务会话：按 task_type + started_at 支撑日志分页。

### 7.4 锁与并发控制

优秀实践（短事务 + 写锁退避重试）：

- **短事务**：每个写操作尽快提交，不跨网络 IO 持锁（规避应避免 3.12 长事务持锁）。
- **写锁退避重试**：`retry_sqlite_locked` 指数退避（已有实现，`attempts=8`，`base=0.2s`，`max=2.5s`）。
- **连接级隔离**：每次操作 `open_db()` 新连接，用完即关，WAL 模式下读写并发。
- **限流隔离**：Provider 级 `throttle()` 限流锁独立于 DB 锁，避免 IO 等待持 DB 锁。

---

## 8. API 规范

### 8.1 API 风格

REST + JSON + 统一响应封装（事实标准 1.4，对标 [Alist](https://github.com/AlistGo/alist) `{code,message,data}` 包络、[MoviePilot](https://github.com/jxxghp/MoviePilot) `/api/v1/`、[Sonarr](https://github.com/Sonarr/Sonarr)/[Radarr](https://github.com/Radarr/Radarr) `/api/v3`）。

- **序列化**：JSON，UTF-8，时间戳 ISO8601。
- **分页**：`?page=1&page_size=20`，响应含 `total`。
- **OpenAPI**：FastAPI 自动生成 `/docs`（Swagger）+ `/redoc`。

### 8.2 路由分组

| 分组 | 前缀 | 用途 |
|------|------|------|
| 设置 | `/api/settings` | 配置增删改查、Provider 列表、插件管理 |
| 资源 | `/api/resource` | 资源搜索、导入、任务查询 |
| 订阅 | `/api/subscription` | 订阅增删改、触发、状态 |
| 监控 | `/api/monitor` | 监控任务、扫描、补扫 |
| 刮削 | `/api/scraper` | 刮削任务、TMDB 识别、重命名预览 |
| STRM | `/api/strm` | STRM 生成、清理、中继 |
| TMDB | `/api/tmdb` | TMDB 搜索、详情、推荐 |
| 事件 | `/api/events` | SSE 推送 |
| 推荐 | `/api/recommendation` | 推荐清单管理 |
| Webhook | `/webhook` | 外部事件接入（独立鉴权） |
| MCP | `/api/v1/mcp` | MCP 协议端点（对标 [MoviePilot](https://github.com/jxxghp/MoviePilot)） |
| 认证 | `/api/auth` | 登录、Passkey、登出 |

### 8.3 统一响应封装

```json
{
  "code": 0,
  "message": "ok",
  "data": { ... }
}
```

- `code: 0` 成功，非 0 失败。
- `message`：人类可读描述（错误时脱敏，见 8.4）。
- `data`：业务数据，失败时为 `null` 或 `{}`。
- 分页响应：`data` 内含 `{items, total, page, page_size}`。

### 8.4 错误处理（脱敏）

规避明文返回异常（应避免 3.3）：

- **不泄露内部异常**：错误响应不返回堆栈、SQL、文件路径、凭据片段。
- **统一错误码**：`4001` 参数错误、`4011` 未认证、`4031` 无权限、`4041` 不存在、`4291` 限流、`5001` 内部错误。
- **日志记录详情**：完整异常写入日志（按任务会话），响应仅返回脱敏 message。
- **Provider 错误降级**：网盘 API 失败返回友好提示（如"网盘暂不可用，请检查 Cookie"），不暴露原始 4xx/5xx。

```python
# app/api/errors.py
@app.exception_handler(Exception)
async def handle_exception(request, exc):
    logger.exception(exc, extra={"session": request.state.session_id})
    if isinstance(exc, HTTPException):
        return JSONResponse({"code": exc.status_code * 10 + 1, "message": exc.detail, "data": None})
    return JSONResponse({"code": 5001, "message": "内部错误，请查看日志", "data": None}, status_code=500)
```

### 8.5 版本化策略

- **URL 版本前缀**：`/api/v1/`（对标 [MoviePilot](https://github.com/jxxghp/MoviePilot)/[Sonarr](https://github.com/Sonarr/Sonarr)）。
- 当前默认 `/api/` 等同 `/api/v1/`，未来破坏性变更走 `/api/v2/` 并保留 v1 兼容期（规避应避免 3.8 升级不兼容）。
- **响应头版本**：`X-API-Version: v1`。

### 8.6 关键端点示例

**资源搜索**：

```
GET /api/resource/search?keyword=三体&providers=pansou,tg&limit=20
响应:
{
  "code": 0, "message": "ok",
  "data": {
    "items": [
      {"id": 1, "title": "三体.2023.4K", "link_url": "...", "link_type": "115", "quality": "4K", "source_name": "tg-channel-a"},
      ...
    ],
    "total": 42,
    "supplemental": false   // 是否还有异步补充结果（借鉴 PanSou）
  }
}
```

异步补充（借鉴 [PanSou](https://github.com/fish2018/pansou) 先返回再补充）：首次返回 `supplemental: false`，后台补充结果通过 SSE 推送 `resource.supplemented` 事件，前端追加。

**订阅触发**：

```
POST /api/subscription/{task_name}/trigger
响应:
{
  "code": 0, "message": "ok",
  "data": {"session_id": "uuid-xxx", "started_at": "2026-07-10T12:00:00"}
}
```

任务启动分配 `session_id`，状态与日志按 session 查询。

**Webhook 接入**：

```
POST /webhook
Headers:
  X-Webhook-Token: <token>
  X-Webhook-Signature: <hmac-sha256>
  X-Webhook-Timestamp: 1720000000
Body: {"event": "resource.imported", "resource_id": 1}
响应: {"code": 0, "message": "ok", "data": {"accepted": true}}
```

---

## 9. 事件系统

### 9.1 事件总线设计

借鉴 [MoviePilot](https://github.com/jxxghp/MoviePilot) `app/core/event.py` 事件驱动（未来方案 4.4）：

```python
# app/infra/event_bus.py
class EventBus:
    _handlers: Dict[str, List[Callable]] = {}

    def publish(self, event_type: str, payload: Dict) -> None:
        for handler in self._handlers.get(event_type, []):
            asyncio.create_task(handler(payload))

    def subscribe(self, event_type: str, handler: Callable) -> None:
        self._handlers.setdefault(event_type, []).append(handler)
```

模块通过订阅事件解耦：监控引擎发布 `monitor.completed` → STRM 引擎订阅生成 STRM → 刮削引擎订阅刮削 → 通知服务订阅推送。

### 9.2 SSE 推送

轻量状态 + 按需拉日志（优秀实践 2.3）：

- **SSE 通道**：`GET /api/events/stream`，推送轻量状态变更（任务状态、进度、Cookie 健康）。
- **按需拉日志**：状态事件仅含 `session_id` + 状态摘要，前端按需 `GET /api/events/{session_id}/logs` 拉取详细日志（流式 tail）。
- **避免大日志推送**：不在 SSE 中推送完整日志，降低带宽与内存峰值。

```python
# SSE 事件示例
event: task.status_changed
data: {"session_id":"uuid","task_type":"subscription","task_name":"三体","status":"running","progress":45}

event: cookie.health_changed
data: {"provider":"115","health":"yellow"}
```

### 9.3 事件类型定义

| 事件类型 | 触发时机 | 负载 |
|---------|---------|------|
| `task.status_changed` | 任务状态变更 | session_id, task_type, task_name, status, progress |
| `resource.imported` | 资源转存完成 | resource_id, job_id, savepath |
| `resource.supplemented` | 异步搜索补充完成 | keyword, items, source |
| `subscription.matched` | 订阅命中 | task_name, resource_id, episode, score |
| `monitor.completed` | 监控扫描完成 | task_name, changed_count, scan_token |
| `scraper.completed` | 刮削完成 | job_id, succeeded, failed |
| `cookie.health_changed` | Cookie 健康变更 | provider, health |
| `strm.generated` | STRM 生成 | task_name, count |
| `notify.sent` | 通知发送 | scene, channel |

### 9.4 节流与去重

- `UI_PUSH_DEBOUNCE`：高频事件（如进度更新）合并去抖，默认 500ms 内仅推最后一帧。
- **去重**：相同 `(event_type, task_name, status)` 在短窗口内不重复推送。
- **背压**：SSE 客户端慢消费时丢弃旧状态，仅保留最新（状态可覆盖，日志不可丢）。

### 9.5 事件订阅模型

```python
# 业务服务订阅事件（解耦）
event_bus.subscribe("monitor.completed", strm_engine.on_monitor_completed)
event_bus.subscribe("monitor.completed", scraper_engine.on_monitor_completed)
event_bus.subscribe("resource.imported", notify_service.on_resource_imported)
event_bus.subscribe("subscription.matched", notify_service.on_subscription_matched)
event_bus.subscribe("cookie.health_changed", notify_service.on_cookie_health_changed)
```

Hook 插件也可订阅任意事件（见第 4 章），实现用户自定义后处理。

---

## 10. 日志系统

### 10.1 日志分级

三类日志分离（未来方案 4.9）：

| 类型 | 用途 | 文件 |
|------|------|------|
| 任务日志 | 订阅/监控/刮削/转存任务执行明细 | `logs/task/{session_id}.log` |
| 访问日志 | HTTP 请求/响应 | `logs/access.log` |
| 系统日志 | 启动/Provider 注册/异常 | `logs/system.log` |

### 10.2 按任务会话分页

借鉴优秀实践（避免按行截断）：

- 每个任务实例分配 `session_id`（UUID），日志写入独立文件 `logs/task/{session_id}.log`。
- 前端按 `session_id` + 分页查询（`?page=1&page_size=100`），而非按行号截断大文件。
- 任务完成后日志保留 N 天后清理。

```python
# app/infra/logger.py
def get_task_logger(session_id: str) -> Logger:
    handler = FileHandler(f"logs/task/{session_id}.log", encoding="utf-8")
    handler.setFormatter(JSONFormatter())  # 结构化 JSON
    logger = Logger(f"task.{session_id}")
    logger.addHandler(handler)
    return logger
```

### 10.3 日志文件组织

```
logs/
├── task/
│   ├── {uuid-1}.log          # 按任务会话独立文件
│   ├── {uuid-2}.log
│   └── ...
├── monitor.log               # 监控引擎汇总（可选，便于运维）
├── subscription.log          # 订阅引擎汇总
├── access.log                # 访问日志
└── system.log                # 系统日志
```

- 任务日志按会话独立，便于隔离排查（避免单文件过大）。
- 引擎汇总日志便于跨任务运维概览。

### 10.4 日志读取

流式 tail + 固定长度（优秀实践）：

- `GET /api/events/{session_id}/logs?tail=100`：返回最后 100 行。
- `GET /api/events/{session_id}/logs?from=offset&limit=100`：分页正向读取。
- **流式 tail**：SSE 推送日志变更，前端实时追加（仅 tail 模式）。
- **固定长度**：避免一次读入大文件导致内存峰值。

### 10.5 可观测性

未来方案 4.9（填补领域前瞻空白，借鉴 [MoviePilot](https://github.com/jxxghp/MoviePilot)/[PanSou](https://github.com/fish2018/pansou) 可观测思路）：

- **Server-Timing 头**：HTTP 响应注入 `Server-Timing: db;dur=12, provider;dur=340, total;dur=380`，暴露内部耗时。

```python
# app/api/middleware.py
class ServerTimingMiddleware:
    async def __call__(self, request, call_next):
        timings = {}
        response = await call_next(request, timings)
        response.headers["Server-Timing"] = format_timings(timings)
        response.headers["X-Server-Time-Ms"] = str(timings.get("total", 0))
        return response
```

- **结构化日志**：JSON 格式，含 `timestamp/level/session_id/task_type/message/extra`，便于 ELK/Loki 采集。
- **指标暴露**（预留 Prometheus）：缓存命中率、上游限流次数、任务耗时分布、Cookie 健康分布。
- **请求追踪**：每个请求分配 `request_id`，贯穿日志与 Server-Timing。

---

## 11. 测试方案

### 11.1 单元测试

pytest（对标 [MoviePilot](https://github.com/jxxghp/MoviePilot)/[AutoBangumi](https://github.com/EstrellaXD/Auto_Bangumi)）：

- **Provider 能力声明**：验证 `supports_*` 布尔开关正确性。
- **链接解析**：分享链/磁力链识别、link_type 判定（`domain/link_parser.py`）。
- **评分算法**：订阅匹配评分、集数账本最优命中（`domain/scoring.py`、`domain/episode_ledger.py`）。
- **命名模板**：变量占位替换、正则捕获（`domain/naming_template.py`）。
- **资源去重**：normalized_title 规范化、link_url 唯一性。
- **配置脱敏**：敏感字段掩码逻辑。
- **锁重试**：`retry_sqlite_locked` 退避逻辑。

```python
# tests/unit/test_scoring.py
def test_episode_ledger_keeps_best_score():
    ledger = EpisodeLedger()
    ledger.record(task="三体", episode=1, score=80, resolution=1080)
    ledger.record(task="三体", episode=1, score=90, resolution=2160)
    assert ledger.best("三体", 1).score == 90
```

### 11.2 集成测试

- **路由测试**：FastAPI `TestClient`，覆盖各路由分组端点、认证、响应封装。
- **数据库测试**：临时 SQLite，验证 schema 迁移、索引、并发写锁重试。
- **后台任务**：模拟订阅触发→匹配→转存→通知全链路。
- **事件总线**：发布订阅链路、SSE 推送。
- **配置热重载**：post_save 触发 Provider 重载。

```python
# tests/integration/test_subscription_flow.py
def test_subscription_full_flow(client, db):
    create_subscription(client, task_name="三体", media_type="tv")
    trigger(client, "三体")
    wait_for_status(client, "三体", "succeeded")
    assert get_episode_ledger(db, "三体") != []
```

### 11.3 Provider 模拟测试

mock 网盘 API（避免真实凭据与风控）：

- **Mock CloudProvider**：实现 `CloudProvider` 接口返回固定/动态响应，模拟分享转存、增量同步、Cookie 探测。
- **Mock DiscoveryProvider**：模拟 TG 频道搜索、盘搜结果，含异步补充。
- **Mock MetadataProvider**：模拟 TMDB/豆瓣响应，含节流限流场景。
- **错误注入**：模拟 429 限流、Cookie 失效、网络超时，验证降级与重试。

```python
# tests/providers/test_pan115_mock.py
class MockPan115(CloudProvider):
    supports_incremental_sync = True
    def list_entries_incremental(self, cookie, cid, scan_token):
        return FIXTURE_ENTRIES[:5], "new_scan_token"
```

### 11.4 测试数据管理

- `tests/fixtures/`：固定的分享链样本、TMDB 响应快照、TG 消息样本。
- **脱敏数据**：测试用 Cookie/Token 一律 mock，禁止真实凭据入仓库（安全）。
- **快照测试**：TMDB/豆瓣响应存 JSON 快照，避免重复请求上游。
- **工厂函数**：`make_resource()`/`make_subscription()` 等构建测试对象。

### 11.5 CI 集成

GitHub Actions（对标 [OpenList](https://github.com/OpenListTeam/OpenList)/[Seerr](https://github.com/seerr-team/seerr) 组织化）：

```yaml
# .github/workflows/ci.yml
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with: { python-version: "3.12" }
      - run: pip install -r requirements.txt -r requirements-dev.txt
      - run: pytest --cov=app --cov-report=xml
      - run: ruff check app tests
      - run: mypy app
  docker:
    needs: test
    steps:
      - uses: docker/build-push-action@v5
```

- **矩阵测试**：Python 3.12 + SQLite/PG 双数据库。
- **覆盖率门槛**：≥ 70%（核心 domain 层 ≥ 90%）。
- **lint + type check**：ruff + mypy。
- **Docker 构建验证**：CI 内构建镜像确认 Dockerfile 可用。

---

## 12. 文档结构

### 12.1 docs/ 目录组织

```
docs/
├── market-analysis.md          # 阶段一、二：市场调研明细（20 项目）
├── competitor-comparison.md     # 阶段三：横向对比矩阵（15 项目）
├── best-practice.md             # 阶段四：最佳实践提炼（事实标准/优秀/应避免/未来）
├── architecture.md              # 阶段五：架构设计（本文档）
├── product-plan.md              # 阶段六：产品规划
├── roadmap.md                   # 路线图
├── DEVELOPMENT.md               # 贡献者开发指南
├── _research/                   # 调研原始材料
│   ├── 01-cloud-storage-media.md
│   ├── 02-subscription-tracking.md
│   ├── 03-scraping-metadata.md
│   ├── 04-search-transfer.md
│   └── 05-media-server-ecosystem.md
└── superpowers/                 # 设计方案与交接文档
    ├── plans/
    └── specs/
```

**文档间引用关系**：`market-analysis` → `competitor-comparison` → `best-practice` → `architecture`（本文档引用前三者作为设计依据）→ `product-plan` → `roadmap`。

### 12.2 API 文档

FastAPI 自动 OpenAPI（事实标准 1.1/1.4）：

- `/docs`：Swagger UI 交互式文档（开发期）。
- `/redoc`：ReDoc 文档（阅读友好）。
- `/openapi.json`：OpenAPI 规范文件，可供外部工具（Requestrr/HomeAssistant）集成。
- **独立 MCP 文档**：`/api/v1/mcp` 端点的工具清单单独维护（对标 [MoviePilot](https://github.com/jxxghp/MoviePilot) Wiki MCP 独立文档）。

每个端点通过 Pydantic 模型 + docstring 自动生成文档，无需手工维护 API 文档。

### 12.3 用户文档

面向 NAS 用户的部署与使用指南（对标 [Alist](https://github.com/AlistGo/alist) 文档站、[MoviePilot](https://github.com/jxxghp/MoviePilot) Wiki）：

- **快速开始**：Docker 部署、首次配置向导、Cookie 配置。
- **功能指南**：订阅配置、监控配置、STRM 配置、刮削配置、通知配置。
- **FAQ**：Cookie 失效处理、429 限流、代理配置（规避应避免 3.13）、302 不能播放。
- **集成指南**：与 Emby/Jellyfin/Plex/Alist 联动、Webhook 接入、MCP 接入。

### 12.4 贡献者文档

`DEVELOPMENT.md`（对标 [Seerr](https://github.com/seerr-team/seerr)/[OpenList](https://github.com/OpenListTeam/OpenList) 组织化，规避应避免 3.6 单点风险）：

- **开发环境搭建**：Python venv、前端构建、数据库初始化。
- **架构概览**：分层说明、Provider 体系、插件开发。
- **Provider 开发指南**：如何新增 CloudProvider/DiscoveryProvider，能力声明、config_fields 定义、注册流程。
- **插件开发指南**：插件接口、生命周期、沙箱限制、配置注入（对标 [PanSou](https://github.com/fish2018/pansou)《插件开发指南.md》）。
- **提交规范**：Conventional Commits、PR 流程、代码审查、测试要求。
- **版本与迁移**：schema 迁移脚本编写、向后兼容策略（规避应避免 3.8）。
- **组织化运营**：多贡献者协作、透明 PR、避免单一维护者停摆（对标 [OpenList](https://github.com/OpenListTeam/OpenList)）。

---

## 附录：设计决策与最佳实践依据映射

| 本方案设计决策 | 最佳实践依据 | 借鉴项目 | 规避的反面 |
|--------------|------------|---------|-----------|
| FastAPI 异步 | 事实标准 1.1 | MoviePilot/quark-auto-save | nas-tools Flask |
| Docker 单容器 | 事实标准 1.2 | MoviePilot/Alist | — |
| SQLite+可选 PG | 事实标准 1.3 | MoviePilot/Seerr | — |
| REST+JSON 统一响应 | 事实标准 1.4 | Alist/MoviePilot | — |
| Webhook 触发 | 事实标准 1.5 | Sonarr/Radarr | — |
| TMDB 元数据 | 事实标准 1.6 | MoviePilot | — |
| cron 调度 | 事实标准 1.7 | quark-auto-save | — |
| Web 管理后台 | 事实标准 1.8 | 全部 | tinyMediaManager VNC |
| 多渠道通知 | 事实标准 1.9 | MoviePilot/nas-tools | — |
| 批量重命名模板 | 事实标准 1.10 | TMM/aliyundrive-subscribe | — |
| Provider 能力声明+UI 自动渲染 | 优秀 2.1 + 未来 4.3 | Radarr/Alist | — |
| Driver init() 注册 | 优秀 2.2 | Alist | — |
| 异步插件先返回再补充 | 优秀 2.3 | PanSou | — |
| 115 开放平台接入 | 优秀 2.4 | qmediasync | Cookie 抓取风控 |
| 元数据双向同步 | 优秀 2.5 | qmediasync | — |
| 增量 scan_token | 优秀 2.6 + 未来 4.7 | qmediasync | Alist 全量 429 |
| Cookie 健康分层+加密 | 优秀 2.7 | CloudSaver/AutoBangumi | 明文存储 |
| WebAuthn Passkey | 优秀 2.8 + 未来 4.10 | AutoBangumi | admin/admin 弱口令 |
| 302 直链代理 | 优秀 2.9 | qmediasync | Alist UA 问题 |
| 豆瓣+TMDB 双源+防封禁 | 优秀 2.10 | metashark | 无防封禁框架 |
| 转存任务组+失效检查 | 优秀 2.11 | quark-auto-save | — |
| 配置热重载 | 优秀 2.12 | MediaMTX | — |
| 事件驱动+多级缓存 | 优秀 2.13 + 未来 4.4 | MoviePilot | — |
| Override Rules | 优秀 2.14 | Seerr | — |
| MCP 端点+AI Agent | 未来 4.1/4.2 | MoviePilot/PanSou | — |
| 插件市场+热插拔 | 未来 4.5 | MoviePilot | — |
| 多网盘统一抽象 | 未来 4.6 | Alist/Radarr | 单盘工具 |
| WebDAV 服务暴露 | 未来 4.8 | Alist | — |
| Server-Timing+任务会话日志 | 未来 4.9 | MoviePilot/PanSou | 领域空白 |
| 组织化运营 | 未来 4.11 | OpenList/Seerr | Alist/nas-tools 单点 |
| Hook 脚本扩展 | 未来 4.13 | MediaMTX | — |
| 摒弃 Flask 同步 | 规避应避免 3.1 | — | nas-tools |
| 摒弃单文件巨石 | 规避应避免 3.2 | — | nas-tools |
| 摒弃明文 Cookie+弱口令 | 规避应避免 3.3 | — | aliyundrive-subscribe |
| 摒弃闭源转向 | 规避应避免 3.5 | — | CloudSaver |
| 摒弃单维护者 | 规避应避免 3.6 | — | Alist/nas-tools |
| 摒弃 PT 认证门槛 | 规避应避免 3.7 | — | nas-tools |
| 摒弃升级不兼容 | 规避应避免 3.8 | — | Alist v2→v3 |
| 摒弃豆瓣无防封禁 | 规避应避免 3.9 | — | MoviePilot/metashark |
| 摒弃 INI 单文件 | 规避应避免 3.10 | — | aliyundrive-subscribe |
| 摒弃全量无增量 | 规避应避免 3.12 | — | Alist |
| 摒弃不处理国内代理 | 规避应避免 3.13 | — | MoviePilot |

---

*本文档为阶段五产出，基于阶段四最佳实践提炼与阶段三横向对比矩阵设计。所有设计决策均引用具体项目实证依据。共覆盖 12 个章节：总体架构、模块设计、目录结构、插件体系、配置体系、权限体系、数据模型、API 规范、事件系统、日志系统、测试方案、文档结构。*
