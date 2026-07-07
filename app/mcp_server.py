"""
115-media-hub MCP Server

Provides AI Agent (Claude Desktop) with tools to:
- Discover media resources from TG channels and PanSou
- Manage subscriptions for automatic media tracking
- Query system status

Usage:
    python mcp_entry.py          # stdio transport (Claude Desktop)
"""

import os
import sys

# ---------------------------------------------------------------------------
# Bootstrap: ensure /app/config exists so the existing code can find its config
# ---------------------------------------------------------------------------
os.environ.setdefault("CONFIG_PATH", "/app/config/settings.json")
os.makedirs("/app/config", exist_ok=True)
os.makedirs("/app/logs", exist_ok=True)

# Ensure the project root is on sys.path
_project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _project_root not in sys.path:
    sys.path.insert(0, _project_root)

# ---------------------------------------------------------------------------
# Import existing 115-media-hub modules
# ---------------------------------------------------------------------------
from app.core import (  # noqa: E402
    get_config,
    save_config,
    normalize_subscription_task,
    normalize_relative_path,
    SUBSCRIPTION_QUALITY_PRIORITY_ALIASES,
)
from app.db import ensure_db  # noqa: E402
from app.resource_store import list_resource_items  # noqa: E402
from app.resource_identity import resource_item_matches_search  # noqa: E402
from app.resource_tg import build_tg_proxy_url  # noqa: E402
from app.providers.pansou import request_pansou_search  # noqa: E402

# Ensure DB tables exist
ensure_db()

# ---------------------------------------------------------------------------
# MCP Server (FastMCP)
# ---------------------------------------------------------------------------
from mcp.server.fastmcp import FastMCP  # noqa: E402

mcp = FastMCP(
    "115-media-hub",
    instructions="AI 媒体助手 — 搜索资源、管理订阅、查询状态",
)


# ── Tool: discover_media ──────────────────────────────────────────────────


@mcp.tool(
    description="搜索媒体资源，支持 TG 频道和 PanSou 盘搜多渠道。返回候选列表，包含标题、来源、质量和链接。",
)
async def discover_media(
    keyword: str,
    provider_filter: str = "115",
    limit: int = 10,
) -> str:
    """
    搜索媒体资源。

    Args:
        keyword: 搜索关键词，如 "黑客帝国 4 2021"
        provider_filter: 网盘过滤，"115"/"quark"/"magnet"/"all"，默认 "115"
        limit: 返回结果数量上限，默认 10
    """
    cfg = get_config()
    results = []

    # 1. Search PanSou if configured
    pansou_base = str(cfg.get("pansou_base_url", "") or "").strip()
    if pansou_base:
        try:
            pansou_result = request_pansou_search(cfg, keyword, provider_filter=provider_filter, limit=limit)
            results.extend(pansou_result.get("items", []))
        except Exception:
            pass  # PanSou is optional

    # 2. Search local resource_items DB
    db_items = list_resource_items(search=keyword, limit=200)
    for item in db_items:
        if resource_item_matches_search(item, keyword):
            results.append(item)

    # 3. Deduplicate and format
    seen = set()
    formatted = []
    for item in results:
        title = str(item.get("title", "") or "").strip()
        link_url = str(item.get("link_url", "") or "").strip()
        link_type = str(item.get("link_type", "") or "").strip()
        quality_tag = str(item.get("quality", "") or "").strip()
        source = str(item.get("source_name", "") or "").strip()

        identity = link_url or title.lower()
        if not identity or identity in seen:
            continue
        seen.add(identity)

        formatted.append(
            f"• {title}\n"
            f"  来源: {source or link_type}  |  质量: {quality_tag or '未知'}\n"
            f"  链接: {link_url or '无'}\n"
        )
        if len(formatted) >= limit:
            break

    if not formatted:
        return f"未找到与「{keyword}」相关的资源"

    return f"找到 {len(formatted)} 个资源：\n\n" + "\n".join(formatted)


# ── Tool: subscribe_media ─────────────────────────────────────────────────


