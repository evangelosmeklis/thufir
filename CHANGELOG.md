# Changelog

All notable changes to the Thufir plugin will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2025-12-19

### Added

#### Core Features
- Initial release of Thufir root cause analysis plugin
- Autonomous RCA agent for end-to-end incident investigation
- Integration with Prometheus, GitHub, and GitLab

#### Skills (4 comprehensive skills)
- **root-cause-analysis**: Systematic RCA methodology with Five Whys technique
- **prometheus-analysis**: PromQL querying and metrics interpretation with 100+ query examples
- **platform-integration**: GitHub and GitLab API usage with complete examples
- **git-investigation**: Git blame, log, diff, and bisect workflows

#### Commands (4 user commands)
- `/rca:analyze-prometheus`: Analyze Prometheus alerts with metric correlation
- `/rca:analyze-github`: Analyze GitHub issues with code search and git history
- `/rca:analyze-gitlab`: Analyze GitLab issues with MR and commit tracking
- `/rca:investigate`: Interactive wizard for manual incident investigation

#### MCP Integrations (3 servers)
- Prometheus MCP server for metrics and alerts API
- GitHub MCP server (official) for repository and issue access
- GitLab MCP server for project and issue management

#### Documentation
- Comprehensive README with installation and usage
- Settings template with configuration examples
- RCA report template for standardized documentation
- Investigation checklists and workflow guides
- PromQL cookbook with production-ready queries
- Git aliases and automation scripts

### Features

#### Investigation Capabilities
- Automatic alert/issue fetching from multiple sources
- Metric querying and time-series analysis
- Codebase search with error correlation
- Git history analysis with blame and commit tracking
- Timeline reconstruction correlating changes with incidents
- Five Whys methodology for root cause identification
- Automated RCA report generation

#### Report Generation
- Professional markdown RCA reports
- Timeline visualization
- Evidence-based conclusions
- Code snippets with file/line references
- Metric graphs and correlations
- Actionable remediation recommendations
- Prevention strategies

### Developer Experience
- Progressive disclosure in skills (lean core + rich references)
- Interactive command workflows
- Autonomous agent triggering on production keywords
- Comprehensive error handling
- Security-first design (no hardcoded credentials)
- Example-driven documentation

### Quality & Standards
- Follows Claude Code plugin best practices
- Professional naming conventions (kebab-case)
- Complete YAML frontmatter for all components
- Modular skill organization
- Extensive inline documentation

## [Unreleased]

### Planned Features
- Slack/PagerDuty integration for alert notifications
- Kubernetes MCP server for container diagnostics
- AWS CloudWatch integration
- Automated incident timeline visualization
- ML-based anomaly detection suggestions
- Historical RCA database for pattern recognition

---

[1.0.0]: https://github.com/evangelosmeklis/thufir/releases/tag/v1.0.0
