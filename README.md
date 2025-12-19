# Thufir - AI-Powered Root Cause Analysis

Autonomous root cause analysis for production incidents. Integrates with Prometheus, GitHub, and GitLab to investigate alerts, analyze metrics, search code, and generate comprehensive RCA reports.

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

**Investigate an alert:**
```bash
/rca:analyze-prometheus HighErrorRate
```

**Analyze a GitHub issue:**
```bash
/rca:analyze-github 456
```

**Analyze a GitLab issue:**
```bash
/rca:analyze-gitlab 789
```

**Interactive wizard:**
```bash
/rca:investigate
```

**Or just mention the problem:**
```
"We're seeing 500 errors in production"
```
→ The RCA agent automatically investigates and generates a report

## What It Does

1. **Fetches** alert/issue details from Prometheus/GitHub/GitLab
2. **Queries** metrics to understand patterns
3. **Searches** your codebase for related code
4. **Analyzes** git history to find recent changes
5. **Correlates** timeline of commits with incident
6. **Identifies** root cause using Five Whys methodology
7. **Generates** professional RCA report in markdown

## Features

- ✅ **Autonomous investigation** - AI agent handles end-to-end RCA
- ✅ **Multi-source integration** - Prometheus, GitHub, GitLab
- ✅ **Metric analysis** - 100+ PromQL query patterns included
- ✅ **Code forensics** - Grep, blame, bisect workflows
- ✅ **Evidence-based** - Correlates metrics + code + git history
- ✅ **Professional reports** - Timeline, evidence, recommendations

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

## Help

**Installation issues:**
```bash
# Verify plugin loaded
/plugin

# Check MCP servers
/mcp
```

**Configuration issues:**
- Check `.claude/thufir.local.md` has correct tokens
- Verify endpoint URLs are accessible
- Ensure tokens have required permissions

**Agent not triggering:**
- Use explicit commands: `/rca:analyze-prometheus`
- Or clear trigger phrases: "investigate this production error"

## Links

- **Repository**: https://github.com/evangelosmeklis/thufir
- **Issues**: https://github.com/evangelosmeklis/thufir/issues
- **License**: MIT

---

**Made with [Claude Code](https://claude.com/claude-code)**
