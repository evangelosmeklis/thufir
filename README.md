# Thufir - AI-Powered Root Cause Analysis

Autonomous root cause analysis for production incidents. Integrates with Prometheus, GitHub, and GitLab to investigate alerts, analyze metrics, search code, and generate comprehensive RCA reports.

![Thufir in action](media/Screenshot%202025-12-20%20at%2012.03.32.png)

## Quick Install

### From Marketplace (Recommended)

```bash
# Add the marketplace
/plugin marketplace add evangelosmeklis/thufir
```

### From GitHub

```bash
git clone https://github.com/evangelosmeklis/thufir.git
cc --plugin-dir ./thufir
```

## Quick Start

### 1. Configure (Optional)

Create `.claude/thufir.local.md`:

```yaml
---
prometheus:
  endpoint: "https://prometheus.example.com"

github:
  token: "ghp_your_token"
  default_repo: "owner/repo"

gitlab:
  token: "glpat_your_token"
  default_project: "group/project"
---
```

**Get tokens:**
- GitHub: https://github.com/settings/tokens (needs `repo` scope)
- GitLab: https://gitlab.com/-/profile/personal_access_tokens (needs `api` scope)

### 2. Use It

** Just write this in claude code**
```bash
/thufir
```
and a drop down will appear 

## Example Output

```markdown
# Root Cause Analysis Report
Date: 2025-12-19
Alert: HighErrorRate - api-service

## Summary
95% error rate at 14:32 UTC due to database connection pool exhaustion

## Root Cause
File: src/database/connection.js:45
Commit: abc123 by John Doe on 2025-12-19
Issue: Connection pool reduced from 100 to 10 connections

## Fix
Revert pool size change or increase based on load testing
```

## Requirements

- Claude Code CLI
- Git repository (for code analysis)
- Optional: Prometheus endpoint, GitHub/GitLab tokens

---

**Made with [Claude Code](https://claude.com/claude-code)** with ❤️ in Athens, Greece 
