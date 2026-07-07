#!/usr/bin/env python3
"""
115 — 115 Media Hub CLI 工具

用法:
  115 status                            系统状态
  115 search <关键词>                    搜索资源
  115 channels sync|list                管理资源频道
  115 subscribe list                     列出订阅
  115 subscribe add <标题> [选项]         创建订阅
  115 subscribe remove <名称>            删除订阅
  115 subscribe start|stop|status|logs   订阅操作
  115 jobs list|clear|retry              管理资源任务
  115 settings [key=value...]            查看/修改配置
  115 logs [tail]                        查看系统日志
  115 cookies check                      检查 Cookie 状态
  115 sign run|status                    115 每日签到
  115 tmdb search|popular|trending|detail TMDB 搜索
  115 monitor list|status|start|stop     文件夹监控
  115 tree run                           目录树同步
  115 api <method> <path> [body]         通用 API 调用
  115 providers                          列出网盘提供商
  115 version                            版本信息

示例:
  115 status
  115 search "黑客帝国 4K"
  115 subscribe add "黑客帝国4" --quality 4K --savepath "/电影"
  115 tmdb search "黑客帝国"
  115 cookies check
  115 settings cookie_115="xxx"
  115 api POST /resource/channels/sync '{"force": true}'
"""

import argparse
import json
import os
import sys
from typing import Any, Dict, Optional

import httpx

API_BASE = os.environ.get("MH_API_BASE", "http://127.0.0.1:18080")
COOKIE_FILE = os.environ.get("MH_COOKIE_FILE", "/tmp/.115_cookies.txt")


# ── API Client ────────────────────────────────────────────────────────────

class Client:
    """HTTP client with session persistence."""

    def __init__(self, base_url: str = API_BASE):
        self.base_url = base_url.rstrip("/")
        self._session: Optional[httpx.Client] = None

    def _ensure_session(self) -> httpx.Client:
        if self._session is not None:
            return self._session
        self._session = httpx.Client(base_url=self.base_url, timeout=30.0)
        if os.path.exists(COOKIE_FILE):
            try:
                with open(COOKIE_FILE) as f:
                    jar = json.load(f)
                    for cookie_data in jar:
                        self._session.cookies.set(
                            cookie_data["name"], cookie_data["value"],
                            domain=cookie_data.get("domain", "127.0.0.1"),
                            path=cookie_data.get("path", "/"),
                        )
            except Exception:
                pass
        return self._session

    def _save_cookies(self):
        jar = [
            {"name": c.name, "value": c.value, "domain": c.domain, "path": c.path}
            for c in self._session.cookies.jar
        ] if self._session else []
        os.makedirs(os.path.dirname(COOKIE_FILE) or ".", exist_ok=True)
        with open(COOKIE_FILE, "w") as f:
            json.dump(jar, f)

    def _login_if_needed(self):
        session = self._ensure_session()
        r = session.get("/status-summary")
        if r.status_code == 401:
            r = session.post("/login", json={"username": "admin", "password": "admin123"})
            if r.status_code != 200:
                sys.exit(f"登录失败 (HTTP {r.status_code}): {r.text[:200]}")
            self._save_cookies()

    def request(self, method: str, path: str, body: Any = None) -> httpx.Response:
        self._login_if_needed()
        session = self._ensure_session()
        url = path if path.startswith("http") else path
        if method == "GET":
            resp = session.get(url, params=body if isinstance(body, dict) else None)
        else:
            headers = {"Content-Type": "application/json"}
            data = json.dumps(body) if body is not None else None
            resp = session.request(method, url, content=data, headers=headers)
        return resp

    def json(self, method: str, path: str, body: Any = None) -> Any:
        resp = self.request(method, path, body)
        if resp.status_code >= 400:
            sys.exit(f"HTTP {resp.status_code} {path}: {resp.text[:300]}")
        try:
            return resp.json()
        except Exception:
            return resp.text


# ── Formatters ────────────────────────────────────────────────────────────

def fmt_json(data: Any) -> str:
    if isinstance(data, (dict, list)):
        return json.dumps(data, ensure_ascii=False, indent=2)
    return str(data)


