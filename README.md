# Thufir - Root Cause Analysis Plugin

A comprehensive Claude Code plugin for investigating production incidents through automated root cause analysis. Integrates with Prometheus, GitHub, and GitLab to correlate alerts, errors, code changes, and commits.

## Features

- **Multi-source incident detection**: Analyze issues from Prometheus alerts, GitHub issues, or GitLab issues
- **Automated code investigation**: Search codebase for relevant code related to errors
- **Commit tracking**: Use git history to identify when and who introduced changes
- **Intelligent analysis**: AI-powered correlation between metrics, errors, and code changes
- **Actionable reports**: Generate detailed RCA reports with suggested fixes

## Installation

### As a local plugin

```bash
# Clone or copy this directory to your Claude plugins directory
cp -r . ~/.claude/plugins/thufir
```

### For project-specific use

```bash
# Use with --plugin-dir flag
cc --plugin-dir /path/to/thufir
```

## Prerequisites

- Claude Code CLI installed
- Access to Prometheus instance (optional)
- GitHub personal access token (optional)
- GitLab personal access token (optional)
- Git repository initialized in your project

## Configuration

Create a configuration file at `.claude/thufir.local.md` in your project:

```markdown
---
prometheus:
  endpoint: "https://prometheus.example.com"
  bearer_token: "optional-bearer-token"

github:
  token: "ghp_your_token_here"
  default_repo: "owner/repository"
  issue_labels: ["production", "incident"]

gitlab:
  token: "glpat_your_token_here"
  default_project: "group/project"
  issue_labels: ["production", "incident"]

analysis:
  commit_search_days: 30
  max_files_to_analyze: 50
  auto_save_reports: true
  reports_directory: "rca-reports"
---

# Thufir Configuration

This file configures the Thufir root cause analysis plugin.

## Prometheus Setup

Set your Prometheus endpoint and optional authentication token.

## GitHub Setup

Create a personal access token with `repo` scope at: https://github.com/settings/tokens

## GitLab Setup

Create a personal access token with `api` scope at: https://gitlab.com/-/profile/personal_access_tokens

## Analysis Preferences

- `commit_search_days`: How far back to search git history (default: 30 days)
- `max_files_to_analyze`: Maximum number of files to deep-dive (default: 50)
- `auto_save_reports`: Automatically save RCA reports to files (default: true)
- `reports_directory`: Where to save reports (default: rca-reports/)
```

## Usage

### Commands

#### Analyze Prometheus Alert

```bash
/rca:analyze-prometheus <alert-name>
```

Fetches alert details from Prometheus and performs root cause analysis.

#### Analyze GitHub Issue

```bash
/rca:analyze-github <issue-number>
# or
/rca:analyze-github https://github.com/owner/repo/issues/123
```

Analyzes a GitHub issue for production incidents.

#### Analyze GitLab Issue

```bash
/rca:analyze-gitlab <issue-number>
# or
/rca:analyze-gitlab https://gitlab.com/group/project/-/issues/123
```

Analyzes a GitLab issue for production incidents.

#### Interactive Investigation

```bash
/rca:investigate
```

Guided wizard for manual root cause analysis.

### Autonomous Agent

The RCA agent triggers automatically when you mention production issues:

```
"We have a production alert firing for high error rates"
"GitHub issue #456 reports users can't login"
"Need to investigate the outage from this morning"
```

## How It Works

1. **Issue Detection**: Fetches alert/issue details from Prometheus, GitHub, or GitLab
2. **Error Extraction**: Parses error messages, stack traces, and metrics
3. **Code Search**: Searches codebase for files, functions, and services related to the error
4. **Commit Analysis**: Uses git blame and log to identify recent changes
5. **Correlation**: Connects timeline of changes with error occurrence
6. **Report Generation**: Creates detailed RCA report with findings and suggested fixes

## Example Output

```markdown
# Root Cause Analysis Report
**Date**: 2025-12-19
**Alert**: HighErrorRate - api-service
**Duration**: 15 minutes

## Summary
The api-service experienced a 95% error rate starting at 14:32 UTC due to a database connection pool exhaustion.

## Timeline
- 14:30 UTC: Deploy of commit abc123
- 14:32 UTC: Error rate spike begins
- 14:35 UTC: Alert fires

## Root Cause
File: `src/database/connection.js:45`
Commit: `abc123` by John Doe on 2025-12-19

The connection pool size was reduced from 100 to 10 connections, causing exhaustion under normal load.

## Suggested Fix
Revert connection pool change or increase to appropriate size based on load testing.
```

## Troubleshooting

**MCP servers not connecting**:
- Verify tokens in `.claude/thufir.local.md`
- Check endpoint URLs are accessible
- Ensure tokens have correct permissions

**Agent not triggering**:
- Use explicit trigger phrases like "analyze this alert"
- Or use commands directly: `/rca:analyze-prometheus`

**No commits found**:
- Check `commit_search_days` setting
- Verify git repository is initialized
- Ensure git history exists

## License

MIT
