# Common RCA Patterns and Solutions

This document catalogs frequently encountered incident patterns, their root causes, and solutions.

## Database-Related Incidents

### Pattern: Connection Pool Exhaustion

**Symptoms:**
- Database timeout errors
- "Could not acquire connection" messages
- Slow API response times
- Gradual degradation over time

**Common Root Causes:**
1. Pool size reduced in configuration change
2. Connection leaks (connections not closed properly)
3. Sudden traffic spike exceeding pool capacity
4. Long-running queries holding connections
5. Missing connection timeout configuration

**Investigation Approach:**
- Check recent config changes to pool size
- Review code for missing `connection.close()` or try-finally blocks
- Analyze query execution times
- Check traffic patterns for spikes
- Review connection pool metrics (active, idle, waiting)

**Typical Solutions:**
- Increase pool size appropriately for load
- Fix connection leaks in code
- Add connection timeouts
- Optimize slow queries
- Implement connection retry logic

---

### Pattern: Missing Database Index

**Symptoms:**
- Gradual query performance degradation
- Database CPU usage increasing over time
- Slow page loads for specific features
- Timeout errors during peak traffic

**Common Root Causes:**
1. New query added without index
2. Schema migration removed index
3. Data volume grew making unindexed queries slow
4. Query pattern changed to no longer use existing index

**Investigation Approach:**
- Identify slow queries from database logs
- Check EXPLAIN output for full table scans
- Review recent schema migrations
- Compare query patterns before/after issue
- Analyze table sizes and growth

**Typical Solutions:**
- Add missing indexes
- Optimize query to use existing indexes
- Implement query result caching
- Paginate large result sets
- Archive old data

---

## Deployment-Related Incidents

### Pattern: Configuration Error in Deployment

**Symptoms:**
- Immediate errors after deployment
- All instances affected simultaneously
- Clear correlation with deployment time
- Errors referencing missing or invalid config values

**Common Root Causes:**
1. Missing environment variable in deployment
2. Typo in configuration value
3. Configuration file not deployed
4. Environment-specific config used in wrong environment
5. Feature flag misconfigured

**Investigation Approach:**
- Compare configuration before and after deployment
- Check deployment logs for warnings
- Verify environment variables in running instances
- Review configuration management commits
- Test configuration parsing code

**Typical Solutions:**
- Fix configuration value
- Redeploy with correct configuration
- Add configuration validation on startup
- Implement configuration drift detection
- Use configuration management tools properly

---

### Pattern: Dependency Version Incompatibility

**Symptoms:**
- Errors immediately after dependency update
- Method not found or type errors
- Behavioral changes in library code
- Breaking changes not caught in testing

**Common Root Causes:**
1. Major version update with breaking changes
2. Transitive dependency conflict
3. Platform-specific dependency issue
4. Deprecated API usage
5. Missing peer dependency

**Investigation Approach:**
- Check recent package.json/requirements.txt changes
- Review dependency changelogs for breaking changes
- Compare dependency versions before/after deployment
- Test with previous dependency versions
- Check for deprecation warnings in logs

**Typical Solutions:**
- Pin dependency to working version
- Update code to use new API
- Add compatibility shims
- Update transitive dependencies
- Improve dependency testing

---

## Memory and Resource Issues

### Pattern: Memory Leak

**Symptoms:**
- Memory usage gradually increasing over time
- Eventual out-of-memory errors or crashes
- Garbage collection pauses increasing
- Performance degrading over hours/days
- Recovery after restart

**Common Root Causes:**
1. Objects not being garbage collected (references retained)
2. Unbounded cache growth
3. Event listener not removed
4. Closure capturing large objects
5. Circular references preventing GC

**Investigation Approach:**
- Analyze memory usage metrics over time
- Take heap dumps at different times
- Compare object counts and sizes
- Review recent code changes for cache additions
- Check for event listener registration patterns
- Profile memory allocation

**Typical Solutions:**
- Fix reference retention issues
- Implement cache size limits (LRU eviction)
- Remove event listeners properly
- Break circular references
- Use weak references where appropriate
- Restart instances on schedule (temporary workaround)

---

### Pattern: Resource Exhaustion (File Handles, Threads)

**Symptoms:**
- "Too many open files" errors
- Thread pool exhausted warnings
- Cannot create new threads/processes
- System-level resource limits hit

**Common Root Causes:**
1. File handles not closed after use
2. Unbounded thread pool creation
3. Resource leak in library code
4. System limits too low for workload
5. Retry logic creating resource explosion

**Investigation Approach:**
- Check system resource limits (`ulimit -n`)
- Monitor file descriptor/thread counts
- Review code for missing close() calls
- Check for resource cleanup in error paths
- Analyze thread pool configuration

**Typical Solutions:**
- Fix resource leaks (use try-finally, context managers)
- Increase system resource limits
- Implement resource pooling
- Add proper cleanup in error paths
- Use bounded thread pools

---

## Performance and Scalability Issues

### Pattern: N+1 Query Problem

**Symptoms:**
- Slow API responses
- Sudden query count spike
- Database connection pool exhaustion
- Linear performance degradation with data size

