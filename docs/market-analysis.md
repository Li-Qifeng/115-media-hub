# 市场调研报告：多网盘媒体自动化管理领域

> 调研时间：2026-07
> 调研范围：GitHub 同领域开源项目
> 调研目的：为 115 Media Hub 的演进提供基于实证的横向参照

---

## 项目清单总表

本报告共调研 5 个类目，去重后保留 **20 个项目**。其中 MoviePilot、nas-tools、quark-auto-save、Radarr 在多个类目中重复出现，已合并信息并归入各自最核心的类目下。Star 数为各分文件查证时点（2026-07-10）的近似值；活跃度判定标准：最近一年内有 commit/push 记录为"活跃"，超过一年为"缓更"，已归档为"已归档"。

| 序号 | 项目名 | 主语言 | Star(近似) | 定位 | 仓库链接 | 活跃度 |
|------|--------|--------|-----------|------|----------|--------|
| 1 | Alist | Go | ~49,000 | 多存储文件列表 / WebDAV 程序 | https://github.com/AlistGo/alist | 缓更（2025-05） |
| 2 | OpenList | Go | ~15,600 | Alist 社区延续 Fork | https://github.com/OpenListTeam/OpenList | 活跃 |
| 3 | MoviePilot | Python | ~11,300 | NAS 媒体库自动化面板 | https://github.com/jxxghp/MoviePilot | 活跃（极活跃） |
| 4 | qmediasync | Go | ~589 | STRM 生成与媒体库联动工具 | https://github.com/qicfan/qmediasync | 活跃 |
| 5 | aliyundrive-subscribe | Go | ~963 | 阿里云盘订阅自动转存 | https://github.com/adminpass/aliyundrive-subscribe | 缓更（2024-02 停滞） |
| 6 | quark-auto-save | Python | ~2,900 | 夸克网盘签到/转存/整理一条龙 | https://github.com/Cp0204/quark-auto-save | 活跃（极活跃） |
| 7 | nas-tools | Python | ~9,000 | NAS 媒体库管理工具（已归档） | https://github.com/NAStool/nas-tools | 已归档（2023-05） |
| 8 | AutoBangumi | Python | ~8,100 | 全自动追番工具 | https://github.com/EstrellaXD/Auto_Bangumi | 活跃 |
| 9 | Sonarr | C# | ~13,500 | 剧集自动追更 PVR | https://github.com/Sonarr/Sonarr | 活跃 |
| 10 | Radarr | C# | ~13,900 | 电影自动管理器 | https://github.com/Radarr/Radarr | 活跃 |
| 11 | PT-Plugin-Plus | JavaScript | ~7,800 | PT 种子下载浏览器扩展 | https://github.com/pt-plugins/PT-Plugin-Plus | 已归档（2025-09） |
| 12 | tinyMediaManager | Java | 信息不足 | 桌面端媒体库刮削管理器 | https://gitlab.com/tinyMediaManager/tinyMediaManager | 活跃 |
| 13 | MediaElch | C++ | ~1,100 | Kodi 媒体管理器（Qt） | https://github.com/Komet/MediaElch | 活跃 |
| 14 | jellyfin-plugin-metashark | C# | ~2,100 | Jellyfin 中文刮削插件 | https://github.com/cxfksword/jellyfin-plugin-metashark | 活跃 |
| 15 | PanSou | Go | ~13,800 | 网盘资源搜索 API 服务 | https://github.com/fish2018/pansou | 活跃 |
| 16 | CloudSaver | Vue/TS + Node.js | ~9,100 | 网盘搜索转存一体化平台 | https://github.com/jiangrui1994/CloudSaver | 活跃（新版本已闭源） |
| 17 | aliyunpan | Go | ~5,100 | 阿里云盘命令行客户端 | https://github.com/tickstep/aliyunpan | 活跃 |
| 18 | Seerr | TypeScript | ~11,800 | 媒体请求与发现管理器 | https://github.com/seerr-team/seerr | 活跃 |
| 19 | MediaMTX | Go | ~19,400 | 实时媒体服务器/媒体代理 | https://github.com/bluenviron/mediamtx | 活跃 |
| 20 | Requestrr | C# | ~480 | Discord 媒体请求 Bot | https://github.com/thomst08/requestrr | 活跃 |

---

## 类目一：网盘媒体管理 / STRM 生成类

> 调研对象：GitHub 上"网盘挂载聚合 / STRM 生成 / 网盘媒体自动化面板"类的高质量开源项目。
> 共调研 7 个项目，覆盖"挂载聚合 / 媒体自动化 / STRM 生成 / 网盘订阅转存"四个细分方向。

---

### 1. Alist

仓库：https://github.com/AlistGo/alist
（早期地址 `alist-org/alist`，已迁移至 `AlistGo` 组织）

#### 可核验指标
- Star 数：约 48,961 | Fork 数：6,636 | Open Issues：522
- 主语言：Go | 协议：AGPL-3.0 | 创建时间：2020-12-23
- 最近 push：2025-05-02（主线较长时间未更新；活跃维护转移到社区 Fork —— OpenList）
- 文档完善度：极高，官方文档站 https://alistgo.com ，中英日三语 README，提供 Apifox API 文档

#### 1. 项目定位
官方一句话定位："🗂️A file list/WebDAV program that supports multiple storages, powered by Gin and Solidjs." —— 是一个支持多存储、提供网页浏览与 WebDAV 服务的文件列表程序，不是媒体自动化工具，而是网盘聚合与挂载层。

#### 2. 解决的问题
各家网盘（阿里/115/百度/夸克/天翼/OneDrive/Google Drive/123 等）账号、Cookie、API 各不相同，用户需要在多个 App/网页间切换；Alist 把 30+ 种网盘抽象成统一的文件树 + WebDAV 接口，再由 Emby/Jellyfin/Plex/Infuse 等播放器通过 WebDAV 或直链消费。

#### 3. 核心功能
- 30+ 存储驱动：本地、阿里云盘(Open)、OneDrive、GoogleDrive、123、天翼(个人/家庭)、百度网盘、夸克、UC、迅雷、115、PikPak、S3、WebDAV、SMB、Seafile、Cloudreve、Dropbox、Mega、Lanzou 等
- 文件预览：PDF/Markdown/代码/纯文本、图片画廊、视频/音频（含字幕歌词）、Office 文档
- WebDAV 服务（可挂载为本地磁盘）
- 在线直链下载、单线程下载的多线程加速
- 跨存储复制（Copy files between two storage）
- 离线下载、Web 上传/删除/重命名/移动/复制/新建目录
- 路径密码保护、账号鉴权、签名访问
- Docker 部署、Cloudflare Workers 代理
- 暗色模式、I18n

#### 4. 技术架构
- 后端：Go + Gin
- 前端：SolidJS（编译期框架，体积小）
- 存储：内置 SQLite（默认）/ MySQL
- 鉴权：JWT (Bearer Token)
- 分层：`drivers/`（每个网盘一个 driver 实现 Storage 接口）→ `server/`（HTTP/WebDAV）→ `internal/`（业务逻辑）→ `cmd/`（CLI 入口）
- 单二进制部署，无外部依赖

#### 5. 模块划分
仓库目录清晰：`drivers/`（存储驱动）、`internal/`（核心逻辑：op/fs/db/fts/搜索/offline_download 等）、`server/`（WebDAV/HTTP/中继）、`cmd/`（CLI）、`pkg/`（工具）、`public/`（前端静态资源）

#### 6. 插件机制
原生不支持插件扩展；扩展性体现在「添加新 Storage Driver」上 —— Driver 实现 `model.Storage` 接口即可在 `drivers/` 下新增一个网盘支持并经 `init()` 注册。Webhook / 离线下载的「离线下载工具」是可插拔的（aria2/qBittorrent/Transmission 等）。前端无插件系统。

#### 7. 配置方式
- `data/config.json`：端口、数据库、token 过期时间、资源路径
- `data/data.db` (SQLite)：用户、存储、设置项
- 后台 Web UI「管理 → 存储 → 添加驱动」表单化配置每个网盘的挂载路径/根目录 ID/Cookie/RefreshToken/排序等
- 环境变量：`ALIST_PORT`、`PUID/PGID` 等用于容器化

#### 8. API 设计
RESTful JSON，统一响应 `{code, message, data}`：
- `POST /api/auth/login`（账号密码换 token）
- `POST /api/fs/list`、`POST /api/fs/get`（列目录/取详情）
- `POST /api/fs/mkdir`、`/rename`、`/move`、`/copy`、`/remove`
- `PUT /api/fs/put`（上传）、`POST /api/fs/dirs`（递归建目录）
- `POST /api/admin/storage/*`（驱动增删改查）
- 完整 API 文档：https://alist-public.apifox.cn/

#### 9. UI 设计
SolidJS 单页应用，文件列表型界面：左侧目录树、右侧文件表格、面包屑、缩略图、暗色模式。后台是同一前端的「管理」子页面。无影视墙/海报刮削类 UI —— 这是与媒体面板最显著的差异。

#### 10. 数据模型
- `User`：用户名、密码 hash、是否禁用、权限位、根目录、是否 guest
- `Storage`：驱动类型、挂载路径、子路径、排序、启用状态、driver 配置（extra 持久化为 JSON）
- `Meta`：路径元信息（密码、是否隐藏、是否允许写入）
- `Setting`：key-value 配置
- 文件对象：`model.Obj`（name、size、is_dir、modified、sign、thumb、type）—— 由各 Driver 返回

#### 11. 扩展能力
- 新增存储驱动：实现 `driver.Driver` 接口即可
- 自定义前端：可整体替换 `public/` 静态资源
- Webhook：在文件操作时可触发回调
- 二次开发：单二进制 + RESTful API 极易被其他工具调用（如 alist-strm、qmediasync、CloudDrive2 等大量项目都把 Alist 作为下游）

#### 12. 优点
- Star 极高（近 5 万），生态最大，国内社区活跃
- 单二进制、部署门槛低、跨平台
- 支持网盘种类最多
- WebDAV 协议完整，可被任意播放器挂载
- 中文文档完善

#### 13. 缺点
- 自 2025 年 5 月后主线代码已较长时间无更新（pushed_at 2025-05-02），社区普遍迁移至社区 Fork `OpenListTeam/OpenList`
- 部分国内网盘 Cookie 易失效，需定期更新
- 不直接做 STRM 生成、不做影视刮削/订阅 —— 是底层挂载层，需配合其他工具
- 缺少增量同步机制
- 主仓库架构变更（如 v2 → v3）时升级路径较陡

#### 14. 社区评价
- 国内 NAS 圈"网盘聚合"的事实标准，常被称作"CloudDrive 替代品"
- 长期被 CSDN/掘金/V2EX 等社区推荐为家庭影音搭建首选底层
- 因维护节奏与商业化争议，2025 年 6 月社区发起 OpenList Fork，已成为活跃开发主战场

#### 15. 常见 Issue
- Cookie/Token 失效导致挂载掉线（115/夸克尤为频繁）
- 部分网盘 302 直链在某些客户端因 UA 问题不能播放
- 大目录列表分页/排序异常
- 115 防火墙限流导致列表请求 429
- 升级 v3 后旧配置不兼容

#### 16. 未来发展方向
- 由 OpenList 社区接力维护，路线图集中于：补齐新网盘驱动、修正 Alist v3 遗留 Bug、推动 docker 多架构、对接 Webhook 与媒体库联动
- 与 STRM 生成器（qmediasync / alist-strm）形成上下游组合方案

---

### 2. OpenList

仓库：https://github.com/OpenListTeam/OpenList

#### 可核验指标
- Star 数：约 15,577 | Fork 数：1,141 | Open Issues：133
- 主语言：Go | 协议：AGPL-3.0 | 创建时间：2025-06-11
- 最近 push：2025-09-08
- 文档完善度：高，文档站 https://doc.oplist.org
- 说明：Fork 自 Alist，README 描述 "A new AList Fork to Anti Trust Crisis"，被 HelloGitHub 评分 10.0

#### 1. 项目定位
Alist 的社区延续版本，定位与 Alist 完全一致：多存储文件列表 / WebDAV 程序，由社区共同维护，标榜"反信任危机"（避免单一维护者造成的项目停摆风险）。

#### 2. 解决的问题
Alist 主维护者减少活跃后，社区需要一个有组织（OpenListTeam）、可接力、可审计的 Fork 来持续合并 PR、修复 Bug、新增网盘驱动，避免项目被"卡脖子"。

#### 3. 核心功能
继承自 Alist 的全部能力（多存储驱动、WebDAV、文件预览、跨存储复制、离线下载、签名访问、I18n、暗色模式等），并在持续合并社区 PR。Topics 显式标注 `alist / aliyunpan / baidupan / openlist`。

#### 4. 技术架构
与 Alist 一致：Go + Gin + SolidJS，单二进制，SQLite/MySQL，分层 `drivers → server → internal → cmd`。

#### 5. 模块划分
仓库结构沿用 Alist 命名（drivers / internal / server / cmd / pkg / public）。差异主要在持续合并的社区补丁与新增驱动。

#### 6. 插件机制
同 Alist：通过新增 Storage Driver 扩展网盘支持，无运行时插件系统。

#### 7. 配置方式
沿用 Alist 的 `config.json` + `data.db` + 后台 Web UI 表单。

#### 8. API 设计
完全兼容 Alist V3 RESTful API（`/api/auth/login`、`/api/fs/*`、`/api/admin/*`），便于已有下游生态（alist-strm、qmediasync、Emby 302 代理等）无缝切换。

#### 9. UI 设计
沿用 SolidJS 文件列表界面；社区正逐步优化细节体验。

#### 10. 数据模型
沿用 Alist 的 User/Storage/Meta/Setting/Obj 模型。

#### 11. 扩展能力
- 继承 Alist 的 Driver 接口扩展机制
- 组织化运营：OpenListTeam 是 GitHub Organization，吸收多名贡献者，PR 流程更规范
- 251+ 贡献者（HelloGitHub 数据）

#### 12. 优点
- 活跃维护中（pushed_at 2025-09-08），与 Alist 主仓库已较长时间未更新形成对比
- 与 Alist 完全 API 兼容，迁移成本低
- 组织化、多贡献者，避免单点风险
- Star 增长极快（3 个月内接近 1.6 万）

#### 13. 缺点
- 与 Alist 的功能差异目前仍较小，对老用户而言切换收益有限
- 仍不直接提供 STRM/媒体自动化能力
- 部分历史 Issue 与文档仍引用 Alist 命名，存在混淆

#### 14. 社区评价
- HelloGitHub 评分 10.0，被收录进第 111 期推荐
- 评论区："很棒的项目！很棒的开发者们！"
- 被视为 Alist 的"官方继任者"

#### 15. 常见 Issue
与 Alist 高度一致：Cookie 失效、115 防火墙限流、个别驱动 Bug。新增关于"与 Alist 兼容性 / 升级路径"的讨论。

#### 16. 未来发展方向
- 成为 Alist 系事实上的活跃主线
- 计划合并更多社区驱动与 Bug 修复
- 文档站 https://doc.oplist.org 持续完善

---

### 3. MoviePilot

仓库：https://github.com/jxxghp/MoviePilot
（前端：https://github.com/jxxghp/MoviePilot-Frontend ；插件：https://github.com/jxxghp/MoviePilot-Plugins ）

#### 可核验指标
- Star 数：≈ 11,331（GitHub API，2026-07-10 精确值）
- Fork 数：1,414 | Open Issues：32
- 主语言：Python（FastAPI 后端）+ Vue 3（前端，独立仓库）
- 协议：GPL-3.0 | 创建时间：2023-05-31 | 默认分支：`v2`
- 最近 commit：2026-07-10（`685f044`，作者 Xuanjie Xia）| 最近 push：2026-07-10（查证当日仍活跃）
- 最新版本：v2.14.2（2026-07-07）
- 累计提交：约 7,767 commits
- 文档完善度：极完善。官方 Wiki https://wiki.movie-pilot.org ，REST API 文档 https://api.movie-pilot.org ，含插件开发、PostgreSQL 部署、MCP API、CLI 等多份独立文档

> 注：MoviePilot 同时在"订阅追更""刮削管理""网盘媒体管理"三个类目中被调研，此处合并三类目的分析，取最完整信息。

#### 1. 项目定位
NAS 媒体库自动化管理工具，基于 NAStool 部分代码重新设计，聚焦"订阅、搜索、下载、整理、刮削、媒体库刷新、消息通知"的自动化核心闭环，定位为中文用户的一站式影视自动化面板。整合 TMDB 识别、资源搜索、订阅追更、文件整理、刮削重命名、媒体服务器同步全链路，是国内该领域 Star 最高的项目之一。

#### 2. 解决的问题
资源分散在多个 PT/网盘站点、手动搜索下载效率低；订阅更新不及时错过剧集；Jellyfin/Plex/Emby 多媒体服务器接口各异配置复杂；阿里云盘等网盘资源转存整理繁琐。MoviePilot 将"找资源 → 下载 → 整理 → 刮削 → 同步到媒体服务器"整条链路收敛进单一 Web 面板，并原生支持中文刮削源（豆瓣）与 PT 站点认证，降低国内用户的使用门槛。

#### 3. 核心功能
- 智能搜索与订阅（电影/电视剧自动追新，豆瓣"想看"联动，支持集数定位模板、季/集偏移）
- 多源资源搜索（PT 站点 RSS 聚合、站点 CookieCloud 同步、Telegram 频道搜索）
- 智能元数据匹配（TMDB 为主，多语言/locale；中文刮削：豆瓣元数据 + TMDB 双源）
- 自动下载管理（qBittorrent / Transmission / rTorrent）
- 智能重命名整理（自定义命名格式，硬链接/软链接/复制/移动/RCLONE/MINIO 多种转移模式）
- 媒体服务器集成（Plex / Emby / Jellyfin / 飞牛影视 / 绿联），自动刷新库
- 元数据源：TMDB / 豆瓣 / Fanart
- 消息通知：微信 / QQ / Telegram / Slack / Discord / SynologyChat / VoceChat
- 内置 AI Agent（Copilot）：自然语言下达搜索/订阅/下载/整理/排障指令
- 工作流（Workflow）引擎
- 插件市场：300+ 官方与社区插件
- CookieCloud 同步
- PT 站点用户认证
- 阿里云盘秒传
- MCP 端点 `/api/v1/mcp`

#### 4. 技术架构
- 后端：Python 3.12 + FastAPI（与本项目 `115 Media Hub` 同栈！），端口 3001，Swagger 在 `/docs`
- 前端：Vue 3（独立仓库 `MoviePilot-Frontend`，Nginx 端口 3000）
- 数据库：SQLite（默认）/ PostgreSQL（支持）
- 部署：Docker（`jxxghp/moviepilot-v2`）+ 本地 CLI（`curl ... | bash` 一键安装）
- 事件驱动（`app/core/event.py`）、多级缓存（`app/core/cache.py`）
- 智能体：内置 AI Agent + MCP 端点 `/api/v1/mcp` + Skills 目录（可被 npx skills add 导入到其他智能体）
- 部分组件用 Rust 重写（仓库 `MoviePilot-Rust`）
- 统一适配层屏蔽不同媒体服务器/云盘差异

#### 5. 模块划分
仓库顶层：`app/`（业务逻辑）、`database/`（数据模型/迁移）、`config/`（默认配置）、`docker/`（镜像构建）、`docs/`（规则、开发、测试、PostgreSQL、CLI、MCP API）、`scripts/`、`skills/`（AI Skill 定义）、`tests/`。`app/` 内按 chain（业务链路：search/subscribe/transfer 等）、modules（媒体服务器/下载器/元数据源等适配器）、plugins、workflow 组织。前端为独立 SPA。相关生态仓库：Frontend / Resources / Plugins / Server / Rust / Wiki。