def fmt_status(data: dict) -> str:
    main = data.get("main", {})
    monitor = data.get("monitor", {})
    sub = data.get("subscription", {})
    lines = [
        "📊 系统状态", "",
        f"  目录树任务: {main.get('running', False) and '🟢 运行中' or '⏸ 空闲'}",
        f"  文件夹监控: {monitor.get('running', False) and '🟢 运行中' or '⏸ 空闲'}",
        f"  订阅引擎:   {sub.get('running', False) and '🟢 运行中' or '⏸ 空闲'}",
    ]
    nr = main.get("next_run")
    if nr:
        lines.append(f"  下次目录树: {nr}")
    return "\n".join(lines)


def fmt_search_items(items: list, keyword: str) -> str:
    if not items:
        return f"未找到与「{keyword}」相关的资源"
    lines = [f"找到 {len(items)} 个资源：", ""]
    for item in items[:20]:
        title = str(item.get("title", "") or "").strip()
        source = str(item.get("source_name", "") or item.get("link_type", "") or "").strip()
        quality = str(item.get("quality", "") or "").strip()
        link = str(item.get("link_url", "") or "").strip()
        lines.append(f"  • {title}")
        if quality or source:
            lines.append(f"    来源: {source or '未知'}  |  质量: {quality or '未知'}")
        if link:
            lines.append(f"    链接: {link[:80]}")
        lines.append("")
    return "\n".join(lines)


def fmt_subscriptions(tasks: list) -> str:
    if not tasks:
        return "当前没有订阅任务"
    lines = [f"共 {len(tasks)} 个订阅任务：", ""]
    for task in tasks:
        name = str(task.get("name", "") or "").strip()
        if not name:
            continue
        media_type = "电影" if task.get("media_type") == "movie" else "电视剧"
        quality = task.get("quality", "balanced")
        savepath = task.get("savepath", "")
        enabled = "🟢" if task.get("enabled", True) else "🔴"
        provider = task.get("provider", "115")
        lines.append(f"  {enabled} {name}")
        lines.append(f"    类型: {media_type}  质量: {quality}  网盘: {provider}")
        lines.append(f"    保存: {savepath}")
        lines.append("")
    return "\n".join(lines)


def fmt_logs(logs: list, title: str = "日志") -> str:
    if not logs:
        return f"暂无{title}"
    lines = []
    for log in logs[:50]:
        text = str(log.get("text", "") or "").strip()
        level = str(log.get("level", "info") or "").strip()
        icon = {"error": "❌", "warning": "⚠️", "success": "✅", "info": "ℹ️"}.get(level, "ℹ️")
        lines.append(f"  {icon} {text}")
    return "\n".join(lines)


def fmt_tmdb_items(items: list) -> str:
    if not items:
        return "未找到结果"
    lines = [f"共 {len(items)} 条：", ""]
    for item in items[:20]:
        title = str(item.get("title", "") or item.get("name", "") or "").strip()
        year = str(item.get("release_date", "") or item.get("first_air_date", "") or "")[:4]
        vote = item.get("vote_average", 0) or 0
        tmdb_id = item.get("id", "?")
        media_type = item.get("media_type", "movie")
        lines.append(f"  • {title} ({year})  ⭐ {vote:.1f}  [{media_type}:{tmdb_id}]")
    return "\n".join(lines)


def fmt_providers(data: Any) -> str:
    providers = data if isinstance(data, list) else data.get("providers", [])
    if not providers:
        return "未获取到提供商信息"
    lines = []
    for p in providers:
        name = p.get("name", "?")
        label = p.get("label", name)
        enabled = "🟢" if p.get("enabled", True) else "🔴"
        configured = "✅" if p.get("configured", p.get("cookie_configured", False)) else "❌"
        lines.append(f"  {enabled} {label} ({name})  Cookie: {configured}")
    return "\n".join(lines)


# ── Subcommands ───────────────────────────────────────────────────────────

def cmd_status(args, c: Client):
    """系统状态"""
    data = c.json("GET", "/status-summary")
    print(fmt_status(data))


def cmd_version(args, c: Client):
    """版本信息"""
    data = c.json("GET", "/version")
    print(fmt_json(data))


