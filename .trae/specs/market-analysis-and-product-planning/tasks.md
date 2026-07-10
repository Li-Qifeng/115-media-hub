# Tasks

## 阶段一 + 阶段二：项目调研与逐项分析（可并行）

> 目标：调研 ≥20 个 GitHub 同领域项目，按统一格式分析后汇入 `docs/market-analysis.md`。
> 每个 sub-agent 负责一个项目类目，独立产出该类目下项目的统一格式分析，互不重叠。

- [x] Task 1: 调研"网盘媒体管理 / STRM 生成"类项目（≥5 个，如 alist、cloudnas、nastools、film-nil Finished 等）
  - [x] SubTask 1.1: 通过 WebSearch 在 GitHub 搜索网盘挂载/STRM/媒体面板类高 Star 项目，记录仓库名/Star/最近 commit/语言
  - [x] SubTask 1.2: 对每个项目按统一 17 字段格式分析（定位/解决的问题/核心功能/技术架构/模块划分/插件机制/配置方式/API设计/UI设计/数据模型/扩展能力/优点/缺点/社区评价/常见Issue/未来方向）
  - [x] SubTask 1.3: 标注 GitHub 仓库链接与可核验活跃度信息
- [x] Task 2: 调研"影视资源订阅 / 自动追更"类项目（≥5 个，如 moviepilot、metube、bilibili-task 等）
  - [x] SubTask 2.1: WebSearch 搜索资源订阅/追更/自动下载类项目
  - [x] SubTask 2.2: 按 17 字段统一格式分析
  - [x] SubTask 2.3: 记录仓库链接与活跃度
- [x] Task 3: 调研"影视刮削 / 元数据管理"类项目（≥4 个，如 tinyMediaManager、MediaElch、tmdb 相关工具）→ 产出 `docs/_research/03-scraping-metadata.md`
  - [x] SubTask 3.1: WebSearch 搜索刮削/元数据/NFO 生成类项目
  - [x] SubTask 3.2: 按 16 字段统一格式分析（注：spec.md Requirement 实际列出 16 字段；tasks.md/checklist.md 中"17"为笔误，按用户要求与 spec.md 的 16 字段执行）
  - [x] SubTask 3.3: 记录仓库链接与活跃度
- [x] Task 4: 调研"网盘资源搜索 / 转存"类项目（≥3 个，如 pansou、cloudsaver、各类网盘 CLI）
  - [x] SubTask 4.1: WebSearch 搜索网盘搜索/转存/离线类项目
  - [x] SubTask 4.2: 按 17 字段统一格式分析
  - [x] SubTask 4.3: 记录仓库链接与活跃度
- [x] Task 5: 调研"媒体服务器生态工具 + 不同语言/架构代表"类项目（≥3 个，如 jellyfin 插件、go 实现的媒体工具、node 实现）
  - [x] SubTask 5.1: WebSearch 搜索不同语言/架构的同类工具，保证语言多样性
  - [x] SubTask 5.2: 按 17 字段统一格式分析
  - [x] SubTask 5.3: 记录仓库链接与活跃度
- [x] Task 6: 汇总 Task 1-5 产出，编写 `docs/market-analysis.md`
  - [x] SubTask 6.1: 合并所有项目分析为统一文档，开头列出全部项目清单表（项目名/语言/Star/定位/仓库链接）
  - [x] SubTask 6.2: 校验项目总数 ≥20，语言多样性 ≥3 种，架构多样性 ≥2 种
  - [x] SubTask 6.3: 每个项目引用 GitHub 链接作为依据

## 阶段三：横向对比（依赖阶段一、二）

- [x] Task 7: 编写 `docs/competitor-comparison.md`
  - [x] SubTask 7.1: 构建对比矩阵（功能支持/实现方式/优缺点/复杂度/维护成本）
  - [x] SubTask 7.2: 列出"大多数项目都有的功能"
  - [x] SubTask 7.3: 列出"少数项目独有的创新"
  - [x] SubTask 7.4: 列出"被用户频繁要求但没人做好"
  - [x] SubTask 7.5: 列出"被大量吐槽的问题"
  - [x] SubTask 7.6: 列出"被放弃的设计"
  - [x] SubTask 7.7: 每条结论引用对应项目作为依据

## 阶段四：提炼最佳实践（依赖阶段三）

- [x] Task 8: 编写 `docs/best-practice.md`
  - [x] SubTask 8.1: 列出"已成为事实标准（de facto standard）"的设计，附原因与项目依据
  - [x] SubTask 8.2: 列出"优秀实践"
  - [x] SubTask 8.3: 列出"应避免的设计"
  - [x] SubTask 8.4: 列出"未来更值得采用的方案"
  - [x] SubTask 8.5: 每条结论说明原因并引用依据

## 阶段五：设计新项目架构（依赖阶段四）

- [x] Task 9: 编写 `docs/architecture.md`
  - [x] SubTask 9.1: 总体架构（结合优秀项目优点，不复制单一项目）
  - [x] SubTask 9.2: 模块设计
  - [x] SubTask 9.3: 目录结构
  - [x] SubTask 9.4: 插件体系
  - [x] SubTask 9.5: 配置体系
  - [x] SubTask 9.6: 权限体系
  - [x] SubTask 9.7: 数据模型
  - [x] SubTask 9.8: API 规范
  - [x] SubTask 9.9: 事件系统
  - [x] SubTask 9.10: 日志系统
  - [x] SubTask 9.11: 测试方案
  - [x] SubTask 9.12: 文档结构

## 阶段六：功能规划（依赖阶段五）

- [x] Task 10: 编写 `docs/product-plan.md`
  - [x] SubTask 10.1: P0（必须）功能清单，每项含：为什么该优先级/依赖模块/复杂度/风险
  - [x] SubTask 10.2: P1（重要）功能清单
  - [x] SubTask 10.3: P2（增强）功能清单
  - [x] SubTask 10.4: P3（未来）功能清单

## 阶段七：Roadmap（依赖阶段六）

- [x] Task 11: 编写 `docs/roadmap.md`
  - [x] SubTask 11.1: v0.1 版本规划（新增功能/重构/兼容策略/风险/交付目标）
  - [x] SubTask 11.2: v0.5 版本规划
  - [x] SubTask 11.3: v1.0 版本规划
  - [x] SubTask 11.4: v2.0 版本规划

## 阶段八：交叉校验

- [x] Task 12: 全量校验
  - [x] SubTask 12.1: 校验 6 个文档均已生成且非空
  - [x] SubTask 12.2: 校验 market-analysis.md 项目数 ≥20 且引用 GitHub 链接
  - [x] SubTask 12.3: 校验对比矩阵/最佳实践/架构/规划/roadmap 各自关键章节齐全
  - [x] SubTask 12.4: 校验语言/架构多样性达标

# Task Dependencies

- Task 6 依赖 Task 1-5（汇总需要各类目分析完成）
- Task 7 依赖 Task 6（对比需要全部项目分析）
- Task 8 依赖 Task 7（最佳实践来自对比结论）
- Task 9 依赖 Task 8（架构设计基于最佳实践）
- Task 10 依赖 Task 9（功能规划基于架构）
- Task 11 依赖 Task 10（路线图基于功能优先级）
- Task 12 依赖 Task 11（全量校验需要所有文档完成）
- Task 1-5 之间无依赖，可并行执行
