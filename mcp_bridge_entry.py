#!/usr/bin/env python3
"""
115-media-hub MCP Bridge — entry point for Claude Desktop.

Dynamically exposes all 100+ API endpoints as MCP tools.

Claude Desktop config:
    "mcpServers": {
        "115-media-hub": {
            "command": "docker",
            "args": ["exec", "-i", "115-media-hub", "python3", "/app/mcp_bridge_entry.py"]
        }
    }
"""

import sys
import os

_project_root = os.path.dirname(os.path.abspath(__file__))
if _project_root not in sys.path:
    sys.path.insert(0, _project_root)

from app.mcp_bridge import main

main()