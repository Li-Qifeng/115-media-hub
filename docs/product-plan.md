# 功能规划：115 Media Hub 演进方案

> 基于市场调研、横向对比、最佳实践提炼和新架构设计，按优先级规划功能演进。
> 调研时间：2026-07
> 优先级定义：P0 必须 / P1 重要 / P2 增强 / P3 未来

---

## 1. 优先级原则

本规划以"五位一体闭环 + 安全合规 + 架构基座"为出发点，将功能按 P0/P1/P2/P3 四级划分。划分标准如下：

- **P0（必须）**：解决核心痛点、安全基础、架构基座，不做则系统无法运行或风险过高。对应横向对比中"被频繁要求但没人做好"的核心闭环、应避免设计中"项目归档/被重构的共同死因"、以及架构基座层（Provider 抽象/安全/并发/分层/配置/迁移）。
- **P1（重要）**：显著提升体验、补齐行业标配、差异化关键能力。对应优秀实践与未来方案中已有多项目实证、能形成差异化但依赖 P0 基座落地的能力（插件化/增量同步/防封禁/可观测性等）。
- **P2（增强）**：增强体验、锦上添花、扩展场景。对应行业标配中"有则更好"、非核心闭环必需的能力（多用户/Passkey/主题/移动端/通知扩展等）。
- **P3（未来）**：前瞻性、未来方向、依赖前序完成。对应未来方案中尚无项目完整落地、需 P0/P1/P2 体系成熟后才能承载的能力（AI Agent/MCP/事件溯源/集群等）。

---

## 2. P0（必须）功能清单

