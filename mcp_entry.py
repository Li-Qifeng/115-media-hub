#!/usr/bin/env python3
"""
115-media-hub MCP Server — stdio entry point for Claude Desktop.

Add to Claude Desktop config:
    "mcpServers": {
        "115-media-hub": {
            "command": "python",
            "args": ["/vol1/1000/Code/115-media-hub/mcp_entry.py"]
        }
    }
"""

import sys
import os

# Ensure the project root is on sys.path so 'app' package can be found
_project_root = os.path.dirname(os.path.abspath(__file__))
if _project_root not in sys.path:
    sys.path.insert(0, _project_root)

from app.mcp_server import main

main()