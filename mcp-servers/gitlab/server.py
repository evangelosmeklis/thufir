#!/usr/bin/env python3
"""
GitLab MCP Server

Provides MCP tools for interacting with GitLab API for issues, merge requests, and commits.
Used by the thufir plugin for root cause analysis.
"""

import os
import sys
import json
import asyncio
from typing import Any, List
import httpx

# MCP protocol implementation
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

# Configuration from environment
GITLAB_URL = os.getenv("GITLAB_URL", "https://gitlab.com")
GITLAB_TOKEN = os.getenv("GITLAB_TOKEN", "")
GITLAB_PROJECT_ID = os.getenv("GITLAB_PROJECT_ID", "")

app = Server("gitlab")


@app.list_tools()
async def list_tools() -> List[Tool]:
    """List available GitLab tools."""
    return [
        Tool(
            name="gitlab_get_issue",
            description="Get details of a specific GitLab issue by IID (internal ID)",
            inputSchema={
                "type": "object",
                "properties": {
                    "issue_iid": {
                        "type": "integer",
                        "description": "Issue internal ID (IID)"
                    },
                    "project_id": {
                        "type": "string",
                        "description": "Optional project ID (defaults to configured project)"
                    }
                },
                "required": ["issue_iid"]
            }
        ),
        Tool(
            name="gitlab_list_issues",
            description="List issues in a GitLab project with optional filters",
            inputSchema={
                "type": "object",
                "properties": {
                    "project_id": {
                        "type": "string",
                        "description": "Optional project ID (defaults to configured project)"
                    },
                    "labels": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "Filter by labels (e.g., ['production', 'incident'])"
                    },
                    "state": {
                        "type": "string",
                        "enum": ["opened", "closed", "all"],
                        "description": "Issue state filter",
                        "default": "opened"
                    },
                    "created_after": {
                        "type": "string",
                        "description": "Filter issues created after this timestamp (ISO 8601)"
                    }
                }
            }
        ),
        Tool(
            name="gitlab_get_merge_request",
            description="Get details of a specific GitLab merge request by IID",
            inputSchema={
                "type": "object",
                "properties": {
                    "mr_iid": {
                        "type": "integer",
                        "description": "Merge request internal ID (IID)"
                    },
                    "project_id": {
                        "type": "string",
                        "description": "Optional project ID (defaults to configured project)"
                    }
                },
                "required": ["mr_iid"]
            }
        ),
        Tool(
            name="gitlab_list_commits",
            description="List commits in a GitLab project repository",
            inputSchema={
                "type": "object",
                "properties": {
                    "project_id": {
                        "type": "string",
                        "description": "Optional project ID (defaults to configured project)"
                    },
                    "since": {
                        "type": "string",
                        "description": "Only commits after this timestamp (ISO 8601)"
                    },
                    "until": {
                        "type": "string",
                        "description": "Only commits before this timestamp (ISO 8601)"
                    },
                    "path": {
                        "type": "string",
                        "description": "Filter commits by file path"
                    },
                    "ref_name": {
                        "type": "string",
                        "description": "Branch or tag name (default: default branch)",
                        "default": "main"
                    }
                }
            }
        ),
        Tool(
            name="gitlab_get_file_blame",
            description="Get git blame information for a specific file",
            inputSchema={
                "type": "object",
                "properties": {
                    "file_path": {
                        "type": "string",
                        "description": "Path to the file in repository"
                    },
                    "ref": {
                        "type": "string",
                        "description": "Branch, tag, or commit SHA",
                        "default": "main"
                    },
                    "project_id": {
                        "type": "string",
                        "description": "Optional project ID (defaults to configured project)"
                    }
                },
                "required": ["file_path"]
            }
        ),
        Tool(
            name="gitlab_search_code",
            description="Search for code in GitLab project",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Search query string"
                    },
                    "project_id": {
                        "type": "string",
                        "description": "Optional project ID (defaults to configured project)"
                    }
                },
                "required": ["query"]
            }
        )
    ]