def cmd_search(args, c: Client):
    """搜索资源"""
    keyword = " ".join(args.keyword)
    data = c.json("GET", "/resource/state", {"q": keyword, "compact": "1"})
    items = []
    if isinstance(data, dict):
        items = data.get("items", data.get("search_items", data.get("results", [])))
    print(fmt_search_items(items, keyword))


def cmd_channels(args, c: Client):
    """管理资源频道"""
    if args.action == "sync":
        data = c.json("POST", "/resource/channels/sync", {"force": args.force})
        print(f"✅ 频道同步已完成: {json.dumps(data, ensure_ascii=False)}")
    elif args.action == "list":
        cfg = c.json("GET", "/get_settings")
        sources = cfg.get("resource_sources", [])
        if not sources:
            print("未配置资源频道")
            return
        print(f"共 {len(sources)} 个资源频道：")
        for s in sources:
            name = str(s.get("name", "") or "").strip()
            channel = str(s.get("channel_id", "") or "").strip()
            enabled = "🟢" if s.get("enabled", True) else "🔴"
            print(f"  {enabled} {name} (@{channel})")


def cmd_subscribe(args, c: Client):
    """管理订阅"""
    cfg = c.json("GET", "/get_settings")
    tasks: list = cfg.get("subscription_tasks", [])
    if not isinstance(tasks, list):
        tasks = []

    if args.action == "list":
        print(fmt_subscriptions(tasks))

    elif args.action == "add":
        title = " ".join(args.name) if args.name else ""
        if not title:
            sys.exit("请指定订阅名称")
        for t in tasks:
            if str(t.get("name", "") or "").strip() == title.strip():
                sys.exit(f"订阅「{title}」已存在")
        new_task = {
            "name": title.strip(),
            "media_type": args.type,
            "title": title.strip(),
            "keyword": title.strip(),
            "quality": args.quality,
            "savepath": args.savepath.rstrip("/") or "/电影",
            "provider": args.provider,
            "enabled": True,
            "score": 60,
            "tmdb_enabled": False,
            "schedule_weekdays": [],
            "schedule_start_time": "00:00",
            "schedule_end_time": "23:59",
            "schedule_interval_minutes": 120,
        }
        tasks.append(new_task)
        cfg["subscription_tasks"] = tasks
        c.json("POST", "/save_settings", cfg)
        print(f"✅ 已创建订阅「{title}」")

    elif args.action == "remove":
        name = " ".join(args.name)
        before = len(tasks)
        cfg["subscription_tasks"] = [t for t in tasks if str(t.get("name", "") or "").strip() != name.strip()]
        removed = before - len(cfg["subscription_tasks"])
        if removed == 0:
            sys.exit(f"未找到订阅「{name}」")
        c.json("POST", "/save_settings", cfg)
        print(f"✅ 已删除订阅「{name}」")

    elif args.action == "start":
        name = " ".join(args.name) if args.name else ""
        if name:
            data = c.json("POST", "/subscription/start", {"task_name": name})
        else:
            data = c.json("POST", "/subscription/start", {})
        print(f"✅ 订阅已触发: {json.dumps(data, ensure_ascii=False)}")

    elif args.action == "stop":
        data = c.json("POST", "/subscription/stop")
        print(f"✅ 订阅已停止: {json.dumps(data, ensure_ascii=False)}")

    elif args.action == "status":
        data = c.json("GET", "/subscription/status")
        print(fmt_json(data))

    elif args.action == "logs":
        data = c.json("GET", "/subscription/logs")
        logs = data if isinstance(data, list) else data.get("logs", [])
        print(fmt_logs(logs, "订阅日志"))


def cmd_jobs(args, c: Client):
    """管理资源任务"""
    if args.action == "list":
        data = c.json("GET", "/resource/jobs/state", {"limit": args.limit, "status": args.status or ""})
        print(fmt_json(data))
    elif args.action == "clear":
        data = c.json("POST", "/resource/jobs/clear")
        print(f"✅ 已清理: {json.dumps(data, ensure_ascii=False)}")
    elif args.action in ("clear_completed", "clear-completed"):
        data = c.json("POST", "/resource/jobs/clear_completed")
        print(f"✅ 已完成任务已清理: {json.dumps(data, ensure_ascii=False)}")
    elif args.action == "retry":
        if not args.job_id:
            sys.exit("请指定任务 ID")
        data = c.json("POST", "/resource/jobs/retry", {"job_id": int(args.job_id[0])})
        print(f"✅ 已重试: {json.dumps(data, ensure_ascii=False)}")


