"""
115-media-hub MCP Bridge — Auto-generate MCP tools from FastAPI routes.

Dynamically creates MCP tools for ALL API endpoints of the running
115-media-hub server via HTTP proxy to localhost:18080.
"""

import json
import os
import sys
from typing import Any, Dict, Optional

import httpx

_project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _project_root not in sys.path:
    sys.path.insert(0, _project_root)

from app.core import app
from fastapi.routing import APIRoute

from mcp.server.fastmcp import FastMCP

# ── API client (sync) ─────────────────────────────────────────────────────

API_BASE = "http://127.0.0.1:18080"
_CLIENT: Optional[httpx.Client] = None


def _get_client() -> httpx.Client:
    global _CLIENT
    if _CLIENT is None:
        _CLIENT = httpx.Client(base_url=API_BASE, timeout=30.0)
        resp = _CLIENT.post(
            "/login",
            json={"username": "admin", "password": "admin123"},
            follow_redirects=True,
        )
        resp.raise_for_status()
    return _CLIENT


def call_api(method: str, path: str, body: Optional[Dict[str, Any]] = None) -> str:
    client = _get_client()
    try:
        if method == "GET":
            resp = client.get(path, params=body)
        else:
            resp = client.post(path, json=body or {})
        resp.raise_for_status()
        data = resp.json()
        if isinstance(data, dict):
            return json.dumps(data, ensure_ascii=False, indent=2)
        return str(data)
    except httpx.HTTPStatusError as e:
        return f"Error {e.response.status_code}: {e.response.text[:500]}"
    except Exception as e:
        return f"Error: {e}"


# ── MCP Server ────────────────────────────────────────────────────────────

mcp = FastMCP(
    "115-media-hub",
    instructions="115 Media Hub 完整 API 桥接 — 覆盖全部功能",
)

# ── Tool factory ──────────────────────────────────────────────────────────


def _make_tool_name(path: str, method: str) -> str:
    """Convert /resource/state + GET → get_resource_state."""
    parts = [p.strip("/{}") for p in path.split("/") if p.strip("/{}")]
    parts = [p for p in parts if not p.startswith("{")]
    if not parts:
        parts = ["root"]
    name = "_".join(parts)
    for prefix in [
        "resource_", "subscription_", "monitor_", "settings_",
        "scraper_", "strm_", "tmdb_", "recommendation_",
    ]:
        if name.startswith(prefix):
            name = name[len(prefix):]
            break
    if method == "GET":
        name = f"get_{name}"
    return name[:60]


def _register_route_tool(path: str, method: str, summary: str, name: str):
    """Register a single route as an MCP tool."""

    # Use a closure factory to capture path/method properly
    def _handler(body: str = "{}") -> str:
        try:
            parsed = json.loads(body) if isinstance(body, str) else body
        except json.JSONDecodeError:
            return f"Invalid JSON: {body[:200]}"
        return call_api(method, path, parsed)

    _handler.__name__ = name
    _handler.__qualname__ = name

    mcp.tool(name=name, description=summary or f"{method} {path}")(_handler)


def _collect_and_register():
    """Collect all API routes from FastAPI app and register them as MCP tools."""
    count = 0
    for route in app.routes:
        if not isinstance(route, APIRoute):
            continue
        path = route.path
        if path in ("/login", "/", "/logout", "/favicon.ico"):
            continue
        methods = [m for m in (route.methods or set()) if m in ("GET", "POST")]
        methods.sort()
        for method in methods:
            summary = route.summary or route.description or ""
            name = _make_tool_name(path, method)
            _register_route_tool(path, method, summary, name)
            count += 1
    return count


_route_count = _collect_and_register()
print(f"[mcp_bridge] Registered {_route_count} tools", file=sys.stderr)


# ── Import hand-crafted tools from original mcp_server ────────────────────

try:
    from app.mcp_server import discover_media, subscribe_media, list_subscriptions, get_status  # noqa: F401
    print("[mcp_bridge] Also loaded 4 hand-crafted tools", file=sys.stderr)
except ImportError:
    pass


# ── Entry point ───────────────────────────────────────────────────────────

def main():
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()