# 横向对比矩阵：多网盘媒体自动化管理领域

> 基于阶段一、二对 20 个 GitHub 项目的调研，生成功能/架构/优缺点对比矩阵。
> 调研时间：2026-07

---

## 1. 对比项目清单

从阶段一、二调研的 20 个项目中，按"Star 高 / 维护活跃 / 与 115 Media Hub 同领域相关性高"三项标准筛选出 **15 个最具代表性的项目**进入横向对比矩阵。选取标准说明：

- **Star 高**：优先选取 Star 数千以上的项目，反映社区认可度。
- **维护活跃**：优先选取 2026 年仍在迭代的项目；对已归档/停滞项目（nas-tools、aliyundrive-subscribe）因其历史奠基性或生态位代表性仍纳入对比，但明确标注状态。
- **同领域相关性高**：覆盖 115 Media Hub 的核心能力域（多网盘、STRM、转存、订阅、刮削、搜索、媒体服务器联动），每个细分方向至少 1 个代表项目。
- 语言与架构多样性：覆盖 Go / Python / C# / TypeScript / Java 五种主语言，单体/插件化/桌面 GUI/浏览器扩展/Jellyfin 插件多种形态。

| 序号 | 项目名 | 主语言 | Star(近似) | 定位 | 仓库链接 | 活跃度 |
|------|--------|--------|-----------|------|----------|--------|
| 1 | MoviePilot | Python | ~11,300 | NAS 媒体库自动化面板 | https://github.com/jxxghp/MoviePilot | 活跃（极活跃） |
| 2 | qmediasync | Go | ~589 | STRM 生成与媒体库联动 | https://github.com/qicfan/qmediasync | 活跃 |
| 3 | quark-auto-save | Python | ~2,900 | 夸克网盘签到/转存/整理 | https://github.com/Cp0204/quark-auto-save | 活跃（极活跃） |
| 4 | Alist | Go | ~49,000 | 多存储文件列表 / WebDAV | https://github.com/AlistGo/alist | 缓更（2025-05） |
| 5 | OpenList | Go | ~15,600 | Alist 社区延续 Fork | https://github.com/OpenListTeam/OpenList | 活跃 |
| 6 | PanSou | Go | ~13,800 | 网盘资源搜索 API 服务 | https://github.com/fish2018/pansou | 活跃 |
| 7 | CloudSaver | Vue/TS + Node.js | ~9,100 | 网盘搜索转存一体化平台 | https://github.com/jiangrui1994/CloudSaver | 活跃（新版已闭源） |
| 8 | aliyundrive-subscribe | Go | ~963 | 阿里云盘订阅自动转存 | https://github.com/adminpass/aliyundrive-subscribe | 缓更（2024-02 停滞） |
| 9 | nas-tools | Python | ~9,000 | NAS 媒体库管理（已归档） | https://github.com/NAStool/nas-tools | 已归档（2023-05） |
| 10 | AutoBangumi | Python | ~8,100 | 全自动追番工具 | https://github.com/EstrellaXD/Auto_Bangumi | 活跃 |
| 11 | Sonarr | C# | ~13,500 | 剧集自动追更 PVR | https://github.com/Sonarr/Sonarr | 活跃 |
| 12 | Radarr | C# | ~13,900 | 电影自动管理器 | https://github.com/Radarr/Radarr | 活跃 |
| 13 | tinyMediaManager | Java | 信息不足 | 桌面端媒体库刮削管理器 | https://gitlab.com/tinyMediaManager/tinyMediaManager | 活跃 |
| 14 | jellyfin-plugin-metashark | C# | ~2,100 | Jellyfin 中文刮削插件 | https://github.com/cxfksword/jellyfin-plugin-metashark | 活跃 |
| 15 | Seerr | TypeScript | ~11,800 | 媒体请求与发现管理器 | https://github.com/seerr-team/seerr | 活跃 |

> 未进入主矩阵但仍在关键发现中作为依据引用的项目：aliyunpan（https://github.com/tickstep/aliyunpan，阿里云盘 CLI）、MediaMTX（https://github.com/bluenviron/mediamtx，媒体路由）、MediaElch（https://github.com/Komet/MediaElch，Qt 刮削器）、PT-Plugin-Plus（https://github.com/pt-plugins/PT-Plugin-Plus，PT 浏览器扩展，已归档）、Requestrr（https://github.com/thomst08/requestrr，Discord 媒体请求 Bot）。

---

## 2. 功能对比矩阵

判定标注：✓ = 原生支持且为核心能力；部分 = 有相关能力但实现不完整/需借助外部工具/仅覆盖部分场景；✗ = 不支持；未知 = 调研未获取到明确信息。

