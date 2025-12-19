---
name: analyze-gitlab
description: Analyze a GitLab issue reporting a production incident to perform root cause analysis
argument-hint: "[issue-iid or issue-url]"
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash
  - AskUserQuestion
  - Write
---

# Analyze GitLab Issue Command

## Purpose

Investigate a GitLab issue reporting a production problem by fetching issue details, extracting error information, searching the codebase for related code, analyzing git history, and generating a root cause analysis report.

## Instructions for Claude

When this command is invoked, perform comprehensive root cause analysis for a GitLab issue:

### Step 1: Gather Issue Information

**If user provided issue IID** (internal ID):
1. Read settings from `.claude/thufir.local.md` to get default project
2. Use gitlab MCP tool to fetch issue details:
   - Tool: `gitlab_get_issue`
   - Parameters: `{issue_iid: <iid>}`

**If user provided issue URL**:
1. Parse URL to extract group, project, and issue IID
2. Use gitlab MCP tool with parsed values

**If no argument provided**:
1. Use AskUserQuestion to ask:
   - "What is the GitLab issue number (IID)?"
   - Or "What project? (leave blank for default from settings)"

**Extract from issue**:
- Issue IID and title
- Description
- Labels (look for "production", "incident", "priority::1", "bug")
- Created/updated timestamps
- Comments/notes (read for additional context)
- Assignees
- Related merge requests mentioned
- Milestones

### Step 2: Parse Error Information

From issue description and comments, extract:

1. **Error messages**:
   - Stack traces
   - Error names (e.g., "ConnectionPoolExhausted")
   - Error codes (500, 503, timeout, etc.)

2. **Reproduction details**:
   - Steps to reproduce
   - Affected features or endpoints
   - User actions that trigger error

3. **Impact information**:
   - When error first occurred (timestamp)
   - How many users affected
   - Frequency (one-time, intermittent, constant)
   - Geographic or segment-specific

4. **System context**:
   - Service or component mentioned
   - Environment (production, staging)
   - Browser or client information

**Parse patterns like**:
- "Users are getting 500 errors..."
- "Error: ConnectionPoolExhausted at 14:32 UTC"
- "Stack trace: ..."
- "Approximately 15,000 users affected"

### Step 3: Search Codebase for Related Code

Based on extracted error information:

1. **Search for error strings**:
```bash
# Use Grep to find error in codebase
grep -r "ConnectionPoolExhausted" --include="*.js" --include="*.py"
```

2. **Search for affected components**:
- If issue mentions "login", search for login-related files
- If mentions specific endpoint, find that endpoint code
- Use Glob to find relevant files by path pattern

3. **Find error-handling code**:
- Where is the error raised?
- What conditions trigger it?
- What code path leads to error?

4. **Identify relevant files**:
- Entry points (API routes, controllers)
- Business logic
- Database access layer
- External integrations
- Configuration files

5. **Read suspicious files** to understand implementation

### Step 4: Analyze Git History

Use Bash to run git commands:

1. **Determine time window**:
   - Start: 24-48 hours before error first occurred
   - End: When error was first reported

2. **List recent commits**:
```bash
git log --since="<window-start>" --until="<error-time>" --oneline
```

3. **Focus on affected files**:
```bash
git log --since="<window>" -- path/to/affected/file.js
```

4. **Use git blame on error location**:
- If stack trace includes file/line, blame that line
```bash
git blame -L <line>,<line> path/to/file.js
```

5. **Review recent commits to config files**:
```bash
git log --since="<window>" -- config/ "*.config.js" ".env*"
```

6. **Show commit details**:
```bash
git show <commit-sha>
```

7. **Check for deployment correlation**:
- Were there commits/merges around error time?
- Check deployment tags or main branch history

### Step 5: Check Related Merge Requests

If issue mentions merge requests or you find suspicious commits:

1. Use gitlab MCP tool to fetch merge request details
2. Review MR description, files changed, and discussion
3. Check if MR was merged around error time
4. Identify if MR introduced the bug