@app.call_tool()
async def call_tool(name: str, arguments: Any) -> List[TextContent]:
    """Handle tool calls."""

    project_id = arguments.get("project_id", GITLAB_PROJECT_ID)
    if not project_id:
        return [TextContent(
            type="text",
            text="Error: No project_id provided and GITLAB_PROJECT_ID not configured"
        )]

    # URL encode project ID
    import urllib.parse
    project_id_encoded = urllib.parse.quote(str(project_id), safe='')

    headers = {
        "PRIVATE-TOKEN": GITLAB_TOKEN
    }

    async with httpx.AsyncClient(timeout=30.0) as client:
        try:
            if name == "gitlab_get_issue":
                issue_iid = arguments["issue_iid"]
                response = await client.get(
                    f"{GITLAB_URL}/api/v4/projects/{project_id_encoded}/issues/{issue_iid}",
                    headers=headers
                )
                response.raise_for_status()
                data = response.json()

                return [TextContent(
                    type="text",
                    text=json.dumps(data, indent=2)
                )]

            elif name == "gitlab_list_issues":
                params = {
                    "state": arguments.get("state", "opened")
                }
                if "labels" in arguments:
                    params["labels"] = ",".join(arguments["labels"])
                if "created_after" in arguments:
                    params["created_after"] = arguments["created_after"]

                response = await client.get(
                    f"{GITLAB_URL}/api/v4/projects/{project_id_encoded}/issues",
                    params=params,
                    headers=headers
                )
                response.raise_for_status()
                data = response.json()

                return [TextContent(
                    type="text",
                    text=json.dumps(data, indent=2)
                )]

            elif name == "gitlab_get_merge_request":
                mr_iid = arguments["mr_iid"]
                response = await client.get(
                    f"{GITLAB_URL}/api/v4/projects/{project_id_encoded}/merge_requests/{mr_iid}",
                    headers=headers
                )
                response.raise_for_status()
                data = response.json()

                return [TextContent(
                    type="text",
                    text=json.dumps(data, indent=2)
                )]

            elif name == "gitlab_list_commits":
                params = {
                    "ref_name": arguments.get("ref_name", "main")
                }
                if "since" in arguments:
                    params["since"] = arguments["since"]
                if "until" in arguments:
                    params["until"] = arguments["until"]
                if "path" in arguments:
                    params["path"] = arguments["path"]

                response = await client.get(
                    f"{GITLAB_URL}/api/v4/projects/{project_id_encoded}/repository/commits",
                    params=params,
                    headers=headers
                )
                response.raise_for_status()
                data = response.json()

                return [TextContent(
                    type="text",
                    text=json.dumps(data, indent=2)
                )]

            elif name == "gitlab_get_file_blame":
                import urllib.parse
                file_path_encoded = urllib.parse.quote(arguments["file_path"], safe='')
                params = {
                    "ref": arguments.get("ref", "main")
                }

                response = await client.get(
                    f"{GITLAB_URL}/api/v4/projects/{project_id_encoded}/repository/files/{file_path_encoded}/blame",
                    params=params,
                    headers=headers
                )
                response.raise_for_status()
                data = response.json()

                return [TextContent(
                    type="text",
                    text=json.dumps(data, indent=2)
                )]

            elif name == "gitlab_search_code":
                params = {
                    "scope": "blobs",
                    "search": arguments["query"]
                }

                response = await client.get(
                    f"{GITLAB_URL}/api/v4/projects/{project_id_encoded}/search",
                    params=params,
                    headers=headers
                )
                response.raise_for_status()
                data = response.json()

                return [TextContent(
                    type="text",
                    text=json.dumps(data, indent=2)
                )]

            else:
                return [TextContent(
                    type="text",
                    text=f"Unknown tool: {name}"
                )]

        except httpx.HTTPStatusError as e:
            return [TextContent(
                type="text",
                text=f"GitLab API error: {e.response.status_code} - {e.response.text}"
            )]
        except Exception as e:
            return [TextContent(
                type="text",
                text=f"Error: {str(e)}"
            )]


async def main():
    """Run the MCP server."""
    async with stdio_server() as (read_stream, write_stream):
        await app.run(read_stream, write_stream, app.create_initialization_options())


if __name__ == "__main__":
    asyncio.run(main())