| 功能项 | MoviePilot | qmediasync | quark-auto-save | Alist | OpenList | PanSou | CloudSaver | aliyundrive-subscribe | nas-tools | AutoBangumi | Sonarr | Radarr | tinyMediaManager | jellyfin-plugin-metashark | Seerr |
|--------|-----------|-----------|-----------------|-------|----------|--------|-----------|----------------------|-----------|-------------|--------|--------|------------------|---------------------------|-------|
| 多网盘支持（115/Quark/阿里/天翼/123/百度等） | 部分 | 部分 | ✗ | ✓ | ✓ | 部分 | 部分 | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ |
| STRM 文件生成 | ✗ | ✓ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ |
| 网盘挂载/WebDAV | ✗ | ✗ | ✗ | ✓ | ✓ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ |
| 资源搜索（盘搜/TG/PT） | ✓ | ✗ | ✗ | ✗ | ✗ | ✓ | ✓ | ✗ | ✓ | 部分 | ✓ | ✓ | ✗ | ✗ | 部分 |
| 自动转存 | 部分 | ✗ | ✓ | ✗ | ✗ | ✗ | ✓ | ✓ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ |
| 影视订阅/自动追更 | ✓ | ✗ | 部分 | ✗ | ✗ | ✗ | ✗ | ✓ | ✓ | ✓ | ✓ | ✓ | ✗ | ✗ | ✓ |
| 剧集/季集管理 | ✓ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | 部分 | ✓ | ✓ | ✓ | 部分 | ✓ | 部分 | 部分 |
| 影视刮削/NFO 生成 | ✓ | 部分 | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✓ | 部分 | ✓ | ✓ | ✓ | ✓ | ✗ |
| TMDB/豆瓣元数据 | ✓ | ✗ | ✗ | ✗ | ✗ | ✗ | 部分 | ✗ | ✓ | 部分 | 部分 | 部分 | 部分 | ✓ | 部分 |
| 批量重命名 | ✓ | ✗ | ✓ | ✗ | ✗ | ✗ | ✗ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✗ | ✗ |
| 文件夹监控 | ✓ | 部分 | 部分 | ✗ | ✗ | ✗ | ✗ | 部分 | ✓ | ✗ | ✓ | ✓ | 部分 | ✗ | ✗ |
| Webhook 触发 | ✓ | ✗ | 部分 | 部分 | 部分 | ✗ | 部分 | ✗ | 部分 | ✗ | ✓ | ✓ | ✗ | ✗ | ✓ |
| 通知推送 | ✓ | 部分 | ✓ | ✗ | ✗ | ✗ | 部分 | ✓ | ✓ | 部分 | ✓ | ✓ | ✗ | ✗ | ✓ |
| 定时签到 | 部分 | ✗ | ✓ | ✗ | ✗ | ✗ | ✗ | ✓ | 部分 | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ |
| 插件机制 | ✓ | ✗ | 部分 | 部分 | 部分 | ✓ | ✗ | ✗ | 部分 | ✗ | 部分 | 部分 | ✓ | 部分 | ✗ |
| REST API | ✓ | 部分 | 部分 | ✓ | ✓ | ✓ | 部分 | 部分 | 部分 | ✓ | ✓ | ✓ | 部分 | ✗ | ✓ |
| Web 管理后台 | ✓ | ✓ | ✓ | ✓ | ✓ | 部分 | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✗ | 部分 | ✓ |
| 多用户/权限 | 部分 | ✗ | ✗ | ✓ | ✓ | ✗ | ✓ | ✗ | 部分 | 部分 | 部分 | 部分 | ✗ | ✗ | ✓ |
| Docker 部署 | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | 部分 | 部分 | ✓ |
| 主题/夜间模式 | 部分 | ✗ | ✗ | ✓ | ✓ | ✗ | ✗ | ✗ | ✗ | ✗ | ✓ | ✓ | ✗ | ✗ | ✓ |

### 判定依据说明