**Common Root Causes:**
1. Missing eager loading in ORM
2. Loop making individual queries
3. GraphQL resolver inefficiency
4. Lazy loading triggering queries in loop

**Investigation Approach:**
- Count database queries per request
- Review ORM query logs
- Check for loops with database calls
- Analyze query patterns in application code
- Use database query profiling

**Typical Solutions:**
- Add eager loading (JOIN or IN queries)
- Implement batch loading (DataLoader pattern)
- Use query result caching
- Refactor to single query
- Implement pagination

---

### Pattern: Unbounded Data Growth

**Symptoms:**
- Performance degrading over time
- Disk space running out
- Queries getting slower
- Memory usage increasing

**Common Root Causes:**
1. No data retention policy
2. Log files not rotated
3. Cache with no eviction
4. No data archiving strategy
5. Unbounded collection growth in memory

**Investigation Approach:**
- Check data volume growth over time
- Analyze table/collection sizes
- Review data lifecycle policies
- Check disk usage trends
- Identify largest tables/files

**Typical Solutions:**
- Implement data retention policies
- Archive old data
- Add cache eviction (TTL, LRU)
- Implement log rotation
- Add data cleanup jobs
- Use time-series databases for metrics

---

## Integration and Dependency Issues

### Pattern: Third-Party API Failure

**Symptoms:**
- Timeout errors calling external service
- Sudden increase in API error rates
- Specific feature failing while others work
- Correlation with third-party status page

**Common Root Causes:**
1. Third-party service outage
2. Rate limiting exceeded
3. API endpoint deprecated or changed
4. Authentication token expired
5. Network connectivity issues

**Investigation Approach:**
- Check third-party status pages
- Review API error responses
- Monitor API call rates
- Check authentication token expiry
- Test API endpoints directly
- Review recent API version changes

**Typical Solutions:**
- Implement retry logic with backoff
- Add circuit breakers
- Cache API responses
- Add fallback mechanisms
- Implement rate limiting awareness
- Monitor third-party SLAs

---

### Pattern: Message Queue Backlog

**Symptoms:**
- Message processing delays
- Queue depth increasing
- Events processed out of SLA
- Consumer lag growing
- Memory pressure on queue servers

**Common Root Causes:**
1. Consumer processing slower than producer rate
2. Consumer instance crash or scaling issue
3. Poison message blocking queue
4. Database bottleneck in consumer
5. Insufficient consumer parallelism

**Investigation Approach:**
- Monitor queue depth over time
- Check consumer processing rates
- Review consumer error logs
- Check for stuck/poison messages
- Analyze consumer resource usage
- Compare producer vs consumer rates

**Typical Solutions:**
- Scale consumer instances
- Optimize consumer processing speed
- Implement dead letter queue for poison messages
- Add consumer parallelism
- Optimize database queries in consumer
- Implement backpressure mechanisms

---

## Concurrency and Race Conditions

### Pattern: Race Condition

**Symptoms:**
- Intermittent, hard-to-reproduce errors
- Different behavior under load
- Data inconsistency issues
- Works in dev/staging, fails in production
- More frequent during high traffic

**Common Root Causes:**
1. Shared state without synchronization
2. Check-then-act pattern (TOCTOU)
3. Non-atomic operations on shared data
4. Missing database transaction isolation
5. Concurrent access to non-thread-safe code

**Investigation Approach:**
- Identify shared state in affected code
- Review concurrency patterns
- Check for missing locks/synchronization
- Analyze database transaction isolation
- Load test to reproduce issue
- Review recent concurrency changes

**Typical Solutions:**
- Add proper synchronization (locks, mutexes)
- Use atomic operations
- Implement optimistic locking
- Use database transactions properly
- Make code idempotent
- Use immutable data structures

---

## Network and Infrastructure Issues

### Pattern: Load Balancer Misconfiguration

**Symptoms:**
- Uneven request distribution
- Some instances overloaded while others idle
- Sticky session issues
- Health check failures
- Sudden traffic drops

**Common Root Causes:**
1. Health check endpoint misconfigured
2. Incorrect load balancing algorithm
3. Session affinity misconfigured
4. Instance registration/deregistration issues
5. Timeout settings too aggressive

**Investigation Approach:**
- Check load balancer configuration
- Review health check responses
- Monitor request distribution across instances
- Check instance registration status
- Review recent infrastructure changes
- Analyze health check logs

**Typical Solutions:**
- Fix health check endpoint
- Adjust load balancing algorithm
- Configure session affinity properly
- Fix instance registration logic
- Adjust timeout settings
- Implement graceful shutdown

---

## How to Use These Patterns

When investigating an incident:

1. **Match symptoms** to patterns above
2. **Check common root causes** for that pattern
3. **Follow investigation approach** to gather evidence
4. **Validate root cause** with specific evidence from your system
5. **Apply appropriate solution** adapted to your context

Remember: Patterns are starting points, not definitive answers. Always validate with your specific evidence.

## Contributing New Patterns

When you encounter a new incident pattern:

1. Document symptoms clearly
2. Identify root cause with evidence
3. Note investigation steps that worked
4. Record solution applied
5. Add to this document for future reference

Build your team's institutional knowledge of production issues.
