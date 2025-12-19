# Root Cause Analysis Investigation Checklist

Use this checklist to ensure systematic, thorough RCA investigation. Check off items as you complete them.

## Phase 1: Initial Information Gathering

- [ ] Capture alert or issue details
  - [ ] Alert name and severity
  - [ ] Time alert fired
  - [ ] Affected systems/services
  - [ ] Alert message and description

- [ ] Collect error information
  - [ ] Error messages from logs
  - [ ] Stack traces (full, not truncated)
  - [ ] Error counts and rates
  - [ ] First occurrence timestamp

- [ ] Gather user reports
  - [ ] User-facing symptoms
  - [ ] Affected user segments
  - [ ] Reproduction steps if available

- [ ] Query relevant metrics
  - [ ] Error rate metrics
  - [ ] Latency percentiles (p50, p95, p99)
  - [ ] Resource utilization (CPU, memory, disk)
  - [ ] Request rate/throughput
  - [ ] Dependency health metrics

## Phase 2: Scope and Impact Assessment

- [ ] Determine affected scope
  - [ ] Which services are impacted?
  - [ ] Which endpoints/features broken?
  - [ ] Which geographic regions affected?
  - [ ] Percentage of requests failing

- [ ] Assess severity
  - [ ] Number of users impacted
  - [ ] Business impact (revenue, SLA breach)
  - [ ] Severity classification (P0/P1/P2/P3)

- [ ] Determine duration
  - [ ] Incident start time
  - [ ] Current status (ongoing/resolved)
  - [ ] Resolution time (if resolved)
  - [ ] Total duration

- [ ] Check for recurrence
  - [ ] Has this happened before?
  - [ ] Is this a new issue or regression?
  - [ ] Frequency pattern (one-time, periodic, continuous)

## Phase 3: Timeline Construction

- [ ] Identify incident start
  - [ ] First error in logs
  - [ ] First metric anomaly
  - [ ] First user report

- [ ] Map recent changes
  - [ ] Deployments in last 24 hours
  - [ ] Configuration changes
  - [ ] Infrastructure changes
  - [ ] Dependency updates
  - [ ] Feature flag changes

- [ ] Note detection and response
  - [ ] When alert fired
  - [ ] When team notified
  - [ ] When investigation started
  - [ ] When mitigation applied

- [ ] Identify resolution (if applicable)
  - [ ] When issue resolved
  - [ ] What action resolved it
  - [ ] Current status

- [ ] Create visual timeline
  - [ ] Plot all events chronologically
  - [ ] Highlight correlations between changes and symptoms
  - [ ] Mark key milestones

## Phase 4: Code Investigation

- [ ] Search for error messages
  - [ ] Grep codebase for error strings
  - [ ] Find where errors are raised
  - [ ] Identify error-handling paths

- [ ] Locate relevant code
  - [ ] Find files mentioned in stack traces
  - [ ] Locate affected API endpoints
  - [ ] Identify service entry points
  - [ ] Find data access layer code

- [ ] Search for related patterns
  - [ ] Database query code
  - [ ] External API calls
  - [ ] Cache operations
  - [ ] Authentication/authorization logic

- [ ] Review code context
  - [ ] Read surrounding code for context
  - [ ] Check error handling completeness
  - [ ] Look for edge cases
  - [ ] Identify assumptions in code

## Phase 5: Git History Analysis

- [ ] Find recent commits
  - [ ] `git log` on affected files
  - [ ] Commits in time window before incident
  - [ ] Authors of recent changes

- [ ] Use git blame
  - [ ] Blame lines mentioned in stack traces
  - [ ] Blame suspicious configuration values
  - [ ] Check when problematic code was added

- [ ] Review commit diffs
  - [ ] `git diff` for recent commits
  - [ ] Compare working vs broken versions
  - [ ] Look for logical errors in changes

- [ ] Check deployment correlation
  - [ ] Match commit times with deployment times
  - [ ] Correlate deployments with incident start
  - [ ] Identify which deployment introduced issue

- [ ] Consider using git bisect
  - [ ] If issue is regression
  - [ ] Binary search to find breaking commit
  - [ ] Automated test to verify regression

## Phase 6: Dependency and Infrastructure Review

- [ ] Check third-party dependencies
  - [ ] External API status pages
  - [ ] Third-party service health
  - [ ] API rate limits or quotas
  - [ ] Authentication token status

- [ ] Review infrastructure health
  - [ ] Instance count and health
  - [ ] Resource limits (CPU, memory, disk)
  - [ ] Network connectivity
  - [ ] Load balancer configuration
  - [ ] Auto-scaling events

- [ ] Check database health
  - [ ] Database query performance
  - [ ] Connection pool status
  - [ ] Database CPU/memory usage
  - [ ] Slow query log
  - [ ] Index usage