@mcp.tool(
    description="创建媒体订阅任务，系统会自动搜索匹配资源并转存到 115 网盘。支持电影和电视剧类型。",
)
async def subscribe_media(
    title: str,
    media_type: str = "movie",
    keyword: str = "",
    quality: str = "balanced",
    savepath: str = "/电影",
    provider: str = "115",
) -> str:
    """
    创建媒体订阅任务。

    Args:
        title: 订阅名称，如 "黑客帝国4"
        media_type: 媒体类型，"movie"（电影）或 "tv"（电视剧）
        keyword: 搜索关键词，为空则使用 title
        quality: 质量偏好，"4K"/"1080p"/"720p"/"balanced"
        savepath: 115 网盘保存路径，如 "/电影"
        provider: 网盘提供商，"115"/"quark"
    """
    cfg = get_config()
    tasks = cfg.get("subscription_tasks", [])
    if not isinstance(tasks, list):
        tasks = []

    quality_key = SUBSCRIPTION_QUALITY_PRIORITY_ALIASES.get(
        quality.lower().strip(), quality.lower().strip()
    )

    new_task = normalize_subscription_task({
        "name": title.strip(),
        "media_type": media_type,
        "title": title.strip(),
        "keyword": (keyword or title).strip(),
        "quality": quality_key,
        "savepath": normalize_relative_path(savepath),
        "provider": provider,
        "enabled": True,
        "score": 60,
        "schedule_weekdays": [],
        "schedule_start_time": "00:00",
        "schedule_end_time": "23:59",
        "schedule_interval_minutes": 120,
    })

    for existing in tasks:
        if str(existing.get("name", "") or "").strip() == new_task.get("name", "").strip():
            return f"订阅「{title}」已存在，无需重复添加"

    tasks.append(new_task)
    cfg["subscription_tasks"] = tasks
    save_config(cfg)

    return (
        f"✅ 已创建订阅「{title}」\n"
        f"   类型: {'电影' if media_type == 'movie' else '电视剧'}\n"
        f"   质量: {quality_key}\n"
        f"   保存路径: {savepath}\n"
        f"   网盘: {provider}\n\n"
        f"系统将在定时调度中自动搜索匹配资源并转存到 115 网盘。"
    )


# ── Tool: list_subscriptions ──────────────────────────────────────────────


@mcp.tool(
    description="列出所有媒体订阅任务及其状态。",
)
async def list_subscriptions() -> str:
    """列出所有订阅任务。"""
    cfg = get_config()
    tasks = cfg.get("subscription_tasks", [])
    if not isinstance(tasks, list) or not tasks:
        return "当前没有订阅任务"

    lines = []
    for task in tasks:
        name = str(task.get("name", "") or "").strip()
        if not name:
            continue
        media_type = str(task.get("media_type", "movie") or "").strip()
        quality = str(task.get("quality", "balanced") or "").strip()
        savepath = str(task.get("savepath", "") or "").strip()
        enabled = bool(task.get("enabled", True))
        provider = str(task.get("provider", "115") or "").strip()

        status_icon = "🟢" if enabled else "🔴"
        type_label = "电影" if media_type == "movie" else "电视剧"
        lines.append(
            f"{status_icon} {name}\n"
            f"   类型: {type_label}  |  质量: {quality}  |  网盘: {provider}\n"
            f"   保存: {savepath}\n"
        )

    return f"共 {len(lines)} 个订阅任务：\n\n" + "\n".join(lines)


# ── Tool: get_status ──────────────────────────────────────────────────────


@mcp.tool(
    description="查询 115 Media Hub 系统状态，包括 Cookie 配置、订阅任务、监控任务等。",
)
async def get_status() -> str:
    """返回系统概览。"""
    cfg = get_config()

    cookie_115 = str(cfg.get("cookie_115", "") or "").strip()
    cookie_status = "✅ 已配置" if cookie_115 else "❌ 未配置"

    pansou_url = str(cfg.get("pansou_base_url", "") or "").strip()
    pansou_status = "✅ 已配置" if pansou_url else "❌ 未配置"

    tg_proxy = build_tg_proxy_url(cfg)
    tg_status = f"✅ 代理 {tg_proxy}" if tg_proxy else "🟡 直连"

    tasks = cfg.get("subscription_tasks", [])
    if isinstance(tasks, list):
        total_tasks = len(tasks)
        enabled_tasks = sum(1 for t in tasks if bool(t.get("enabled", True)))
    else:
        total_tasks = 0
        enabled_tasks = 0

    monitors = cfg.get("monitor_tasks", [])
    monitor_count = len(monitors) if isinstance(monitors, list) else 0

    sources = cfg.get("resource_sources", [])
    source_count = len(sources) if isinstance(sources, list) else 0

    strm_host = str(cfg.get("strm_external_host", "") or "").strip()

    return (
        "📊 115 Media Hub 状态\n\n"
        f"🔑 115 Cookie: {cookie_status}\n"
        f"🔍 PanSou 盘搜: {pansou_status}\n"
        f"📡 TG 连接: {tg_status}\n"
        f"🌐 STRM 地址: {strm_host or '❌ 未配置'}\n\n"
        f"📋 订阅任务: {enabled_tasks}/{total_tasks} 启用\n"
        f"📁 文件夹监控: {monitor_count} 个\n"
        f"📡 资源频道: {source_count} 个\n"
    )


# ── Prompt: media assistant ──────────────────────────────────────────────


@mcp.prompt()
def media_assistant() -> str:
    """预置提示词，指导 AI 如何使用媒体工具"""
    return """你是一个媒体助手，帮助用户搜索和管理媒体资源。

你可以：
1. discover_media — 搜索资源（TG 频道、PanSou 盘搜）
2. subscribe_media — 创建订阅，自动追更
3. list_subscriptions — 查看当前订阅
4. get_status — 查看系统状态

当用户说"找一部电影/电视剧"时，先用 discover_media 搜索。
当用户说"追更"或"订阅"时，用 subscribe_media 创建订阅。
"""


# ── Main entry ────────────────────────────────────────────────────────────


def main():
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()