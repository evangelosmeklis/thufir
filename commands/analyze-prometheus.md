---
name: analyze-prometheus
description: Analyze a Prometheus alert to perform root cause analysis
argument-hint: "[alert-name or alert-json]"
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash
  - AskUserQuestion
  - Write
---

# Analyze Prometheus Alert Command

## Purpose

Investigate a Prometheus alert by fetching alert details, querying related metrics, searching the codebase for relevant code, analyzing git history, and generating a root cause analysis report.

## Instructions for Claude

When this command is invoked, perform comprehensive root cause analysis for a Prometheus alert:

### Step 1: Gather Alert Information

**If user provided alert name**:
1. Use prometheus MCP tool to fetch alert details
2. Extract alert expression, labels, severity, and active time

**If user provided alert JSON**:
1. Parse the alert JSON
2. Extract key fields: alertname, expr, labels, annotations, activeAt

**If no argument provided**:
1. Use AskUserQuestion to ask:
   - "What is the alert name?"
   - Or "Please paste the alert JSON"
2. Fetch or parse accordingly

**Extract from alert**:
- Alert name
- PromQL expression that triggered
- Threshold value
- Time alert started firing
- Affected labels (service, instance, job, etc.)
- Alert severity
- Alert annotations (description, summary)

### Step 2: Query Prometheus Metrics

Use prometheus MCP tools to query related metrics:

1. **Execute alert expression** to see current value:
   - Query the alert's PromQL expression
   - Check how far above threshold the metric is

2. **Query metric over time** to see pattern:
   - Use query_range for last 2-6 hours
   - Identify: sudden spike, gradual increase, or other pattern

3. **Query breakdown metrics**:
   - Break down by labels (endpoint, instance, status code)
   - Identify which specific component is affected

4. **Query correlated metrics**:
   - Error rate metrics
   - Latency metrics (p95, p99)
   - Resource usage (CPU, memory)
   - Request rate metrics
   - Dependency health metrics

5. **Analyze metric patterns**:
   - When did anomaly start?
   - Sudden or gradual?
   - Correlated with other metric changes?

### Step 3: Search Codebase

Based on alert and metrics, search code for relevant files:

1. **From alert labels**, identify:
   - Service name
   - Endpoint or feature affected
   - Component mentioned in annotations

2. **Use Grep to search for**:
   - Error messages from alert annotations
   - Service names
   - Endpoint paths
   - Metric names used in alert

3. **Use Glob to find** relevant files:
   - Configuration files
   - Service implementation files
   - Database connection files
   - API endpoint files

4. **Read suspicious files** to understand code

### Step 4: Analyze Git History

Use Bash to run git commands:

1. **Determine investigation time window**:
   - Start: 6-24 hours before alert fired
   - End: When alert started

2. **List recent commits**:
```bash
git log --since="<time-window-start>" --until="<alert-start-time>" --oneline
```

3. **Check commits to affected files**:
```bash
git log --since="<time-window>" -- path/to/relevant/file.js
```

4. **For suspicious files, use git blame**:
```bash
git blame path/to/file.js | grep "suspicious code"
```

5. **Show commit details** for recent changes:
```bash
git show <commit-sha>
```

6. **Correlate commit timestamps** with alert start time

### Step 5: Identify Root Cause

Synthesize all evidence to identify root cause:

1. **Timeline correlation**:
   - When did metric anomaly start?
   - Were there deployments/commits just before?
   - Do timestamps align?

2. **Code analysis**:
   - What code changes were made?
   - Do changes affect the alerted metric?
   - Are there obvious bugs or config errors?

3. **Metric validation**:
   - Do metrics support the hypothesis?
   - Are there correlated metric changes?

4. **Apply Five Whys**:
   - Why did alert fire? → Metric exceeded threshold
   - Why did metric exceed threshold? → (dig deeper)
   - Continue until reaching root cause

5. **Identify specific root cause**:
   - File: exact file path
   - Line: specific line or section
   - Commit: SHA and author
   - Change: what was changed
   - Why: why it caused the alert

### Step 6: Generate RCA Report

Use Write tool to create RCA report:

1. **Create report file**: `rca-reports/prometheus-<alert-name>-<date>.md`

2. **Use RCA report template** from root-cause-analysis skill

3. **Include**:
   - **Summary**: Brief overview of alert and root cause
   - **Alert Details**: Name, expression, threshold, labels
   - **Timeline**: When alert fired, when anomaly started, recent commits
   - **Metrics Evidence**: Graphs or data showing metric pattern
   - **Root Cause**: Specific code/config change with commit SHA
   - **Evidence**: Git commit details, code diffs, metric correlations
   - **Suggested Fix**: How to resolve the issue
   - **Prevention**: How to prevent recurrence

4. **Output summary to console** for user

### Step 7: Suggest Next Steps

After generating report, suggest:
- Immediate mitigation (revert commit, adjust config, scale resources)
- Validation steps (test fix in staging, verify metrics recover)
- Prevention measures (add tests, improve monitoring, code review checklist)

## Example Invocations

**With alert name**:
```
/rca:analyze-prometheus HighErrorRate
```

**With alert JSON**:
```
/rca:analyze-prometheus {
  "labels": {"alertname": "HighErrorRate", "service": "api"},
  "annotations": {"summary": "Error rate above 5%"},
  "startsAt": "2025-12-19T14:32:00Z"
}
```

**Interactive** (no arguments):
```
/rca:analyze-prometheus
```
→ Prompts user for alert details

## Key Considerations

- **Load skills**: Activate prometheus-analysis, root-cause-analysis, and git-investigation skills as needed
- **Use MCP tools**: Leverage prometheus MCP server for metrics
- **Correlate timestamps**: Always align git commits with alert start time
- **Be specific**: Root cause should point to exact file/line/commit
- **Evidence-based**: Support conclusions with metrics and code
- **Actionable**: Provide clear fix and prevention steps

## Output

- Comprehensive RCA report saved to `rca-reports/` directory
- Console summary of findings
- Clear root cause identification
- Suggested remediation steps

---

Perform systematic, thorough root cause analysis that transforms a Prometheus alert into actionable insights with clear evidence and specific fixes.