### P0-1: Provider 抽象体系重构（含 DiscoveryProvider 接口）
- **为什么放该优先级**：横向对比 5.3 "被频繁要求但没人做好"第 1 项明确指出"多网盘（5+）+ STRM 生成 + TG 资源同步 + 影视订阅 + 刮削管理"五位一体闭环在 20 个调研项目中无人完整覆盖，而多网盘异构抽象正是该闭环的架构前提；优秀实践 2.1/2.2 + 未来方案 4.3/4.6 将 Provider 体系 + 能力声明 + `init()` 运行时注册列为多网盘规模化的唯一可持续范式。无此抽象，转存/STRM/订阅/刮削无法跨盘复用，核心闭环无法运行。对标 [Radarr](https://github.com/Radarr/Radarr) Provider 体系 + [Alist](https://github.com/AlistGo/alist) Driver 接口，规避 [quark-auto-save](https://github.com/Cp0204/quark-auto-save)/[aliyundrive-subscribe](https://github.com/adminpass/aliyundrive-subscribe) 单盘工具生态位狭窄（未来方案 4.6 反面）。
- **依赖模块**：Provider 适配层（`providers/base.py`、`discovery_base.py`、`metadata_base.py`、`notify_base.py`、`registry.py`）、资源中心、订阅引擎、监控引擎、STRM 引擎、刮削引擎、通知服务、基础设施（HttpClient/Crypto/ConfigStore）。
- **预计复杂度**：高 — 需定义 CloudProvider/DiscoveryProvider/MetadataProvider/NotifyProvider 四类抽象基类 + 能力声明布尔开关 + 运行时注册表 + `config_fields` UI 渲染协议，并迁移现有 5 网盘（115/夸克/阿里/123/天翼）实现至新接口。
- **风险**：抽象不当导致后续 Provider 难以实现或能力泄漏到主流程。缓解：先以现有 5 盘验证接口完备性，参考 Alist `Storage` 接口与 Radarr Provider 字段定义收敛能力开关；保留 `supports_*` 默认值降低迁移成本。

### P0-2: 安全基线（bcrypt/CSRF/登录限流/敏感字段脱敏/Cookie 加密）
- **为什么放该优先级**：应避免 3.3 明文 Cookie/Token + 默认弱口令是该领域项目"首日被入侵"主因（[aliyundrive-subscribe](https://github.com/adminpass/aliyundrive-subscribe) admin/admin 被吐槽）；架构原则 7 安全合规、第 6 章权限体系、5.3 敏感字段处理均要求加密存储/脱敏返回。所有调研项目共识"Cookie 等同账号密码、必须私有化部署"。不做则凭据泄露风险过高，属安全基础。
- **依赖模块**：认证与权限（`services/auth.py`、`routes/auth.py`）、配置中心（敏感字段处理 5.3）、基础设施（`infra/crypto.py` Fernet、`db.py` credentials 表）、API 层（`middleware.py` CSRF、`errors.py` 脱敏）。
- **预计复杂度**：中 — bcrypt/CSRF/Fernet 均为成熟库，主要工作在贯穿配置读写加密与 API 响应脱敏的统一处理 + 首启动强制改密流程。
- **风险**：加密密钥管理不当（如密钥随镜像分发）。缓解：密钥派生自 `JWT_SECRET` 环境变量、首启动强制改密、脱敏逻辑单测覆盖、错误响应统一不泄露内部异常。

### P0-3: SQLite 并发加固（短事务/锁重试/WAL）
- **为什么放该优先级**：对比 5.4 被吐槽问题第 2 项 115 防火墙 429、[Alist](https://github.com/AlistGo/alist)/[OpenList](https://github.com/OpenListTeam/OpenList) "database is locked" 类并发写问题；应避免 3.12 长事务持锁。SQLite 是默认存储（事实标准 1.3），后台任务与 API 并发写若不加固将频繁锁冲突导致面板卡顿/任务失败。属架构基座。
- **依赖模块**：基础设施（`infra/db.py`）、任务调度器、所有业务服务层（短事务规范）。
- **预计复杂度**：中 — WAL/`busy_timeout`/`retry_sqlite_locked` 指数退避已有实现，主要在约束全链路短事务（不跨网络 IO 持锁）+ 限流锁与 DB 锁隔离。
- **风险**：部分 NAS 挂载文件系统不支持 WAL。缓解：启动期检测并降级、可选 PostgreSQL（SQLAlchemy 抽象层）、`synchronous=NORMAL` 平衡性能与可靠。

### P0-4: 后台任务运行时隔离
- **为什么放该优先级**：应避免 3.1 Flask 同步阻塞事件循环（[nas-tools](https://github.com/NAStool/nas-tools) 被放弃/被重写）；架构原则 2 异步、2.7 任务调度器要求后台运行时不阻塞事件循环。网盘 API 普遍数百毫秒至秒级延迟，同步阻塞会让 Web 请求超时、SSE 中断。属架构基座。
- **依赖模块**：任务调度器（`services/scheduler.py`、`background.py`）、基础设施（EventBus、Logger）、Provider 适配层。
- **预计复杂度**：中 — APScheduler + asyncio 任务隔离，关键在 Provider 级 `throttle()` 限流与任务并发控制避免触发网盘风控。
- **风险**：任务并发触发网盘风控。缓解：Provider 级限流锁 + 任务并发上限 + 失败退避重试。

### P0-5: 单文件巨石拆分（core.py 拆分）
- **为什么放该优先级**：应避免 3.2 单文件巨石 `core.py` + 功能臃肿（[nas-tools](https://github.com/NAStool/nas-tools) 被 [MoviePilot](https://github.com/jxxghp/MoviePilot) "聚焦核心需求、简化功能设置"重构的反面教材）；架构原则 5 反巨石、第 3 章目录结构将 `core.py` 拆解为 `api/routes/services/domain/infra/providers` 五层。不做则后续功能无法并行开发、维护成本指数上升。
- **依赖模块**：全部分层（`api/`、`routes/`、`services/`、`domain/`、`infra/`、`providers/`）、目录结构（第 3 章）。
- **预计复杂度**：高 — 需梳理现有 `core.py` 职责并迁移到对应层、保持行为不变，属大规模重构，需先补集成测试再迁移。
- **风险**：迁移过程引入回归 bug。缓解：先补集成测试覆盖现有行为、分阶段拆分、保留向后兼容期、每阶段独立验证。

### P0-6: 配置分层与热重载基座
- **为什么放该优先级**：应避免 3.10 INI 单文件配置缺乏分层（[aliyundrive-subscribe](https://github.com/adminpass/aliyundrive-subscribe) 反面）；架构原则 4 配置即数据、第 5 章四层叠加（默认值→环境变量→配置文件→运行时覆盖）+ 5.5 热重载、2.8 配置中心 `post_save` 回调。配置是所有功能的基础，无分层与热重载则 Provider/调度/通知变更需重启进程，违背事实标准 1.2 NAS 零折腾原则。
- **依赖模块**：配置中心（`infra/config_store.py`、`config_runtime.py`）、基础设施、API 层（`routes/settings.py`）。
- **预计复杂度**：中 — `JsonConfigStore` 线程安全 + mtime 缓存已有实现，主要在四层叠加规范化 + `post_save` 按变更字段分发（Provider 重载/调度重设/通知重载）。
- **风险**：热重载误触发 Provider 重建中断进行中任务。缓解：热重载仅影响新请求、已建立 SSE/WebSocket 会话保持、敏感重建走平滑切换。

### P0-7: schema 版本化迁移与向后兼容
- **为什么放该优先级**：应避免 3.8 升级后配置/插件不兼容（[Alist](https://github.com/AlistGo/alist) v2→v3 被吐槽、[MoviePilot](https://github.com/jxxghp/MoviePilot) 升级后插件失效、[nas-tools](https://github.com/NAStool/nas-tools) 归档后无修复）；架构原则 9 向后兼容、`versioning.py`。NAS 用户升级意愿低，升级失败丢数据是口碑杀手。属架构基座。
- **依赖模块**：基础设施（`infra/db.py`、`versioning.py`）、数据模型（第 7 章）。
- **预计复杂度**：中 — 迁移脚本框架 + 现有表沿用 + 新增表（credentials/users/webauthn_credentials/task_sessions/plugins_state）迁移。
- **风险**：迁移脚本本身有 bug 导致数据损坏。缓解：迁移前自动备份 SQLite 文件、迁移事务化、失败可回滚、保留 v1 兼容期。

---

## 3. P1（重要）功能清单

### P1-1: 插件化机制（Provider/Discovery/Metadata/通知/Hook 插件）
- **为什么放该优先级**：未来方案 4.5 插件市场 + 热插拔（[MoviePilot](https://github.com/jxxghp/MoviePilot) 300+ 插件）；架构第 4 章五类插件统一接口（CloudProvider/DiscoveryProvider/MetadataProvider/NotifyProvider/HookPlugin）。是补齐行业标配 + 差异化关键能力，让第三方扩展无需改主程序。但运行时沙箱/生命周期/配置注入较复杂，依赖 P0 Provider 抽象与分层基座，故列 P1 而非 P0。
- **依赖模块**：插件体系（`plugins/base.py`、`manager.py`、`manifest.py`）、Provider 适配层、配置中心、基础设施（EventBus、Logger、Cache）。
- **预计复杂度**：高 — 生命周期（注册→加载→启用/禁用→卸载）+ 进程内沙箱隔离 + `PluginContext` 配置注入 + 目录扫描与热加载。
- **风险**：第三方插件安全风险（恶意外联/资源耗尽/异常传播）。缓解：默认禁用网络白名单外地址、`PLUGIN_TIMEOUT` 超时与内存限额、异常隔离降级返回空结果、敏感操作（删除/转存）二次确认。

### P1-2: 多网盘能力声明统一
- **为什么放该优先级**：优秀实践 2.1 + 未来方案 4.3 Provider 能力声明 + UI 自动渲染（[Radarr](https://github.com/Radarr/Radarr)）；架构 2.1 能力声明驱动 UI、4.4 Capability 枚举。补齐"新增 Provider 零侵入主流程、UI 按能力自动展示对应配置面板"的行业标配能力，是差异化关键。
- **依赖模块**：Provider 适配层（`registry.py`、`base.py` 能力开关）、配置中心、API 层（`GET /api/settings/providers`）、表现层（动态表单渲染）。
- **预计复杂度**：中 — 能力布尔开关 + `config_fields` 字段定义 + 前端按定义动态渲染表单。
- **风险**：能力声明与实际实现不一致（声明支持但方法未覆写）。缓解：能力声明单测 + Provider mock 测试覆盖每个 `supports_*` 对应方法。

### P1-3: 增量扫描 scan_token + mtime 比对
- **为什么放该优先级**：优秀实践 2.6 + 未来方案 4.7（[qmediasync](https://github.com/qicfan/qmediasync) 增量缓存，3 万文件全量约 10 分钟）；应避免 3.12 全量无增量（[Alist](https://github.com/AlistGo/alist) 缺增量导致 429 反面）；对比 5.4 被吐槽 115 防火墙 429。是大规模媒体库可维护的关键。
- **依赖模块**：监控引擎（`services/monitor.py`）、STRM 引擎、基础设施（`db.py` `local_files.scan_token`）、Provider 适配层（`list_entries_incremental`）。
- **预计复杂度**：中 — scan_token 游标 + mtime 比对 + 仅拉变更集 + 增量 STRM 更新。
- **风险**：scan_token 失效或部分网盘不支持增量。缓解：能力声明 `supports_incremental_sync`，不支持则降级全量 + 限流退避。

### P1-4: 流式解析降内存
- **为什么放该优先级**：未来方案 4.7 流式处理（大目录列表流式分页 + 大文件流式解析）；架构增量优先原则。万级文件下全量加载内存峰值过高，是性能与稳定性的优秀实践。
- **依赖模块**：监控引擎、STRM 引擎、刮削引擎、基础设施（`http_client.py` 流式）。
- **预计复杂度**：中 — 分页拉取 + 流式解析 + 增量更新 + 断点续传。
- **风险**：流式中断导致数据不一致。缓解：分页幂等 + 游标续传 + 失败重试。

### P1-5: Cookie 健康分层 + 加密存储
- **为什么放该优先级**：优秀实践 2.7（[CloudSaver](https://github.com/jiangrui1994/CloudSaver)/[AutoBangumi](https://github.com/EstrellaXD/Auto_Bangumi)）；对比 5.4 被吐槽 Cookie/Token 失效是网盘类项目通用痛点。可视化健康度（绿/黄/红）让用户主动维护，按需探测而非定时轮询。差异化关键能力。
- **依赖模块**：Provider 适配层（`probe_connectivity`）、基础设施（`db.py` credentials 表 `health_status`、`crypto.py`）、事件总线（`cookie.health_changed`）、通知服务、表现层（健康栏）。
- **预计复杂度**：中 — 探测 + 分层 + SSE 推送 + 紧凑状态栏 UI。
- **风险**：探测本身触发网盘风控。缓解：按需探测（用户触发/任务前探测）+ 限流 + 失败退避，避免高频轮询。

### P1-6: 按任务会话分页日志
- **为什么放该优先级**：未来方案 4.9（按任务会话 ID 分页查询，避免按行截断大文件）；架构第 10 章日志系统。便于隔离排查 Cookie 失效、429 限流、刮削失败等高频问题，是该领域调试体验的差异化。
- **依赖模块**：基础设施（`logger.py`、`task_sessions` 表）、任务调度器、API 层（`GET /api/events/{session_id}/logs`）。
- **预计复杂度**：中 — session_id 分配 + 独立日志文件 + 分页/流式 tail API + 结构化 JSON。
- **风险**：日志文件过多占用磁盘。缓解：保留 N 天自动清理 + 引擎汇总日志便于跨任务运维概览。

### P1-7: 豆瓣元数据 + 防封禁框架
- **为什么放该优先级**：对比 5.2 独有创新第 10 项（[jellyfin-plugin-metashark](https://github.com/cxfksword/jellyfin-plugin-metashark) 豆瓣+TMDB+防封禁）；优秀实践 2.10；应避免 3.9 强依赖豆瓣无防封禁（[MoviePilot](https://github.com/jxxghp/MoviePilot)/[metashark](https://github.com/cxfksword/jellyfin-plugin-metashark) 被吐槽长期脆弱）。填补中文刮削防封禁工程化空白，是独有创新。
- **依赖模块**：刮削引擎（`services/scraper.py`）、Provider 适配层（`metadata_base.py`、`douban.py`）、基础设施（`http_client.py` 限流/代理/重试、`cache.py`）、配置中心（代理配置）。
- **预计复杂度**：高 — 节流 + 代理 + 重试 + 缓存 + 双源融合（豆瓣中文剧情/评分 + TMDB 季集结构/海报）+ 反爬持续应对。
- **风险**：豆瓣反爬持续升级导致长期脆弱。缓解：工程化防封禁 + 缓存兜底 + 双源互补降级 + 代理配置默认值引导（应避免 3.13）。

### P1-8: 可观测性 Server-Timing
- **为什么放该优先级**：未来方案 4.9（该领域尚无项目完整落地 Server-Timing，是前瞻性机会）；架构 10.5 可观测性。显著提升调试体验，暴露内部耗时（db/provider/total）便于定位网盘高延迟瓶颈。
- **依赖模块**：API 层（`middleware.py` ServerTimingMiddleware）、基础设施（`metrics.py`、`logger.py` request_id）、配置中心。
- **预计复杂度**：中 — 中间件 + 计时埋点 + request_id 贯穿日志与 Server-Timing。
- **风险**：埋点过多影响性能。缓解：可开关、默认开发/调试模式开启、生产可关闭、`UI_PUSH_DEBOUNCE` 合并高频事件。

### P1-9: 转存任务组 + 失效检查 + 新链挑选
- **为什么放该优先级**：优秀实践 2.11（[quark-auto-save](https://github.com/Cp0204/quark-auto-save) 多任务组 + 星期调度 + 失效检查 + 新链挑选 + 增量转存）；架构 2.3 订阅引擎 `ShareSelection`。分享链失效是网盘追更常态，自动化接力是无人值守闭环的关键。差异化能力。
- **依赖模块**：订阅引擎（`subscription_runner`、`subscription_share_selection`）、资源中心、Provider 适配层、任务调度器。
- **预计复杂度**：中 — 任务组调度 + 失效探测 + 新链挑选 + 集数账本联动。
- **风险**：新链挑选误判导致转存错误内容。缓解：评分算法 + 集数账本最优命中校验 + 内容指纹去重。

### P1-10: 302 直链代理 + UA 适配
- **为什么放该优先级**：优秀实践 2.9（[qmediasync](https://github.com/qicfan/qmediasync) 内置 115 下载链接代理解决 UA 不能播放）；对比 5.4 被吐槽 302 直链 UA 问题不能播放（[Alist](https://github.com/AlistGo/alist) 常见 Issue）。直链不可播是网盘 + 媒体服务器联动高频痛点。
- **依赖模块**：STRM 引擎（`services/strm_files.py` 中继服务）、基础设施（`http_client.py` 代理改写）、Provider 适配层（`resolve_download_url`）。
- **预计复杂度**：中 — 内置轻量 HTTP 代理端口 + UA/鉴权头改写 + 直链优先/代理兜底。
- **风险**：代理成为性能瓶颈或单点。缓解：可选启用、直链优先代理兜底、流式转发不缓存全文件。

---

## 4. P2（增强）功能清单

### P2-1: 多用户与 RBAC
- **为什么放该优先级**：架构 6.5 预留 RBAC 扩展（[Seerr](https://github.com/seerr-team/seerr) 权限位 + [Alist](https://github.com/AlistGo/alist) 用户体系）；对比矩阵多用户/权限为部分项目支持。多用户场景增强体验，但当前单管理员已够用，属增强而非必需，故 P2。
- **依赖模块**：认证与权限（`services/auth.py`）、基础设施（`users` 表、`webauthn_credentials` 表）、API 层（middleware 权限校验）、表现层。
- **预计复杂度**：中 — 角色（admin/user/guest）+ 权限位 + 多用户配额 + Override Rules。
- **风险**：权限模型过度设计增加心智负担。缓解：先三角色 + 权限位最小集，按需扩展。

### P2-2: 插件市场/插件管理 UI
- **为什么放该优先级**：未来方案 4.5（[MoviePilot](https://github.com/jxxghp/MoviePilot) 300+ 插件市场一键安装）；架构 4.3 插件加载机制、`marketplace.py` 预留。依赖 P1 插件化机制完成，是插件体验增强。
- **依赖模块**：插件体系（`marketplace.py`、`manager.py`）、API 层（`settings/plugins`）、表现层（插件管理 UI）、基础设施（`plugins_state` 表）。
- **预计复杂度**：中 — 市场清单 + 一键安装 + 启用/禁用/配置 UI。
- **风险**：第三方插件质量参差。缓解：插件评分 + 沙箱隔离 + 默认禁用 + 敏感操作二次确认。

### P2-3: WebAuthn Passkey 登录
- **为什么放该优先级**：优秀实践 2.8 + 未来方案 4.10（[AutoBangumi](https://github.com/EstrellaXD/Auto_Bangumi) Passkey 无密码）；规避 [aliyundrive-subscribe](https://github.com/adminpass/aliyundrive-subscribe) admin/admin 弱口令。无密码登录体验提升，但 P0 已有 bcrypt 安全基线，Passkey 为增强。
- **依赖模块**：认证与权限（`routes/auth.py` passkey）、基础设施（`webauthn_credentials` 表、`crypto.py`）、表现层（Passkey 注册/登录 UI）。
- **预计复杂度**：中 — WebAuthn 注册/认证流程 + 多设备管理。
- **风险**：WebAuthn 跨设备/跨浏览器兼容。缓解：多凭据绑定 + 密码/Passkey 并存兜底。

### P2-4: 主题/夜间模式完善
- **为什么放该优先级**：对比矩阵主题/夜间模式（[Alist](https://github.com/AlistGo/alist)/[OpenList](https://github.com/OpenListTeam/OpenList)/[Sonarr](https://github.com/Sonarr/Sonarr)/[Radarr](https://github.com/Radarr/Radarr)/[Seerr](https://github.com/seerr-team/seerr) 均支持）；事实标准 1.8 Web 管理后台体验。增强体验。
- **依赖模块**：表现层（Vue3 + Tailwind 暗色模式）、配置中心（主题偏好持久化）。
- **预计复杂度**：低 — Tailwind dark mode + 主题切换 + 偏好持久化。
- **风险**：暗色模式对比度不足影响可读性。缓解：遵循 WCAG 对比度标准。

### P2-5: 移动端适配增强
- **为什么放该优先级**：事实标准 1.8 移动端响应式（[MoviePilot](https://github.com/jxxghp/MoviePilot)/[AutoBangumi](https://github.com/EstrellaXD/Auto_Bangumi)）；架构表现层移动端响应式。NAS 用户远程/移动访问刚需。
- **依赖模块**：表现层（响应式布局、触控交互）、API 层（分页适配）。
- **预计复杂度**：中 — 响应式重构 + 触控优化 + 移动端导航。
- **风险**：移动端功能裁剪不当影响核心操作。缓解：核心功能（订阅/转存/监控状态）移动端可用，高级配置走桌面端。

### P2-6: 通知通道扩展（Telegram/Discord/Bark）
- **为什么放该优先级**：事实标准 1.9 多渠道通知（[MoviePilot](https://github.com/jxxghp/MoviePilot) 8 渠道、[nas-tools](https://github.com/NAStool/nas-tools) ServerChan/微信/TG/Bark）；架构 2.10 通知服务多渠道。补齐行业标配通知渠道。
- **依赖模块**：通知服务（`services/notify.py`）、Provider 适配层（`notify/telegram`、`discord`、`bark`）、事件总线、配置中心。
- **预计复杂度**：低 — 各渠道 SDK 集成 + 事件路由 + `notification_dedupe` 去重。
- **风险**：各渠道 API 变更导致失效。缓解：Provider 抽象 + 降级 + 单渠道失败不影响其他渠道。

### P2-7: Override Rules 条件化请求默认值
- **为什么放该优先级**：优秀实践 2.14（[Seerr](https://github.com/seerr-team/seerr) Override Rules 基于用户/标签的条件化默认值）；架构 6.5。多用户场景下避免每次手动选默认值。依赖 P2 多用户完成。
- **依赖模块**：认证与权限（用户/标签）、订阅引擎、推荐清单、配置中心。
- **预计复杂度**：中 — 规则引擎 + 用户/标签条件化默认值 + 优先级。
- **风险**：规则冲突导致预期外默认值。缓解：规则优先级 + 冲突检测 + 显式提示。

### P2-8: WebDAV 服务对外暴露
- **为什么放该优先级**：未来方案 4.8（[Alist](https://github.com/AlistGo/alist)/[OpenList](https://github.com/OpenListTeam/OpenList) WebDAV 完整服务）；架构基础设施 `webdav.py` 预留。让 Emby/Jellyfin/Plex/Alist 可直接挂载复用媒体库，扩展场景。
- **依赖模块**：基础设施（`webdav.py`）、Provider 适配层（文件操作）、认证与权限、配置中心。
- **预计复杂度**：中 — WebDAV 协议实现 + 鉴权 + 性能。
- **风险**：WebDAV 大文件列表性能。缓解：直链优先 + 流式 + 缓存目录列表。

---

## 5. P3（未来）功能清单

### P3-1: LLM/AI Agent 集成（智能匹配/对话式操作）
- **为什么放该优先级**：未来方案 4.1（[MoviePilot](https://github.com/jxxghp/MoviePilot) Copilot 自然语言下达搜索/订阅/整理指令）；架构 1.4 AI 集成。降低使用门槛的新范式，但依赖 MCP 协议与事件驱动完善，故 P3。
- **依赖模块**：API 层（`routes/mcp.py`）、事件总线、订阅引擎、资源中心、表现层（对话 UI）。
- **预计复杂度**：高 — Agent 编排 + 意图识别 + 工具调用 + 上下文管理 + 多轮对话。
- **风险**：LLM 幻觉导致误操作（误订阅/误转存/误删除）。缓解：敏感操作二次确认 + 操作可回滚 + 工具白名单。

### P3-2: MCP 协议支持
- **为什么放该优先级**：未来方案 4.2（[MoviePilot](https://github.com/jxxghp/MoviePilot)/[PanSou](https://github.com/fish2018/pansou) MCP 端点）；架构 API 层 `routes/mcp.py`。面板能力标准化为 MCP 工具供外部 LLM 复用，是 AI 集成的前置。
- **依赖模块**：API 层（`routes/mcp.py`）、认证与权限（MCP Token 鉴权）、Provider 适配层（能力暴露为 MCP 工具）。
- **预计复杂度**：中 — MCP 协议实现 + 工具清单 + 独立鉴权 + 独立文档。
- **风险**：MCP 协议演进导致不兼容。缓解：跟踪官方规范 + 版本化端点 + `/api/v1/mcp` 独立文档维护。

### P3-3: 事件驱动架构完善（事件溯源）
- **为什么放该优先级**：未来方案 4.4（[MoviePilot](https://github.com/jxxghp/MoviePilot) `app/core/event.py` 事件驱动 + 多级缓存）；架构第 9 章。基础 EventBus 在 P0/P1 已建立，P3 完善为完整事件溯源 + 复杂事件链 + 多级缓存联动。
- **依赖模块**：事件总线、所有业务服务层、基础设施（`cache.py` 多级、`metrics.py`）。
- **预计复杂度**：高 — 事件溯源 + 复杂事件链 + 背压/去重 + 可观测性追踪。
- **风险**：事件链复杂难以调试。缓解：事件溯源 + Server-Timing 追踪 + request_id 贯穿。

### P3-4: 元数据双向同步
- **为什么放该优先级**：优秀实践 2.5（[qmediasync](https://github.com/qicfan/qmediasync) 本地刮削后 NFO/海报回传网盘）；架构 2.6 刮削引擎元数据双向同步。避免多端刮削重复劳动，保证网盘原始资源也带元数据。依赖刮削引擎 + 网盘文件写能力完成。
- **依赖模块**：刮削引擎、Provider 适配层（文件写/上传）、基础设施（`cache.py`、`http_client.py`）。
- **预计复杂度**：中 — NFO/海报回传 + 元数据大小校验 + 冲突处理。
- **风险**：回传冲突覆盖用户手动修改。缓解：大小校验 + 冲突策略（跳过/覆盖/备份）+ 显式确认。

### P3-5: 多媒体服务器深度集成（Emby/Jellyfin/Plex 回调）
- **为什么放该优先级**：事实标准 1.5 Webhook + 对比 5.1 行业标配媒体服务器联动；架构 Webhook 接入。深度回调双向集成（库刷新/播放状态/刮削触发）。
- **依赖模块**：API 层（`routes/webhook.py`）、事件总线、刮削引擎、通知服务、配置中心。
- **预计复杂度**：中 — 各服务器 Webhook 协议适配 + 双向回调 + 库刷新触发。
- **风险**：各服务器 API 差异大。缓解：Provider 抽象 + 每服务器独立适配层 + 配置即数据。

### P3-6: 集群/分布式部署
- **为什么放该优先级**：架构 7.1 可选 PostgreSQL（对标 [MoviePilot](https://github.com/jxxghp/MoviePilot)/[Seerr](https://github.com/seerr-team/seerr)）；多用户高并发场景。依赖前序 PG 切换 + 任务调度分布式完成。前瞻性未来方向。
- **依赖模块**：基础设施（`db.py` PG、`cache.py` 分布式、`event_bus.py` 分布式）、任务调度器（分布式锁）。
- **预计复杂度**：高 — 分布式锁 + 任务分片 + 状态同步 + 一致性保障。
- **风险**：分布式一致性复杂。缓解：先 PostgreSQL 单机验证、后选型分布式协调（Redis/etcd）、保留单机模式兜底。

### P3-7: IM Bot 入口 + 语音发起请求
- **为什么放该优先级**：未来方案 4.14（[Requestrr](https://github.com/thomst08/requestrr) Discord 斜杠命令 + Siri 语音，社区长期诉求 Telegram 支持）；将面板能力带入 IM 日常入口。依赖 MCP/事件驱动完成。
- **依赖模块**：通知服务（Bot 双向）、API 层、事件总线、订阅引擎。
- **预计复杂度**：中 — Bot 命令解析 + 权限绑定 + 会话状态。
- **风险**：Bot 鉴权与越权操作。缓解：Token 绑定用户 + 命令白名单 + 敏感操作二次确认。

---

## 6. 优先级总览表

| 功能名 | 优先级 | 依赖模块 | 复杂度 | 风险等级 |
|--------|--------|---------|--------|---------|
| Provider 抽象体系重构（含 DiscoveryProvider） | P0 | Provider 适配层/资源中心/订阅/监控/STRM/刮削/通知/基础设施 | 高 | 中 |
| 安全基线（bcrypt/CSRF/限流/脱敏/加密） | P0 | 认证权限/配置中心/基础设施(crypto,db)/API 层 | 中 | 高 |
| SQLite 并发加固（短事务/锁重试/WAL） | P0 | 基础设施(db)/任务调度器/业务服务层 | 中 | 中 |
| 后台任务运行时隔离 | P0 | 任务调度器/基础设施(EventBus,Logger)/Provider 适配层 | 中 | 中 |
| 单文件巨石拆分（core.py 拆分） | P0 | 全部分层(api/routes/services/domain/infra/providers) | 高 | 中 |
| 配置分层与热重载基座 | P0 | 配置中心/基础设施/API 层(settings) | 中 | 中 |
| schema 版本化迁移与向后兼容 | P0 | 基础设施(db,versioning)/数据模型 | 中 | 高 |
| 插件化机制（五类插件） | P1 | 插件体系/Provider 适配层/配置中心/基础设施 | 高 | 高 |
| 多网盘能力声明统一 | P1 | Provider 适配层(registry,base)/配置中心/API 层/表现层 | 中 | 中 |
| 增量扫描 scan_token + mtime | P1 | 监控引擎/STRM 引擎/基础设施(db)/Provider 适配层 | 中 | 中 |
| 流式解析降内存 | P1 | 监控/STRM/刮削引擎/基础设施(http_client) | 中 | 中 |
| Cookie 健康分层 + 加密存储 | P1 | Provider 适配层/基础设施(db,crypto)/事件总线/通知/表现层 | 中 | 中 |
| 按任务会话分页日志 | P1 | 基础设施(logger,task_sessions)/任务调度器/API 层 | 中 | 低 |
| 豆瓣元数据 + 防封禁框架 | P1 | 刮削引擎/Provider 适配层(metadata,douban)/基础设施(http_client,cache)/配置中心 | 高 | 高 |
| 可观测性 Server-Timing | P1 | API 层(middleware)/基础设施(metrics,logger)/配置中心 | 中 | 低 |
| 转存任务组 + 失效检查 + 新链挑选 | P1 | 订阅引擎(share_selection)/资源中心/Provider 适配层/任务调度器 | 中 | 中 |
| 302 直链代理 + UA 适配 | P1 | STRM 引擎/基础设施(http_client)/Provider 适配层 | 中 | 中 |
| 多用户与 RBAC | P2 | 认证权限/基础设施(users,webauthn)/API 层/表现层 | 中 | 中 |
| 插件市场/插件管理 UI | P2 | 插件体系(marketplace,manager)/API 层/表现层/基础设施(plugins_state) | 中 | 中 |
| WebAuthn Passkey 登录 | P2 | 认证权限(routes/auth)/基础设施(webauthn,crypto)/表现层 | 中 | 中 |
| 主题/夜间模式完善 | P2 | 表现层/配置中心 | 低 | 低 |
| 移动端适配增强 | P2 | 表现层/API 层 | 中 | 低 |
| 通知通道扩展（TG/Discord/Bark） | P2 | 通知服务/Provider 适配层(notify)/事件总线/配置中心 | 低 | 低 |
| Override Rules 条件化默认值 | P2 | 认证权限/订阅引擎/推荐清单/配置中心 | 中 | 中 |
| WebDAV 服务对外暴露 | P2 | 基础设施(webdav)/Provider 适配层/认证权限/配置中心 | 中 | 中 |
| LLM/AI Agent 集成 | P3 | API 层(mcp)/事件总线/订阅引擎/资源中心/表现层 | 高 | 高 |
| MCP 协议支持 | P3 | API 层(routes/mcp)/认证权限/Provider 适配层 | 中 | 中 |
| 事件驱动架构完善（事件溯源） | P3 | 事件总线/业务服务层/基础设施(cache,metrics) | 高 | 中 |
| 元数据双向同步 | P3 | 刮削引擎/Provider 适配层(文件写)/基础设施(cache,http_client) | 中 | 中 |
| 多媒体服务器深度集成（Emby/Jellyfin/Plex） | P3 | API 层(webhook)/事件总线/刮削引擎/通知服务/配置中心 | 中 | 中 |
| 集群/分布式部署 | P3 | 基础设施(db-PG,cache,event_bus)/任务调度器(分布式锁) | 高 | 高 |
| IM Bot 入口 + 语音发起 | P3 | 通知服务(Bot)/API 层/事件总线/订阅引擎 | 中 | 中 |

---

## 7. 依赖关系图

下图描述功能间的依赖关系（箭头 `→` 表示"依赖于"，即前者需要后者先完成；同层内可并行）。

```
                        ┌─────────────────────────────────────────────┐
                        │            P0 基座层（必须先行）              │
                        └─────────────────────────────────────────────┘

  P0-5 巨石拆分 ─┬─→ P0-1 Provider 抽象体系重构 ──┐
                ├─→ P0-6 配置分层与热重载基座 ──────┤
                └─→ P0-2 安全基线 ←── P0-6 ─────────┤
                                                    │
  P0-3 SQLite 并发加固 ──→ P0-4 后台任务运行时隔离 ──┤
          │                       ↑                  │
          └──→ P0-7 schema 迁移 ──┘                  │
                                                    │
                        ┌──────────────────────────┘
                        ↓
                        ┌─────────────────────────────────────────────┐
                        │            P1 重要能力层                    │
                        └─────────────────────────────────────────────┘

  P0-1 Provider 抽象 ─┬─→ P1-1 插件化机制 ──────→ P2-2 插件市场 UI
                     ├─→ P1-2 多网盘能力声明统一
                     ├─→ P1-3 增量扫描 scan_token ←── P0-4 后台隔离
                     ├─→ P1-4 流式解析降内存
                     ├─→ P1-5 Cookie 健康分层 ←── P0-2 安全基线(credentials)
                     ├─→ P1-9 转存任务组+新链挑选 ←── P0-4
                     └─→ P1-10 302 直链代理

  P0-2 安全基线 ─────→ P1-7 豆瓣防封禁 ←── P0-6 配置(代理)
  P0-4 后台隔离 ─────→ P1-6 按任务会话分页日志
  P0-5 巨石拆分 ─────→ P1-8 可观测性 Server-Timing(middleware)

                        ┌─────────────────────────────────────────────┐
                        │            P2 增强层                        │
                        └─────────────────────────────────────────────┘

  P0-2 安全基线 ─┬─→ P2-1 多用户与 RBAC ──→ P2-7 Override Rules
                └─→ P2-3 WebAuthn Passkey
  P1-1 插件化 ────→ P2-2 插件市场 UI
  P0-1 Provider ──→ P2-6 通知通道扩展(notify provider)
  P0-1 Provider ──→ P2-8 WebDAV 服务对外暴露
  （独立）P2-4 主题/夜间模式
  （独立）P2-5 移动端适配增强

                        ┌─────────────────────────────────────────────┐
                        │            P3 未来层                        │
                        └─────────────────────────────────────────────┘

  P1-2 能力声明 ──→ P3-2 MCP 协议支持 ──┬─→ P3-1 LLM/AI Agent 集成
                                       └─→ P3-7 IM Bot 入口
  基础 EventBus ──→ P3-3 事件驱动架构完善 ──→ P3-1 AI Agent
                                          └─→ P3-6 集群/分布式部署
  P1-7 豆瓣刮削 ──→ P3-4 元数据双向同步
  P0-1 Provider ──→ P3-5 多媒体服务器深度集成(Emby/Jellyfin/Plex)
  P0-3 SQLite(PG)──→ P3-6 集群/分布式部署
  P2-6 通知扩展 ──→ P3-7 IM Bot 入口
```

**关键依赖路径说明**：

1. **基座先行**：P0-5（巨石拆分）是绝大多数功能的隐性前置——分层不清则后续模块无处安放。P0-1（Provider 抽象）是核心闭环的架构前提，P1 大量功能（插件化/能力声明/增量/健康分层/转存组/302 代理）都依赖它。
2. **安全贯穿**：P0-2（安全基线）是 P1-5（Cookie 健康分层，依赖 credentials 加密表）与 P2-1/P2-3（RBAC/Passkey）的前置。
3. **插件链路**：P1-1（插件化机制）→ P2-2（插件市场 UI），前者定义接口与沙箱，后者提供分发与管理。
4. **AI 链路**：P3-2（MCP）+ P3-3（事件驱动完善）共同支撑 P3-1（AI Agent），任一缺失则 Agent 无法编排面板能力。
5. **分布式链路**：P3-6（集群）依赖 P0-3（SQLite→PG 切换）与 P3-3（分布式事件总线），是最终演进终点。
6. **独立项**：P2-4 主题、P2-5 移动端为纯前端增强，可与任意阶段并行推进。

---

*本文档为阶段六产出，基于阶段五架构设计（[`docs/architecture.md`](./architecture.md)）、阶段四最佳实践提炼（[`docs/best-practice.md`](./best-practice.md)）、阶段三横向对比矩阵（[`docs/competitor-comparison.md`](./competitor-comparison.md)）规划。每个功能的优先级理由均引用调研/对比/最佳实践依据，共规划 P0 7 项、P1 10 项、P2 8 项、P3 7 项，合计 32 项功能。*