def cmd_settings(args, c: Client):
    """查看/修改配置"""
    cfg = c.json("GET", "/get_settings")

    if not args.kv:
        keys = [
            "cookie_115", "cookie_quark", "pansou_base_url",
            "tg_proxy_enabled", "tg_proxy_host", "tg_proxy_port",
            "tmdb_enabled", "tmdb_api_key",
            "resource_sources", "subscription_tasks", "monitor_tasks",
            "strm_external_host", "extensions",
        ]
        print(f"配置 ({len(cfg)} 项)")
        print()
        for key in keys:
            val = cfg.get(key)
            if val is None:
                continue
            if "cookie" in key.lower() or "password" in key.lower() or "secret" in key.lower() or "token" in key.lower():
                displayed = (str(val)[:8] + "..." + str(val)[-4:]) if len(str(val)) > 16 else ("***" if str(val).strip() else "(空)")
            elif isinstance(val, list):
                displayed = f"[{len(val)} 项]" if val else "[]"
            elif isinstance(val, dict):
                displayed = f"{{{len(val)} 字段}}"
            else:
                displayed = str(val)
            print(f"  {key}: {displayed}")
    else:
        for kv in args.kv:
            if "=" not in kv:
                print(f"⚠️ 跳过无效格式: {kv} (需要 key=value)")
                continue
            key, val = kv.split("=", 1)
            key = key.strip()
            existing = cfg.get(key)
            if isinstance(existing, bool):
                cfg[key] = val.lower() in ("true", "1", "yes")
            elif isinstance(existing, int):
                cfg[key] = int(val)
            elif isinstance(existing, float):
                cfg[key] = float(val)
            elif isinstance(existing, list):
                try:
                    cfg[key] = json.loads(val)
                except json.JSONDecodeError:
                    cfg[key] = [v.strip() for v in val.split(",") if v.strip()]
            elif isinstance(existing, dict):
                try:
                    cfg[key] = json.loads(val)
                except json.JSONDecodeError:
                    print(f"⚠️ 字典字段需要 JSON 格式")
                    continue
            else:
                cfg[key] = val
            print(f"  ✅ {key} = {cfg[key]}")
        c.json("POST", "/save_settings", cfg)
        print("✅ 配置已保存")


def cmd_logs(args, c: Client):
    """查看系统日志"""
    data = c.json("GET", "/logs")
    logs = data if isinstance(data, list) else data.get("logs", [])
    if args.tail:
        logs = logs[-int(args.tail):]
    print(fmt_logs(logs, "系统日志"))


def cmd_cookies(args, c: Client):
    """检查 Cookie 状态"""
    if args.action == "check":
        data = c.json("POST", "/settings/cookies/check")
        print(fmt_json(data))
    elif args.action == "status":
        data = c.json("GET", "/settings/cookies/status")
        print(fmt_json(data))


def cmd_sign(args, c: Client):
    """115 每日签到"""
    if args.action == "run":
        data = c.json("POST", "/settings/115/sign/run")
        print(f"✅ 签到结果: {json.dumps(data, ensure_ascii=False)}")
    elif args.action == "status":
        data = c.json("GET", "/settings/115/sign/status")
        print(fmt_json(data))