#### 6. 插件机制
插件化是核心扩展方式：
- 插件开发文档：https://wiki.movie-pilot.org/zh/plugindev
- 300+ 官方与社区插件（插件市场 Web UI 一键安装、即装即用、无需重启）
- 插件独立目录，模块化设计，支持热插拔与动态加载
- 插件可挂载事件、注册 API、提供配置页面
- 配套仓库 `MoviePilot-Plugins`
- 工作流（Workflow）+ AI Agent 提供更高层扩展

#### 7. 配置方式
- 环境变量驱动容器配置（Docker Compose 示例 + 完整环境变量表）
- `config/` 目录存放默认配置与 user.conf
- Web UI 内完成订阅、下载、媒体库、消息渠道、插件配置
- 分类策略通过 `category.yaml` 自定义
- PostgreSQL 部署说明独立成文档 `docs/postgresql-setup.md`
- 本地 CLI `moviepilot` 命令支持 init/start/stop/update/config 子命令
- 配置优先级：环境变量 > env 文件（或 Web 界面配置）> 默认值

#### 8. API 设计
FastAPI 自动生成的 REST API，文档 https://api.movie-pilot.org，本地 `/docs`；新增 MCP 端点 `/api/v1/mcp` 让外部 MCP 客户端可调用 MoviePilot 全部工具能力。前端通过统一 RESTful 接口与后端通信。AI Agent / MCP 的引入使 API 不仅是前端消费，也可被模型驱动——这是相对传统刮削器的显著代际差异。

#### 9. UI 设计
Vue 3 + 现代化仪表盘风格：首页统计仪表盘、订阅管理页（自动追剧卡片）、插件市场页、媒体库管理页。响应式可在手机/平板使用；多标签页式面板布局，刮削/订阅/搜索/设置分页。重命名预览、刮削结果绑定均以列表+操作流形式呈现。UI 设计投入明显高于桌面端老牌工具，符合"现代面板"审美。支持主题风格自定义（CSS 脚本）。

#### 10. 数据模型
- 媒体识别信息：基于 TMDB/TVDB/豆瓣交叉验证，30+ 元数据字段
- 订阅：标题、类型、画质、更新间隔、过滤词、保存目录，含集数定位、最佳版本下载记录（note 持久化）等字段
- 下载历史、转移记录、媒体库映射、用户、消息渠道配置
- 工作流与插件状态持久化（SQLite/Postgres）
- TMDB ID 作为跨资源/跨服务器的统一标识（resource identity）
- 订阅与下载任务状态机驱动追更流程

#### 11. 扩展能力
- 插件市场（核心扩展点，300+ 插件）
- Workflow 引擎（可自定义下载完成通知、按类型分类、低质替换高质等动作）
- AI Agent + Skills（可被其他智能体导入操作能力）
- MCP 端点（标准化模型上下文协议集成）
- 多媒体服务器统一适配层（统一 connect/get_library/update_metadata 接口）
- 配套项目矩阵：Frontend / Resources / Plugins / Server / Rust / Wiki
- 前后端分离 + 独立前端仓库，便于定制 UI

#### 12. 优点
- 与本项目 `115 Media Hub` 技术栈完全一致（FastAPI + Python），架构思路可直接借鉴
- 文档极完善（Wiki + API + 插件开发 + MCP + CLI + 部署 + 测试 多份独立文档）
- 插件生态最大（300+），社区最活跃
- 内置 AI Agent / MCP，走在自动化工具前沿
- Release 节奏极快（两周内连发 v2.13.10 → v2.14.2，查证当日仍有提交）
- 国产工具中文优化好，原生中文刮削（豆瓣 + TMDB）与 PT 站点认证
- 全链路一体化（搜索/订阅/下载/整理/刮削/同步），减少工具拼接

#### 13. 缺点
- 主要面向 PT/BT 资源场景，对网盘（115/夸克/天翼）原生支持不如对下载器那么深
- 不直接生成 STRM（需配合 qmediasync / alist-strm 等外部工具）
- 仓库声明"仅用于学习交流，请勿在国内平台宣传"，限制了传播
- 插件质量参差，部分插件维护跟不上主版本
- 配置项繁多，新手学习曲线陡
- 强依赖 PT 站点与外部服务（TMDB/豆瓣/媒体服务器），某一环节失效即影响链路
- 豆瓣刮削易受反爬/限流影响
- GPL-3.0 协议对商业二次集成有传染性约束

#### 14. 社区评价
- 国内 NAS 圈"媒体自动化"事实标准，被视作 nas-tools 的正统继任
- README 明确声明"基于 NAStool 部分代码重新设计"
- 第三方博客大量"5 步打造零维护智能媒体库"教程
- 用户认证机制（PT 站点）维护社区生态但也带来争议
- 贡献者众多（InfinityPace、thsrite、wikrin 等核心 PR 作者活跃）

#### 15. 常见 Issue
- 环境配置错误（Python/Node 版本不匹配）
- 媒体服务器连接失败（Emby/Plex/Jellyfin IP 或 Token 错）
- TMDB 代理配置问题（国内访问）
- 插件兼容性问题（升级后插件失效）
- 订阅识别准确率（中文剧名匹配）
- CookieCloud 同步异常
- 豆瓣/TMDB 刮削失败（反爬、限流、Cookie 过期）
- PT 站点认证/签到失效（站点改版、Cookie 失效）
- 模拟登录竞态失败（如最新提交修复的 page.content() 问题）

#### 16. 未来发展方向
- AI Agent / MCP 深度集成（已完成 `/api/v1/mcp` 端点，注入 shell 命令、托管会话）
- Rust 重写性能敏感模块（MoviePilot-Rust）
- 工作流引擎持续扩展
- 飞牛影视、绿联等国产 NAS 媒体服务器适配
- PostgreSQL 大库支持
- 与更多下载器/媒体服务器/搜索源适配

---

### 4. qmediasync（原 q115-strm）

仓库：https://github.com/qicfan/qmediasync

#### 可核验指标
- Star 数：约 589 | Fork 数：78 | Open Issues：27
- 主语言：Go | 协议：GPL-3.0 | 创建时间：2025-09-08
- 最近 push：2026-04-09（活跃维护中）| 默认分支：main
- 文档完善度：中（README + 论坛帖，无独立文档站）
- 说明：API description 为 "基于 网盘 开放平台接口来同步生成 STRM、元数据下载、元数据上传，直链解析播放和外网302播放，Emby联动删除网盘文件、刷新媒体库、入库通知等"

#### 1. 项目定位
单一聚焦的 STRM 生成与媒体库联动工具，原称 `q115-strm`，现更名为 `qmediasync`。专为「网盘 → STRM 文件 → Emby/Jellyfin/Plex/飞牛影视」链路设计，主打 115 开放平台接口。

#### 2. 解决的问题
网盘文件需要在 Emby/Jellyfin 中播放，但又不想把几十 TB 文件下载到本地；STRM 文件（仅几 KB 的文本快捷方式，指向网盘直链）让媒体服务器像播放本地文件一样播放网盘资源。qmediasync 自动化生成 STRM、维护增量同步、并解决 302 直链播放与 Emby 联动。

#### 3. 核心功能
- STRM 文件批量生成（按目录划分，支持多账号、多同步目录）
- 元数据下载与上传（本地刮削后自动同步回网盘）
- 播放链接解析与外网 302 直链访问
- 内置 Emby 外网 302 代理（8095 端口代理 Emby）
- 内置 115 下载链接代理（解决 UA 导致不能播放）
- 支持同步源：115 开放平台、Openlist（账号密码方式）、CD2 本地挂载、飞牛远程挂载
- 定时任务同步（最小间隔半小时）
- 增量同步缓存（115 全量查询后缓存，增量基于缓存）
- 元数据大小校验，自动下载变更文件
- Telegram 通知
- 跨平台可执行文件（Windows/Linux/MacOS）+ Docker（amd64/arm64）

#### 4. 技术架构
- 后端：Go（GPL-3.0，但作者在论坛帖中说明"不开源"，仓库目前可见代码但许可证限制再分发收费）
- 同步源适配层：115 开放平台 / Openlist / CD2 / 飞牛
- STRM 生成 + 元数据同步 + 302 代理三套独立服务
- 缓存层用于增量同步
- Web 管理界面（端口 12333）

#### 5. 模块划分
仓库目录：`FNOS/`（飞牛 NAS 适配）、`assets/`（静态资源）、`build_scripts/`（构建脚本）、`.changes/`（变更日志）、`.github/workflows/`（CI）。从 Release 节奏看，作者采用 .changes 累积式发版说明。

#### 6. 插件机制
无运行时插件系统；扩展点在于"同步源类型"（115 / Openlist / CD2 / 飞牛本地挂载），每新增一种同步源即扩展支持的网盘范围。论坛帖作者明确表示暂不开放插件机制以避免被商业化二次封装。

#### 7. 配置方式
- Web UI 配置（`http://yourip:12333`）
- 「系统设置 - 网盘账号管理」添加 115/Openlist 账号，扫码二维码授权
- 「系统设置 - STRM 设置」调整 STRM 生成参数
- 「同步 - 同步目录」添加同步目录，配置源路径与目标路径
- 卡片式开关控制定时任务启停

#### 8. API 设计
主要为 Web 后台 REST 接口（账号管理、同步目录、同步记录、STRM 设置）。Emby 302 代理走 8095 端口，115 下载链接代理独立端口。无公开 REST API 文档。

#### 9. UI 设计
卡片式 Web 管理界面：
- 网盘账号卡片（含授权状态、扫码授权弹窗）
- 同步目录卡片（含定时任务开关、全量/增量同步按钮）
- 同步记录列表（展示同步状态、文件数、耗时）
- 系统设置表单

#### 10. 数据模型
- 网盘账号（类型、授权状态、Token、二维码会话）
- 同步目录（源路径、目标路径、定时任务、是否启用）
- STRM 设置项（生成策略、签名、302 配置）
- 同步记录（时间、状态、新增/变更文件数）
- 缓存表（115 文件列表缓存，用于增量）

#### 11. 扩展能力
- 新增同步源类型（Openlist / CD2 / 飞牛本地挂载 已支持，可继续扩展）
- Emby 302 代理与下载链接代理可分别启用
- 支持多账号、多同步目录并行
- 跨平台二进制与 Docker 多架构分发

#### 12. 优点
- 与本项目 `115 Media Hub` 的 STRM 生成模块方向高度一致，可作直接参照
- 115 开放平台接口官方接入，规避风控风险
- 性能优化到位：3 万文件全量约 10 分钟，增量约 30 秒
- 元数据双向同步（本地刮削回传网盘）
- 一站式覆盖 STRM + 302 + Emby 联动
- 维护活跃（2026 年仍在持续发版，v0.14.22 在 2026-04-09）

#### 13. 缺点
- 作者声明"不开源"（GPL-3.0 但限制再分发收费），与完全开源项目定位有差异，社区贡献受限
- 全量查询导致速度上限受网盘 API 限制
- 缓存机制无法感知 115 文件夹重命名/移动
- Openlist 与本地挂载模式同步效率不如 115 开放平台模式
- 文档仅 README + 论坛帖，缺乏独立文档站

#### 14. 社区评价
- 飞牛 NAS 论坛（club.fnnas.com）作者亲自发帖介绍，引发讨论
- 用户认可"开放平台接口，不担心风控，不担心暴毙"的定位
- 172 个 Release Tags 反映迭代极频繁
- 460 commits 显示开发投入度高

#### 15. 常见 Issue
- 115 二维码授权过期或扫码失败
- 同步记录异常中断
- 元数据上传失败（权限/网络）
- Emby 302 代理与 115 下载链接代理端口冲突（作者说明只能选其一）
- 同步目录缓存失效（重命名/移动文件后无法感知）

#### 16. 未来发展方向
- 持续优化 115 开放平台性能（增量同步速度）
- 扩展同步源类型
- 完善 FNOS（飞牛 NAS）适配
- 解决文件夹重命名/移动感知问题
- 文档独立化

---

### 5. aliyundrive-subscribe

仓库：https://github.com/adminpass/aliyundrive-subscribe

#### 可核验指标
- Star 数：约 963 | Fork 数：108 | Open Issues：154
- 主语言：null（GitHub 未识别主语言；从配置文件格式与构建产物判断为 Go，发布二进制 `aliyundrive-subscribe_linux_amd64`）
- 协议：Apache-2.0 | 创建时间：2022-02-09
- 最近 push：2024-02-23（已超过 2 年未更新，处于停滞状态）
- 文档完善度：中（README + Wiki）
- 说明：description 为 "阿里云盘订阅"

#### 1. 项目定位
阿里云盘专属的"分享链订阅 + 自动转存 + 重命名 + 远程下载"工具。是早期网盘订阅自动化的代表性项目，专注于"追剧式"自动转存场景。

#### 2. 解决的问题
阿里云盘分享链接更新后，用户需要手动复制、转存、重命名；连载剧集追更体验差。本工具监控分享链，新文件出现即自动转存到指定目录，并支持剧集正则重命名、Aria2 远程下载、Emby/Plex 通知。

#### 3. 核心功能
- 订阅链管理（添加/删除/编辑/刷新所有订阅）
- 自动转存（监控分享链，新文件自动转存到指定云盘目录）
- 智能命名（`01.mp4 → 不会恋爱的我们.E01.mp4`，支持 E/EP/第N集/第N话 等正则识别）
- 远程下载（Aria2 RPC 集成，可对订阅目录或分享链直接下载）
- 资源管理（云盘文件的新建/删除/重命名/下载/分享）
- 福利码兑换、自动签到
- 通知：钉钉机器人、腾讯 HiFlow
- 媒体库联动：Emby / Plex（server-url + token + delay）
- 缓存目录（m3u8 在线播放资源，4 小时自动清除）

#### 4. 技术架构
- 后端：Go（从二进制命名与 `app.ini` 配置风格推断，仓库未明示）
- 配置：`config/app.ini`（INI 格式，分段 `[app] / [aliyundrive] / [aria2rpc] / [emby] / [plex] / [notify]`）
- 数据库：默认 SQLite（`conf/data.db`），可切换 MySQL
- Docker 镜像：`looby/aliyundrive-subscribe`
- Web 后台：端口 8002，默认账号 admin/admin

#### 5. 模块划分
仓库根目录较扁平：`V2.6_20200218/`（发布版本目录，含可执行文件与 `conf/app.ini`）、`screenshots/`（功能截图）。代码仓库本身只有少量提交（30 commits）。

#### 6. 插件机制
无插件系统。扩展点在于配置文件中的 `app-episode-regex`（识别正则）与保存名称模板（支持 `{}` 序号占位、`E`/`EP` 结尾自动命名）。

#### 7. 配置方式
全部通过 `config/app.ini` 一个文件分段配置：
- `[app]`：端口、账号密码、数据库、检查周期、并发数、缓存目录、通知
- `[aliyundrive]`：refresh-token、open refresh-token、oauth 地址、根目录、空间类型、签到
- `[aria2rpc]`：Aria2 RPC URL、secret、下载目录、开关
- `[emby]` / `[plex]`：媒体服务器 URL、token、delay
- `[notify]`：通知 URL 与 body

#### 8. API 设计
- Web 后台 REST 接口（订阅链 CRUD、云盘资源操作、下载任务、分享管理）
- 阿里云盘官方 API（refresh-token / open refresh-token 双模式）
- Aria2 RPC 集成
- Emby / Plex 通知 API
- 无公开 REST API 文档

#### 9. UI 设计
传统 Web 后台风格：左侧菜单（订阅清单、最近记录、云盘设置、云盘助手、云盘资源、云盘分享）+ 右侧表格/表单。功能截图显示为简洁的列表型管理界面，无海报墙。

#### 10. 数据模型
- 订阅链（订阅地址、保存目录 ID、保存名称模板、过滤词、截止记录 ID、完结状态、分享开关）
- 转存记录（订阅时间、订阅主题、最近更新记录）
- 云盘资源（文件/目录树、ID、size、type）
- 分享记录（30 天限时分享）
- 下载任务（Aria2 关联）
- 用户与配置

#### 11. 扩展能力
- 通过 `app-episode-regex` 自定义剧集识别
- 通过保存名称模板灵活命名
- Aria2 远程下载 + Emby/Plex 通知组合
- 阿里云盘 refresh-token / open refresh-token 双模式
- 不支持自定义插件或新网盘接入

#### 12. 优点
- 阿里云盘订阅自动化的早期开创者，思路清晰
- 配置项集中（单 INI 文件）
- 集成 Aria2 下载与 Emby/Plex 通知
- Apache-2.0 协议宽松
- Docker 部署简单

#### 13. 缺点
- **已停滞**：最近 push 2024-02-23，超过 2 年未更新，154 个 open issues 无人处理
- 仅支持阿里云盘，不支持 115/夸克/天翼/123 等其他网盘
- 阿里云盘 API 多次变更后部分功能可能失效
- 30 commits、单一开发者，社区贡献极少
- 无插件机制、无运行时扩展
- 无公开 API 文档

#### 14. 社区评价
- 早期被广泛推荐（CSDN 多篇教程"实现自动订阅阿里云盘剧集"）
- 被视为阿里云盘追剧的"懒人神器"
- 停滞后用户逐渐迁移到 MoviePilot + 网盘插件 / quark-auto-save / qmediasync 等活跃项目

#### 15. 常见 Issue
- refresh-token 失效后无法自动刷新
- 阿里云盘 API 变更导致转存失败
- 订阅链识别正则不够灵活
- Aria2 远程下载连接异常
- Emby 通知不触发
- 无人响应的 Issue 累积（154 个）

#### 16. 未来发展方向
- 项目已停滞，无明确路线图
- 可能被社区 Fork 接力，但目前未见活跃 Fork
- 功能诉求已被 MoviePilot 的阿里云盘插件、quark-auto-save 等项目分流

---

### 6. quark-auto-save

仓库：https://github.com/Cp0204/quark-auto-save

#### 可核验指标
- Star 数：≈ 2,912 | Fork 数：406 | Open Issues：7（数量极少，维护响应快）
- 主语言：Python | 协议：AGPL-3.0 | 创建时间：2023-12-26
- 最近 push：2026-07-09（前一天刚 push，极活跃）| 累计提交：458 commits
- 文档完善度：完善（README + Wiki，明确要求先翻 Issues/Wiki 再提问）

> 注：quark-auto-save 同时在"网盘媒体管理"和"搜索转存"两个类目中被调研，此处合并两类目的分析。

#### 1. 项目定位
夸克网盘专属的"签到 + 自动转存 + 命名整理 + 推送提醒 + 刷新媒体库"一条龙自动化工具。聚焦夸克单网盘的转存自动化与追更，而非跨网盘搜索聚合。是夸克网盘自动化的事实标准。

#### 2. 解决的问题
持续更新的资源（如连载剧集）每次手动转存繁琐；转存后文件名混乱、媒体库不刷新；夸克网盘需每日签到扩容。该工具把这些重复劳动自动化，搭配 Alist/rclone/Emby 实现"自动追更 + 在线播放"。

#### 3. 核心功能
- 多账号自动签到（每天定时，独立记录连续签到天数与获得空间）
- 智能转存任务（监控分享链，新文件自动转存到指定目录，支持子目录、提取码、失效跳过、智能填充）
- 正则化文件命名（去除广告前缀、统一剧集格式，支持捕获组替换）
- 文件管理（自动新建目录、跳过已转存、正则过滤/替换文件名、忽略指定后缀）
- 任务管理（多任务组、执行周期控制、子任务按星期执行）
- 多渠道通知（企业微信、Telegram 等，推送插件）
- 媒体库自动刷新（Emby / Plex，转存后自动 refresh，模块化扩展）
- WebUI 图形化配置
- 自动解压（auto_unarchive 插件，支持全局启用）
- 失效分享链自动跳过
- 增量转存（跳过已存在文件）
- 失效检查与新链挑选逻辑优化