### Step 6: Correlate with Metrics (if available)

If Prometheus integration is configured:

1. Query metrics around error time:
   - Error rate metrics
   - Latency metrics
   - Resource utilization

2. Look for metric anomalies correlating with issue timestamp

3. Add metric evidence to RCA

### Step 7: Identify Root Cause

Synthesize all evidence:

1. **Timeline reconstruction**:
   - When did error first occur?
   - What commits were made before that?
   - Were there deployments or merges?

2. **Code analysis**:
   - What code could cause this error?
   - Were there recent changes to that code?
   - Do changes align with error symptoms?

3. **Apply Five Whys**:
   - Why are users seeing errors?
   - Why is that happening?
   - (Continue drilling down)

4. **Identify specific root cause**:
   - **File**: Exact file path
   - **Line**: Specific line or function
   - **Commit**: SHA, author, timestamp
   - **Change**: What was changed and why it broke
   - **Mechanism**: How the change causes the error
   - **MR**: Related merge request if applicable

### Step 8: Generate RCA Report

Use Write tool to create report:

1. **Create report file**: `rca-reports/gitlab-issue-<iid>-<date>.md`

2. **Use RCA report template**

3. **Include**:
   - **Summary**: Overview of issue and root cause
   - **Issue Details**: IID, title, labels, reporter, timestamp, project
   - **Error Information**: Error messages, stack traces, reproduction steps
   - **Impact**: Users affected, duration, severity
   - **Timeline**: When error started, commits, MRs, detection, resolution
   - **Root Cause**: Specific code/commit with evidence
   - **Code Evidence**: Git diffs, blame output, commit messages
   - **MR Evidence** (if applicable): Related merge request details
   - **Metrics Evidence** (if available): Error rate graphs, correlations
   - **Suggested Fix**: How to resolve
   - **Prevention**: How to prevent recurrence

4. **Link back to GitLab issue**: Include issue URL in report

### Step 9: Suggest Actions

After generating report, suggest:

1. **Immediate fix**:
   - Revert problematic commit/MR
   - Apply hotfix
   - Adjust configuration

2. **Validation**:
   - Test fix in staging
   - Verify error no longer occurs
   - Check metrics return to normal

3. **Communication**:
   - Update GitLab issue with findings
   - Notify affected users if needed

4. **Prevention**:
   - Add tests to catch this bug
   - Improve code review process
   - Add monitoring/alerting
   - Update documentation

5. **GitLab issue comment** (optional):
   - Ask if user wants to post RCA summary as issue comment

## Example Invocations

**With issue IID (uses default project from settings)**:
```
/rca:analyze-gitlab 456
```

**With full GitLab URL**:
```
/rca:analyze-gitlab https://gitlab.com/group/project/-/issues/456
```

**Interactive** (no arguments):
```
/rca:analyze-gitlab
```
→ Prompts for issue IID and project

## Key Considerations

- **Load skills**: Activate platform-integration, root-cause-analysis, and git-investigation skills
- **Use MCP tools**: Leverage gitlab MCP server for issue data
- **IID vs ID**: GitLab uses IID (internal ID) for issues, not global ID
- **Parse carefully**: Extract all error details from description and comments
- **Correlate timestamps**: Align git commits with error occurrence time
- **Be specific**: Root cause must point to exact code change
- **Evidence-based**: Support with code diffs and git history
- **Check settings**: Use default_project from `.claude/thufir.local.md`
- **Handle missing data**: If issue lacks error details, ask user for clarification
- **MR integration**: Check for related merge requests

## Output

- Comprehensive RCA report saved to `rca-reports/` directory
- Console summary of findings
- Clear root cause with code evidence
- Suggested fix and prevention steps
- Option to update GitLab issue with findings

---

Transform GitLab issue reports into detailed root cause analyses with specific code changes, clear evidence, and actionable remediation steps.
