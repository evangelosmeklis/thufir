# Root Cause Analysis Report

**Incident ID**: [e.g., INC-2025-001]
**Date**: [e.g., 2025-12-19]
**Investigator(s)**: [Name(s)]
**Status**: [Draft / Under Review / Final]

---

## Executive Summary

[One paragraph overview covering: what broke, when, impact, root cause, and resolution status]

**Example:**
> The api-service experienced a 95% error rate from 14:32 to 14:47 UTC on December 19, 2025, affecting approximately 15,000 users and causing login failures. The root cause was a database connection pool size reduction from 100 to 10 connections in commit `abc123`, deployed at 14:30 UTC. The issue was resolved by reverting the configuration change and redeploying at 14:47 UTC.

---

## Incident Overview

### Basic Information

| Field | Value |
|-------|-------|
| **Service/System** | [e.g., api-service] |
| **Incident Start** | [e.g., 2025-12-19 14:32 UTC] |
| **Detection Time** | [e.g., 2025-12-19 14:35 UTC] |
| **Resolution Time** | [e.g., 2025-12-19 14:47 UTC] |
| **Total Duration** | [e.g., 15 minutes] |
| **Severity** | [P0 / P1 / P2 / P3] |

### Impact

| Metric | Value |
|--------|-------|
| **Users Affected** | [e.g., ~15,000 users] |
| **Error Rate** | [e.g., 95% of requests] |
| **Geographic Scope** | [e.g., Global / US-East / etc.] |
| **Revenue Impact** | [e.g., Estimated $5,000 in lost transactions] |
| **SLA Breach** | [Yes / No] |

### Symptoms

- [Symptom 1: e.g., Users unable to log in]
- [Symptom 2: e.g., API returning 500 errors]
- [Symptom 3: e.g., Database connection timeout warnings]
- [Add more as needed]

---

## Timeline

Chronological sequence of events:

| Time (UTC) | Event | Type |
|------------|-------|------|
| 14:25 | Deployment pipeline started for version 2.3.1 | Change |
| 14:30 | Deployment completed, new version live | Change |
| 14:32 | Error rate begins spiking from 0.1% to 95% | Symptom |
| 14:33 | Database connection pool exhaustion warnings appear | Symptom |
| 14:35 | PagerDuty alert fires: "HighErrorRate - api-service" | Detection |
| 14:36 | On-call engineer acknowledges alert | Response |
| 14:38 | Investigation begins, checking recent deployments | Response |
| 14:42 | Connection pool configuration change identified in commit abc123 | Discovery |
| 14:44 | Decision made to revert deployment | Mitigation |
| 14:45 | Revert deployment initiated | Mitigation |
| 14:47 | Revert deployment completed | Mitigation |
| 14:48 | Error rate returns to baseline (0.1%) | Resolution |
| 14:50 | Incident declared resolved | Resolution |

**Key Correlation**: Deployment at 14:30 directly precedes error spike at 14:32 (2 minute lag)

---

## Root Cause

### Specific Cause

**File**: `src/config/database.js`
**Line**: 45
**Commit**: `abc123def456789` by [Developer Name] on 2025-12-19 at 10:15 UTC
**Change**: Connection pool size reduced from 100 to 10

```javascript
// Before (working)
const pool = new Pool({
  max: 100,  // Maximum number of connections
  min: 10
});

// After (broken)
const pool = new Pool({
  max: 10,   // Changed to 10 - CAUSE OF INCIDENT
  min: 10
});
```

### Mechanism of Failure

1. Connection pool size reduced from 100 to 10 connections
2. Normal production load requires ~80-90 concurrent database connections during peak traffic
3. With only 10 connections available, pool exhausted immediately
4. New requests waited for available connections, timing out after 5 seconds
5. Timeouts resulted in 500 errors returned to users
6. Error rate spiked to 95% as connection pool could not service demand

### Why Root Cause Wasn't Caught Earlier

- **Code Review**: Change was part of larger refactoring; reviewer missed significance of pool size change
- **Testing**: Staging environment has lower traffic, didn't expose pool exhaustion
- **Monitoring**: No pre-deployment validation of connection pool sizing vs. expected load
- **Gradual Rollout**: Change deployed to all instances simultaneously (no canary)

---

## Supporting Evidence

### Metrics

**Error Rate Graph**:
```
Error Rate (%)
100 |                    ╭──╮
 90 |                   ╭╯  ╰╮
 80 |                  ╭╯    ╰╮
    |                 ╭╯      ╰╮
  0 |─────────────────╯        ╰─────────
    14:25   14:30   14:35   14:45   14:50
            ↑                 ↑
         Deploy          Revert
```

**Database Connection Pool Usage**:
```
Connections
100 |
 90 |╭──────────────────╮
 80 |│ ████████████████ │ Requests waiting (exhausted)
    |│ ████████████████ │
 10 |╰──────────────────╯──────────────
  0 |
    14:25   14:30   14:35   14:45   14:50
```