#### 4. 技术架构
- 后端：Python（FastAPI 风格的 Web 服务，端口 5005）
- 前端：WebUI（重写过一次，引入数据库模块支持转存历史记录）
- 部署：Docker（`cp0204/quark-auto-save:latest`）、青龙面板（`ql repo`）、本地脚本
- 配置：`config/` 目录 + WebUI 表单
- 任务调度基于定时周期
- 模块化设计，媒体库刷新、解压等以插件形式存在
- 插件目录 `plugins/`（如调用 Alist 刷新）

#### 5. 模块划分
仓库结构：`app/`（主程序与运行逻辑，含 run、_path_to_fid 等）、`plugins/`（auto_unarchive 等扩展插件）、`notify.py`（通知模块）、`img/`（文档图片）、`Dockerfile`、`.github/`（CI）。WebUI 重塑后引入数据库模块记录转存历史。近期 refactor 提交聚焦 `_path_to_fid` 逻辑简化与正确报错，显示 app 层有清晰的路径解析抽象。

#### 6. 插件机制
- `plugins/` 目录下可放置联动插件（如转存后调用 Alist 刷新目录、调用 Emby 刷新媒体库）
- 有明确的 `plugins/` 目录与插件化扩展：auto_unarchive（自动解压，支持全局启用）、媒体库刷新模块化扩展
- 插件参与运行流程（转存后处理、媒体库刷新等），近期持续有 plugin 相关 commit
- WebUI 内可配置插件启用与参数
- 与 MoviePilot 的全功能插件市场相比，规模小但够用
- 开发者强调"模块化扩展"是设计取向

#### 7. 配置方式
- 环境变量：`WEBUI_USERNAME`、`WEBUI_PASSWORD`、`QUARK_COOKIE`、`TZ`、`AUTOUPDATE`
- WebUI 表单：账号 Cookie、通知参数、Emby 配置、定时规则
- 任务配置：任务名称、分享链接、保存路径、匹配规则（`$TV` 等魔法变量）、执行周期
- 命名规则：正则 pattern + replace 表达式
- 多账号通过配置管理
- 作者明确警告"严禁设定过高的定时运行频率，以免账号风控和给夸克服务器造成压力"

#### 8. API 设计
以 WebUI 交互为主，内部 API 支撑任务管理、转存执行、签到、媒体库刷新。侧重任务编排而非开放 RESTful API 给外部调用。`_path_to_fid` 抽象负责路径与文件 ID 互转，是夸克网盘操作的核心 API 封装。

#### 9. UI 设计
WebUI 重塑后界面直观：
- 签到状态卡片（账号、连续签到、累计空间）
- 转存任务列表（创建/编辑/管理，每个任务独立周期与规则）
- 转存历史记录（数据库化，可查询）
- 通知与 Emby 配置页
- 实时日志窗口
设计偏功能性，满足"建任务、看日志、改配置"需求，非视觉重投入。

#### 10. 数据模型
- 夸克账号（Cookie、签到状态、连续天数、累计空间）
- 转存任务（名称、分享链接、保存路径、匹配规则、周期、启用状态）
- 转存历史记录（任务、文件名、转存时间、状态）
- 任务组（多任务编组、按星期执行子任务）
- 通知配置（类型、key）
- Emby 配置（URL、API key、刷新开关）
- 文件：FID（夸克文件 ID）、路径、是否已转存标记

#### 11. 扩展能力
- `plugins/` 目录插件机制（Alist 刷新、Emby 刷新、自动解压等）
- 多账号 + 多任务并行
- 多任务组 + 星期调度支持复杂追更场景
- 正则命名引擎（捕获组替换）
- Webhook 与通知渠道扩展
- 青龙面板集成（脚本玩家友好）
- 可与 Alist、rclone、Emby、CloudSaver 组合形成完整链路

#### 12. 优点
- 极活跃（pushed_at 2026-07-09，前一天刚 push，458 commits 累计迭代充分）
- Open Issues 仅 7 个，维护响应极快
- 夸克网盘自动化事实标准，Star 近 3 千
- 一条龙覆盖签到→转存→命名→通知→媒体库刷新
- WebUI 图形化配置，新手友好
- Docker / 青龙面板 / 本地脚本多种部署
- 增量转存与失效链接跳过等细节完善
- Python 栈，对 115 Media Hub（FastAPI）技术栈亲和，可借鉴任务调度与插件设计
- AGPL-3.0 协议对衍生项目友好
- 文档与 Wiki 完善，Issue 质量较高

#### 13. 缺点
- 仅支持夸克网盘，不覆盖 115/天翼/123/阿里云盘
- 强依赖夸克 Cookie，账号风控风险（作者反复警告频率）
- 不生成 STRM（需配合 qmediasync / alist-strm）
- 不做影视刮削/订阅识别（需配合 MoviePilot）
- 无独立文档站，依赖第三方博客教程
- 插件规模小于 MoviePilot
- 磁力/离线下载能力有限（夸克侧能力受限）
- 无搜索聚合，需配合 PanSou/CloudSaver 使用

#### 14. 社区评价
- 夸克网盘追剧党强烈推荐，第三方博客大量教程
- GitCode / CSDN / 知乎 / B 站 / 什么值得买 / 飞牛社区 等多平台测评
- "5 分钟搭建自动化系统" 类教程传播度高
- 与 Alist / qmediasync / MoviePilot / CloudSaver 形成互补工具链
- 评价"开发者≠客服，Wiki 完善，遇到问题先翻 Issues"

#### 15. 常见 Issue
- Cookie 失效（需重新获取）
- 转存路径不存在（需开启 auto_create_dir）
- 网络超时（需调整 TIMEOUT）
- 命名正则不匹配特殊文件名
- Emby 媒体库刷新未触发（API key 或权限问题）
- 任务频率过高触发风控
- 文件名正则替换未达预期
- 多账号切换与配额查询问题

#### 16. 未来发展方向
- 持续优化 WebUI 与数据库化历史记录
- 持续优化失效检查与新链挑选逻辑（近期重点）
- 扩展通知与插件渠道（解压、通知、媒体库）
- 计划中的 Chrome 插件版（免抓包配置）
- 与 SmartStrm 等 STRM 工具联动形成完整方案
- 与 CloudSaver/Alist/Emby 的集成文档深化
- 可能向兼容青龙调度方向靠拢

---

### 7. nas-tools

仓库：https://github.com/NAStool/nas-tools
（Wiki https://wiki.nastool.org ；Docker `nastool/nas-tools`）

#### 可核验指标
- Star 数：约 9,048 | Fork 数：1,730 | Open Issues：170（已 archived，无法新增）
- 主语言：null（GitHub 未识别；早期为 Python + Flask，历史版本基于 FastAPI + Vue）
- 协议：AGPL-3.0 | 创建时间：2021-08-04
- 最近 push：2023-05-16 | 默认分支：master
- **archived: true（已归档，只读）**
- 文档完善度：中（Wiki 在 wiki.nastool.org / TG 频道，README 较简洁；现仓库精简）

> 注：nas-tools 同时在"网盘媒体管理"和"订阅追更"两个类目中被调研，此处合并两类目的分析。

#### 1. 项目定位
NAS 媒体库资源归集与整理自动化工具，MoviePilot 的直接前身。初衷是"实现影视资源自动化管理，释放双手、聚焦观影"，需良好网络与私有站点。聚焦 PT/BT 资源场景，把"检索 → 订阅 → 下载 → 整理 → 刮削 → 通知"整合进单一面板，专为中文环境优化。

#### 2. 解决的问题
早期 NAS 用户使用 Sonarr/Radarr/Bazarr 等英文工具链配置繁琐、中文识别差；站点 RSS 聚合追新、豆瓣联动自动检索下载、下载完成自动识别硬链接到媒体库重命名、站点养护（数据统计/自动登录保号/全自动托管养站）、消息远程控制订阅下载。nas-tools 提供国产化、中文优化、消息渠道本土化（微信/Telegram/Slack/Bark/PushPlus/ServerChan）的一站式方案。

#### 3. 核心功能
- 资源检索订阅：站点 RSS 聚合，想看的加入订阅自动追新；微信/Telegram/Slack/Web 聚合搜索下载；豆瓣标记想看后台自动检索
- 媒体库整理：监控下载器自动识别真实名称硬链接重命名；目录监控自动识别；专为中文环境优化，Emby/Jellyfin/Plex 100% 刮削
- 站点养护：站点数据统计、流量监测、自动登录保号、全自动托管养站、远程下载器
- 消息服务：ServerChan/微信/Slack/Telegram/Bark/PushPlus/爱语飞飞 等图文通知与远程控制
- 文件转移模式：复制、硬链接、软链接、移动、RCLONE、MINIO（六种）
- 媒体库联动：Emby / Jellyfin / Plex
- TMDB 元数据刮削
- PT 自动刷流（老版本支持）

#### 4. 技术架构
- 后端：Python + FastAPI + Vue 前后端分离（与 MoviePilot 同源）
- 数据库：SQLAlchemy ORM
- 部署：Docker（`jxxghp/nas-tools` / `nastool/nas-tools`）、群晖 SPK 套件、Windows exe、本地源码
- API: `http://localhost:3000/api/v1/`（与 MoviePilot 端口/API 路径同源，MoviePilot 沿用并扩展）
- 消息：requests 库对接各通知渠道

#### 5. 模块划分
README 与 Wiki 显示按功能域划分：资源检索订阅、媒体库整理、站点养护、消息服务四大板块；含 RSS 聚合、豆瓣联动、下载器监控、文件识别重命名、站点统计等子模块。代码层 `app/` 组织各业务模块。

#### 6. 插件机制
早期版本无完整插件市场，历史版本提供插件体系，后被 MoviePilot 继承并强化；当前归档仓库未保留完整插件实现。扩展性体现在：
- 文件转移模式可插拔（复制/硬链接/软链接/移动/RCLONE/MINIO）
- 通知渠道可扩展（持续增加新通知服务）
- 站点 RSS 聚合配置化
- 消息渠道远程控制（微信/Telegram/Slack 远程订阅下载）

#### 7. 配置方式
- 环境变量：`NASTOOL_CONFIG`（指向 config.yaml）、`NASTOOL_AUTO_UPDATE`、`NASTOOL_CN_UPDATE`
- `config/config.yaml` 主配置
- Web UI 配置（站点、订阅、媒体库、消息、下载器）
- 申请 TMDB API KEY
- 申请消息通知服务（企业微信 / Server酱 / Telegram Bot / Bark / Slack）
- 群晖 SPK 套件源（矿神 imnks.com / spk.imnks.com）
- `NASTOOL_AUTO_UPDATE=false` 避免连不上 GitHub

#### 8. API 设计
REST API `http://localhost:3000/api/v1/`，无公开 API 文档。前后端通过 FastAPI 路由通信。

#### 9. UI 设计
历史 Web UI，功能入口多但被诟病设置繁杂——这正是 MoviePilot"聚焦核心需求、简化功能设置"重构的出发点。截图显示为蓝色系管理界面，含媒体库仪表盘、订阅管理、站点统计、消息配置等页面。

#### 10. 数据模型
围绕媒体库、订阅、站点、下载历史、消息通知建模；媒体识别信息（TMDB 元数据）、订阅（关键词、过滤、保存路径）、下载历史与转移记录、站点配置（Cookie、RSS、统计）、消息渠道配置、用户与权限。与 MoviePilot 数据层有继承关系。

#### 11. 扩展能力
历史较强（插件 + 站点适配 + 消息渠道），但已停止维护，无新扩展；价值在于作为 MoviePilot 的演进参照与中文 NAS 自动化生态的奠基。

#### 12. 优点
- 国内 NAS 圈"媒体自动化"的奠基性项目，Star 接近 9 千
- 中文环境优化好，国产剧集和动漫识别准确率高
- 文件转移模式丰富（六种）
- 消息渠道本土化（微信/Telegram/Slack/Bark 等）
- 群晖套件源降低部署门槛
- 培养了大量用户与开发者（后续衍生 MoviePilot）
- 整合度高（检索+整理+养站+通知一体）、社区教程极丰富

#### 13. 缺点
- **已 archived**：2023-05-16 后停止维护，170 个 Issue 无法处理
- Flask 架构较老，扩展性不如 FastAPI（注：历史版本已转 FastAPI）
- 无完整插件市场（不如 MoviePilot）
- 主要面向 PT/BT，对网盘支持弱
- 不生成 STRM
- 单一开发者（jxxghp）后转向 MoviePilot 开发
- 3.0.0+ 引入 PT 站点认证门槛；老版本绕过认证存在合规争议
- UI 繁杂（被 MoviePilot 重构解决）

#### 14. 社区评价
- HelloGitHub 评分 10.0，被收录进第 77 期
- 早期被视作"NAS 媒体管理神器"，CSDN/掘金大量教程
- 评论："好像已经停电了" / "好像停止发电了"（2023 年归档后用户惋惜）
- 用户普遍迁移至 MoviePilot（同作者继任项目）
- 曾是国内 NAS 影视自动化的事实标准

#### 15. 常见 Issue
- 站点 Cookie 失效
- TMDB 代理访问问题
- 硬链接失败（目录不在同一分区 / 跨分区限制）
- 中文剧名识别错误
- 消息通知不触发
- 升级后配置不兼容（已 archived 后无修复）
- PT 自动刷流规则
- 自动更新失败、认证机制争议

#### 16. 未来发展方向
- **项目已 archived，不再发展**
- 作者 jxxghp 将精力全部投入 MoviePilot
- nas-tools 的代码、用户、社区由 MoviePilot 继承
- 作为"前辈项目"在调研中具有参照价值：展示了一个国产 NAS 媒体工具从兴起到归档的完整生命周期，以及如何通过继任项目（MoviePilot，FastAPI 重写 + 插件市场 + AI Agent）实现技术升级
- 对 115 Media Hub 而言，nas-tools 是"被简化重构"的反面教材，提示避免功能臃肿与设置繁杂

---

## 类目二：影视资源订阅 / 自动追更类

> 调研对象：影视订阅 / 追更 / 自动下载类项目。两处"已归档"项目（nas-tools 已归入类目一，PT-Plugin-Plus）因其在生态中的历史地位或对 PT/BT 自动下载方向的代表性仍纳入分析，并明确标注归档状态。

---

### 1. AutoBangumi（Auto_Bangumi）

仓库：https://github.com/EstrellaXD/Auto_Bangumi
（官网/文档：https://www.autobangumi.org ）

#### 可核验指标
- Star 数：约 8.1k（HelloGitHub 收录数据；Fork 约 437）
- 最近活跃：活跃。最新提交 `36f67a8` 于 2026-07-08（合并 3.3-dev），主分支累计约 1,969 次提交，28 分支、166 标签
- 主语言：Python（后端，FastAPI + 异步 httpx/aiosqlite）+ Vue3（前端）
- 协议：MIT
- 文档完善度：完善。官方文档 autobangumi.org，含本地/Docker/群晖部署、RSS 配置、changelog（中英日多语）
- Issue/PR：Open Issues 约 132、Open PR 约 19

#### 1. 项目定位
全自动追番工具，专注通过 RSS 订阅（Mikan Project 等）实现番剧的自动下载、整理与重命名，输出兼容 Plex/Jellyfin/Emby 的标准媒体库结构。

#### 2. 解决的问题
追番需手动找资源、解析复杂文件名、整理季集目录；季中追番漏集补全麻烦；命名不规范导致媒体服务器刮削失败。

#### 3. 核心功能
- 监控 RSS 源（Mikan）自动获取最新番剧更新
- 智能解析番剧元数据（剧集、季数、集数）
- 自动触发 qBittorrent 下载
- 下载完成自动整理重命名（如 `[Lilith-Raws] Kakkou no Iinazuke - 07 ...` → `Kakkou no Iinazuke S01E07.mp4`）
- TMDB 集成生成标准元数据；Mikan RSS 反代支持
- 季中追番自动补全错过的剧集、季/集偏移自动检测
- 番剧归档、Bangumi.tv 放送日历视图、首次运行设置向导

#### 4. 技术架构
Python 后端（FastAPI），v3.2 起完全异步：数据库层 aiosqlite、网络层由 requests 迁移至 httpx AsyncClient、RSS/下载器/解析器全异步；`uv` 包管理（pyproject.toml + uv.lock）；共享 HTTP 连接池复用 TCP/SSL。

#### 5. 模块划分
RSS 引擎、下载器适配（qBittorrent）、解析器（TMDB、Mikan）、重命名模块、Checker/后台扫描线程、用户与认证（Passkey WebAuthn）、API 层、前端 Vue3。

#### 6. 插件机制
偏轻量单体，无 MoviePilot 式重型插件市场；扩展性主要体现在可配置的 RSS 源、命名规则、搜索 provider 配置（`/search/provider/config` API）等参数化能力，而非插件 SDK。

#### 7. 配置方式
Docker Compose（推荐，常与 qBittorrent + Jellyfin 组合）、本地运行（Python 3.10+ 虚拟环境）、群晖；环境变量配置下载器地址等；新版提供 7 步引导式首次设置向导（账号/下载器/RSS/媒体路径/通知）。

#### 8. API 设计
RESTful API，含 `POST /bangumi/detect-offset`（偏移检测）、`PATCH /bangumi/archive/{id}`、`PATCH /bangumi/dismiss-review/{id}`、`GET /bangumi/refresh/metadata`、`GET/PUT /search/provider/config` 等；首次运行设置 API 认证豁免（完成后 403）。

#### 9. UI 设计
Vue3 Web UI（默认端口 7892），提供番剧列表、订阅管理、下载状态、日历视图；初始账号 admin/adminadmin（建议改密，密码遗忘需删 `data/data.db` 重置）。

#### 10. 数据模型
围绕 Bangumi（番剧，含 title_raw、needs_review、needs_review_reason、deleted 等字段）、RSSItem、Torrent（url/rss_id 索引）、Episode/SeasonInfo（使用 `__slots__` 降内存）、User（含 WebAuthn 凭据）建模；SQLite 存储。

#### 11. 扩展能力
中等。靠 RSS 源接入与命名/搜索 provider 配置扩展；异步化后性能大幅提升（RSS 刷新约 10 倍、种子下载约 5 倍、重命名文件列表约 20 倍提速）；可通过自建 Mikan 反代扩展稳定性。

#### 12. 优点
开箱即用、专注追番场景极致、命名规范与媒体库兼容好、异步性能优秀、文档多语、MIT 友好；与 115 Media Hub 的"订阅自动追更"诉求高度对口。

#### 13. 缺点
功能聚焦番剧，剧集/电影覆盖弱；插件生态薄；强依赖 Mikan/TMDB 与 qBittorrent；WebUI 早期英文为主、密码重置不友好。

#### 14. 社区评价
追番场景事实标准之一，HelloGitHub 第 87 期收录，近一周仍有 Star 增长；社区以 Docker 部署教程流传广泛。

#### 15. 常见 Issue
RSS 连接状态/反代失效、季集偏移识别（放送间隔超 6 个月分 Part）、TMDB 匹配不准、qBittorrent 连接、密码重置、种子名解析正则覆盖。

#### 16. 未来发展方向
WebAuthn Passkey 无密码登录深化、异步与缓存优化、搜索 provider 多源化、番剧归档/元数据刷新自动化、首次设置向导完善。

---

### 2. Sonarr

仓库：https://github.com/Sonarr/Sonarr
（官网 https://sonarr.tv ；Wiki https://wiki.servarr.com/sonarr ；API https://sonarr.tv/docs/api ）