- [ ] Review message queues
  - [ ] Queue depth and lag
  - [ ] Consumer health
  - [ ] Poison messages
  - [ ] Processing rates

## Phase 7: Correlation and Analysis

- [ ] Apply Five Whys technique
  - [ ] Why did symptom occur? (surface level)
  - [ ] Why did that happen? (one level deeper)
  - [ ] Why did that happen? (two levels deeper)
  - [ ] Why did that happen? (three levels deeper)
  - [ ] Why did that happen? (root cause)

- [ ] Correlate timeline events
  - [ ] Do changes align with incident start?
  - [ ] Is there temporal correlation?
  - [ ] Which change is most suspicious?

- [ ] Analyze metrics patterns
  - [ ] Sudden spike or gradual degradation?
  - [ ] Which metrics correlate?
  - [ ] Leading vs lagging indicators
  - [ ] Anomaly detection insights

- [ ] Consider multiple hypotheses
  - [ ] List possible root causes
  - [ ] Rank by likelihood and evidence
  - [ ] Test each hypothesis

## Phase 8: Root Cause Identification

- [ ] Formulate root cause hypothesis
  - [ ] Specific code, config, or infrastructure change
  - [ ] Explanation of why it caused symptoms
  - [ ] Mechanism of failure

- [ ] Verify hypothesis is specific
  - [ ] Not vague ("code is buggy")
  - [ ] Points to exact file, line, or configuration
  - [ ] Explains causal mechanism

- [ ] Ensure it's actionable
  - [ ] Can be fixed with concrete changes
  - [ ] Solution is clear
  - [ ] Prevention strategies exist

- [ ] Validate with evidence
  - [ ] Supported by timeline correlation
  - [ ] Consistent with logs and metrics
  - [ ] Explains all symptoms
  - [ ] No contradicting evidence

## Phase 9: Hypothesis Testing

- [ ] Review supporting evidence
  - [ ] Timeline alignment
  - [ ] Metric correlations
  - [ ] Log patterns
  - [ ] Code analysis

- [ ] Check for counter-evidence
  - [ ] Are there cases where hypothesis doesn't fit?
  - [ ] Are there unexplained symptoms?
  - [ ] Is timeline correlation coincidental?

- [ ] Consider alternative explanations
  - [ ] Are there other plausible causes?
  - [ ] How do alternatives explain evidence?
  - [ ] Which explanation is most likely?

- [ ] Test if possible
  - [ ] Can root cause be reproduced in staging?
  - [ ] Would reverting change fix the issue?
  - [ ] Does fix address symptoms?

## Phase 10: Documentation

- [ ] Write RCA report summary
  - [ ] One-paragraph incident overview
  - [ ] Clear root cause statement
  - [ ] Impact summary

- [ ] Document complete timeline
  - [ ] Chronological event sequence
  - [ ] Highlighted correlations
  - [ ] Key milestones marked

- [ ] Detail root cause
  - [ ] Specific file, commit, or configuration
  - [ ] Code snippets or diffs
  - [ ] Explanation of mechanism
  - [ ] Why it wasn't caught earlier

- [ ] Provide evidence
  - [ ] Metric graphs
  - [ ] Relevant log excerpts
  - [ ] Commit information
  - [ ] Timeline correlation

- [ ] Suggest remediation
  - [ ] Immediate fix
  - [ ] Long-term solution
  - [ ] Prevention strategies
  - [ ] Monitoring improvements

- [ ] Add lessons learned
  - [ ] What went well
  - [ ] What could improve
  - [ ] Process changes needed
  - [ ] Technical debt identified

## Quality Checks

Before finalizing RCA, verify:

- [ ] Root cause is specific, not vague
- [ ] Evidence supports conclusion
- [ ] Timeline correlation is clear
- [ ] All symptoms are explained
- [ ] Fix addresses root cause (not just symptoms)
- [ ] Prevention strategies identified
- [ ] Report is clear and complete

## Common Pitfalls to Avoid

- [ ] Stopping at symptoms instead of drilling to root cause
- [ ] Jumping to conclusions without evidence
- [ ] Ignoring timeline correlations
- [ ] Blaming individuals instead of systems
- [ ] Incomplete documentation
- [ ] Not identifying prevention strategies
- [ ] Treating correlation as causation without validation
- [ ] Overlooking multiple contributing factors

## Follow-Up Actions

- [ ] Share RCA report with team
- [ ] Create tickets for remediation work
- [ ] Implement fixes
- [ ] Improve monitoring and alerting
- [ ] Update runbooks
- [ ] Schedule post-mortem meeting if needed
- [ ] Track action items to completion

---

Use this checklist to maintain rigor and completeness in RCA investigations. Adapt as needed for your specific context.