- **多网盘支持**：Alist/OpenList 以 30+ 驱动覆盖最广（[Alist](https://github.com/AlistGo/alist)、[OpenList](https://github.com/OpenListTeam/OpenList)）；PanSou 识别 13 类网盘链接但仅做搜索不做管理（[PanSou](https://github.com/fish2018/pansou)）；CloudSaver 支持 115/夸克/天翼/123 四家转存（[CloudSaver](https://github.com/jiangrui1994/CloudSaver)）；qmediasync 通过 115 开放平台 + Openlist/CD2/飞牛同步源间接覆盖多网盘（[qmediasync](https://github.com/qicfan/qmediasync)）；MoviePilot 网盘原生支持弱，主要通过阿里云盘秒传与插件实现（[MoviePilot](https://github.com/jxxghp/MoviePilot)）。
- **STRM 文件生成**：仅 qmediasync 把 STRM 作为核心能力（[qmediasync](https://github.com/qicfan/qmediasync)）；MoviePilot 明确不生成 STRM，需配合 qmediasync/alist-strm（[MoviePilot 缺点](https://github.com/jxxghp/MoviePilot)）。
- **网盘挂载/WebDAV**：Alist/OpenList 提供完整 WebDAV 服务（[Alist](https://github.com/AlistGo/alist)）；aliyunpan 提供 WebDAV 但仅阿里单盘（[aliyunpan](https://github.com/tickstep/aliyunpan)，未进矩阵但作为依据）。
- **资源搜索**：MoviePilot 聚合 PT 站点 RSS + TG 频道搜索 + CookieCloud（[MoviePilot](https://github.com/jxxghp/MoviePilot)）；PanSou 多频道并发搜索 13 类网盘链接（[PanSou](https://github.com/fish2018/pansou)）；CloudSaver 多源聚合 + 豆瓣榜单（[CloudSaver](https://github.com/jiangrui1994/CloudSaver)）；nas-tools 站点 RSS 聚合 + 豆瓣联动（[nas-tools](https://github.com/NAStool/nas-tools)）；Sonarr/Radarr 走 RSS/索引器（[Sonarr](https://github.com/Sonarr/Sonarr)、[Radarr](https://github.com/Radarr/Radarr)）；Seerr 仅 TMDb 发现浏览，非 PT/网盘搜索（[Seerr](https://github.com/seerr-team/seerr)）。
- **自动转存**：quark-auto-save 监控分享链自动转存到夸克指定目录（[quark-auto-save](https://github.com/Cp0204/quark-auto-save)）；CloudSaver 一键转存 115/夸克/天翼/123（[CloudSaver](https://github.com/jiangrui1994/CloudSaver)）；aliyundrive-subscribe 阿里云盘分享链自动转存（[aliyundrive-subscribe](https://github.com/adminpass/aliyundrive-subscribe)）；MoviePilot 仅阿里云盘秒传，非通用转存（[MoviePilot](https://github.com/jxxghp/MoviePilot)）。
- **影视订阅/自动追更**：MoviePilot、nas-tools、AutoBangumi、Sonarr、Radarr、Seerr 均为核心能力；quark-auto-save 仅任务组追更非影视订阅。
- **刮削/NFO**：tinyMediaManager、MoviePilot、nas-tools、Sonarr、Radarr、jellyfin-plugin-metashark 均支持；qmediasync 仅元数据双向同步非完整刮削（[qmediasync](https://github.com/qicfan/qmediasync)）。
- **TMDB/豆瓣元数据**：MoviePilot、jellyfin-plugin-metashark 实现豆瓣 + TMDB 双源；其余多仅 TMDB/TVDB。
- **插件机制**：MoviePilot 300+ 插件热插拔最成熟（[MoviePilot](https://github.com/jxxghp/MoviePilot)）；tinyMediaManager v4.2+ SPI 刮削器 addon（[TMM](https://gitlab.com/tinyMediaManager/tinyMediaManager)）；PanSou 异步插件系统带开发指南（[PanSou](https://github.com/fish2018/pansou)）；Radarr Provider 体系配置即启用但需编译（[Radarr](https://github.com/Radarr/Radarr)）；qmediasync 作者明确不开放插件（[qmediasync](https://github.com/qicfan/qmediasync)）。
- **多用户/权限**：Alist/OpenList 用户/权限位/guest 体系（[Alist](https://github.com/AlistGo/alist)）；CloudSaver 管理员/普通用户 + 注册码（[CloudSaver](https://github.com/jiangrui1994/CloudSaver)）；Seerr 权限位 + 配额 + SSO（[Seerr](https://github.com/seerr-team/seerr)）。
- **主题/夜间模式**：Alist/OpenList 暗色模式；Sonarr/Radarr 深色/浅色主题；Seerr 深色为主；MoviePilot 主题自定义 CSS 脚本（[MoviePilot](https://github.com/jxxghp/MoviePilot)）。
- **Web 管理后台**：tinyMediaManager 为桌面 GUI 无 Web UI（需 VNC），标 ✗；jellyfin-plugin-metashark 复用 Jellyfin 插件配置页，标部分；PanSou 有 pansou-web 前端但偏状态/搜索，标部分。

---

## 3. 实现方式对比矩阵

| 对比维度 | MoviePilot | qmediasync | quark-auto-save | Alist | OpenList | PanSou | CloudSaver | aliyundrive-subscribe | nas-tools | AutoBangumi | Sonarr | Radarr | tinyMediaManager | jellyfin-plugin-metashark | Seerr |
|---------|-----------|-----------|-----------------|-------|----------|--------|-----------|----------------------|-----------|-------------|--------|--------|------------------|---------------------------|-------|
| 技术栈（语言+框架） | Python 3.12 + FastAPI + Vue3 | Go | Python（FastAPI 风格） | Go + Gin + SolidJS | Go + Gin + SolidJS | Go + Gin | Vue3 + TS + Node/Express + Inversify | Go（推断） | Python + FastAPI + Vue | Python + FastAPI + Vue3（异步） | C# .NET + React | C# .NET 8 + React | Java + Swing + Maven | C# .NET + HTML | TypeScript + Node.js 22 + React + TypeORM |
| 架构形态 | 插件化（chain/modules/plugins/workflow） | 单体（STRM+302+元数据三服务） | 单体 + plugins 目录 | 单体（Driver 接口扩展） | 单体（Driver 接口扩展） | 单体 + 异步插件 | 前后端分离 monorepo（controller-service） | 单体 | 单体 | 轻量单体 | 单体（*arr 骨架） | 单体（Provider 体系） | 单体桌面 GUI | Jellyfin 插件（SPI） | 单体（多适配层） |
| 数据存储 | SQLite / PostgreSQL | 缓存层（增量同步） | SQLite（数据库化历史） | SQLite / MySQL | SQLite / MySQL | 内存 LRU + 磁盘分片缓存 | SQLite3 + Sequelize | SQLite / MySQL | SQLAlchemy ORM | SQLite（aiosqlite） | SQLite / PostgreSQL | SQLite / PostgreSQL | 本地 NFO（XML）+ 文件 | 复用 Jellyfin | SQLite / PostgreSQL（TypeORM） |
| 任务调度方式 | 事件驱动 + 定时 + 多级缓存 | 定时任务（最小半小时） | 定时周期 | 内置调度 | 内置调度 | goroutine + worker pool | 定时 | 定时检查周期 | 定时 | 异步后台扫描线程 | 内置任务调度器 | 内置任务调度器 | 手动 / CLI 批处理 | 随 Jellyfin 刮削流程 | 内置任务调度 |
| 配置方式 | 环境变量 + Web UI + config + category.yaml | Web UI 表单（12333 端口） | 环境变量 + WebUI 表单 | config.json + data.db + Web UI 表单 + 环境变量 | 同 Alist | 环境变量为主 + docker-compose | .env + Web 后台 | INI 单文件分段（app.ini） | config.yaml + 环境变量 + Web UI | Docker Compose + 环境变量 + 7 步向导 | Web UI + 环境变量 + Docker | Web UI + 环境变量 + Docker | GUI 可视化 + JMTE 模板 | Jellyfin 插件配置页 | Web 向导 + 环境变量 + Web 设置页 |
| 插件加载机制 | 热插拔动态加载（300+，市场一键安装） | 无（作者明确不开放） | plugins/ 目录（Alist 刷新/Emby 刷新/解压） | Driver 接口（新增 Storage Driver 经 init() 注册） | 同 Alist | 异步插件系统（先返回再补充，含开发指南） | 无代码插件（配置驱动频道导入） | 无 | 历史插件体系（不完整） | 无（RSS 源/命名参数化） | 自定义脚本 + Release Profile（无运行时） | Provider 体系（配置即启用，需编译） | SPI 刮削器 addon（v4.2+，Java SPI） | Jellyfin 插件 SPI（本身即插件） | 无（配置即集成） |
| API 风格 | FastAPI REST + MCP 端点（/api/v1/mcp） | Web 后台 REST（无公开文档） | 内部 API（任务编排） | RESTful JSON 统一响应 + WebDAV | Alist V3 兼容 RESTful + WebDAV | RESTful + MCP 集成 | RESTful（controller-service） | Web 后台 REST（无文档） | /api/v1/（无文档） | RESTful（偏移检测/archive 等） | REST /api/v3 | REST /api/v3 + API Key | HTTP API + CLI | 无独立（通过 Jellyfin 调用） | REST /api/v1 + OpenAPI |
| 认证机制 | Web 账号 + PT 站点认证 + CookieCloud | 网盘账号扫码授权 | WebUI 账号密码 | JWT Bearer Token + 路径密码 | JWT（同 Alist） | 无（开放 API） | JWT_SECRET + 注册码（管理员/用户） | admin/admin 默认账号 | Web UI 账号 | WebAuthn Passkey 无密码 | API Key | API Key | 无（本地应用） | Jellyfin 认证 | 媒体服务器 SSO（Plex OAuth/Jellyfin token）+ 本地用户 |

---

## 4. 优缺点与复杂度对比

| 项目 | 优点 | 缺点 | 实现复杂度 | 维护成本 |
|------|------|------|-----------|---------|
| [MoviePilot](https://github.com/jxxghp/MoviePilot) | 全链路一体化（搜索/订阅/下载/整理/刮削/同步）；插件生态最大（300+）；内置 AI Agent + MCP 走在自动化前沿；文档极完善；FastAPI 与 115 Media Hub 同栈可直借 | 主要面向 PT/BT，网盘原生支持弱；不生成 STRM；配置项繁多学习曲线陡；插件质量参差；强依赖外部服务（TMDB/豆瓣/媒体服务器）；GPL-3.0 传染性 | 高 | 高 |
| [qmediasync](https://github.com/qicfan/qmediasync) | 115 开放平台官方接入规避风控；STRM + 302 + Emby 联动一站式；性能优化到位（3 万文件全量约 10 分钟）；元数据双向同步 | 作者声明"不开源"限制再分发；不跨网盘（除 Openlist 间接）；缓存无法感知 115 文件夹重命名/移动；无独立文档站 | 中 | 中 |
| [quark-auto-save](https://github.com/Cp0204/quark-auto-save) | 极活跃（Open Issues 仅 7）；夸克自动化事实标准；一条龙覆盖签到→转存→命名→通知→媒体库刷新；Python 同栈亲和；AGPL 友好 | 仅夸克单盘；强依赖 Cookie 风控；不生成 STRM；不做刮削/订阅；无独立文档站 | 中 | 中 |
| [Alist](https://github.com/AlistGo/alist) | Star 极高（近 5 万）；单二进制部署门槛低；网盘种类最多（30+）；WebDAV 完整；中文文档完善 | 主线已较长时间无更新（2025-05）；Cookie 易失效；不做 STRM/刮削/订阅；缺增量同步；v2→v3 升级路径陡 | 高 | 高 |
| [OpenList](https://github.com/OpenListTeam/OpenList) | 活跃维护中；与 Alist API 兼容迁移成本低；组织化多贡献者避免单点风险；Star 增长极快 | 与 Alist 功能差异小；仍不提供 STRM/媒体自动化；历史 Issue 引用 Alist 命名混淆 | 高 | 高 |
| [PanSou](https://github.com/fish2018/pansou) | 性能取向明确（Go + 并发 + 二级缓存）；Star 增长极快；插件机制开放含开发指南；部署门槛低；MCP 集成 | 仅搜索不转存；强依赖 TG 频道需代理；部分高级特性疑似规划项；默认频道需自行获取 | 中 | 中 |
| [CloudSaver](https://github.com/jiangrui1994/CloudSaver) | 搜转一体闭环体验好；前后端分离 TS 工程化高；响应式 UI 覆盖移动端；Star 高社区教程丰富 | 最新版已闭源仅 Docker；需用户提供 Cookie 安全责任重；仅 4 家转存；无自动定时转存/追更 | 中 | 中 |
| [aliyundrive-subscribe](https://github.com/adminpass/aliyundrive-subscribe) | 阿里云盘订阅自动化早期开创者；配置集中（单 INI）；集成 Aria2 + Emby/Plex 通知；Apache-2.0 宽松 | 已停滞 2 年（154 open issues）；仅阿里云盘；API 变更后功能失效；单一开发者无社区贡献 | 低 | 低（已停滞） |
| [nas-tools](https://github.com/NAStool/nas-tools) | 国内 NAS 媒体自动化奠基性项目；中文环境优化好；文件转移模式丰富（六种）；消息渠道本土化；培养了 MoviePilot 继任者 | 已 archived 停止维护；Flask 架构较老；无完整插件市场；主要面向 PT/BT 网盘弱；UI 繁杂被重构 | 中 | 低（已归档无维护） |
| [AutoBangumi](https://github.com/EstrellaXD/Auto_Bangumi) | 开箱即用专注追番极致；命名规范媒体库兼容好；异步性能优秀（RSS 刷新约 10 倍提速）；文档多语；MIT 友好 | 功能聚焦番剧，剧集/电影覆盖弱；插件生态薄；强依赖 Mikan/TMDB/qBittorrent；密码重置不友好 | 中 | 中 |
| [Sonarr](https://github.com/Sonarr/Sonarr) | 国际剧集自动追更事实标准；稳定成熟；文档社区顶级（Servarr Wiki + Discord）；跨平台；API 完善；*arr 生态协作 | 中文/国产剧集站点适配弱；单一实例只管剧集；对国内网盘无原生支持；无运行时插件需编译 | 高 | 高（社区大分担） |
| [Radarr](https://github.com/Radarr/Radarr) | 电影自动化管理事实标准；自动化链路完整；Provider 体系设计优雅 UI 自动渲染表单；API 完整文档；Custom Formats 精细质量控制 | 同一电影只支持一种版本需多实例；无运行时插件需编译；前端沿用较老 React 栈；中文/网盘弱 | 高 | 高 |
| [tinyMediaManager](https://gitlab.com/tinyMediaManager/tinyMediaManager) | 历史悠久生态成熟覆盖全品类；刮削源丰富可插拔多源叠加；GUI + CLI 双形态；JMTE 模板化灵活；Apache-2.0 友好 | 源码 GitLab 非 GitHub 可见度弱；Swing GUI 传统无 Web UI 需 VNC；构建依赖 GitHub Packages 令牌；无原生中文刮削 | 高 | 中 |
| [jellyfin-plugin-metashark](https://github.com/cxfksword/jellyfin-plugin-metashark) | 填补 Jellyfin 中文刮削空白；豆瓣 + TMDB 组合质量高；AnitomySharp 动漫解析；防封禁 + 图片代理；安装即用 | 强绑定 Jellyfin 无法独立；依赖豆瓣非公开抓取长期脆弱；扩展性有限；仅刮削不重命名/订阅 | 低 | 中（豆瓣反爬持续跟进） |
| [Seerr](https://github.com/seerr-team/seerr) | 一站式请求/发现/通知覆盖全主流媒体服务器；社区活跃（190+ 贡献者）；合并后单代码库；PostgreSQL 支持；MIT 友好 | 仅 Node 单体水平扩展受限；无运行时插件 SDK 需改源码；仅支持单一媒体服务器集成；TMDB/TVDB 强依赖需代理 | 高 | 高 |

---

## 5. 关键发现清单（核心章节）

### 5.1 大多数项目都有的功能（行业标配）

以下能力已被行业内多数项目实现，可视为"网盘媒体自动化"领域的行业标配：

1. **Web 管理后台**：除桌面端 tinyMediaManager（[TMM](https://gitlab.com/tinyMediaManager/tinyMediaManager)）外，几乎所有服务端项目均提供 Web UI，包括 [MoviePilot](https://github.com/jxxghp/MoviePilot)、[qmediasync](https://github.com/qicfan/qmediasync)、[quark-auto-save](https://github.com/Cp0204/quark-auto-save)、[Alist](https://github.com/AlistGo/alist)、[OpenList](https://github.com/OpenListTeam/OpenList)、[CloudSaver](https://github.com/jiangrui1994/CloudSaver)、[aliyundrive-subscribe](https://github.com/adminpass/aliyundrive-subscribe)、[nas-tools](https://github.com/NAStool/nas-tools)、[AutoBangumi](https://github.com/EstrellaXD/Auto_Bangumi)、[Sonarr](https://github.com/Sonarr/Sonarr)、[Radarr](https://github.com/Radarr/Radarr)、[Seerr](https://github.com/seerr-team/seerr)。
2. **Docker 部署**：几乎所有服务端项目均提供官方 Docker 镜像，是当前部署方式事实标准；桌面端 [TMM](https://gitlab.com/tinyMediaManager/tinyMediaManager) 与 [jellyfin-plugin-metashark](https://github.com/cxfksword/jellyfin-plugin-metashark) 依赖宿主或 Jellyfin 容器。
3. **REST API**：[MoviePilot](https://github.com/jxxghp/MoviePilot)、[Alist](https://github.com/AlistGo/alist)、[OpenList](https://github.com/OpenListTeam/OpenList)、[PanSou](https://github.com/fish2018/pansou)、[Sonarr](https://github.com/Sonarr/Sonarr)、[Radarr](https://github.com/Radarr/Radarr)、[Seerr](https://github.com/seerr-team/seerr)、[AutoBangumi](https://github.com/EstrellaXD/Auto_Bangumi) 均提供完整 REST API。
4. **通知推送**：[MoviePilot](https://github.com/jxxghp/MoviePilot)（微信/QQ/TG/Slack/Discord 等 8 渠道）、[quark-auto-save](https://github.com/Cp0204/quark-auto-save)（企业微信/TG）、[aliyundrive-subscribe](https://github.com/adminpass/aliyundrive-subscribe)（钉钉/HiFlow）、[nas-tools](https://github.com/NAStool/nas-tools)（ServerChan/微信/TG/Bark 等）、[Sonarr](https://github.com/Sonarr/Sonarr)、[Radarr](https://github.com/Radarr/Radarr)、[Seerr](https://github.com/seerr-team/seerr)（Discord/Slack/Email/TG/Pushover 等）。
5. **批量重命名**：[MoviePilot](https://github.com/jxxghp/MoviePilot)、[quark-auto-save](https://github.com/Cp0204/quark-auto-save)（正则捕获组替换）、[aliyundrive-subscribe](https://github.com/adminpass/aliyundrive-subscribe)（智能命名模板）、[nas-tools](https://github.com/NAStool/nas-tools)、[AutoBangumi](https://github.com/EstrellaXD/Auto_Bangumi)、[Sonarr](https://github.com/Sonarr/Sonarr)、[Radarr](https://github.com/Radarr/Radarr)、[TMM](https://gitlab.com/tinyMediaManager/tinyMediaManager)（JMTE 模板引擎）。
6. **影视订阅/自动追更**：[MoviePilot](https://github.com/jxxghp/MoviePilot)、[aliyundrive-subscribe](https://github.com/adminpass/aliyundrive-subscribe)（分享链订阅）、[nas-tools](https://github.com/NAStool/nas-tools)（豆瓣联动）、[AutoBangumi](https://github.com/EstrellaXD/Auto_Bangumi)（RSS 订阅追番）、[Sonarr](https://github.com/Sonarr/Sonarr)、[Radarr](https://github.com/Radarr/Radarr)、[Seerr](https://github.com/seerr-team/seerr)（请求系统 + Watchlist）。
7. **TMDB 元数据集成**：[MoviePilot](https://github.com/jxxghp/MoviePilot)、[nas-tools](https://github.com/NAStool/nas-tools)、[AutoBangumi](https://github.com/EstrellaXD/Auto_Bangumi)、[Sonarr](https://github.com/Sonarr/Sonarr)、[Radarr](https://github.com/Radarr/Radarr)、[TMM](https://gitlab.com/tinyMediaManager/tinyMediaManager)、[Seerr](https://github.com/seerr-team/seerr)、[jellyfin-plugin-metashark](https://github.com/cxfksword/jellyfin-plugin-metashark)（TMDB + 豆瓣双源）。

### 5.2 少数项目独有的创新

1. **AI Agent + MCP 端点**：[MoviePilot](https://github.com/jxxghp/MoviePilot) 内置 AI Agent（Copilot）自然语言下达搜索/订阅/下载/整理指令，并暴露 `/api/v1/mcp` 端点供外部 MCP 客户端调用，走在自动化工具前沿。
2. **MCP 协议集成作为 AI 工具**：[PanSou](https://github.com/fish2018/pansou) 集成 MCP，可被 LLM 模型直接调用作为搜索工具，将"网盘搜索能力"标准化暴露给 AI Agent。
3. **300+ 插件市场 + 热插拔**：[MoviePilot](https://github.com/jxxghp/MoviePilot) 拥有该领域最大插件生态（300+ 官方与社区插件），支持 Web UI 一键安装、即装即用、无需重启。
4. **Provider 体系 + UI 自动渲染配置表单**：[Radarr](https://github.com/Radarr/Radarr) 的索引器/下载客户端/通知/元数据/列表均为 Provider，实现统一接口后 UI 自动根据 Provider 定义字段生成配置表单，是处理多网盘异构的最佳范式。
5. **115 开放平台官方接入规避风控**：[qmediasync](https://github.com/qicfan/qmediasync) 通过 115 开放平台接口而非 Cookie 抓取，规避风控风险（用户评价"不担心暴毙"）。
6. **元数据双向同步（本地刮削回传网盘）**：[qmediasync](https://github.com/qicfan/qmediasync) 支持本地刮削后自动同步回网盘，区别于单向刮削。
7. **异步插件先返回再补充 + 二级缓存**：[PanSou](https://github.com/fish2018/pansou) 插件可在主响应返回后继续追加结果，配合内存 LRU + 磁盘分片二级缓存降低重复查询延迟。
8. **JavaScript 插件系统（CLI 形态）**：[aliyunpan](https://github.com/tickstep/aliyunpan)（未进主矩阵但作为依据）提供下载/上传/同步处理器三类 JS 插件，用户可用 JS 自定义文件处理流程无需改 Go 源码。
9. **WebAuthn Passkey 无密码登录**：[AutoBangumi](https://github.com/EstrellaXD/Auto_Bangumi) 采用 WebAuthn 凭据无密码登录，是同类面板中较前沿的认证实践。
10. **豆瓣 + TMDB 双源 + 防封禁 + AnitomySharp 动漫解析**：[jellyfin-plugin-metashark](https://github.com/cxfksword/jellyfin-plugin-metashark) 组合豆瓣抓取 + TMDB 补全 + 请求节流/代理防封禁 + 动漫命名解析，是中文刮削的可直借方案。
11. **热重载配置不中断连接**：[MediaMTX](https://github.com/bluenviron/mediamtx)（未进主矩阵但作为依据）支持配置热重载不中断已有客户端连接，运维友好。
12. **Discord 斜杠命令 + Siri 语音发起媒体请求**：[Requestrr](https://github.com/thomst08/requestrr)（未进主矩阵但作为依据）把媒体请求带入 IM，并集成 Apple Siri 语音入口。
13. **Override Rules 条件化请求默认值**：[Seerr](https://github.com/seerr-team/seerr) 基于用户/标签的条件化请求默认值，可视为轻量规则引擎。

### 5.3 被用户频繁要求但没人做好

1. **"多网盘（5+）+ STRM 生成 + TG 资源同步 + 影视订阅 + 刮削管理"五位一体闭环**：阶段二生态位空白分析明确指出，目前没有任何一个项目同时做到这五项能力完整闭环——[MoviePilot](https://github.com/jxxghp/MoviePilot) 订阅强但不生成 STRM、网盘弱；[qmediasync](https://github.com/qicfan/qmediasync) STRM 强但不订阅不跨网盘；[quark-auto-save](https://github.com/Cp0204/quark-auto-save) 转存强但仅夸克单盘无 STRM；[Alist](https://github.com/AlistGo/alist) 网盘广但不做 STRM/刮削/订阅。
2. **中文刮削防封禁工程化方案**：豆瓣中文刮削是长期痛点（反爬/限流），[MoviePilot](https://github.com/jxxghp/MoviePilot) 与 [jellyfin-plugin-metashark](https://github.com/cxfksword/jellyfin-plugin-metashark) 均受影响，但均未形成成熟的开源防封禁框架。
3. **服务端 PT/网盘混合搜索 + 自动转存一体化**：[PT-Plugin-Plus](https://github.com/pt-plugins/PT-Plugin-Plus)（已归档浏览器扩展，非服务端）做多站聚合搜索；[PanSou](https://github.com/fish2018/pansou) 做服务端搜索但不做转存；[CloudSaver](https://github.com/jiangrui1994/CloudSaver) 做搜转一体但已闭源。无活跃开源项目同时做到"服务端多源搜索 + 多网盘自动转存 + 追更调度"。
4. **阿里云盘转存支持（CloudSaver 用户呼声）**：[CloudSaver](https://github.com/jiangrui1994/CloudSaver) 仅支持 115/夸克/天翼/123 四家转存，未覆盖阿里云盘，社区用户呼声高但未落地。
5. **Telegram 平台支持（Requestrr 社区长期诉求）**：[Requestrr](https://github.com/thomst08/requestrr)（未进主矩阵但作为依据）仅 Discord 平台，Telegram 支持是社区长期诉求，原设计预留扩展性但未实现。
6. **运行时插件 SDK（Seerr/Radarr 社区多次讨论）**：[Seerr](https://github.com/seerr-team/seerr) 团队明确"更多服务集成将在未来加入"但未公开稳定第三方扩展 SDK；[Radarr](https://github.com/Radarr/Radarr) 无运行时插件加载，新增 Provider 需编译发版。
7. **文件夹重命名/移动感知**：[qmediasync](https://github.com/qicfan/qmediasync) 缓存机制无法感知 115 文件夹重命名/移动，是用户高频反馈的痛点。
8. **网盘原生 + 轻量刮削 + API + 插件化中间态**：刮削类工具 [TMM](https://gitlab.com/tinyMediaManager/tinyMediaManager)/[MediaElch](https://github.com/Komet/MediaElch) 偏桌面端封闭；面板类 [MoviePilot](https://github.com/jxxghp/MoviePilot) 偏全功能重；没有项目做到"网盘原生接入 + 轻量刮削管理 + 开放 API + 插件化扩展"的中间态定位。

### 5.4 被大量吐槽的问题

1. **Cookie/Token 失效导致挂载/转存掉线**：[Alist](https://github.com/AlistGo/alist)（115/夸克 Cookie 易失效，需定期更新）、[quark-auto-save](https://github.com/Cp0204/quark-auto-save)（夸克 Cookie 失效，作者反复警告频率避免风控）、[aliyundrive-subscribe](https://github.com/adminpass/aliyundrive-subscribe)（refresh-token 失效后无法自动刷新）、[aliyunpan](https://github.com/tickstep/aliyunpan)（Refresh Token 过期 FAQ 高频问题）。这是网盘类项目的通用痛点。
2. **115 防火墙限流 429**：[Alist](https://github.com/AlistGo/alist) 与 [OpenList](https://github.com/OpenListTeam/OpenList) 均报告 115 防火墙限流导致列表请求 429。
3. **配置繁多学习曲线陡**：[MoviePilot](https://github.com/jxxghp/MoviePilot) 配置项繁多新手学习曲线陡；[nas-tools](https://github.com/NAStool/nas-tools) UI 繁杂被 MoviePilot"聚焦核心需求、简化功能设置"重构解决。
4. **豆瓣反爬/限流导致刮削失败**：[MoviePilot](https://github.com/jxxghp/MoviePilot)（豆瓣刮削易受反爬/限流影响）、[jellyfin-plugin-metashark](https://github.com/cxfksword/jellyfin-plugin-metashark)（豆瓣反爬/限流导致抓取失败为核心痛点，长期脆弱性）。
5. **升级后配置/插件不兼容**：[Alist](https://github.com/AlistGo/alist) v2→v3 升级后旧配置不兼容；[MoviePilot](https://github.com/jxxghp/MoviePilot) 升级后插件失效；[nas-tools](https://github.com/NAStool/nas-tools) 已 archived 后升级配置不兼容无修复。
6. **302 直链 UA 问题导致不能播放**：[Alist](https://github.com/AlistGo/alist) 部分国内网盘 302 直链在某些客户端因 UA 问题不能播放；[qmediasync](https://github.com/qicfan/qmediasync) 内置 115 下载链接代理专门解决此问题。
7. **PT 站点认证争议**：[nas-tools](https://github.com/NAStool/nas-tools) 3.0.0+ 引入 PT 站点认证门槛，老版本绕过认证存在合规争议。
8. **闭源转向引发用户担忧**：[CloudSaver](https://github.com/jiangrui1994/CloudSaver) 最新版本不开源引发用户担忧，部分用户转回历史开源版本 fork。
9. **单维护者停摆风险**：[Alist](https://github.com/AlistGo/alist) 主仓库自 2025-05 后较长时间无更新，社区发起 OpenList Fork"反信任危机"；[aliyundrive-subscribe](https://github.com/adminpass/aliyundrive-subscribe) 停滞 2 年 154 个 Issue 无人处理；[nas-tools](https://github.com/NAStool/nas-tools) 单一开发者后归档。
10. **浏览器扩展 Manifest V2 不兼容**：[PT-Plugin-Plus](https://github.com/pt-plugins/PT-Plugin-Plus) 基于 MV2，Chrome 139+ 已移除 MV2 支持，需降级或迁移 PT-depiler。
11. **TMDB 代理访问问题（国内）**：[MoviePilot](https://github.com/jxxghp/MoviePilot)、[nas-tools](https://github.com/NAStool/nas-tools) 均报告 TMDB 代理配置问题导致刮削失败。

### 5.5 被放弃的设计

1. **Flask 架构被 FastAPI 重写**：[nas-tools](https://github.com/NAStool/nas-tools) 早期 Flask 架构较老扩展性不如 FastAPI，作者 jxxghp 转向 [MoviePilot](https://github.com/jxxghp/MoviePilot) 用 FastAPI 重写，nas-tools 于 2023-05 归档。
2. **功能臃肿 + UI 繁杂被重构简化**：[nas-tools](https://github.com/NAStool/nas-tools) 因功能臃肿、设置繁杂被 [MoviePilot](https://github.com/jxxghp/MoviePilot)"聚焦核心需求、简化功能设置"重构，是"被简化重构"的反面教材。
3. **Manifest V2 被 Chrome 弃用**：[PT-Plugin-Plus](https://github.com/pt-plugins/PT-Plugin-Plus) 基于 Manifest V2，Chrome 139+ 移除 MV2 支持，官方建议迁移继任者 PT-depiler（推测向 MV3 迁移）。
4. **Alist 主仓库维护节奏变化触发社区 Fork**：[Alist](https://github.com/AlistGo/alist) 主维护者减少活跃后，2025-06 社区发起 [OpenList](https://github.com/OpenListTeam/OpenList) Fork，标榜"反信任危机"避免单一维护者造成的项目停摆风险。
5. **开源转向闭源**：[CloudSaver](https://github.com/jiangrui1994/CloudSaver) 最新版本已闭源仅 Docker 部署，"去除内置源"暗示源由用户自管理，避免内置源维护负担与合规风险。
6. **QML/QtQuick 被移除回归 Qt Widgets**：[MediaElch](https://github.com/Komet/MediaElch)（未进主矩阵但作为依据）近期 refactor "Remove usage of QML and QtQuick" 回归 Qt Widgets 降低复杂度。
7. **旧二级缓存实现被移除**：[PanSou](https://github.com/fish2018/pansou) 近期 commit "移除旧的二级缓存实现"暗示缓存层架构演进。
8. **双线维护合并为单代码库**：原 Overseerr（sct/overseerr，已 archive）+ Jellyseerr（Fallenbagel/jellyseerr）双线维护负担重，2026-02 合并为 [Seerr](https://github.com/seerr-team/seerr) 单代码库。
9. **原仓库归档迁移至社区 fork**：原 darkalfx/requestrr 于 2024-01 归档，社区迁移至 [thomst08/requestrr](https://github.com/thomst08/requestrr) fork 维护。
10. **功能被活跃项目接管分流**：[aliyundrive-subscribe](https://github.com/adminpass/aliyundrive-subscribe) 停滞后，功能诉求被 [MoviePilot](https://github.com/jxxghp/MoviePilot) 的阿里云盘插件、[quark-auto-save](https://github.com/Cp0204/quark-auto-save)、[qmediasync](https://github.com/qicfan/qmediasync) 等活跃项目分流。

---

## 6. 对 115 Media Hub 的定位启示

基于上述横向对比，115 Media Hub 在矩阵中的位置与差异化机会如下：

### 6.1 当前矩阵中的位置

115 Media Hub 处于一个尚未被任何单一项目完整覆盖的**生态位空白**：介于 [MoviePilot](https://github.com/jxxghp/MoviePilot)（全功能重面板，偏 PT/BT、无 STRM）与 [qmediasync](https://github.com/qicfan/qmediasync)（STRM 单点、不跨网盘）之间，定位为"多网盘原生 + STRM + 订阅 + 刮削"的中间态网盘媒体面板。阶段二生态位空白分析明确指出"五位一体"（多网盘 5+ / STRM 生成 / TG 资源同步 / 影视订阅 / 刮削管理）能力组合在 20 个项目中无人完整闭环。

### 6.2 差异化机会

1. **五位一体闭环填补生态空白**：相比 [MoviePilot](https://github.com/jxxghp/MoviePilot) 不生成 STRM、网盘弱；[qmediasync](https://github.com/qicfan/qmediasync) 不订阅不跨网盘；[quark-auto-save](https://github.com/Cp0204/quark-auto-save) 仅夸克单盘无 STRM；[Alist](https://github.com/AlistGo/alist) 不做 STRM/刮削/订阅——115 Media Hub 可原生覆盖 115/Quark/天翼/123/阿里五大网盘转存 + STRM 生成 + 订阅 + 刮削全链路。

2. **FastAPI 同栈可直接借鉴 MoviePilot 但避免其偏向**：[MoviePilot](https://github.com/jxxghp/MoviePilot) 同为 FastAPI + Python，其"chain 业务链路 + modules 适配器 + plugins + workflow + skills/MCP"架构可直接借鉴，但应避免其 PT/BT 偏向与配置繁多学习曲线陡的问题。

3. **多网盘（5+）原生转存超越单盘工具**：[qmediasync](https://github.com/qicfan/qmediasync) 与 [quark-auto-save](https://github.com/Cp0204/quark-auto-save) 均聚焦单网盘，115 Media Hub 覆盖 5+ 网盘原生转存是明确差异化。

4. **借鉴 Radarr Provider 体系 + Alist Driver 接口抽象**：[Radarr](https://github.com/Radarr/Radarr) 的 Provider 统一接口 + UI 自动渲染配置表单是处理多网盘异构的最佳范式；[Alist](https://github.com/AlistGo/alist) 的 30+ Driver 接口抽象是网盘覆盖广度的标杆。本项目 `app/providers/` 已覆盖 aliyun/quark/pan115/pan123/tianyi，可对照此模式扩展。

5. **借鉴 qmediasync 115 开放平台接入 + 元数据双向同步**：[qmediasync](https://github.com/qicfan/qmediasync) 的"115 开放平台官方接入规避风控 + 增量缓存 + 元数据双向同步 + Emby 302 代理"组合方案值得 STRM 模块直接对照。

6. **借鉴 PanSou 异步插件 + 二级缓存 + MCP**：[PanSou](https://github.com/fish2018/pansou) 的"异步插件先返回再补充 + 二级缓存 + MCP 集成"模式可借鉴到 TG 频道同步与盘搜模块，降低首屏延迟并对接 AI Agent。

7. **借鉴 metashark 豆瓣 + TMDB 双源 + 防封禁**：[jellyfin-plugin-metashark](https://github.com/cxfksword/jellyfin-plugin-metashark) 的"豆瓣抓取 + TMDB 补全 + 请求节流/代理防封禁 + AnitomySharp 动漫解析"是中文刮削可直借方案，若做出工程化防封禁框架将填补生态空白。

8. **借鉴 quark-auto-save 转存任务编排**：[quark-auto-save](https://github.com/Cp0204/quark-auto-save) 的"多任务组 + 星期调度 + 失效检查 + 新链挑选 + 增量转存"逻辑可移植到转存/追更模块。

9. **坚持开源避免 CloudSaver 闭源转向流失**：[CloudSaver](https://github.com/jiangrui1994/CloudSaver) 闭源转向引发用户担忧，115 Media Hub 应坚持开源避免因商业化而闭源导致用户流失。

10. **组织化运营避免 Alist/nas-tools 单点风险**：[Alist](https://github.com/AlistGo/alist) 主仓库长期不更新触发"信任危机" Fork；[nas-tools](https://github.com/NAStool/nas-tools) 单一开发者后归档；[aliyundrive-subscribe](https://github.com/adminpass/aliyundrive-subscribe) 单一开发者停滞 2 年。115 Media Hub 应保持透明开发节奏与组织化运营，避免单点风险。

11. **保持核心闭环聚焦避免功能膨胀**：[nas-tools](https://github.com/NAStool/nas-tools) 因功能臃肿、设置繁杂被 MoviePilot 重构简化，是"被简化重构"的反面教材。115 Media Hub 应保持"网盘媒体面板"核心闭环聚焦，避免功能膨胀。

### 6.3 核心定位结论

115 Media Hub 的差异化定位应聚焦于**"多网盘（5+）+ STRM 生成 + TG 资源同步 + 影视订阅 + 刮削管理"五位一体的网盘媒体面板**，在"网盘媒体面板"细分赛道形成完整闭环，填补目前生态中"五位一体"能力组合的空白。安全合规层面，应在 Cookie 健康检查与加密存储上做重投入（所有调研项目都强调 Cookie 等同账号密码、必须私有化部署）。

---

*本文档基于阶段一、二对 20 个 GitHub 项目的 16 字段调研生成，每条结论均引用具体项目（项目名 + 仓库链接）作为依据。参与对比矩阵的项目共 15 个，功能对比矩阵覆盖 20 项功能，实现方式对比矩阵覆盖 8 个维度。*