#### 可核验指标
- Star 数：约 13k–14k（star-history 显示 14.3k，gh.mlsub 显示 13.1k；Fork 约 1.7k）
- 最近活跃：活跃。主分支 `v5-develop` 累计约 11,712 次提交，最近提交 `7c41dcb` 于 2026-05-22，53 分支、164 标签
- 主语言：C#（.NET，v5-develop 已 Bump .NET 至 10）；前端 React
- 协议：GPL-3.0
- 文档完善度：极完善。Servarr 统一 Wiki，含安装/快速开始/库/日历/活动/Wanted/设置/自定义脚本/FAQ/PostgreSQL/故障排除等
- Issue/PR：Open Issues 约 78–84

#### 1. 项目定位
面向 Usenet 与 BitTorrent 用户的智能 PVR（个人视频录像机），专注电视剧集的自动监控、搜索、下载与整理，是 Servarr 生态与 \*arr 范式的奠基者。

#### 2. 解决的问题
手动追剧繁琐、错过首播/补集、画质升级需手动替换、命名混乱；将"监控 RSS → 检测新集 → 下载客户端拉取 → 命名归档"全流程自动化。

#### 3. 核心功能
- 监控多 RSS 源，新集播出自动抓取
- 季/集自动排序命名（`{Series Title} - S{season:00}E{episode:00}`）
- 画质配置文件与自动升级（cutoff unmet 重抓更高画质）
- 失败下载自动处理与重试
- 季票订阅、缺失集补全、首播集优先
- 列表导入（Trakt/IMDb/自定义）、日历视图、批量编辑
- 与 SABnzbd/NZBGet/qBittorrent/Deluge/Transmission 等下载客户端集成

#### 4. 技术架构
C# .NET 后端 + React 前端，单容器部署（LinuxServer.io 镜像 `lscr.io/linuxserver/sonarr`），默认端口 8989；REST API；与 Prowlarr/Jackett 索引器、Bazarr 字幕、Plex/Jellyfin/Emby 通知库更新联动。

#### 5. 模块划分
`src/NzbDrone.Core/` 下按职责划分：Series/Tvdb、Profiles（质量配置）、MediaFiles（文件处理）、Search（搜索策略）、Indexers、DownloadClients、Notifications、Calendar、Wanted 等；前端独立仓库。

#### 6. 插件机制
无传统插件 SDK，靠"自定义脚本（Custom Scripts）"事件钩子、质量/延迟配置文件、Release Profile（正则规则）、标签（Tags）分配索引器/规则等参数化机制扩展；生态扩展更多依赖 Prowlarr/Jackett/Bazarr 等配套 \*arr 应用组合。

#### 7. 配置方式
Docker（推荐）、Windows/Linux/macOS/Raspberry Pi；`/config`、媒体目录、下载目录挂载；`PUID/PGID/TZ`；Web 界面配置索引器、下载客户端、质量配置、根目录、监控策略；支持 PostgreSQL。

#### 8. API 设计
完整 REST API（端口 8989，`/api/v3`），文档 https://sonarr.tv/docs/api ，用于与 \*arr 生态、Ombi/Overseerr 请求、家庭仪表盘联动。

#### 9. UI 设计
React Web UI，系列库/日历/活动/Wanted/设置等模块，过滤与批量编辑强大；与 Radarr 共享 UI 范式（学一个即会另一个）。

#### 10. 数据模型
Series → Season → Episode 层级；Series Type（Standard/Daily/Anime 影响搜索）、监控状态（All/Future/Missing/Existing/First Season/Latest/None）、质量配置文件、根目录、标签、Release Profile。

#### 11. 扩展能力
生态型扩展强：Prowlarr 统一索引器管理、Jackett 索引器代理、Bazarr 字幕、Overseerr 请求、TRaSH-Guides 规范；自定义脚本与 Webhook 通知扩展。

#### 12. 优点
国际剧集自动追更的事实标准、稳定成熟、文档与社区（Discord/Reddit/Forum）顶级、跨平台、API 完善、与 \*arr 生态无缝协作。

#### 13. 缺点
针对中文/国产剧集与动漫的命名与站点适配弱（无原生 PT 站点支持，靠 Prowlarr/Jackett 间接）；单一实例只管剧集（需配合 Radarr 管电影）；对国内网盘（115/阿里）无原生支持。

#### 14. 社区评价
自托管媒体自动化基石项目，全球用户基础大；与 Radarr 共享 Servarr Wiki 与 Discord，开发团队协调紧密。

#### 15. 常见 Issue
索引器/RSS 同步失败、Release 命名解析不匹配、画质升级循环、库导入路径权限（NFS `nolock`/SMB `nobrl`）、Anime 列表 XEM 映射。

#### 16. 未来发展方向
v5 重构与 .NET 10 升级、UI 重设计分支（redesign）、PostgreSQL 大库支持、与 Prowlarr/Overseerr 集成深化、Anime/多语言元数据增强。

---

### 3. Radarr

仓库：https://github.com/Radarr/Radarr
（官网 / 文档：https://radarr.video ｜ https://wiki.servarr.com/radarr ；API 文档：https://radarr.video/docs/api/）

#### 可核验指标
- Star 数：13,944 | Fork 数：1,184 | Open Issues：488
- 主语言：C#（.NET 8）
- 最近 push：2026-07-02（活跃）
- License：GPL-3.0 | 创建时间：2016-12
- 最新稳定版：v6.2.1.10461（2026-06-08）| 总 Release：263
- 文档完善度：高（Servarr Wiki 统一文档站、API 文档、Discord 支持）

> 注：Radarr 同时在"订阅追更"和"媒体服务器生态"两个类目中被调研，此处合并两类目的分析。

#### 1. 项目定位
面向 Usenet / BitTorrent 用户的**电影收藏管理器（Movie Collection Manager）**，2017 年从 Sonarr fork 而来，针对电影（单文件、版本/发行版差异、上映状态）优化的电影收藏自动管理器，是 Servarr 生态的电影管理组件。自动监控 RSS、抓取、整理、重命名、质量升级。属 \*arr 生态（与 Sonarr 电视剧、Lidarr 音乐、Readarr 书籍同源同架构）的核心成员之一。

#### 2. 解决的问题
"想看的电影怎么自动下载、下载后怎么按规范命名入库、已有低画质版本如何自动升级到高画质"三大问题；多版本（导演剪辑版/剧场版/加长版）管理混乱、画质升级（DVD→Blu-Ray→4K）需手动替换、上映前预发布监控缺失。Radarr 监控多个 RSS/索引器源，对接下载客户端，自动完成"添加 → 检索 → 下载 → 失败重试 → 导入 → 重命名 → 质量升级"全链路。

#### 3. 核心功能
- 电影添加（含预告片、评分、海报等元数据）
- 监控多 RSS 源抓取想看电影
- 多版本支持与特别版识别（Director's Cut 等）
- 基于上映日期的可用性判断与预发布监控
- 质量自动升级（如 DVD → Blu-Ray）
- 画质配置文件与自动升级（cutoff）
- 失败下载自动处理：失败则尝试下一个 release
- 手动搜索：可选择任意 release 并查看未下载原因
- 下载客户端集成：SABnzbd、NZBGet、qBittorrent、Deluge、rTorrent、Transmission、uTorrent 等
- 自动检索 + RSS 同步
- 已下载电影自动导入
- 识别特别版、导演剪辑版、硬字幕、AKA 片名
- 自定义格式（Custom Formats）精细分级、AKA 别名识别
- 与 Kodi / Plex 集成（通知 + 媒体库更新）
- 元数据导入（预告片、字幕）并为 Kodi 等生成海报/NFO
- Profile 高级自定义，确保下载所需版本
- 美观的 Web UI

#### 4. 技术架构
- C# / .NET 8（2025-09 起从 .NET 升级到 .NET 8）
- 单体 Web 应用：后端 ASP.NET + 前端 React/React-Redux（沿用 Sonarr 的前端栈）
- 数据访问：内置 SQLite（默认），可配 PostgreSQL
- 调度：内置任务调度器周期执行 RSS 同步、刷新、清理
- 构建：Azure DevOps Pipeline（`dev.azure.com/Radarr/Radarr`）
- 多平台打包：跨平台 .NET 发布 + Docker（linuxserver 镜像为主流部署方式）

#### 5. 模块划分
\*arr 系列共享统一骨架：
- `NzbDrone.Core/`：核心域（电影、下载、索引、通知、元数据、质量 Profile）
- `NzbDrone.Api/` / API 控制器层
- 前端 `frontend/src/`：React SPA
- `NzbDrone.Common/`、`NzbDrone.Core.Test/`：通用库与测试
按功能域划分：Movies、Calendar、Wanted、Activity、Settings、System。
索引器（Indexers）、下载客户端（Download Clients）、通知（Notifications）、元数据（Metadata）、列表（Lists）均为可插拔 Provider 体系。

#### 6. 插件机制
- **Provider 体系是 Radarr 最值得借鉴的扩展机制**：索引器、下载客户端、通知、元数据生成器、列表源均为"Provider"，通过实现统一接口 + 注册即可新增，且 UI 自动根据 Provider 定义的字段生成配置表单。
- 用户可在设置页直接启用/禁用 Provider，多实例可并存。
- 新增 Provider 仍需改源码编译，但对使用者而言是"配置即启用"。
- 无运行时动态加载第三方 DLL 的机制。
- 同 Sonarr，靠自定义格式（Custom Formats，正则+评分）、质量配置文件、列表导入（Trakt/IMDb/TMDb/自定义）、自定义脚本、Webhook 扩展；生态靠 \*arr 组合。

#### 7. 配置方式
- Web UI 设置页（多 Tab：媒体管理、Indexers、Download Clients、Profiles/Quality、Metadata、Notifications、Lists、Connect、General、UI）
- 持久化：SQLite 数据库（`nzbdrone.db` 系列），可选 PostgreSQL
- 环境变量覆盖部分启动参数
- 配置导入/导出支持
- Docker（推荐，LinuxServer.io 镜像）、Windows/Linux/macOS/Raspberry Pi；`PUID/PGID/TZ`；`/config`+`/movies`+`/downloads`

#### 8. API 设计
- 完整 RESTful API（`/api/v3/...`，端口 7878），官方 API 文档 `https://radarr.video/docs/api/`
- API Key 鉴权
- 覆盖电影增删改查、搜索、添加、列表、日历、队列、历史、命令、通知、配置等
- 被 Overseerr/Seerr、Requestrr 等上游工具作为标准对接对象

#### 9. UI 设计
- React SPA，深色/浅色主题，左导航（Movies / Calendar / Activity / Wanted / Settings / System）
- 电影卡片网格、详情页（Cast、历史、文件、质量）
- 日历视图按上映日期展示
- Wanted 列表管理待下载/缺失电影
- 设置页按 Provider 动态渲染表单字段，统一且可扩展
- 与 Sonarr 几乎一致（电影库/日历/活动/Wanted/设置），Custom Formats 配置强大；学习成本低

#### 10. 数据模型
- `Movie`：电影实体（TMDb id、标题、年份、质量 Profile、监控状态、文件路径、状态）
- `MovieFile`：实际文件（路径、质量、版本）
- `QualityProfile` / `Profile`：质量规则集
- `Indexer` / `DownloadClient` / `Notification` / `Metadata` / `List`：Provider 实例配置
- `History` / `Queue` / `ScheduledTask` / `Command`：运行时状态
- TMDb id 是跨系统关联主键

#### 11. 扩展能力
- Provider 体系覆盖 Indexer/DownloadClient/Notification/Metadata/List，新增源成本低
- Lists 接入第三方电影列表（TMDb List、IMDb List、Trakt 等）自动同步想看
- Connect 与 Kodi/Plex 联动
- API 完整，便于被请求管理工具（Seerr/Requestrr）编排
- Custom Formats 规则体系增强（TRaSH-Guides 社区维护高质量分级规则）
- 局限：无运行时插件加载，扩展需编译；电视剧需 Sonarr，音乐需 Lidarr，各 \*arr 分治

#### 12. 优点
- \*arr 生态成熟稳定，Radarr 是电影管理事实标准，Star 与下载量高
- 自动化链路完整：监控 → 检索 → 下载 → 失败重试 → 导入 → 重命名 → 升级
- Provider 体系设计优雅，UI 自动渲染表单，扩展新源体验好
- 完整 REST API + 文档，便于上下游集成
- 跨平台 + Docker（linuxserver）部署成熟，社区文档（Servarr Wiki）齐全
- Custom Formats 精细质量控制
- 与 Sonarr 共享生态与 UI

#### 13. 缺点
- 同一电影只支持一种版本类型，4K + 1080p 并存需多实例（官方说明）
- 无运行时插件，新增 Provider 需编译发版
- 前端沿用较老 React 栈，部分体验相对 Seerr 略陈旧
- 仅做电影，电视剧/音乐/书籍需配套其他 \*arr，运维多个服务
- 索引器依赖 Prowlarr 等外部工具统一管理较佳
- 中文/国产电影与国内网盘原生支持弱
- 对国内 PT 站点靠 Prowlarr/Jackett 间接

#### 14. 社区评价
- 公认的电影自动化管理标杆，与 Sonarr 并列 \*arr 双核
- Open Collective 有 Backers/Sponsors/Mega Sponsors 多级赞助，财务可持续
- Servarr Wiki 作为 \*arr 系列统一文档站，社区支持活跃（Discord）
- GitHub Issue 主要用于 Bug 与 Feature Request（README 明确）
- osuider 开源日报收录（GPL-3.0、10.6k+ 星量级）
- 过去一年 Issue 平均关闭时间约 6 小时（issues.ecosyste.ms 统计），响应较快

#### 15. 常见 Issue
- 4K + 1080p 多实例配置困惑（官方建议多实例）
- 索引器配置与 Prowlarr 协同问题
- 失败下载重试策略与"卡在队列"问题
- 质量升级误判（特别版识别、硬字幕识别）
- 导入路径/权限问题（Docker volume 权限）
- API 与上游工具（Seerr/Requestrr）版本兼容（如 Sonarr V4+ 语言字段变化）
- Custom Format 规则匹配、多版本/特别版识别、预发布监控误判

#### 16. 未来发展方向
- 持续跟进 .NET LTS（已到 .NET 8）
- 与 Prowlarr（索引器聚合）深度协同，统一索引器管理
- 与 Seerr 等请求管理工具的 API 契约持续对齐
- 质量识别算法迭代（特别版、HDR/DV/Atmos 检测）
- \*arr 系列持续共享内核（Sonarr/Radarr/Lidarr 同架构演进）
- Custom Formats 规则体系增强、PostgreSQL 支持、UI 持续优化

---

### 4. PT-Plugin-Plus（PT 助手 Plus）

仓库：https://github.com/pt-plugins/PT-Plugin-Plus
（Wiki https://github.com/pt-plugins/PT-Plugin-Plus/wiki ；原作者 ronggang，后迁移至 pt-plugins 组织）

#### 可核验指标
- Star 数：约 7.8k（star-history 数据；Fork 约 896）—— **仓库已归档（Public archive，2025-09-01 归档为只读）**
- 最近活跃：归档前最后提交 `f5a2168` 于 2025-08-05（Update README），主分支累计约 2,116 次提交，7 分支、114 标签
- 主语言：JavaScript（浏览器扩展 Web Extension）
- 协议：MIT
- 文档完善度：完善。Wiki 含支持站点列表、FAQ、安装使用说明；社区有大量部署教程
- Issue/PR：Open Issues 约 79
- 注意：官方建议迁移至继任者 **PT-depiler**；基于 Manifest V2，Chrome 139+ 已移除 MV2 支持，需降级或替代浏览器

#### 1. 项目定位
浏览器扩展（Edge/Chrome/Firefox Web Extension），辅助下载 PT（Private Tracker）站种子，在 PT 站点页面提供一键下载、多站聚合搜索、批量操作与下载客户端管理。

#### 2. 解决的问题
多 PT 站点间手动复制种子链接、切换下载客户端繁琐；同资源跨站质量难对比；RSS 订阅灵活性不足；豆瓣/IMDb 影视页面到 PT 资源跳转断裂。

#### 3. 核心功能
- 一键发送种子到下载服务器（Transmission/qBittorrent v4.1+/Deluge/µTorrent/ruTorrent/Flood/Synology Download Station）
- 多站聚合搜索同关键字，按大小/做种/时间排序筛选
- 批量下载当前页所有种子、批量复制下载链接
- 按站点配置不同下载服务器与保存路径（比 RSS 灵活）
- 豆瓣电影/Top250、IMDb 电影/Top250 页面一键搜索 PT 种子
- 站点专属功能（封面模式浏览）、下载历史记录、默认下载器可用空间显示

#### 4. 技术架构
浏览器扩展，`src/background/`（与下载服务器长连接、核心业务）、`src/content/`（网页注入交互元素如下载按钮）、`src/options/`（配置 UI）三大模块；Webpack 构建；Manifest V2（受新版浏览器限制）。

#### 5. 模块划分
background（下载客户端通信与调度）、content（站点页面注入与解析）、options（设置界面）、resource（站点适配规则）、public（manifest 与静态资源）、debug（调试）。

#### 6. 插件机制
本身即插件形态；站点适配通过 `resource/` 下站点规则配置文件扩展（新增站点即加规则文件，如 PR 增加 PTzone 适配）；下载客户端通过配置接入，无运行时插件 SDK。

#### 7. 配置方式
开发者模式加载解压扩展（Chrome/Edge 加载 `public` 或构建后 `dist`；Firefox 临时加载 manifest）；配置入口在插件选项页：下载客户端（地址/端口/认证/默认路径）、站点规则、搜索解决方案。

#### 8. API 设计
无独立 REST API（浏览器扩展形态）；通过浏览器扩展消息机制与下载客户端 Web API（Transmission/qBittorrent 等各自 API）通信；站点适配靠页面 DOM 解析规则。

#### 9. UI 设计
浏览器工具栏弹窗 + 选项页；站点页面注入下载按钮/批量按钮；搜索结果聚合页按站点分类。轻量实用风格。

#### 10. 数据模型
下载客户端配置、站点配置（含 Cookie/Passkey）、保存路径规则、搜索解决方案、下载历史；以扩展存储（localStorage/extension storage）持久化。

#### 11. 扩展能力
站点适配规则文件式扩展（社区贡献站点 PR）；多下载客户端协议适配；豆瓣/IMDb 页面注入扩展；但已归档，新增能力需迁移 PT-depiler。

#### 12. 优点
PT 下载场景效率神器、多站聚合搜索与一键下载体验好、豆瓣/IMDb 联动贴近找片流程、配置灵活（按站点分流下载器/路径）、MIT 协议；覆盖了任务候选方向中的"PT/BT 自动订阅/下载工具"。

#### 13. 缺点
**已归档停止维护**；Manifest V2 与新版浏览器（Chrome 139+）不兼容，需降级或迁移 PT-depiler；站点适配随 PT 站改版易失效无人修；浏览器形态无法做后台自动追更（非服务端常驻）。

#### 14. 社区评价
PT 圈经典工具，Star 7.8k；归档后社区仍广泛流传源码部署教程；官方引导迁移 PT-depiler。

#### 15. 常见 Issue
站点改版致解析失效、MV2 浏览器兼容、未配置站点送种出错、Firefox 临时加载不持久、Cookie/Passkey 失效、下载客户端连接失败。

#### 16. 未来发展方向
**无后续发展**（已归档）。路线由继任者 PT-depiler 接续（推测向 Manifest V3、现代化前端迁移）。对 115 Media Hub 的启示：PT 种子自动下载/多站聚合搜索是高频诉求，但浏览器扩展形态与服务端面板互补——服务端可借鉴其"多站聚合搜索 + 按站点分流下载器/路径"的交互思路。

---

## 类目三：影视刮削 / 元数据管理类

> 调研对象：影视刮削 / 元数据管理 / NFO 生成 / TMDB 集成类开源项目。
> 说明：tinyMediaManager 源码托管于 GitLab，GitHub 上仅有 Pages 占位仓库，故该项目以 GitLab 为权威来源、GitHub Star 标注"信息不足"。

