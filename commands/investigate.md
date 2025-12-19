---
name: investigate
description: Interactive wizard for general root cause analysis investigation
argument-hint: ""
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash
  - AskUserQuestion
  - Write
---

# Interactive RCA Investigation Command

## Purpose

Guide users through a comprehensive root cause analysis investigation via an interactive wizard. This command is flexible and works for any type of production incident, whether from Prometheus, GitHub, GitLab, or manual investigation.

## Instructions for Claude

When this command is invoked, guide the user through a systematic RCA investigation:

### Step 1: Gather Initial Information

Use AskUserQuestion to collect incident details:

**Question 1: Incident Source**
Ask: "How did you learn about this incident?"
Options:
- "Prometheus alert"
- "GitHub issue"
- "GitLab issue"
- "Manual detection (user report, logs, etc.)"

**Based on answer, branch**:
- If Prometheus: Delegate to `/rca:analyze-prometheus` command
- If GitHub: Delegate to `/rca:analyze-github` command
- If GitLab: Delegate to `/rca:analyze-gitlab` command
- If Manual: Continue with questions below

**Question 2: Basic Incident Info** (for manual investigations)
Ask user to provide:
- "What is the problem? (Brief description)"
- "When did it start? (Timestamp or approximate time)"
- "Is it still occurring?"

**Question 3: Symptoms**
Ask: "What symptoms are you seeing?"
Allow multi-select or free text:
- Error messages
- Performance degradation
- Service unavailability
- Data inconsistency
- Other (specify)

**Question 4: Impact**
Ask: "How severe is the impact?"
Options:
- "Critical - Major user impact"
- "High - Significant user impact"
- "Medium - Some users affected"
- "Low - Minor or no user impact"

### Step 2: Collect Error Details

Ask user for specific error information:

**Error Messages**:
- "Please paste any error messages, stack traces, or relevant logs"
- Parse and extract:
  - Error names
  - Stack traces (file paths and line numbers)
  - Error codes
  - Timestamps

**Affected Components**:
- "Which service, feature, or component is affected?"
- "Which API endpoints or pages are failing?"

**Scope**:
- "Is this affecting all users or specific segments?"
- "Are specific geographic regions affected?"

### Step 3: Search Codebase

Based on error information:

1. **Extract searchable terms**:
   - Error strings from logs
   - Service names
   - Endpoint paths
   - Component names

2. **Search for errors in code**:
```bash
grep -r "<error-string>" --include="*.js" --include="*.py" --include="*.go"
```

3. **Find relevant files**:
   - Use Glob to find files by pattern
   - Look in likely locations (src/, lib/, config/)

4. **Ask user**:
   - "I found the error in these files: [list]"
   - "Are any of these the main source of the issue?"

5. **Read suspicious files** to understand code

### Step 4: Analyze Git History

**Determine time window**:
- Use incident start time from Step 1
- Look 24-48 hours before incident

**List recent commits**:
```bash
git log --since="<window-start>" --until="<incident-time>" --oneline
```

**Show to user**:
- "Here are recent commits before the incident: [list]"
- "Do any of these look suspicious?"

**For suspicious commits**:
```bash
git show <commit-sha>
```

**If user identifies suspicious commit**:
- Review commit details
- Check what files changed
- Analyze diffs for bugs or config errors

**If user is unsure**:
- Focus on commits to affected files
- Look for configuration changes
- Check commits to error-related code

### Step 5: Check for Recent Changes

Ask user:
- "Were there any recent deployments?"
- "Any configuration changes?"
- "Any infrastructure changes (scaling, migrations, etc.)?"
- "Any dependency updates?"

**If yes to any**:
- Get details and timestamps
- Correlate with incident timeline
- Review changes for potential issues

### Step 6: Review Metrics (if available)

If Prometheus is configured:

Ask: "Do you want to check Prometheus metrics?"

If yes:
- "What metrics should we look at?"
  - Error rates
  - Latency
  - Resource usage (CPU, memory)
  - Request rates
  - Custom metrics

- Query relevant metrics around incident time
- Look for anomalies or spikes
- Correlate metric changes with incident timeline

### Step 7: Apply Five Whys

Guide user through Five Whys:

1. **Why 1**: "Why did the incident occur?"
   - Help user articulate surface-level cause

2. **Why 2**: "Why did [answer from Why 1] happen?"
   - Dig one level deeper

3. **Why 3**: "Why did [answer from Why 2] happen?"
   - Continue drilling down

4. **Why 4**: "Why did [answer from Why 3] happen?"
   - Getting closer to root cause

5. **Why 5**: "Why did [answer from Why 4] happen?"
   - Likely at or near root cause

**After Five Whys**:
- Synthesize to identify root cause
- Ensure it's specific and actionable

### Step 8: Identify Root Cause

Based on all gathered evidence:

1. **Summarize findings**:
   - Timeline of events
   - Error information
   - Code changes identified
   - Metric anomalies (if any)
   - Five Whys conclusion

2. **Propose root cause**:
   - Specific file and line (if applicable)
   - Commit SHA (if identified)
   - Configuration change
   - Infrastructure change
   - Or other specific cause

3. **Ask user to confirm**:
   - "Based on this evidence, the root cause appears to be: [summary]"
   - "Does this align with your understanding?"
   - "Is there anything else we should investigate?"

4. **Refine if needed** based on user feedback

### Step 9: Generate RCA Report

Once root cause is confirmed:

1. **Ask**: "Would you like me to generate an RCA report?"

2. **If yes, create report**:
   - File: `rca-reports/manual-investigation-<date>.md`
   - Use RCA report template
   - Include all gathered information:
     - Incident description
     - Timeline
     - Symptoms and impact
     - Error details
     - Code analysis
     - Git history findings
     - Metrics (if any)
     - Five Whys analysis
     - Root cause identification
     - Evidence supporting root cause

3. **Output summary to console**

### Step 10: Suggest Remediation

After report generation (or if user declines report):

1. **Immediate fix**:
   - Based on root cause, suggest fix
   - Revert commit, adjust config, hotfix, etc.

2. **Validation steps**:
   - How to verify fix works
   - What metrics or tests to check

3. **Prevention measures**:
   - Tests to add
   - Monitoring improvements
   - Process changes
   - Documentation updates

4. **Ask**: "Would you like help implementing any of these fixes?"

## Example Invocation

```
/rca:investigate
```

→ Starts interactive wizard that walks through all steps

## Flow Variations

**Quick path** (if user knows details):
- Fewer questions
- Jump directly to relevant investigation
- Still thorough but faster

**Deep path** (if user unsure):
- More questions
- More exploration
- More guidance through process

**Delegation** (if from standard source):
- Detect Prometheus/GitHub/GitLab
- Delegate to specialized command
- Return to wizard if needed

## Key Considerations

- **Be conversational**: Guide user naturally through process
- **Don't overwhelm**: Ask questions progressively, not all at once
- **Be flexible**: Adapt to user's knowledge level and situation
- **Provide context**: Explain why you're asking each question
- **Show findings**: Share what you discover as you investigate
- **Collaborate**: Treat it as partnership, not interrogation
- **Load skills**: Activate root-cause-analysis, git-investigation as needed
- **Use evidence**: Support conclusions with data
- **Be specific**: Root cause must be actionable

## Output

- Interactive Q&A guiding through investigation
- Code search results and git history
- Metrics analysis (if applicable)
- Five Whys analysis
- Root cause identification with evidence
- Optional RCA report
- Remediation suggestions

---

Provide a guided, interactive root cause analysis experience that systematically investigates incidents and identifies specific, actionable root causes.
