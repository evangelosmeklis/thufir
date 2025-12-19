# Thufir - AI-Powered Root Cause Analysis

**Transform production incidents into actionable insights with autonomous RCA.**

## 🎯 What is Thufir?

Thufir is an elite Site Reliability Engineer in plugin form. When production breaks, Thufir investigates the incident end-to-end: fetching alerts, analyzing metrics, searching code, tracing git history, and generating comprehensive RCA reports—all automatically.

## ✨ Key Features

### 🚨 Multi-Source Incident Detection
- **Prometheus Alerts**: Automatically analyze firing alerts with metric correlation
- **GitHub Issues**: Investigate production issues with code search and blame
- **GitLab Issues**: Track incidents through MRs and commit history
- **Manual Investigation**: Guided wizard for any incident type

### 🤖 Autonomous Investigation
- **RCA Agent**: Elite SRE agent that performs full investigation autonomously
- **Systematic Methodology**: Applies Five Whys and industry best practices
- **Evidence-Based**: Correlates metrics, code changes, and git history
- **Timeline Reconstruction**: Aligns deployments with incident occurrence

### 📊 Comprehensive Analysis
- **Metric Analysis**: Query Prometheus with 100+ pre-built PromQL patterns
- **Code Search**: Find error sources in codebase automatically
- **Git Investigation**: Use blame, log, diff, bisect to identify changes
- **Pattern Recognition**: Match incidents to common failure patterns

### 📝 Professional Reports
- **Auto-Generated**: Creates detailed RCA reports in markdown
- **Structured Format**: Timeline, evidence, root cause, recommendations
- **Actionable**: Includes immediate fixes and prevention strategies
- **Shareable**: Ready for stakeholder review and post-mortems

## 🎓 What You Get

### 4 Comprehensive Skills
1. **Root Cause Analysis**: Systematic RCA methodology with patterns
2. **Prometheus Analysis**: PromQL mastery with query cookbook
3. **Platform Integration**: GitHub/GitLab API expertise
4. **Git Investigation**: Advanced git forensics techniques

### 4 Powerful Commands
- `/rca:analyze-prometheus` - Analyze Prometheus alerts
- `/rca:analyze-github` - Investigate GitHub issues
- `/rca:analyze-gitlab` - Investigate GitLab issues
- `/rca:investigate` - Interactive RCA wizard

### 1 Autonomous Agent
- **rca-agent**: Triggers automatically on production keywords
- Performs 6-phase investigation process
- Generates complete RCA reports with evidence

### 3 MCP Integrations
- **Prometheus**: Metrics and alerting API
- **GitHub**: Repository and issue access (official server)
- **GitLab**: Project and commit tracking

## 🚀 Getting Started

### Quick Install

```bash
# Install from marketplace (coming soon)
cc plugin install thufir

# Or install from GitHub
git clone https://github.com/evangelosmeklis/thufir.git
cc --plugin-dir ./thufir
```

### Configure

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

### Use

```bash
# Investigate an alert
/rca:analyze-prometheus HighErrorRate

# Analyze a GitHub issue
/rca:analyze-github 456

# Or just mention the problem
"We're seeing 500 errors in production"
# → RCA agent triggers automatically
```

## 💡 Use Cases

### For SREs
- **Incident Response**: Rapid root cause identification during outages
- **Post-Mortems**: Auto-generate detailed RCA documentation
- **Pattern Recognition**: Learn from past incidents

### For DevOps Engineers
- **Deployment Issues**: Correlate code changes with failures
- **Performance Problems**: Analyze metric patterns and code
- **Configuration Errors**: Track config changes through git

### For Development Teams
- **Production Debugging**: Systematic investigation of prod issues
- **Knowledge Transfer**: Learn RCA best practices through AI
- **Documentation**: Generate professional incident reports

## 📈 Why Thufir?

### Before Thufir
1. ⏰ Manual alert investigation (30+ minutes)
2. 🔍 Searching logs and metrics separately
3. 📝 Writing RCA reports from scratch
4. 🤔 Guessing at root causes
5. 📊 Incomplete evidence gathering

### After Thufir
1. ✅ Autonomous investigation (5 minutes)
2. ✅ Automatic correlation of all data sources
3. ✅ Professional RCA reports generated
4. ✅ Evidence-based root cause identification
5. ✅ Comprehensive evidence with metrics, code, git

### Results
- **10x faster** incident investigation
- **100% coverage** of metrics, code, and git
- **Professional** documentation every time
- **Systematic** methodology prevents missed causes
- **Actionable** recommendations for prevention

## 🏆 Quality Standards

- ✅ Follows Claude Code plugin best practices
- ✅ Comprehensive documentation (30+ files)
- ✅ Production-ready code
- ✅ Security-first design
- ✅ MIT licensed open source
- ✅ Active maintenance

## 🔒 Security

- No hardcoded credentials
- Environment variable configuration
- Token-based authentication
- Supports read-only API access
- Excludes sensitive data from reports

## 📚 Rich Documentation

- **100+ PromQL queries** ready to use
- **Complete API examples** for GitHub/GitLab
- **RCA report templates** for consistency
- **Investigation checklists** for thoroughness
- **Git workflows** for forensics
- **Real-world patterns** from production

## 🤝 Support

- **GitHub Issues**: https://github.com/evangelosmeklis/thufir/issues
- **Documentation**: Comprehensive README and inline docs
- **Examples**: Working examples for all components
- **Community**: Open source MIT license

## 🎯 Perfect For

- ✅ SRE teams managing production systems
- ✅ DevOps engineers investigating deployments
- ✅ Development teams debugging production
- ✅ Anyone doing incident response
- ✅ Teams wanting to improve RCA processes

## 📦 What's Included

- 4 skills with 25+ reference files
- 4 commands for different incident sources
- 1 autonomous RCA agent
- 3 MCP server integrations
- Complete configuration templates
- Professional report templates
- Investigation checklists
- PromQL query library
- Git forensics tools
- API integration examples

---

**Transform your incident response with AI-powered root cause analysis.**

**Install Thufir today and never manually investigate production issues again.** 🚀