---

### 1. tinyMediaManager

仓库（权威源，GitLab）：https://gitlab.com/tinyMediaManager/tinyMediaManager
GitHub 组织（仅 Pages 占位）：https://github.com/tinymediamanager/tinymediamanager
官网 / 文档：https://www.tinymediamanager.org ｜ https://www.tinymediamanager.org/docs/

#### 可核验指标
- Star 数：信息不足（GitHub 仅 Pages 占位仓库，3 commits、最近提交 2020-12-18；社区规模需以 GitLab 为准）
- Fork 数：信息不足（同上，GitHub 占位仓库无参考价值）
- 累计提交：约 1.2 万 commits（来源：第三方统计聚合站 mygit.top / repos.ecosyste.ms，非官方实时，仅作量级参考）
- 最近活跃：持续活跃；当前主版本 v5，AUR 包 `tinymediamanager-bin 5.2.12-1` 最近更新于 2026-05-14
- 默认分支：`devel`（GitLab）
- 主语言：Java（Swing GUI），Maven 构建
- 开源协议：Apache-2.0
- 贡献者：约 150+（第三方聚合统计，量级参考）
- 代码规模：约 26 万行（第三方聚合统计，量级参考）
- 文档完善度：完善（tinymediamanager.org/docs/ 覆盖安装/刮削器/模板/脚本，含截图、changelog、nightly 构建）

#### 1. 项目定位
tinyMediaManager（TMM）是一款全功能（full-featured）的本地媒体库管理器，定位为"为 Kodi（原 XBMC）、Plex、MediaPortal、Emby、Jellyfin 及其他兼容媒体中心整理与清理媒体库"的刮削与元数据编辑工具。作为纯 Java 应用，跨平台运行于 Windows / Linux / macOS。它是影视刮削领域历史最久、覆盖面最广的桌面端"事实标准"之一，常被作为同类工具的对照基线。

#### 2. 解决的问题
媒体文件散落在磁盘各处、命名混乱、缺少元数据与封面，导致媒体中心无法正确识别与展示。TMM 把"识别 → 刮削 → 编辑 → 重命名 → 生成 NFO → 下载海报/剧照/预告片/字幕"整合为单一桌面流程，并允许用户对任意元数据字段手工修正，弥补全自动刮削器识别不准时的可干预空间。

#### 3. 核心功能
- 元数据刮削器：IMDb、TheMovieDb（TMDb）、TVDb、OFDb、Moviemeter、Trakt 等；v4.2+ 支持第三方刮削器插件。
- 海报/剧照下载器：TheMovieDb、TVDb、FanArt.tv。
- 预告片下载：TheMovieDb、HD-Trailers.net。
- 字幕下载：OpenSubtitles.org。
- 手工编辑任意元数据字段。
- 按用户自定义格式自动重命名文件（基于 JMTE 模板引擎）。
- 自定义过滤器与排序的强大搜索。
- 自动生成 `.nfo` 文件，被 Kodi 与多数媒体中心原生识别。
- 从媒体文件提取技术元数据（编码、时长、分辨率）。
- 电影集合（Movie Sets）分组及集合专属海报。
- 任意文件组织方式导入电视剧集。
- 同时提供 GUI 与命令行（CLI）界面，支持无人值守批量刮削。
- 自动更新（release / pre-release / nightly 三通道，应用内自动更新）。

#### 4. 技术架构
Java 单体桌面应用，GUI 基于 Swing；构建工具为 Apache Maven（`mvn -P dist clean package`）。元数据与媒体信息持久化为本地 `.nfo`（XML）文件，图片/海报落到本地资源目录。构建依赖 GitHub Packages（需在 `~/.m2/settings.xml` 配置 GitHub 访问令牌拉取部分依赖）。官方声明使用 GitHub Copilot 等 AI 辅助开发，但所有生成代码经人工评审与整合。

#### 5. 模块划分
GitLab 仓库按 Maven 多模块组织，覆盖电影（movies）、电视剧（tv shows）、音乐会（concerts）、音乐（music）等媒体类型；刮削器（scrapers）以独立 addon 形式存在；模板引擎（JMTE）负责重命名与 NFO 输出格式；GUI / CLI 为两种入口共享同一业务核心；存在 HTTP API 模块用于对外暴露刮削能力（便于被面板类应用集成）。PR 需基于 `devel` 分支提交。

#### 6. 插件机制
v4.2 起引入第三方刮削器 addon（基于 Java SPI 机制），定义 `IMovieMetadataProvider`、`IMovieArtworkProvider` 等接口供外部实现。社区已有第三方插件示例（如针对特定内容源的 scraper addon）。刮削器可独立于主程序更新，是 TMM 长期可扩展的关键设计。

#### 7. 配置方式
GUI 内可视化配置为主：刮削器启用/优先级、元数据源、重命名模板（JMTE）、NFO 输出格式、图片尺寸与命名、字幕语言、代理设置等。配置与数据库存放在用户数据目录；CLI 模式通过参数与配置文件驱动批量任务。多数据源可叠加（如 TMDb 取主元数据、IMDb 取评分）。

#### 8. API 设计
提供 HTTP API（对外暴露刮削/重命名能力），可被其他面板类应用或脚本调用，用于把 TMM 作为"刮削后端"。CLI 亦是一种"API"——可被定时任务/容器编排无人值守调用。具体端点文档以官方 docs 站为准。

#### 9. UI 设计
传统 Swing 桌面 GUI：左侧媒体类型导航树、中间列表/网格、右侧详情与编辑面板、底部进度与日志。重功能、轻装饰，信息密度高，适合深度编辑场景。v5 截图显示界面较 v4 有现代化调整。无 Web UI（需通过 Docker + VNC 5900 端口在容器中运行 GUI）。

#### 10. 数据模型
以媒体条目（电影/剧集/集/音乐会/音乐）为核心实体，包含标题、原始标题、年份、评分、剧情、演员、类型、制片厂、集合、文件路径等字段；元数据落地为 Kodi 兼容的 `.nfo`（XML）格式，海报/剧照为同名图片文件；技术元数据（编码、分辨率、时长）单独提取并写入 NFO 对应标签。

#### 11. 扩展能力
- 第三方刮削器 SPI 插件是主要扩展点，可新增数据源而不改主程序。
- 重命名与 NFO 输出格式完全模板化（JMTE），可适配任意命名规范。
- CLI + HTTP API 使其可作为后端被面板应用编排。
- 跨平台 + Docker（社区维护的 v5 Docker 镜像如 `dzhuang/tinymediamanager5-docker`）扩展部署形态。

#### 12. 优点
- 历史悠久、生态成熟，覆盖电影/电视剧/音乐会/音乐全品类。
- 刮削源丰富且可插拔，支持多源叠加与人工修正。
- GUI + CLI 双形态，既适合交互式整理也适合自动化批处理。
- 模板化重命名与 NFO 输出灵活度极高。
- Apache-2.0 协议对二次集成友好；持续活跃（2026 仍在更新 v5）。

#### 13. 缺点
- 源码在 GitLab 而非 GitHub，对以 GitHub 为中心的国内开发者社区可见度/Star 口碑偏弱。
- 基于 Swing 的 GUI 较为"传统"，无原生 Web UI，容器化需 VNC。
- v4 起部分功能/构建依赖 GitHub Packages 令牌，构建门槛略高。
- 对中文刮削（豆瓣等）无原生支持，需第三方插件。
- Swing 跨平台但在高 DPI / 新 macOS 上偶有渲染问题。

#### 14. 社区评价
被广泛视为桌面端刮削的"老牌标杆"，常出现在 Kodi/Plex/Emby/Jellyfin 社区的"如何整理媒体库"教程中；因 GUI 重、上手略陡，新用户更倾向 Web 化方案（如 MoviePilot），但重度整理与精细修正场景仍首选 TMM。第三方 Docker 封装（romancin、dzhuang 等）反映社区需求旺盛。

#### 15. 常见 Issue
- 刮削源 API 变更或限流导致识别失败（TMDb/TVDb 接口变动）。
- 中文影片命名识别与中文元数据缺失。
- 高 DPI / macOS 新版本渲染与字体问题。
- Docker 容器内运行 GUI 需 VNC，配置较繁琐。
- Maven 构建因 GitHub Packages 令牌缺失而失败。

#### 16. 未来发展方向
持续向 v5 演进（模板引擎、刮削器 SPI、自动更新通道已就位）；AI 辅助开发提升迭代速度；更完善的第三方刮削器生态；与 Web 化面板（Emby/Jellyfin/Plex）的集成更紧密。对本项目（115 Media Hub）的启示：TMM 的"模板化重命名 + NFO 输出 + 刮削器 SPI"三件套是值得借鉴的事实标准。

---

### 2. MediaElch（Komet/MediaElch）

仓库：https://github.com/Komet/MediaElch
官方文档：https://mediaelch.github.io/mediaelch-doc/about.html ｜ 博客 https://mediaelch.github.io/mediaelch-blog/posts/

#### 可核验指标
- Star 数：≈ 1,078（GitHub API，2026-07-10 精确值）| Fork 数：119 | Open Issues：307
- 累计提交：约 3,863 commits（OpenHub 统计）
- 最近 commit：2026-06-18（`f97abde`，作者 Andre Meyering，"refactor: constructor-inject persistence classes"）
- 创建时间：2012-03-04
- 主语言：C++（基于 Qt；GitHub 识别主语言为 C++）
- 开源协议：LGPL-3.0
- 代码规模：约 43 万行（OpenHub）；Coverity Scan 统计约 61.8 万行、缺陷密度 0.75
- 文档完善度：完善（mediaelch.github.io/mediaelch-doc/，覆盖下载/构建/使用/贡献；活跃于 Kodi 论坛）

#### 1. 项目定位
MediaElch 定位为面向 Kodi（亦兼容其他媒体中心）的本地媒体管理器，核心是"为电影/电视剧/音乐会/音乐生成与编辑 NFO 元数据、自动下载 fanart 海报"。与 TMM 同属桌面端老牌刮削器，但以 C++/Qt 实现、原生跨平台，强调轻量与原生体验。

#### 2. 解决的问题
媒体库缺 NFO/海报导致媒体中心展示不全或识别错误。MediaElch 提供可视化刮削与编辑界面，从 TheMovieDb、IMDb、Fanart.tv 等拉取元数据与图片并落地为 Kodi 友好的 NFO + 图片，弥补全自动刮削器在德语/欧洲内容与精细编辑上的不足（项目有较强德语社区背景，支持 fernsehserien.de、Videobuster 等欧洲源）。

#### 3. 核心功能
- 支持电影、电视剧、音乐会、音乐四类媒体的元数据管理。
- 刮削器：The Movie DB、IMDb、Videobuster、TVMaze、fernsehserien.de、Fanart.tv（海报/剧照）。
- 自动下载 fanart 与海报，落地为 NFO + 同名图片。
- 手工编辑任意元数据字段。
- 文件重命名与目录整理。
- 从媒体文件提取技术元数据（借助 MediaInfo/MediaInfoLib、ZenLib）。
- 截图生成（借助外部 ffmpeg）。
- 多语言界面（Transifex 协作翻译）。

#### 4. 技术架构
C++ 单体桌面应用，基于 Qt（构建从 QMake 迁移到 CMake，当前支持 Qt 6，文档示例仍含 Qt 5.15.2 路径）；依赖 MediaInfo（DLL）、MediaInfoLib、ZenLib、QuaZip（git submodule）。CI 通过 GitHub Actions + Docker（MXE 交叉编译 Windows、clang 19 格式化）构建多平台产物；Coverity Scan 持续静态扫描，缺陷密度约 0.75。

#### 5. 模块划分
仓库目录分层清晰：`src/`（核心 C++ 实现，含 scraper、movies/tvshows/concerts/music 模块、导出/重命名）、`test/`（单元测试）、`data/`（数据与界面资源、i18n 翻译）、`cmake/`、`scripts/`、`docs/`（开发者文档）、`third_party/`（子模块依赖）、`.ci/`（CI 配置）。`MediaElch.pro` / `CMakeLists.txt` 双构建入口，`CMakePresets.json` 含 memory sanitizer 等预设。

#### 6. 插件机制
不像 TMM 那样提供正式 SPI 刮削器插件接口；刮削器以 C++ 类内置实现于 `src/scrapers/`，新增数据源需改源码并重新编译。扩展性主要体现为"刮削器列表内置可配置启用/优先级"，而非运行时插件。这是相对 TMM 的明显短板。

#### 7. 配置方式
GUI 内可视化配置：刮削器选择与启用、元数据字段映射、图片下载策略、重命名规则、代理、界面语言。配置存于用户目录的设置文件。构建侧通过 CMake 选项与 CMakePresets 控制（如 sanitizer、平台）。

#### 8. API 设计
无对外 HTTP API（纯桌面应用）。对外能力主要通过"命令行参数 + 导出/导入 NFO"间接暴露，便于脚本化批处理，但不像 TMM 那样提供 HTTP API 供面板集成。

#### 9. UI 设计
Qt 原生桌面 GUI，左侧导航、中部列表/网格、右侧详情编辑。原生控件体验优于 Swing，高 DPI 支持更好；近期重构移除了 QML/QtQuick（`refactor: Remove usage of QML and QtQuick`），回归 Qt Widgets，降低复杂度。整体偏功能型，设计投入中等。

#### 10. 数据模型
以电影/剧集/集/音乐会/音乐/专辑/艺术家为实体，字段含标题、原始标题、年份、评分、剧情、演员、类型、制片厂、标签、文件路径等；元数据落地为 Kodi 兼容 NFO（XML），图片为同名 fanart/poster。技术元数据（MediaInfo）单独存储。提供导出功能（如 HTML 导出）。

#### 11. 扩展能力
- 刮削器为内置 C++ 实现，扩展需改源码（门槛较高）。
- 重命名规则可配置但非模板引擎，灵活度低于 TMM 的 JMTE。
- 可作为 NFO 生成与编辑的"前端工具"被脚本调用。
- CI/静态分析（Coverity、clang-tidy、cspell、cmake-format）工程化程度高，便于贡献者参与。

#### 12. 优点
- C++/Qt 原生跨平台，性能与体验优于 Java Swing。
- 覆盖电影/电视剧/音乐会/音乐四类，欧洲内容源（fernsehserien.de、Videobuster）丰富。
- 工程质量高：Coverity 缺陷密度低、clang-tidy、单元测试、CI 多平台构建。
- LGPL 协议友好；持续活跃（2026-06 仍有提交）。
- 文档与构建指南完善，对贡献者友好。

#### 13. 缺点
- 无运行时刮削器插件机制，新增数据源需改源码重编译。
- 无对外 HTTP API / 无 Web UI，难以作为后端被面板应用集成。
- Star 体量（约 1.1k）小于 MoviePilot/TMM 量级，中文社区认知度一般。
- 无原生中文刮削源（豆瓣等）。
- Qt 依赖使构建对普通用户略复杂（需 Qt 安装器与子模块）。

#### 14. 社区评价
在 Kodi 社区与德语/欧洲用户中口碑稳固，被视为 TMM 的轻量原生替代；OpenHub 显示近 12 个月约 75 commits（同比降 47%）、9 贡献者（同比增 80%），呈"小而稳"的成熟维护状态。主要维护者 bugwelle 持续投入，社区以 issue 反馈与翻译贡献为主。

#### 15. 常见 Issue
- 刮削源 API 变动或限流导致识别失败（TMDb、IMDb 页面结构变化）。
- Qt 6 升级带来的构建/依赖问题（如 libqt6svg6 依赖）。
- HDR10 等技术元数据检测 bug（近期修复 `fix: HDR10 detection for media files`）。
- 翻译与多语言相关 issue。
- macOS/Windows 构建环境配置问题。

#### 16. 未来发展方向
继续 Qt 6 迁移与代码现代化（移除 QML/QtQuick、constructor-inject 持久化类便于测试）；强化静态分析与测试覆盖；完善技术元数据检测（HDR10 等）。对本项目的启示：MediaElch 的"高质量工程实践 + 原生 NFO 输出"值得借鉴，但其"无插件/无 API"的封闭性正是本项目可超越的方向（以 API + 插件化刮削为核心差异化）。

---

### 3. jellyfin-plugin-metashark（cxfksword/jellyfin-plugin-metashark）

仓库：https://github.com/cxfksword/jellyfin-plugin-metashark

#### 可核验指标
- Star 数：≈ 2,088（GitHub API，2026-07-10 精确值）| Fork 数：95 | Open Issues：3
- 累计提交：约 206-217 commits
- 最近 commit：2026-05-19（`5f90775`，作者 cxfksword，"chore: add isAnime property to parse result"）| 最近 push：2026-05-19
- 创建时间：2022-10-25 | 默认分支：`main`
- 主语言：C#（约 95.7%）+ HTML（约 3.8%）+ Python（约 0.5%）
- 开源协议：GPL-3.0
- 最新版本：v2.3.4（2026-05-19）
- 构建要求：.NET Core SDK 9.0
- 兼容性：Jellyfin 10.9.x / 10.10.x
- 文档完善度：较完善（README 含安装、配置、防封禁、图片代理说明；以 Jellyfin 插件配置页为交互入口）

#### 1. 项目定位
jellyfin-plugin-metashark 是一款 Jellyfin 媒体服务器插件，定位为"用豆瓣 + TMDB 元数据为 Jellyfin 刮削影片"，专为中文用户解决 Jellyfin 原生刮削器对中文影片识别差、缺豆瓣评分/简介的问题。它以 Jellyfin 插件机制分发，安装即用，是 Jellyfin 中文生态中 Star 最高的刮削插件之一。

#### 2. 解决的问题
Jellyfin 默认刮削源（TMDb/TheMovieDb）对国产/华语影片的中文标题、剧情简介、豆瓣评分支持不足；豆瓣无开放 API，直接抓取易被 IP 封禁。metashark 通过"豆瓣抓取 + TMDB 补全 + 防封禁策略 + AnitomySharp 动漫命名解析"组合，在 Jellyfin 内提供高质量中文元数据，并规避豆瓣反爬。

#### 3. 核心功能
- 豆瓣元数据抓取：影片标题、剧情、演员、评分等。
- TMDB 元数据补全与交叉。
- AnitomySharp 动漫命名解析（自动识别番剧的剧集/季/集信息）。
- `isAnime` 属性标记（最新提交新增），便于动漫特殊处理。
- 防封禁功能：避免豆瓣 IP 封禁（请求节流/代理策略）。
- 图片代理配置：海报/剧照通过代理拉取，规避直连限制。
- 作为 Jellyfin 插件，复用 Jellyfin 刮削流程与配置体系。

#### 4. 技术架构
C# / .NET 插件，遵循 Jellyfin 插件规范（实现 Jellyfin 的元数据提供者接口）。构建需 .NET Core SDK 9.0。HTML 用于插件配置页（Jellyfin 插件配置 UI）。少量 Python（约 0.5%，可能为辅助脚本/数据生成）。打包为 Jellyfin 可识别的插件产物，通过 Jellyfin 插件仓库或手动安装。

#### 5. 模块划分
作为单一插件项目，模块围绕 Jellyfin 插件接口组织：元数据提供者（MetadataProvider）实现、豆瓣抓取器、TMDB 抓取器、AnitomySharp 命名解析适配、防封禁/限流策略、图片代理、配置页（HTML）。仓庘认为单一 DLL 产物，结构聚焦。

#### 6. 插件机制
本项目本身就是"插件"——它就是 Jellyfin 插件机制的产物，实现 Jellyfin 的元数据提供者 SPI。因此其"插件机制"= Jellyfin 插件 SPI。它不提供自身的二级插件扩展（不是平台，是插件）。