### Log Evidence

**Connection Pool Exhaustion** (`/var/log/api-service/error.log`):
```
[2025-12-19 14:32:15 UTC] ERROR ConnectionPoolExhausted: Could not acquire connection within timeout (5000ms)
[2025-12-19 14:32:16 UTC] ERROR ConnectionPoolExhausted: Could not acquire connection within timeout (5000ms)
[2025-12-19 14:32:17 UTC] ERROR ConnectionPoolExhausted: Could not acquire connection within timeout (5000ms)
[... repeating thousands of times ...]
```

### Code Evidence

**Git Commit**:
```bash
$ git show abc123def456789

commit abc123def456789
Author: Developer Name <dev@example.com>
Date:   Thu Dec 19 10:15:00 2025 +0000

    Refactor database configuration for consistency

diff --git a/src/config/database.js b/src/config/database.js
@@ -42,7 +42,7 @@ function createConnectionPool() {
   return new Pool({
     host: process.env.DB_HOST,
     port: process.env.DB_PORT,
-    max: 100,
+    max: 10,  // Align with staging environment
     min: 10,
     idleTimeoutMillis: 30000
   });
```

**Git Blame**:
```bash
$ git blame src/config/database.js | grep "max:"
abc123def45 (Developer Name 2025-12-19 10:15:00) max: 10,
```

---

## Remediation

### Immediate Fix (Completed)

**Action**: Revert deployment to previous version 2.3.0
**Executed**: 2025-12-19 14:45 UTC
**Result**: Error rate returned to baseline within 2 minutes
**Status**: ✅ Completed

### Permanent Fix (In Progress)

**Action**: Update database configuration to use appropriate pool size based on load testing
**Plan**:
1. Conduct load testing to determine optimal pool size for production workload
2. Update configuration to use 120 connections (20% buffer over peak observed usage of 100)
3. Add configuration validation on startup to warn if pool size seems too small
4. Update staging to match production pool sizing

**Assignee**: [Developer Name]
**Target**: 2025-12-20
**Tracking**: [TICKET-123]
**Status**: 🔄 In Progress

### Prevention Strategies

| Strategy | Description | Owner | Status |
|----------|-------------|-------|--------|
| **Load-based validation** | Add pre-deployment check that validates connection pool size against expected traffic | DevOps Team | [TICKET-124] |
| **Canary deployments** | Implement gradual rollout (5% → 25% → 50% → 100%) to catch issues early | Platform Team | [TICKET-125] |
| **Connection pool monitoring** | Add alerting for connection pool utilization >80% | SRE Team | [TICKET-126] |
| **Config review checklist** | Add "resource sizing" item to code review checklist | Engineering | [TICKET-127] |
| **Staging parity** | Ensure staging environment mirrors production load characteristics | DevOps Team | [TICKET-128] |

---

## Lessons Learned

### What Went Well ✅

- Alert fired within 3 minutes of incident start (good detection)
- On-call engineer responded quickly (1 minute to acknowledge)
- Root cause identified quickly through systematic investigation (7 minutes)
- Revert decision made confidently and executed smoothly
- Communication was clear throughout incident

### What Could Be Improved 🔧

- Configuration change slipped through code review without scrutiny
- Staging environment didn't catch the issue due to lower traffic
- No automated validation of connection pool sizing
- Deployment was all-at-once instead of gradual rollout
- Resource utilization metrics didn't trigger proactive alerts

### Action Items

1. **[TICKET-124]** Implement pre-deployment validation for resource configurations
2. **[TICKET-125]** Enable canary deployments for api-service
3. **[TICKET-126]** Add connection pool utilization alerting (threshold: 80%)
4. **[TICKET-127]** Update code review checklist to include resource sizing
5. **[TICKET-128]** Improve staging environment to better match production load
6. **[TICKET-129]** Conduct training on resource sizing best practices
7. **[TICKET-130]** Document connection pool sizing guidelines

---

## Post-Incident Review

**Meeting Date**: [e.g., 2025-12-20]
**Attendees**: [List of attendees]
**Recording**: [Link if applicable]
**Notes**: [Link to meeting notes]

### Key Decisions

- [Decision 1: e.g., All resource configuration changes require load testing validation]
- [Decision 2: e.g., Staging environment will be upgraded to production-equivalent traffic]
- [Add more as needed]

---

## Appendices

### Appendix A: Detailed Metrics

[Include additional metric graphs, dashboards, or detailed data]

### Appendix B: Full Log Excerpts

[Include relevant log sections if needed for reference]

### Appendix C: Communication Timeline

[Timeline of incident communication: status updates, stakeholder notifications, etc.]

---

**Report Version**: 1.0
**Last Updated**: [Date]
**Next Review**: [Date if applicable]