def cmd_tmdb(args, c: Client):
    """TMDB 搜索"""
    if args.action == "search":
        keyword = " ".join(args.keyword) if args.keyword else ""
        if not keyword:
            sys.exit("请指定搜索关键词")
        data = c.json("GET", "/tmdb/search", {"query": keyword, "page": args.page or 1})
        items = data if isinstance(data, list) else data.get("results", data.get("items", []))
        print(fmt_tmdb_items(items))

    elif args.action == "popular":
        data = c.json("GET", "/tmdb/popular", {"page": args.page or 1})
        items = data if isinstance(data, list) else data.get("results", data.get("items", []))
        print(fmt_tmdb_items(items))

    elif args.action == "trending":
        data = c.json("GET", "/tmdb/trending", {"page": args.page or 1})
        items = data if isinstance(data, list) else data.get("results", data.get("items", []))
        print(fmt_tmdb_items(items))

    elif args.action == "detail":
        if not args.tmdb_id:
            sys.exit("请指定 TMDB ID")
        data = c.json("GET", "/tmdb/detail", {"tmdb_id": int(args.tmdb_id[0])})
        print(fmt_json(data))

    elif args.action == "genres":
        data = c.json("GET", "/tmdb/genres")
        print(fmt_json(data))

    elif args.action == "discover":
        data = c.json("GET", "/tmdb/discover", {"page": args.page or 1})
        items = data if isinstance(data, list) else data.get("results", data.get("items", []))
        print(fmt_tmdb_items(items))


def cmd_monitor(args, c: Client):
    """文件夹监控管理"""
    if args.action == "list":
        cfg = c.json("GET", "/get_settings")
        tasks = cfg.get("monitor_tasks", [])
        if not tasks:
            print("未配置文件夹监控任务")
            return
        print(f"共 {len(tasks)} 个监控任务：")
        for t in tasks:
            name = str(t.get("name", "") or "").strip()
            path = str(t.get("scan_path", "") or "").strip()
            cron = t.get("cron_minutes", 0)
            enabled = "🟢" if t.get("enabled", True) else "🔴"
            print(f"  {enabled} {name}  (扫描: {path}, 周期: {cron}分钟)")

    elif args.action == "status":
        data = c.json("GET", "/monitor/status")
        running = data.get("running", False)
        current = data.get("current_task", "") or ""
        queued = data.get("queued", [])
        print(f"  运行中: {'🟢 是' if running else '⏸ 否'}")
        if current:
            print(f"  当前任务: {current}")
        if queued:
            print(f"  排队中: {', '.join(queued)}")

    elif args.action == "start":
        data = c.json("POST", "/monitor/start")
        print(f"✅ 监控已启动: {json.dumps(data, ensure_ascii=False)}")

    elif args.action == "stop":
        data = c.json("POST", "/monitor/stop")
        print(f"✅ 监控已停止: {json.dumps(data, ensure_ascii=False)}")

    elif args.action == "logs":
        data = c.json("GET", "/monitor/logs/tasks")
        print(fmt_json(data))


def cmd_tree(args, c: Client):
    """目录树同步"""
    if args.action == "run":
        data = c.json("POST", "/start")
        print(f"✅ 目录树同步已触发: {json.dumps(data, ensure_ascii=False)}")
    elif args.action == "status":
        data = c.json("GET", "/status-summary")
        main = data.get("main", {})
        running = main.get("running", False)
        progress = main.get("progress", {})
        print(f"  运行中: {'🟢 是' if running else '⏸ 否'}")
        if progress:
            step = progress.get("step", "") or ""
            detail = progress.get("detail", "") or ""
            pct = progress.get("percent", 0) or 0
            print(f"  步骤: {step}  ({pct}%)")
            if detail:
                print(f"  详情: {detail}")


def cmd_api(args, c: Client):
    """通用 API 调用"""
    method = args.method.upper()
    path = args.path
    body = None
    if args.body:
        try:
            body = json.loads(args.body)
        except json.JSONDecodeError:
            body = args.body
    resp = c.request(method, path, body)
    print(f"HTTP {resp.status_code}")
    print()
    try:
        print(fmt_json(resp.json()))
    except Exception:
        print(resp.text[:2000])


def cmd_providers(args, c: Client):
    """列出提供商"""
    data = c.json("GET", "/api/providers")
    print(fmt_providers(data))


# ── Main CLI ──────────────────────────────────────────────────────────────