#### 7. 配置方式
通过 Jellyfin 插件配置页（HTML）可视化配置：启用刮削源、豆瓣/TMDB 参数、防封禁策略、图片代理、动漫识别开关。配置存于 Jellyfin 插件配置体系，随 Jellyfin 实例持久化。

#### 8. API 设计
不暴露独立 API——作为 Jellyfin 插件，其能力通过 Jellyfin 刮削流程被调用（Jellyfin 在扫描媒体时调用插件的元数据提供者接口）。对外交互面是 Jellyfin 本身的 API + 插件配置页。

#### 9. UI 设计
无独立 UI——复用 Jellyfin 插件配置页（标准 Jellyfin Web UI 的一部分）。用户在 Jellyfin 设置 → 插件中配置 metashark。设计遵循 Jellyfin 插件 UI 规范，体验取决于 Jellyfin 本体。

#### 10. 数据模型
复用 Jellyfin 的媒体元数据模型（影片/剧集/集，含标题、剧情、演员、评分、图片等字段），插件职责是"填充"这些字段。豆瓣与 TMDB 数据映射到 Jellyfin 元数据字段；动漫解析结果（季/集）映射到剧集结构。

#### 11. 扩展能力
- 扩展面较窄（是插件而非平台），新增数据源需改插件源码。
- 防封禁策略与图片代理可配置，适配不同网络环境。
- AnitomySharp 解析可复用于其他动漫命名场景。
- 依赖 Jellyfin 插件生态分发与版本兼容（10.9.x / 10.10.x）。

#### 12. 优点
- 填补 Jellyfin 中文刮削空白，豆瓣 + TMDB 组合质量高。
- AnitomySharp 动漫命名解析，番剧识别准确。
- 防封禁 + 图片代理设计贴合国内网络现实。
- 作为 Jellyfin 插件安装即用，零额外部署成本。
- Star 2,088、Open Issues 仅 3，维护质量与稳定性好；v2.3.4（2026-05）仍活跃。

#### 13. 缺点
- 强绑定 Jellyfin，无法独立用于其他媒体服务器或面板。
- 依赖豆瓣非公开抓取，站点改版或加强反爬即失效（长期脆弱性）。
- 扩展性有限，新增数据源需改源码重编译。
- 仅做"刮削"不做"重命名/整理/订阅"，非全功能工具。
- .NET 9.0 SDK 构建要求对自编译用户略高。

#### 14. 社区评价
Jellyfin 中文社区高度认可，几乎是"Jellyfin 中文刮削"的事实首选；Open Issues 仅 3、Star 持续增长，反映用户满意度与稳定性。与 MoviePilot 的豆瓣刮削常被并列为中文刮削两大方案。争议主要在豆瓣反爬的长期可持续性。

#### 15. 常见 Issue
- 豆瓣反爬/限流导致抓取失败（核心痛点）。
- 豆瓣页面结构变动导致解析失效。
- 动漫命名识别边界 case（AnitomySharp 解析不准）。
- Jellyfin 版本兼容（10.9 vs 10.10 升级问题）。
- 图片代理配置不当导致海报缺失。

#### 16. 未来发展方向
跟进 Jellyfin 版本兼容（10.10+）；强化豆瓣防封禁与代理；完善动漫解析（`isAnime` 等属性）。对本项目的启示：metashark 的"豆瓣 + TMDB 双源 + 防封禁 + 动漫命名解析"组合，是本项目刮削模块可直借的中文刮削方案——尤其在"豆瓣抓取防封禁"这一工程难点上，metashark 的实践可作为直接参照（本项目刮削管理亦涉及 TMDB 识别绑定，可对照其豆瓣补全与防封禁策略）。

---

## 类目四：网盘资源搜索 / 转存类

> 调研对象：网盘资源搜索 / 转存类项目。

---

### 1. PanSou（fish2018/pansou）

仓库：https://github.com/fish2018/pansou

#### 可核验指标
- Star 数：≈ 13,805 | Fork 数：3,303 | 累计提交：245 commits
- 最近 push：2026-06-14 | 创建时间：2025-07-10
- 主语言：Go | 开源协议：MIT | Open Issues：10
- 文档完善度：较完善（README + docs/ 目录，含插件开发指南）

#### 1. 项目定位
高性能的网盘资源搜索 API 服务，主打"搜索"环节而非转存。README 明确声明"仅供学习研究，请勿以各种形式用于盈利目的"。通过聚合 Telegram 频道与自定义插件，对外提供 RESTful 搜索接口，docker 集成前后端一键启动、开箱即用。

#### 2. 解决的问题
网盘资源分散在各大 TG 频道与小众搜索站，用户需逐站翻找且难以并发检索。PanSou 把"多频道并发搜索 + 智能排序 + 网盘类型自动分类"封装成统一 API，供个人或上层应用（如媒体面板、IM 机器人）调用。

#### 3. 核心功能
- 多频道并发搜索（Go 协程 + 工作池）。
- 异步插件系统：先返回结果再持续补充，已内置 quarktv、dyyjpro、gaoqing888、panyq、xuexizhinan 等插件。
- 自动识别 13 类网盘链接：百度、阿里、夸克、天翼、UC、移动云盘、115、PikPak、迅雷、123、磁力、电驴、其他。
- 多维度智能排序（时间新鲜度 0.3、关键词匹配 0.3、来源可靠性 0.2、资源完整性 0.1、用户反馈 0.1）。
- 二级缓存（内存 LRU + 磁盘分片），降低重复查询延迟。
- MCP（Model Context Protocol）集成，可作为 AI 工具被模型调用。
- 提供 Web 前端（ghcr.io/fish2018/pansou-web 镜像），可在浏览器直接搜索。

#### 4. 技术架构
Go 语言单服务，Gin 框架提供 RESTful API 与中间件。并发模型基于 goroutine + worker pool；缓存层为内存 LRU + 磁盘分片存储，写入策略支持 hybrid 模式。前后端打包进同一 Docker 镜像，由 GitHub Actions 自动构建并推送 ghcr.io。

#### 5. 模块划分
仓库目录体现清晰分层：`api/`（HTTP 接口与中间件）、`config/`（配置项）、`model/`（数据结构与 ext 自定义扩展参数）、`plugin/`（异步搜索插件实现）、`service/`（业务编排与排序）、`util/`（TG 频道链接匹配等工具）、`docs/`（含《插件开发指南.md》）、`.github/workflows/`（CI 构建）。

#### 6. 插件机制
提供接口规范，支持异步插件：插件可在主响应返回后继续追加结果。文档 `docs/插件开发指南.md` 描述开发规范，仓库内置多个示例插件可作模板。插件支持自定义 `ext` 扩展参数透传，可控制插件超时（`PLUGIN_TIMEOUT`）与等级（参与排序权重）。

#### 7. 配置方式
环境变量为主：`PORT`、`CHANNELS`（默认搜索频道）、`PROXY`（SOCKS5 代理访问 TG）、`CONCURRENCY`、`CACHE_TTL`、`CACHE_MAX_SIZE`、`CACHE_PATH`、`SHARD_COUNT`、`CACHE_WRITE_STRATEGY`、`ASYNC_RESPONSE_TIMEOUT` 等。同时提供 `docker-compose.yml` 模板，支持 volume 持久化 cache 与 data。

#### 8. API 设计
RESTful 风格：搜索 API（关键词、频道过滤、网盘类型过滤、分页）、`/api/health` 健康检查、`/api/status` 配置与性能监控。支持"快速响应超时"（ASYNC_RESPONSE_TIMEOUT，默认 4s）实现异步流式补充。接口对 MCP 协议友好，可作为 LLM 工具被调用。

#### 9. UI 设计
提供 pansou-web 前端镜像，浏览器输入关键词即可搜索，结果按网盘类型分类展示，并提供状态页查看配置与性能指标。UI 偏功能型，非重度设计投入。

#### 10. 数据模型
核心模型为"搜索结果条目"，含网盘类型、链接、提取码、标题、发布时间、来源频道/插件、插件等级等字段；`ext` 字段支持自定义扩展参数透传。缓存以查询关键词为 key、结果列表为 value，分片存储。

#### 11. 扩展能力
- 插件系统是主要扩展点，可新增网盘源或聚合站。
- MCP 集成使其能被 AI Agent 复用。
- 环境变量驱动的代理、并发、缓存参数可适配不同部署规模。
- 二级缓存分片数可调，便于横向扩展。

#### 12. 优点
- 性能取向明确，Go + 并发 + 二级缓存，查询延迟低。
- Star 增长极快（2025-07 创建，一年内即破 1.38 万），社区关注度高。
- 插件机制开放，已内置多源，可自助扩展。
- 部署门槛低，单镜像一键启动。
- 同时提供 API 与 Web 前端，覆盖开发者与普通用户。

#### 13. 缺点
- 仅做"搜索"不做"转存"，需配合转存工具形成完整链路。
- 强依赖 Telegram 频道作为主源，TG 访问需代理，国内部署有门槛。
- 文档虽完善但部分高级特性（如机器学习排序优化）README 中提及但仓库未见对应实现，疑似规划项。
- 默认频道清单需自行从社区渠道获取并批量导入。

#### 14. 社区评价
飞牛 NAS、什么值得买、CSDN 等社区均有部署教程，普遍评价"搜索速度快、能搜到磁链内容、基本满足家用"。常见吐槽集中在 TG 频道搜索需配置代理、个别资源链接失效需多翻几个源。HelloGitHub/掘金等平台将其与 aipan 并列为网盘搜索首选方案。

#### 15. 常见 Issue
- TG 频道搜索无结果（多因代理未配置或代理失效）。
- 外网无法访问（端口映射/反代配置问题）。
- 缓存膨胀需定期清理。
- 插件源失效（频道改版或被封）。
- 资源链接打开后丢失（频道方下架，非程序问题）。

#### 16. 未来发展方向
- 持续新增搜索插件（近期已新增 quarktv、dyyjpro、gaoqing888 等）。
- MCP 协议集成深化，对接更多 AI Agent。
- 机器学习排序权重优化（README 已列入规划）。
- 缓存层重构（近期 commit "移除旧的二级缓存实现" 暗示架构演进）。

---

### 2. CloudSaver（jiangrui1994/CloudSaver）

仓库：https://github.com/jiangrui1994/CloudSaver

#### 可核验指标
- Star 数：≈ 9.1K | Fork 数：765 | 累计提交：125 commits
- 最近 commit：2026-04-20（Update README.md）
- 主语言：Vue / TypeScript（前端）+ Node.js/Express（后端）
- 开源协议：MIT（历史版本；最新版已转闭源仅 Docker 部署）
- Open Issues：44
- 文档完善度：较完善（README + 语雀更新日志 + Wiki + DeepWiki 自动索引）

#### 1. 项目定位
基于 Vue 3 + Express 的"网盘资源搜索 + 一键转存"一体化平台，主打"搜转一体"。强调私有化部署、全程数据闭环，官方明确不提供在线服务或 Demo。

#### 2. 解决的问题
找资源（分散在 TG 频道、订阅源、豆瓣榜单）与转存（需复制链接、登录网盘、选文件夹、确认）割裂，用户在多个网盘与频道间反复横跳。CloudSaver 把"搜索 → 识别网盘 → 一键转存到指定文件夹"压成单次点击。

#### 3. 核心功能
- 多源资源搜索：聚合多个资源订阅源，支持关键词搜索与资源链接解析。
- 豆瓣热门榜单展示，快速发现影视资源。
- 网盘转存：支持 115、夸克、天翼、123 云盘一键转存，可选目标文件夹。
- 多用户系统：注册登录，区分管理员（注册码 230713）与普通用户（注册码 9527）。
- 响应式设计：PC 端 Element Plus、移动端 Vant，自适应布局。
- 搜索频道批量导入（从社区配置代码一键粘贴）。

#### 4. 技术架构
前后端分离的 monorepo。前端 Vue 3 + TypeScript + Vite + Pinia + Vue Router；后端 Node.js + Express + TypeScript，采用 controller-service 架构与 Inversify 依赖注入。数据库 SQLite3（Sequelize ORM）。实时通信用 Socket.io。CI 用 GitHub Actions，部署用 Docker（镜像 jiangrui1994/cloudsaver，latest 稳定 / test 测试双标签）。

#### 5. 模块划分
前端 `frontend/src/` 下分 `components`、`views`、`stores`（Pinia）、`router`、`layouts`（PC/Mobile）、`api`、`assets`。后端 `backend/src/` 下分 `controllers`、`services`、`routes`、`models`、`core`、`database`。根目录提供 `pnpm dev / build / build:frontend / build:backend / start` 等脚本统一编排。

#### 6. 插件机制
无明显代码级插件系统。扩展方式偏"配置驱动"：通过批量导入搜索频道订阅源来扩充资源池，而非代码插件。近期 commit "去除内置源" 暗示源由用户自管理，避免内置源维护负担与合规风险。后端 service 层有清晰分层，可二次开发新增网盘适配。

#### 7. 配置方式
后端 `.env` 文件（参考 `.env.example`），核心项含 `JWT_SECRET`、`TELEGRAM_BASE_URL`。Docker 部署需挂载 `/app/data`（数据）与 `/app/config`（配置）两个卷，端口默认 8008。注册码在管理后台可修改以增强安全性。

#### 8. API 设计
后端 `routes/api.ts` 定义 RESTful 路由，按 controller-service 分层。涵盖搜索、转存、网盘账号绑定（Cookie 管理）、用户与权限、频道订阅导入等。前端通过 `api` 客户端服务统一调用。

#### 9. UI 设计
设计投入相对较多：PC 用 Element Plus、移动用 Vant，登录/注册、最新资源、关键词搜索、热门榜单、转存、系统设置多视图。界面简洁，社区评价"比同类好看"。近期 commit "去除悬浮效果" 显示有持续视觉打磨。

#### 10. 数据模型
- 用户模型：账号、密码哈希、角色（admin/user）、注册码校验。
- 网盘账号模型：网盘类型、Cookie/凭证。
- 资源模型：来源频道、标题、链接、网盘类型识别、提取码、时间。
- 转存任务：源分享、目标文件夹、状态。
基于 SQLite3 + Sequelize，模型集中在 `backend/src/models` 与 `database`。

#### 11. 扩展能力
- 通过频道订阅批量导入扩充搜索源。
- 网盘适配在 service 层新增适配器即可（已有 115/夸克/天翼/123 四家）。
- 推送插件有独立 Wiki 配置说明，可对接通知渠道。
- 多用户 + 权限模型支持小型团队/家庭共享。

#### 12. 优点
- "搜转一体"闭环体验好，单次点击完成转存。
- 前后端分离 + TypeScript，工程化程度高，易于二次开发。
- 响应式 UI 覆盖移动端，体验完整。
- Docker 一键部署，门槛低。
- Star 高（≈9.1k）、社区教程丰富（什么值得买、B 站、掘金均有）。

#### 13. 缺点
- **最新版本已闭源，仅 Docker 部署**（社区评论明确指出），二次开发需基于历史开源版本。
- 需用户提供各网盘 Cookie，等同于网盘账号密码，安全责任重；官方反复强调"切勿使用他人部署版本"。
- 仅支持 115/夸克/天翼/123 四家转存，未覆盖阿里云盘、UC、PikPak 等。
- 无自动定时转存/追更能力（需配合 quark-auto-save 等工具补足）。
- Issues 较多（44 个），维护响应节奏一般。

#### 14. 社区评价
HelloGitHub 评分 10.0，被收录于第 108 期。社区评价"开箱即用、又快又好用"。最显著的争议是闭源转向——最新版本不开源引发用户担忧，部分用户转回历史开源版本 fork。

#### 15. 常见 Issue
- 代理配置后仍无法搜索 TG 内容。
- 115/夸克 Cookie 失效导致转存失败。
- 注册码遗忘无法登录管理员。
- 内置源被去除后不知去哪找频道配置。
- 外网访问/反代配置问题。

#### 16. 未来发展方向
- 闭源后聚焦 Docker 镜像迭代，源管理交由社区。
- 可能新增更多网盘适配（用户呼声高的是阿里云盘）。
- 推送插件生态扩展（已有独立配置说明）。
- 与 quark-auto-save、Alist、Emby 等组合形成"搜转存播"全链路。

---

### 3. aliyunpan（tickstep/aliyunpan）

仓库：https://github.com/tickstep/aliyunpan

#### 可核验指标
- Star 数：≈ 5,076 | Fork 数：395 | 累计提交：670 commits
- 最近 push：2026-07-05 | 创建时间：2021-08-04
- 主语言：Go | 开源协议：Apache-2.0 | Open Issues：19
- 文档完善度：完善（README 含完整目录、安装、使用、FAQ、多平台安装方式）

#### 1. 项目定位
阿里云盘命令行客户端，支持 JavaScript 插件与同步备份功能。定位为"开发者/服务器场景下的阿里云盘管理 CLI"，覆盖文件管理、上传下载、WebDAV 服务、双向同步。

#### 2. 解决的问题
阿里云盘官方客户端偏 GUI、不适合服务器与自动化场景；浏览器下载单线程速度慢、无法批量。aliyunpan 提供 CLI + 多线程 + WebDAV + 同步备份，适配 Linux 服务器、NAS、定时任务等无头场景。

#### 3. 核心功能
- 文件操作：ls/cd/mkdir/mv/cp/rm/rename/search/tree/info。
- 多线程上传下载、秒传检测、分片传输、SHA1/MD5 校验、断点续传。
- WebDAV 服务：将阿里云盘挂载为本地/网络磁盘。
- 同步备份：本地与云端双向同步，基于文件哈希比对，支持 sync_drive_config.json 配置。
- JavaScript 插件系统：下载/上传/同步处理器插件，示例齐全。
- 多用户管理：多账号切换。
- 多平台安装：apt/yum/brew/winget/docker/直接下载。
- 切换网盘（备份盘/资源库）。
- VIP 会员推荐码机制。

#### 4. 技术架构
Go 单二进制 CLI，模块化设计。核心组件：PanClient（与阿里云盘 API 通信）、Downloader（多线程下载管理器）、Uploader（分片上传管理器）、SyncManager（双向同步控制器）。配置目录可自定义，支持 systemd 服务化（Linux 自动同步）。

#### 5. 模块划分
仓库目录：`cmder/`（命令行交互层，支持登录例程重构）、`assets/`（资源与示例 sync 配置）、`docker/sync/`（同步容器化）、`.github/ISSUE_TEMPLATE/`（Issue 模板）。代码内部按 PanClient/Downloader/Uploader/SyncManager 分层。2 个分支、41 个 Tag，发布版本管理规范。

#### 6. 插件机制
JavaScript 插件系统是核心扩展点。插件放在 `~/.aliyunpan/plugins`，在配置中启用。官方提供下载处理器、上传处理器、同步处理器三类示例插件。用户可用 JS 自定义文件处理流程（重命名、过滤、转码触发等），无需改 Go 源码。

#### 7. 配置方式
CLI 交互式登录或 `-refresh-token` 登录（Refresh Token 从浏览器 Local Storage 获取）。配置文件自动保存到用户目录。同步功能用 `sync_drive_config.json`（local_dir/remote_dir/sync_mode）。WebDAV 用 `--port` 启动。全局参数可通过 `config set` 调整（download-parallel、block-size 等）。

#### 8. API 设计
命令行 API 为主：`aliyunpan <command> [flags]`，子命令风格（ls/download/upload/sync/webdav/login/user/config）。WebDAV 服务对外暴露标准 WebDAV 协议。内部 PanClient 封装阿里云盘私有 API。无对外 RESTful API（CLI 定位决定）。

#### 9. UI 设计
纯命令行交互，无 GUI。提供进度条、传输速度实时显示、彩色输出。WebDAV 服务可通过文件管理器图形化访问。

