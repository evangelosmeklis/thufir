#!/usr/bin/env python3
"""
Prometheus MCP Server

Provides MCP tools for querying Prometheus metrics and alerts.
Used by the thufir plugin for root cause analysis.
"""

import os
import sys
import json
import asyncio
from datetime import datetime
from typing import Any, Dict, List
import httpx

# MCP protocol implementation
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

# Configuration from environment
PROMETHEUS_URL = os.getenv("PROMETHEUS_URL", "http://localhost:9090")
PROMETHEUS_TOKEN = os.getenv("PROMETHEUS_TOKEN", "")

app = Server("prometheus")


@app.list_tools()
async def list_tools() -> List[Tool]:
    """List available Prometheus tools."""
    return [
        Tool(
            name="prometheus_query",
            description="Execute an instant Prometheus query at a single point in time",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "PromQL query expression (e.g., 'rate(http_requests_total[5m])')"
                    },
                    "time": {
                        "type": "string",
                        "description": "Optional evaluation timestamp in RFC3339 format (default: now)"
                    }
                },
                "required": ["query"]
            }
        ),
        Tool(
            name="prometheus_query_range",
            description="Execute a Prometheus query over a time range to get time-series data",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "PromQL query expression"
                    },
                    "start": {
                        "type": "string",
                        "description": "Start timestamp in RFC3339 format (e.g., '2025-12-19T14:00:00Z')"
                    },
                    "end": {
                        "type": "string",
                        "description": "End timestamp in RFC3339 format (e.g., '2025-12-19T16:00:00Z')"
                    },
                    "step": {
                        "type": "string",
                        "description": "Query resolution step width (e.g., '15s', '1m', '5m')",
                        "default": "15s"
                    }
                },
                "required": ["query", "start", "end"]
            }
        ),
        Tool(
            name="prometheus_labels",
            description="Get all label names or values for a specific label",
            inputSchema={
                "type": "object",
                "properties": {
                    "label": {
                        "type": "string",
                        "description": "Optional label name to get values for (omit to get all label names)"
                    },
                    "start": {
                        "type": "string",
                        "description": "Start timestamp in RFC3339 format"
                    },
                    "end": {
                        "type": "string",
                        "description": "End timestamp in RFC3339 format"
                    }
                }
            }
        ),
        Tool(
            name="prometheus_series",
            description="Find time series matching label selectors",
            inputSchema={
                "type": "object",
                "properties": {
                    "match": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "Series selector matchers (e.g., ['http_requests_total{status=\"500\"}'])"
                    },
                    "start": {
                        "type": "string",
                        "description": "Start timestamp in RFC3339 format"
                    },
                    "end": {
                        "type": "string",
                        "description": "End timestamp in RFC3339 format"
                    }
                },
                "required": ["match"]
            }
        ),
        Tool(
            name="prometheus_alerts",
            description="Get currently active Prometheus alerts",
            inputSchema={
                "type": "object",
                "properties": {}
            }
        )
    ]


@app.call_tool()
async def call_tool(name: str, arguments: Any) -> List[TextContent]:
    """Handle tool calls."""

    headers = {}
    if PROMETHEUS_TOKEN:
        headers["Authorization"] = f"Bearer {PROMETHEUS_TOKEN}"

    async with httpx.AsyncClient(timeout=30.0) as client:
        try:
            if name == "prometheus_query":
                params = {"query": arguments["query"]}
                if "time" in arguments:
                    params["time"] = arguments["time"]

                response = await client.get(
                    f"{PROMETHEUS_URL}/api/v1/query",
                    params=params,
                    headers=headers
                )
                response.raise_for_status()
                data = response.json()

                return [TextContent(
                    type="text",
                    text=json.dumps(data, indent=2)
                )]

            elif name == "prometheus_query_range":
                params = {
                    "query": arguments["query"],
                    "start": arguments["start"],
                    "end": arguments["end"],
                    "step": arguments.get("step", "15s")
                }

                response = await client.get(
                    f"{PROMETHEUS_URL}/api/v1/query_range",
                    params=params,
                    headers=headers
                )
                response.raise_for_status()
                data = response.json()

                return [TextContent(
                    type="text",
                    text=json.dumps(data, indent=2)
                )]

            elif name == "prometheus_labels":
                if "label" in arguments and arguments["label"]:
                    # Get values for specific label
                    endpoint = f"/api/v1/label/{arguments['label']}/values"
                else:
                    # Get all label names
                    endpoint = "/api/v1/labels"

                params = {}
                if "start" in arguments:
                    params["start"] = arguments["start"]
                if "end" in arguments:
                    params["end"] = arguments["end"]

                response = await client.get(
                    f"{PROMETHEUS_URL}{endpoint}",
                    params=params,
                    headers=headers
                )
                response.raise_for_status()
                data = response.json()

                return [TextContent(
                    type="text",
                    text=json.dumps(data, indent=2)
                )]

            elif name == "prometheus_series":
                params = {
                    "match[]": arguments["match"]
                }
                if "start" in arguments:
                    params["start"] = arguments["start"]
                if "end" in arguments:
                    params["end"] = arguments["end"]

                response = await client.get(
                    f"{PROMETHEUS_URL}/api/v1/series",
                    params=params,
                    headers=headers
                )
                response.raise_for_status()
                data = response.json()

                return [TextContent(
                    type="text",
                    text=json.dumps(data, indent=2)
                )]

            elif name == "prometheus_alerts":
                response = await client.get(
                    f"{PROMETHEUS_URL}/api/v1/alerts",
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
                text=f"Prometheus API error: {e.response.status_code} - {e.response.text}"
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