def _build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="115",
        description="115 Media Hub CLI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    sp = p.add_subparsers(dest="command")

    # status
    sp.add_parser("status", help="系统状态")

    # version
    sp.add_parser("version", help="版本信息")

    # search
    sp_search = sp.add_parser("search", help="搜索资源")
    sp_search.add_argument("keyword", nargs="+", help="搜索关键词")

    # channels
    sp_ch = sp.add_parser("channels", help="管理资源频道")
    sp_ch.add_argument("action", choices=["sync", "list"], help="sync=同步频道, list=列出频道")
    sp_ch.add_argument("--force", action="store_true", help="强制重新同步")

    # subscribe
    sp_sub = sp.add_parser("subscribe", help="管理订阅")
    sp_sub.add_argument("action", choices=["list", "add", "remove", "start", "stop", "status", "logs"])
    sp_sub.add_argument("name", nargs="*", help="订阅名称 (add/remove/start)")
    sp_sub.add_argument("--type", default="movie", choices=["movie", "tv"], help="媒体类型")
    sp_sub.add_argument("--quality", default="balanced", help="质量偏好 (4K/1080p/720p/balanced)")
    sp_sub.add_argument("--savepath", default="/电影", help="115 保存路径")
    sp_sub.add_argument("--provider", default="115", choices=["115", "quark"], help="网盘提供商")

    # jobs
    sp_jobs = sp.add_parser("jobs", help="管理资源任务")
    sp_jobs.add_argument("action", choices=["list", "clear", "clear_completed", "clear-completed", "retry"])
    sp_jobs.add_argument("job_id", nargs="*", help="任务 ID (retry)")
    sp_jobs.add_argument("--limit", type=int, default=20, help="列表条数")
    sp_jobs.add_argument("--status", default="", help="过滤状态 (pending/submitted/completed/failed)")

    # settings
    sp_set = sp.add_parser("settings", help="查看/修改配置")
    sp_set.add_argument("kv", nargs="*", help='key=value (例如 cookie_115="xxx")')

    # logs
    sp_logs = sp.add_parser("logs", help="查看系统日志")
    sp_logs.add_argument("tail", nargs="?", type=int, default=0, help="只显示最后 N 条")

    # cookies
    sp_cookies = sp.add_parser("cookies", help="检查 Cookie 状态")
    sp_cookies.add_argument("action", choices=["check", "status"], help="check=检测, status=查看缓存状态")

    # sign
    sp_sign = sp.add_parser("sign", help="115 每日签到")
    sp_sign.add_argument("action", choices=["run", "status"])

    # tmdb
    sp_tmdb = sp.add_parser("tmdb", help="TMDB 搜索")
    sp_tmdb.add_argument("action", choices=["search", "popular", "trending", "detail", "genres", "discover"])
    sp_tmdb.add_argument("keyword", nargs="*", help="搜索关键词 (search)")
    sp_tmdb.add_argument("tmdb_id", nargs="*", help="TMDB ID (detail)")
    sp_tmdb.add_argument("--page", type=int, default=1, help="页码")

    # monitor
    sp_mon = sp.add_parser("monitor", help="文件夹监控管理")
    sp_mon.add_argument("action", choices=["list", "status", "start", "stop", "logs"])

    # tree
    sp_tree = sp.add_parser("tree", help="目录树同步")
    sp_tree.add_argument("action", choices=["run", "status"])

    # api
    sp_api = sp.add_parser("api", help="通用 API 调用")
    sp_api.add_argument("method", help="HTTP 方法 (GET/POST)")
    sp_api.add_argument("path", help="API 路径 (如 /resource/state)")
    sp_api.add_argument("body", nargs="?", help='JSON 请求体 (如 \'{"key":"val"}\')')

    # providers
    sp.add_parser("providers", help="列出网盘提供商")

    return p


def main():
    parser = _build_parser()
    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    c = Client()

    dispatch = {
        "status": cmd_status,
        "version": cmd_version,
        "search": cmd_search,
        "channels": cmd_channels,
        "subscribe": cmd_subscribe,
        "jobs": cmd_jobs,
        "settings": cmd_settings,
        "logs": cmd_logs,
        "cookies": cmd_cookies,
        "sign": cmd_sign,
        "tmdb": cmd_tmdb,
        "monitor": cmd_monitor,
        "tree": cmd_tree,
        "api": cmd_api,
        "providers": cmd_providers,
    }

    handler = dispatch.get(args.command)
    if handler:
        handler(args, c)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()