#### 10. 数据模型
- 文件/目录：FileID、名称、大小、SHA1、创建/修改时间、是否目录。
- 网盘：DriveID（区分备份盘/资源库）。
- 用户：账号、Refresh Token、当前激活账号。
- 同步任务：local_dir、remote_dir、sync_mode（two_way 等）。
- 下载/上传任务：并发数、分片大小、重试次数、速度限制。

#### 11. 扩展能力
- JavaScript 插件系统，扩展文件处理流程。
- WebDAV 服务可被任何支持 WebDAV 的客户端（文件管理器、Jellyfin/Emby、Alist）挂载复用。
- 多用户 + 多 DriveID 支持复杂账号场景。
- Docker sync 容器化部署，适合 NAS/服务器常驻。
- systemd 集成支持开机自启同步。

#### 12. 优点
- 阿里云盘 CLI 事实标准，Star 5k+、活跃度高（2026-07 仍在更新）。
- 功能完备：文件管理 + 传输 + WebDAV + 同步 + 插件，覆盖个人与企业场景。
- Go 单二进制跨平台，部署极简。
- 文档极完善：README 含完整目录、多平台安装、FAQ、Debug 调试指南。
- Apache-2.0 协议友好，便于商业/衍生项目集成。
- 41 个 Tag 版本管理规范，发布稳定。

#### 13. 缺点
- 仅支持阿里云盘，不跨网盘。
- 强依赖 Refresh Token，过期需重新获取（FAQ 高频问题）。
- 阿里云盘 API 变动可能导致功能失效，需作者跟进（云盘官方限速/限频风险）。
- JS 插件文档深度一般，复杂插件需读源码。
- 无搜索聚合与转存分享链接能力（CLI 定位所致）。

#### 14. 社区评价
GitHub 5k+ Star、Apache-2.0、被多篇 CSDN/gitcode 教程引用为"阿里云盘 Linux 服务器首选方案"。高校实验室（如山西医科大学大数据实验室）官方教程推荐用于服务器文件上传下载。评价"亲测可达带宽上限"。

#### 15. 常见 Issue
- Refresh Token 过期/登录失败。
- 下载速度不达预期（需调整并发与分片参数）。
- 同步冲突与哈希比对异常。
- WebDAV 挂载认证问题。
- 大文件（>4GB）分块上传稳定性。
- Debug 日志开启方法（FAQ 专门说明）。

#### 16. 未来发展方向
- 跟进阿里云盘 API 变更（持续维护，670 commits 显示迭代充分）。
- JS 插件生态丰富（已有下载/上传/同步三类示例）。
- Docker sync 容器化与 systemd 集成深化。
- 多平台安装渠道持续扩展（apt/yum/brew/winget/docker）。
- 可能向更多云盘协议抽象（目前聚焦阿里）。

---

## 类目五：媒体服务器生态工具 / 多语言架构代表项目

> 本调研面向 115 Media Hub 项目，横向选取 GitHub 上不同语言、不同架构形态的同类/相邻开源工具作为参照，重点关注其架构模式、扩展机制与可借鉴的设计思路。
> 语言覆盖：TypeScript(Node.js) / Go / C#(.NET)，满足"至少 2 个非 Python 实现"的要求。

---

### 1. Seerr（原 Overseerr + Jellyseerr 合并）

仓库：https://github.com/seerr-team/seerr
官网 / 文档：https://seerr.dev ｜ https://docs.seerr.dev

#### 可核验指标
- Star 数：11,845 | Fork 数：911 | Open Issues：344
- 主语言：TypeScript（Node.js 22.x 后端 + React 前端）
- 最近 push：2026-07-09（前一日仍活跃）
- License：MIT | 贡献者：190+，本地化语言 25+
- 文档完善度：高（官方文档站 docs.seerr.dev、迁移指南、构建说明齐全）

#### 1. 项目定位
面向家庭/社区共享媒体服务器的**开源媒体请求与发现管理器**，作为 Jellyfin / Plex / Emby 媒体服务器与 Sonarr / Radarr 自动化下载工具之间的"请求中台"。2026-02 由原 Overseerr（sct/overseerr，已 archive）团队与 Jellyseerr（Fallenbagel/jellyseerr）团队合并统一而来，是当前该生态事实上的标准请求管理方案。

#### 2. 解决的问题
家庭/共享 NAS 场景下"成员想看什么 → 管理员手动搜片 → 手动丢给下载器 → 下载完成手动入库"的割裂流程。Seerr 把"发现 → 请求 → 审批 → 转发到 DVR → 入库同步 → 通知"整合为单一 Web 应用，并提供配额、权限、审批工作流，避免每个用户都直接接触 Sonarr/Radarr。

#### 3. 核心功能
- 与 Jellyfin / Plex / Emby 全量集成（认证 + 用户导入 + 媒体库同步扫描）。
- 与 Sonarr / Radarr 双向集成：自动转发请求、选择质量 Profile、监控处理状态、4K 与 1080p 分实例管理。
- 媒体发现：TMDb 浏览热门/即将上映/趋势内容，内嵌推荐。
- 请求系统：按季/按片请求、高级请求（自定义目标文件夹与质量 Profile）、Override Rules（按用户/标签条件覆盖默认请求设置）。
- Watchlist / Blocklist：白名单/黑名单管理，按标签隐藏内容。
- 通知系统：Discord / Slack / Email / Telegram / Pushover / Pushbullet / ntfy.sh / Webhook（支持动态占位符）。
- 多数据库：PostgreSQL 与 SQLite，ORM 使用 TypeORM。
- 权限粒度：每个用户可分配独立功能权限；请求配额（按时间段限制电影/剧集请求数）。
- 移动端友好，可作为 Home Screen PWA 近原生使用。

#### 4. 技术架构
- 后端：Node.js 22.x + TypeScript，单体应用，Express 路由层 + TypeORM 数据访问层。
- 前端：React + TypeScript，使用 `@headlessui/react`、Tailwind，构建产物随包发布。
- 包管理：pnpm（已升级至 v10），构建走 `pnpm build`。
- 部署：官方 Docker 镜像 `ghcr.io/seerr-team/seerr`、Helm Chart（`charts/seerr-chart`，便于 K8s 部署）、systemd / launchd / PM2 多种服务化方式。
- 测试：Cypress 端到端 + 服务端单测（2026-03 起支持服务端单元测试）。
- CI：GitHub Actions，husky 做 git hooks。

#### 5. 模块划分
源码顶层目录反映其模块化：
- `server/`：Node.js 后端（路由、控制器、任务调度、第三方集成适配器）。
- `client/` 或 `src/`：React 前端。
- `config/`：默认配置与 schema。
- `cypress/`：E2E 测试。
- `charts/seerr-chart/`：Helm 部署清单。
- `gen-docs/` / `docs/`：文档与自动文档生成。
- `bin/`：辅助脚本。
按职责可识别出：媒体服务器适配层（Plex/Jellyfin/Emby）、DVR 适配层（Sonarr/Radarr）、元数据提供者层（TMDB/TVDB/AniDB）、通知 agent 层、权限/配额层。

#### 6. 插件机制
**无传统意义上的运行时插件 API**。扩展性体现为"配置即集成"：
- 通过设置页接入新的媒体服务器实例（多 Radarr/Sonarr，区分 4K/1080p）。
- 元数据提供者可在"Metadata Providers"标签切换/新增（TMDB、TVDB，并带 AniDB fallback）。
- 通知 agent 列表为内置但可配置；Webhook 支持动态占位符以对接外部服务。
- 真正的功能扩展需通过 PR 合入主线。Seerr 团队明确"更多服务集成将在未来加入"，但未公开稳定的第三方扩展 SDK。

#### 7. 配置方式
- 首次启动 Web 向导：配置媒体服务器、Sonarr/Radarr、通知。
- 持久化：SQLite（默认）或 PostgreSQL（`DATABASE_URL` 环境变量）。
- 运行时配置：Web 设置页（多 Tab：通用、媒体服务器、DVR、通知、权限、网络、元数据提供者）。
- 环境变量：`PORT`（默认 5055）、`HOST`、`FORCE_IPV4_FIRST`、`LOG_LEVEL`、`TZ`、`DATABASE_URL` 等。
- 配置热更新部分支持（如 DNS Cache、通知开关），无需重启。

#### 8. API 设计
- 内置 RESTful API（`/api/v1/...`），公开端点 `/api/v1/settings/public` 用于健康检查。
- API 文档由后端 OpenAPI 规范生成（仓库 `gen-docs/` 目录辅助生成）。
- 第三方（如 Requestrr）即通过其 API 提交请求、查询状态。
- 认证基于媒体服务器 SSO（Plex OAuth、Jellyfin/Emby token）+ 本地用户体系。

#### 9. UI 设计
- 现代 React SPA，深色为主，卡片式内容浏览，响应式适配移动端。
- 左侧导航：Discover / Movies / Tv / Requests / Settings 等；右侧展示最近添加与待处理请求。
- 媒体详情页：评分、演职人员、流媒体可用性、请求按钮。
- 管理面板：请求审批支持批量操作、按状态过滤。
- 视觉风格统一，国际化覆盖 25+ 语言。

#### 10. 数据模型
基于 TypeORM 实体，核心表包括：
- `User`：用户、权限位、配额、关联媒体服务器账号。
- `Media` / `MediaRequest`：媒体条目与请求记录（状态：PENDING/APPROVED/DECLINED/COMPLETED）。
- `SeasonRequest`：剧集按季请求子表。
- `Issue`：用户提交的内容问题（错版、缺字幕等）。
- `Watchlist` / `Blocklist`：白/黑名单。
- `Notification` / 通知 agent 配置表。
- `Settings`：键值化全局设置。
元数据来源 ID（TMDB id / TVDB id）作为跨服务关联键。

#### 11. 扩展能力
- 多实例 DVR（4K/1080p 分流）。
- Override Rules：基于用户/标签的条件化请求默认值，可视为轻量规则引擎。
- Webhook 动态占位符支持对接自建服务。
- 元数据多源（TMDB/TVDB/AniDB fallback）。
- Helm Chart 降低 K8s 部署门槛。
- DNS Cache 缓解大型 Jellyfin 媒体库对 Pi-Hole/Adguard 的 DNS 压力。
- 局限：缺乏运行时插件机制，所有适配器需内置编译。

#### 12. 优点
- 一站式请求/发现/通知，覆盖 Plex+Jellyfin+Emby 全主流媒体服务器。
- 社区活跃（190+ 贡献者，前一日仍有提交），文档与迁移指南完善。
- 合并后单一代码库，避免 Overseerr/Jellyseerr 双线维护负担。
- PostgreSQL 支持满足中大型部署；移动端体验接近原生。
- MIT 协议友好，Docker/Helm 部署成熟。

#### 13. 缺点
- 仅 Node.js 单体，水平扩展依赖多实例 + 共享 DB，无原生分布式调度。
- 无运行时插件 SDK，新增第三方集成必须改源码发版。
- 仅支持"单一媒体服务器集成"（同一时间只能接 Plex 或 Jellyfin 或 Emby 之一），多服务器混合场景受限。
- TMDB/TVDB 强依赖，国内访问需自备代理。
- 资源占用相对同类型 Go 工具偏高（Node 运行时 + 前端构建产物）。

#### 14. 社区评价
- 官方自我定位为"Plex/Jellyfin/Emby 用户的专业级请求管理方案"，社区普遍认可其为 Overseerr 的正统继任者。
- 第三方教程（QuickBox、RapidSeedbox、picksinfo 等）均给出"部署简单、UI 现代化、通知覆盖广"的正面评价。
- 合并公告后，原 Jellyseerr/Overseerr 用户迁移积极；Discord 社区活跃。

#### 15. 常见 Issue
- 元数据不一致：TMDB 与 Sonarr 使用的 TVDB 季集编号差异（已通过新增 TVDB 元数据提供者缓解）。
- DNS 限流：大型 Jellyfin 媒体库触发 Pi-Hole/Adguard 限流（已通过 DNS Cache 实验性缓解）。
- Plex OAuth 登录失败 / token 刷新问题。
- Sonarr V4+ 语言字段处理（Requestrr 侧也为此适配）。
- PostgreSQL 迁移与 schema 升级偶发问题。
- 大库扫描耗时与定时任务冲突。

#### 16. 未来发展方向
- 继续整合原 Overseerr/Jellyseerr 全部功能并收敛到单代码库。
- 更多 DVR / 媒体服务器集成（Lidarr、Readarr 等已在路线）。
- TVDB 元数据提供者从实验转稳定；AniDB fallback 扩展动漫覆盖。
- 通知与 Webhook 增强（动态占位符已落地，后续可能支持条件触发）。
- 运行时扩展机制（社区多次讨论，但未见官方 SDK 承诺）。

---

### 2. MediaMTX

仓库：https://github.com/bluenviron/mediamtx
官网 / 文档：https://mediamtx.org ｜ https://mediamtx.org/docs/kickoff/introduction

#### 可核验指标
- Star 数：19,438 | Fork 数：2,290 | Open Issues：221
- 主语言：Go（含少量 C / Bash / JavaScript）
- 最近 push：2026-07-08（活跃）| License：MIT | 贡献者：119
- 创建时间：2019-12 | 最新 Release：v1.19.2（2026-06-28）
- 文档完善度：高（独立站点 mediamtx.org，含安装/使用/鉴权/录制/API/hooks/metrics 等分章节）

#### 1. 项目定位
**零依赖、单可执行文件的实时媒体服务器与媒体代理**（"media router"），定位是把音视频流在不同协议间路由、转换、转发、录制、回放。与"内容管理"类工具不同，它聚焦在**传输与协议层**，是 IP 摄像头、直播推流、协议桥接场景的轻量基础设施。

#### 2. 解决的问题
实时音视频场景协议碎片化（RTSP / RTMP / HLS / WebRTC / SRT / MPEG-TS / RTP / Media-over-QUIC）导致的互通难题：摄像头只推 RTSP、浏览器只读 WebRTC/HLS、OBS 只推 RTMP/SRT。MediaMTX 作为中间路由，让任一协议的源被任一协议的读者读取，且无需安装 FFmpeg/GStreamer 等重依赖。

#### 3. 核心功能
- 多协议发布（Publish）：SRT、WebRTC、RTSP、RTMP、HLS、MPEG-TS、RTP。
- 多协议读取（Read）：SRT、WebRTC、RTSP、RTMP、HLS。
- **自动协议转换**：源用任一协议发布，读者可用任一协议拉取。
- 多路径（path）并发，每条路径独立流。
- 录制：以 fMP4 或 MPEG-TS 落盘。
- 回放：录制后的流可回放。
- 鉴权：内置 / HTTP 回调 / JWT 三种认证。
- 转发（Forward）：把流推到其他服务器。
- 代理（Proxy）：拉取远端流再分发。
- Control API：通过 HTTP API 控制服务器。
- 热重载配置：不中断已有客户端连接即可重载配置。
- Prometheus 指标监控。
- Hooks：客户端连接/断开/读/推时触发外部命令。
- 跨平台：Linux / Windows / macOS，单可执行文件，无解释器依赖。

#### 4. 技术架构
- 纯 Go 实现，单二进制，"zero-dependency"指运行时无需额外运行时/库。
- 核心 abstractions：`path`（路径，流的逻辑容器）、`publisher` / `reader`（按协议适配）、`source` 抽象允许流在协议间转换。
- 协议库多自研，部分拆分为独立库（gortsplib、gohlslib、gortmplib、mediacommon），均归 bluenviron 组织维护。
- 配置驱动 + API 驱动双模：YAML 配置文件 + REST Control API。
- 内置 HTTP/HTTPS 服务用于 API 与 Web 管理界面。
- 录制为内置模块，不依赖外部 muxer。

#### 5. 模块划分
仓库顶层目录：
- `internal/`：核心实现（path manager、各协议 server/client、认证、录制、转发、代理、hooks）。
- `api/`：Control API 定义与 OpenAPI 规范。
- `docker/`：镜像构建。
- `scripts/`：构建与发布脚本。
- 配置文件 `mediamtx.yml` 为入口。
协议层模块化清晰：RTSP / RTMP / HLS / WebRTC / SRT / MPEG-TS / RTP / Media-over-QUIC 各自独立。

#### 6. 插件机制
- **无传统动态插件**，但提供两类外部扩展点：
  - **Hooks**：在客户端连接/断开/读/发布事件时调用外部命令（shell），可视为"脚本化插件"。
  - **HTTP 鉴权**：把鉴权委托给外部 HTTP 服务，便于接入自建用户体系。
- 协议适配器为内置编译，新增协议需改源码。
- 配置中的 path 可绑定不同 source（proxy 拉远端、本地发布），相当于"声明式路由规则"。

#### 7. 配置方式
- 主配置 `mediamtx.yml`：定义路径、端口、协议开关、鉴权、录制、转发、hooks、metrics 等。
- 支持热重载（不中断连接）。
- 命令行参数可覆盖配置项。
- 环境变量支持部分覆盖。
- Control API 可在运行时动态增删 path 与配置。

#### 8. API 设计
- RESTful Control API（OpenAPI 规范在 `api/` 目录），支持列出/增删 path、查询流、控制录制、获取指标等。
- 兼容 Prometheus `/metrics` 端点（可直接被 Prometheus 抓取）。
- 鉴权 API：HTTP/JWT。
- API 设计聚焦"控制面"而非"数据面"，数据面是协议层本身。

#### 9. UI 设计
- 内置极简 Web 界面，主要用于流列表浏览与简单播放（WebRTC/HLS 内嵌播放）。
- 不做内容管理或元数据展示，定位是运维/调试用，而非终端用户消费界面。

#### 10. 数据模型
- 非数据库驱动。核心运行时实体是 `path`（路径名 + source 描述 + publisher + readers 列表 + 录制状态）。
- 配置实体：路径规则、认证规则、转发目标、录制参数、hooks。
- 录制产物为文件（fMP4/MPEG-TS），元数据通过文件名约定。
- 无持久化用户/媒体库概念，重启后 path 状态按配置重建。

#### 11. 扩展能力
- 协议桥接是核心扩展形态（任意协议进、任意协议出）。
- Hooks 脚本扩展事件行为。
- HTTP 鉴权对接外部身份系统。
- Proxy/Forward 形成级联拓扑。
- 自研协议库（gortsplib 等）可被其他 Go 项目复用。
- 局限：扩展点偏运维/集成侧，无业务级插件市场。

#### 12. 优点
- 真正零依赖单二进制，部署与跨平台体验极佳，资源占用低。
- 协议覆盖最全（含 Media-over-QUIC 前沿协议），自动转换能力强。
- 配置热重载 + Control API 双模管理，运维友好。
- 录制/回放/转发/代理一体化。
- MIT 协议 + 文档独立站点完善 + 高 Star 高活跃。
- 性能稳定，适合生产直播/监控场景。

#### 13. 缺点
- 不涉及内容元数据、媒体库、用户体系，纯传输层，不能替代媒体管理工具。
- 无运行时插件 SDK，扩展依赖 hooks 脚本或改源码。
- Web UI 极简，不适合终端用户消费。
- 协议复杂度高，新手调参（HLS 分片、WebRTC ICE、SRT passphrase）有学习曲线。
- 录制管理（按时间/事件触发、清理策略）相对基础。

#### 14. 社区评价
- 在 awesome-go、awesome-video、awesome-ip-camera、awesome-pion 等多个 awesome 列表收录，被定位为"simple, ready-to-use RTSP/RTMP/WebRTC server and proxy"。
- gstars.dev 健康分 75，周增长稳定，下载量（v1.19.2 单版本 1.7 万下载）。
- 社区评价聚焦于"轻量、稳定、协议全"，常见对标 SRS / ZLMediaKit（C++）。

#### 15. 常见 Issue
- WebRTC ICE/STUN/TURN 在 NAT 环境下的连通性问题。
- RTSP 摄像头兼容性（不同厂商 SDP/认证差异）。
- HLS 延迟与分片配置调优。
- 录制文件的磁盘 IO 与分片策略。
- SRT 版本与 passphrase 兼容性。
- 热重载时偶发的 path 状态竞争。

#### 16. 未来发展方向
- Media-over-QUIC 持续完善（已在标题显著位置）。
- 更细粒度的录制管理（事件触发、清理策略）。
- Prometheus 指标扩展（每路流粒度）。
- 协议库持续抽离为独立可复用 Go 库。
- 可能引入更丰富的鉴权与多租户能力（当前 HTTP/JWT 已具备基础）。

---

### 3. Requestrr（thomst08 活跃 fork）

仓库：https://github.com/thomst08/requestrr
（原仓库 darkalfx/requestrr 已于 2024-01 归档，社区迁移至此 fork 维护）
文档：https://github.com/thomst08/requestrr/wiki

#### 可核验指标
- Star 数：477 | Fork 数：36 | Open Issues：47
- 主语言：C# 52.8% / JavaScript 26.1% / SCSS 21.0%（.NET Core 后端 + React 前端）
- 最近 push：2026-06-23（活跃）| License：MIT
- 总 Commits：365 | 最新 Release：V2.1.10（2026-06-04）
- 文档完善度：中（Wiki + README，无独立文档站，覆盖部署/构建/配置）

#### 1. 项目定位
**聊天机器人式的媒体请求接入层**，把 Sonarr / Radarr / Lidarr / Overseerr / Ombi 的请求能力通过 Discord 斜杠命令暴露给社区成员，是"IM 入口 → 媒体自动化"的桥接工具。区别于 Seerr 的 Web 入口，Requestrr 走 IM Bot 形态。

#### 2. 解决的问题
部分社区成员不习惯/不方便使用 Web 面板提交请求，更愿意在 Discord 内直接 `/movie` `/tv` 完成请求与查询。Requestrr 让媒体请求"就地发生"在聊天中，并自动清理命令消息保持频道整洁、请求完成时回推通知。

#### 3. 核心功能
- Discord 斜杠命令 + 按钮交互请求内容。
- Sonarr（V2-V4）集成，多实例支持（经 Overseerr 区分 4K/1080p）。
- Radarr（V2-V5）集成。
- Lidarr（V1-V2）集成（音乐）。
- Overseerr 集成：每用户权限/配额 + Issue 提交。
- Ombi（V3/V4）集成：每用户角色/配额 + Issue 提交。
- 请求完成通知（用户收到可观看提醒）。
- 完全通过 Web Portal 配置（无需改代码）。
- Docker 一键部署（端口 4545）。
- Apple Siri 语音集成（语音发起请求）。

#### 4. 技术架构
- 后端：.NET Core（构建依赖 .NET Core SDK 6.0.407），ASP.NET Web API（`Requestrr.WebApi`）。
- 前端：React（`Requestrr.WebApi/ClientApp`，`npm run install:clean`），SCSS 样式。
- Discord 接入：DSharpPlus 库（Discord bot 框架）。
- 配置：JSON 持久化到 `/root/config`。
- 部署：Docker（`thomst08/requestrr`）为主，亦可源码构建。
- 架构上是"Web 配置面板 + Bot 长连接"双职责单体。

#### 5. 模块划分
仓库结构：
- `Requestrr.WebApi/`：主项目（Web API + Bot 主机 + 配置门户）。
- `Requestrr.WebApi/ClientApp/`：React 前端（配置门户）。
- `Logos/`：图标资源。
按职责：Bot 引擎层（DSharpPlus 命令注册、交互组件）、上游适配层（Sonarr/Radarr/Lidarr/Overseerr/Ombi 各 client）、配置层（设置门户 + 持久化）。

#### 6. 插件机制
- 无运行时插件机制。
- 上游集成（Sonarr/Radarr/Lidarr/Overseerr/Ombi）为内置 client，新增需改源码。
- 扩展点偏弱：主要通过配置启停各集成、调整命令权限。
- 聊天平台扩展性：设计上"便于适配新平台"，但当前仅 Discord。

#### 7. 配置方式
- 首次启动访问 `http://youraddress:4545/` 创建管理员账号，随后全部通过 Web Portal 配置。
- 环境变量：`REQUESTRR_PORT`（容器内监听端口，默认 4545）、`REQUESTRR_BASEURL`（反向代理子路径，默认 `/`）。
- 配置持久化到挂载卷 `/root/config`。
- Docker 部署模板在 README 给出（含 volume/restart）。

#### 8. API 设计
- 内部 Web API 供配置门户使用（非面向第三方公开 API）。
- 真正"对外"的接口是 Discord Bot 的斜杠命令（`/help`、`/movie`、`/tv` 等）与按钮交互。
- 鉴权依赖 Discord Bot Token + 各上游服务 API Key。

#### 9. UI 设计
- 配置 Web Portal：React SPA，仅用于管理员配置 Bot 与上游连接，非终端用户消费界面。
- 终端用户交互界面即 Discord 本身（斜杠命令、Embed 卡片、按钮）。
- 视觉风格简洁实用，无独立品牌化设计。

#### 10. 数据模型
- 配置驱动而非数据库驱动：JSON 文件存储 Bot 设置、Discord 账号、各上游 client 配置、频道映射、权限。
- 运行时实体：Discord 用户 → 上游服务用户的映射、请求状态缓存。
- 无持久化请求历史库（请求状态委托上游 Sonarr/Radarr/Overseerr 管理）。

#### 11. 扩展能力
- 多上游集成并存（Sonarr/Radarr/Lidarr/Overseerr/Ombi）。
- 多实例 Sonarr/Radarr（经 Overseerr 区分 4K/1080p）。
- Discord 服务器多频道/角色权限映射。
- Siri 集成作为非 IM 入口补充。
- 局限：无运行时插件、仅 Discord 平台、无独立 API 对外。

#### 12. 优点
- 把媒体请求能力带入 Discord，对 IM 优先的社区友好。
- 上游集成覆盖 \*arr 全家桶 + Overseerr + Ombi，桥接价值明确。
- Web Portal 全量配置，零代码上手。
- Docker 部署简单，环境变量支持反向代理子路径。
- MIT 协议，社区 fork 在原仓库归档后持续维护（2026 年仍有 release）。

#### 13. 缺点
- Star/Fork 体量小（477/36），维护者较少，遇 Bug 需自力更生或 PR。
- 仅 Discord 平台，未支持 Telegram（社区长期呼声但未落地）。
- 无运行时插件，新增上游或聊天平台需改源码编译。
- 无独立对外 API，仅作 IM 入口，不能替代 Web 请求面板。
- 配置为 JSON 文件，无数据库，大规模/多租户场景受限。
- .NET Core SDK 6.0 偏老，依赖升级节奏慢。

#### 14. 社区评价
- 作为 Overseerr/Seerr 的"IM 入口补充"被广泛部署于家庭/小型社区。
- 原 darkalfx/requestrr 归档后，thomst08 fork 被官方 README 指定为新仓库，社区认可其正统性。
- 第三方教程（QuickBox、RapidSeedbox）将其列为媒体请求栈的可选组件。
- 评价集中在"部署简单、Discord 体验好"，但也常被建议"若需 Telegram/Web 入口则用 Seerr"。

#### 15. 常见 Issue
- Discord Bot Token 权限与斜杠命令注册（guild 全局命令生效延迟）。
- Sonarr V4+ 语言字段处理（Jellyseerr/Seerr 发 NULL 时的兼容，V2.1.9 已修）。
- Overseerr/Jellyseerr 升级后的 API 兼容。
- 反向代理子路径（`REQUESTRR_BASEURL`）配置不当导致资源 404。
- 通知未送达（请求完成 webhook 失败）。
- Lidarr 未监控艺术家添加问题（V2.1.10 已修）。

#### 16. 未来发展方向
- Telegram 支持是社区长期诉求（原设计预留扩展性，但未实现）。
- 对齐 Seerr 合并后的新 API 契约。
- 更多聊天平台（Slack、Matrix）适配（依赖贡献者投入）。
- .NET 运行时升级（脱离 6.0）。
- 与 \*arr V4+ 新字段持续兼容。
- 受限于维护者规模，演进速度依赖社区 PR。

---

## 调研总结与关键发现

### 语言与架构多样性统计

本次调研共覆盖 **20 个项目**，跨 **7 种主语言**、**9 种架构形态**，充分体现了该领域技术栈的多样性。

#### 语言覆盖统计

| 序号 | 语言 | 项目数 | 代表项目 |
|------|------|--------|----------|
| 1 | Go | 7 | Alist、OpenList、qmediasync、PanSou、aliyunpan、MediaMTX、aliyundrive-subscribe |
| 2 | Python | 4 | MoviePilot、quark-auto-save、nas-tools、AutoBangumi |
| 3 | C# / .NET | 4 | Sonarr、Radarr、jellyfin-plugin-metashark、Requestrr |
| 4 | TypeScript (Node.js) | 2 | Seerr、CloudSaver |
| 5 | JavaScript | 1 | PT-Plugin-Plus |
| 6 | Java | 1 | tinyMediaManager |
| 7 | C++ | 1 | MediaElch |

#### 架构形态统计

| 序号 | 架构形态 | 代表项目 | 特点 |
|------|----------|----------|------|
| 1 | 单二进制 CLI / 服务 (Go) | Alist、aliyunpan、MediaMTX、PanSou | 零依赖、跨平台、部署极简 |
| 2 | 前后端分离 Web 面板 (FastAPI/Python) | MoviePilot、quark-auto-save、AutoBangumi | 与 115 Media Hub 同栈，可借鉴度最高 |
| 3 | 前后端分离 Web 面板 (Node/TS + React) | Seerr、CloudSaver | 工程化程度高，TypeScript 类型安全 |
| 4 | 单体 Web 应用 (C#/.NET + React) | Sonarr、Radarr | *arr 生态，Provider 体系设计优雅 |
| 5 | 桌面 GUI 应用 (Java/Swing) | tinyMediaManager | 老牌刮削器，GUI + CLI 双形态 |
| 6 | 桌面 GUI 应用 (C++/Qt) | MediaElch | 原生跨平台，工程质量高 |
| 7 | 浏览器扩展 (JavaScript) | PT-Plugin-Plus | IM 入口，非服务端常驻 |
| 8 | 媒体服务器插件 (C#/.NET) | jellyfin-plugin-metashark | 依附 Jellyfin，安装即用 |
| 9 | Bot + Web 配置门户 (C#/.NET + React) | Requestrr | IM 入口，桥接 *arr 生态 |

### 技术栈分布观察

1. **Go 主导底层与传输层**：7 个 Go 项目集中在网盘聚合（Alist/OpenList）、CLI 工具（aliyunpan）、搜索 API（PanSou）、STRM 生成（qmediasync）、媒体路由（MediaMTX）等"基础设施"层，特点是单二进制、高性能、部署极简。Go 在"工具型"项目上占据主导。

2. **Python 主导自动化面板**：4 个 Python 项目（MoviePilot、quark-auto-save、nas-tools、AutoBangumi）均为"自动化面板"或"追更工具"，采用 FastAPI 或异步架构。与 115 Media Hub 技术栈高度一致，是可借鉴度最高的群体。

3. **C#/.NET 主导 *arr 生态**：4 个 C# 项目分属 *arr 生态（Sonarr/Radarr）、Jellyfin 插件、Discord Bot，共享 Servarr 架构骨架。Provider 体系是其中最值得借鉴的设计。

4. **前端技术趋于统一**：无论是 Python（Vue3）、Node/TS（React）、C#（React），前端均趋向现代 SPA 框架（Vue3/React），告别了早期 Flask 模板渲染风格。

5. **AI/MCP 成为新趋势**：MoviePilot（AI Agent + MCP 端点）、PanSou（MCP 集成）已走在将面板能力暴露给 LLM 的前沿，这是自动化工具的新范式。

6. **WebDAV 与 REST API 是通用接口约定**：Alist、aliyunpan 通过 WebDAV 暴露文件系统；Radarr、Sonarr、Seerr、MoviePilot 通过 REST API 暴露能力，形成可编排的接口生态。

### 生态位空白分析

通过对 20 个项目的横向比较，可以清晰识别出当前生态中尚未被单一项目完整覆盖的能力组合：

1. **"多网盘（5+）+ STRM 生成 + TG 资源同步 + 影视订阅 + 刮削管理"五位一体空白**：目前没有任何一个项目同时做到这五项能力的完整闭环。各项目的能力分布如下：
   - **MoviePilot**：订阅 + 搜索 + 下载 + 刮削 + 媒体库（强），但不生成 STRM、网盘原生支持弱
   - **qmediasync**：STRM + 元数据双向 + Emby 联动（强），但不做订阅、不跨网盘
   - **quark-auto-save**：转存 + 签到 + 命名 + 媒体库刷新（强），但仅夸克单盘、不做 STRM
   - **Alist/OpenList**：30+ 网盘挂载（强），但不做 STRM、不做刮削/订阅
   - **PanSou**：多频道搜索 + 13 类网盘识别（强），但不做转存
   - **Sonarr/Radarr**：PT/BT 自动追更（强），但对国内网盘无原生支持
   - **TMM/MediaElch**：刮削 + NFO + 重命名（强），但无 Web UI、无 API（MediaElch）

2. **"网盘原生 + 轻量刮削 + API + 插件化"组合空白**：刮削类工具（TMM/MediaElch）偏桌面端、封闭；面板类工具（MoviePilot）偏全功能、重；没有项目做到"网盘原生接入 + 轻量刮削管理 + 开放 API + 插件化扩展"的中间态定位。

3. **中文刮削防封禁的工程化方案空白**：豆瓣中文刮削是长期痛点（反爬/限流），MoviePilot 与 metashark 均受影响，但均未形成成熟的开源防封禁框架。115 Media Hub 若在"豆瓣 + TMDB 双源 + 防封禁策略"上做出工程化方案，将填补这一空白。

4. **服务端 PT/网盘混合搜索 + 自动转存一体化空白**：PT-Plugin-Plus（浏览器扩展，已归档）做多站聚合搜索但非服务端；PanSou 做服务端搜索但不做转存；CloudSaver 做搜转一体但已闭源。没有活跃开源项目同时做到"服务端多源搜索 + 多网盘自动转存 + 追更调度"。

5. **IM 入口与网盘面板的融合空白**：Requestrr 提供了 Discord Bot 入口但仅桥接 *arr，没有项目把"网盘媒体面板 + IM Bot 入口"融合到同一服务中。

### 对 115 Media Hub 差异化定位的启示

基于上述生态位空白分析，对 115 Media Hub 的差异化定位提出以下关键启示：

#### 1. 技术栈与架构借鉴

- **FastAPI + chain/modules/plugins 架构**：MoviePilot 与本项目同为 FastAPI + Python，其"chain 业务链路 + modules 适配器 + plugins + workflow + skills/MCP"架构可直接借鉴，尤其是「适配器统一接口」与「插件市场」设计。
- **Provider 体系**：Radarr 的"Provider 统一接口 + UI 自动渲染配置表单"是处理多网盘异构的最佳范式，本项目 `app/providers/` 已覆盖 aliyun/quark/pan115/pan123/tianyi，可对照此模式扩展。
- **Driver 接口抽象**：Alist/OpenList 的 30+ 驱动是网盘覆盖广度的标杆，可对照其 Driver 接口抽象方式扩展网盘支持。

#### 2. 核心模块对标

- **STRM 生成模块**：qmediasync 是与本项目 STRM 模块最贴近的项目，其「115 开放平台接入 + 增量缓存 + 元数据双向同步 + Emby 302 代理」组合方案值得直接对照；本项目 `app/services/strm_files.py`、`app/routes/strm.py` 可对标其设计。
- **转存订阅模块**：quark-auto-save 的"多任务组 + 星期调度 + 失效检查 + 新链挑选"逻辑可移植到本项目的转存/追更模块；aliyundrive-subscribe + quark-auto-save 共同定义了"分享链监控 + 自动转存 + 正则命名 + 媒体库刷新"的范式。
- **资源中心**：PanSou 的"异步插件先返回再补充 + 二级缓存"模式可直接借鉴到 TG 频道同步与 PanSou 盘搜模块，降低首屏延迟。
- **刮削管理**：TMM 的"模板化重命名（JMTE）+ NFO 输出 + 刮削器 SPI"三件套是事实标准；metashark 的"豆瓣 + TMDB 双源 + 防封禁 + AnitomySharp 动漫解析"是中文刮削可直借方案。

#### 3. 扩展机制设计

- **插件市场**：MoviePilot 的 300+ 插件 + 热插拔 + AI Agent + MCP 是当前最前沿的扩展范式，与本项目 FastAPI 面板天然契合。
- **Hook 脚本扩展**：MediaMTX 在事件（入库、转码完成等）暴露 hook 脚本，可弥补无运行时插件的灵活度。
- **完整 REST API + Webhook**：作为面板应提供稳定 REST API 与 Webhook 通知，便于被 Requestrr 类工具或 HomeAssistant 编排。
- **WebDAV 服务**：aliyunpan 的 WebDAV 服务思路可让本项目对外暴露 WebDAV，便于 Emby/Jellyfin/Alist 挂载复用媒体库。

#### 4. 避免重蹈覆辙

- **nas-tools 因 Flask 架构与单维护者而归档** → 本项目用 FastAPI 已规避架构问题，但需注意组织化运营，避免单点风险。
- **aliyundrive-subscribe 单一网盘 + 长期不维护** → 本项目应坚持多网盘（5+）+ 持续迭代。
- **Alist 主仓库长期不更新被 Fork 接力** → 本项目应保持透明开发节奏，避免"信任危机"。
- **nas-tools 因功能臃肿、设置繁杂被重构** → 本项目应保持核心闭环聚焦，避免功能膨胀。
- **CloudSaver 闭源转向** → 本项目应坚持开源，避免因商业化而闭源导致用户流失。
- **PanSou 明确"仅供学习"** → 此类项目存在合规与维护风险，应在 README 与产品定位上保持克制。

#### 5. 安全与合规共识

所有调研项目都强调 Cookie 等同账号密码、必须私有化部署。本项目应在 Cookie 健康检查与加密存储上做重投入（参见本项目已有的 cookie-health-bar 设计）。

#### 6. 核心差异化定位

综合以上分析，115 Media Hub 的差异化定位应聚焦于 **"多网盘（5+）+ STRM 生成 + TG 资源同步 + 影视订阅 + 刮削管理"五位一体的网盘媒体面板**：

- 相比 **MoviePilot**（偏 PT/BT、无 STRM）：本项目覆盖 115/Quark/天翼/123/阿里五大网盘原生转存 + STRM 生成。
- 相比 **qmediasync**（偏 STRM 单点、不跨网盘）：本项目覆盖多网盘 + 订阅 + 刮削全链路。
- 相比 **quark-auto-save**（偏夸克单盘、无 STRM）：本项目多网盘 + STRM + 刮削管理。
- 相比 **Alist/OpenList**（偏底层挂载、无媒体自动化）：本项目在上层提供 STRM + 订阅 + 刮削的完整面板。
- 相比 **Sonarr/Radarr**（对国内网盘无原生支持）：本项目原生支持国内网盘生态。

本项目有机会在"网盘媒体面板"细分赛道形成完整闭环，填补目前生态中"五位一体"能力组合的空白。

---

> 数据来源：GitHub REST API（`api.github.com/repos/{owner}/{repo}`，2026-07-10 实时核验）、各仓库 GitHub 主页与 README、官方文档站、GitLab 仓库主页（tinyMediaManager）、issues.ecosyste.ms / star-history / HelloGitHub 等第三方统计。无法获取的细节已标注"信息不足"，未编造数据。