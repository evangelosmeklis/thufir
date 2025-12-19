# PromQL Cookbook for Root Cause Analysis

This cookbook provides battle-tested PromQL queries for common RCA scenarios. Copy and adapt these queries for your investigation.

## HTTP Service Metrics

### Error Rates

**Total error rate (5xx errors)**:
```promql
sum(rate(http_requests_total{status=~"5.."}[5m]))
```

**Error rate percentage**:
```promql
(sum(rate(http_requests_total{status=~"5.."}[5m])) /
 sum(rate(http_requests_total[5m]))) * 100
```

**Error rate by endpoint**:
```promql
sum(rate(http_requests_total{status=~"5.."}[5m])) by (endpoint)
```

**Error rate by status code**:
```promql
sum(rate(http_requests_total{status=~"5.."}[5m])) by (status)
```

**4xx client errors**:
```promql
sum(rate(http_requests_total{status=~"4.."}[5m]))
```

**Top 5 endpoints by error count**:
```promql
topk(5, sum(rate(http_requests_total{status=~"5.."}[5m])) by (endpoint))
```

### Request Rates

**Total request rate**:
```promql
sum(rate(http_requests_total[5m]))
```

**Request rate by endpoint**:
```promql
sum(rate(http_requests_total[5m])) by (endpoint)
```

**Request rate by method**:
```promql
sum(rate(http_requests_total[5m])) by (method)
```

**Successful request rate (2xx)**:
```promql
sum(rate(http_requests_total{status=~"2.."}[5m]))
```

**Success rate percentage**:
```promql
(sum(rate(http_requests_total{status=~"2.."}[5m])) /
 sum(rate(http_requests_total[5m]))) * 100
```

### Latency

**95th percentile latency**:
```promql
histogram_quantile(0.95,
  sum(rate(http_request_duration_seconds_bucket[5m])) by (le)
)
```

**99th percentile latency**:
```promql
histogram_quantile(0.99,
  sum(rate(http_request_duration_seconds_bucket[5m])) by (le)
)
```

**Median (50th percentile) latency**:
```promql
histogram_quantile(0.50,
  sum(rate(http_request_duration_seconds_bucket[5m])) by (le)
)
```

**Latency by endpoint (p95)**:
```promql
histogram_quantile(0.95,
  sum(rate(http_request_duration_seconds_bucket[5m])) by (le, endpoint)
)
```

**Average latency**:
```promql
rate(http_request_duration_seconds_sum[5m]) /
rate(http_request_duration_seconds_count[5m])
```

**Latency spike detection** (current vs 1 hour ago):
```promql
histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m])) /
histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m] offset 1h))
```

## Database Metrics

### Connection Pools

**Connection pool utilization percentage**:
```promql
(sum(db_connection_pool_active) / sum(db_connection_pool_max)) * 100
```

**Active connections**:
```promql
sum(db_connection_pool_active)
```

**Idle connections**:
```promql
sum(db_connection_pool_idle)
```

**Waiting for connection**:
```promql
sum(db_connection_pool_waiting)
```

**Connection pool saturation**:
```promql
sum(db_connection_pool_active) >= sum(db_connection_pool_max)
```

### Query Performance

**Slow query count**:
```promql
sum(rate(db_query_duration_seconds_bucket{le="1.0"}[5m]))
```

**Query rate**:
```promql
sum(rate(db_queries_total[5m]))
```

**Query rate by operation**:
```promql
sum(rate(db_queries_total[5m])) by (operation)
```

**Average query duration**:
```promql
rate(db_query_duration_seconds_sum[5m]) /
rate(db_query_duration_seconds_count[5m])
```

**Query errors**:
```promql
sum(rate(db_query_errors_total[5m]))
```

## System Resource Metrics

### CPU

**CPU usage percentage**:
```promql
(1 - avg(rate(node_cpu_seconds_total{mode="idle"}[5m]))) * 100
```

**CPU usage by instance**:
```promql
(1 - avg(rate(node_cpu_seconds_total{mode="idle"}[5m])) by (instance)) * 100
```

**Process CPU usage**:
```promql
rate(process_cpu_seconds_total[5m]) * 100
```

**Top 5 CPU-consuming processes**:
```promql
topk(5, rate(process_cpu_seconds_total[5m]))
```

### Memory

**Memory usage percentage**:
```promql
(node_memory_MemTotal_bytes - node_memory_MemAvailable_bytes) /
node_memory_MemTotal_bytes * 100
```

**Process memory usage (RSS)**:
```promql
process_resident_memory_bytes
```

**Process memory usage (MB)**:
```promql
process_resident_memory_bytes / 1024 / 1024
```

**Memory usage by instance**:
```promql
(node_memory_MemTotal_bytes - node_memory_MemAvailable_bytes) by (instance)
```

**Memory usage growth rate**:
```promql
deriv(process_resident_memory_bytes[5m])
```

**Memory leak detection** (steady increase over time):
```promql
delta(process_resident_memory_bytes[1h])
```

### Disk

**Disk usage percentage**:
```promql
(node_filesystem_size_bytes - node_filesystem_free_bytes) /
node_filesystem_size_bytes * 100
```

**Disk I/O rate**:
```promql
rate(node_disk_io_time_seconds_total[5m])
```

**Disk space available (GB)**:
```promql
node_filesystem_free_bytes / 1024 / 1024 / 1024
```

**Disk filling rate** (GB per day):
```promql
predict_linear(node_filesystem_free_bytes[1h], 24*3600) / 1024 / 1024 / 1024
```

### Network

**Network receive rate (MB/s)**:
```promql
rate(node_network_receive_bytes_total[5m]) / 1024 / 1024
```

**Network transmit rate (MB/s)**:
```promql
rate(node_network_transmit_bytes_total[5m]) / 1024 / 1024
```

**Network errors**:
```promql
rate(node_network_receive_errs_total[5m]) +
rate(node_network_transmit_errs_total[5m])
```

## Application-Specific Metrics

### Queue Depths

**Message queue depth**:
```promql
sum(queue_depth)
```

**Queue depth by queue name**:
```promql
sum(queue_depth) by (queue)
```

**Queue depth growth**:
```promql
deriv(queue_depth[5m])
```

**Consumer lag**:
```promql
sum(queue_depth) - sum(queue_processing_rate[5m] * 300)
```

### Cache

**Cache hit rate percentage**:
```promql
(sum(rate(cache_hits_total[5m])) /
 (sum(rate(cache_hits_total[5m])) + sum(rate(cache_misses_total[5m])))) * 100
```

**Cache size**:
```promql
cache_entries_total
```

**Cache eviction rate**:
```promql
rate(cache_evictions_total[5m])
```

### Garbage Collection

**GC pause time (total)**:
```promql
rate(gc_pause_seconds_sum[5m])
```

**GC frequency**:
```promql
rate(gc_pause_seconds_count[5m])
```

**Average GC pause duration**:
```promql
rate(gc_pause_seconds_sum[5m]) / rate(gc_pause_seconds_count[5m])
```

## Service Health and Availability

### Uptime

**Service up/down status**:
```promql
up
```

**Count of down instances**:
```promql
count(up == 0)
```

**Service availability percentage (last hour)**:
```promql
avg_over_time(up[1h]) * 100
```

**Instance count**:
```promql
count(up)
```

**Healthy instance count**:
```promql
count(up == 1)
```

### Dependency Health

**Dependency call success rate**:
```promql
sum(rate(dependency_calls_total{status="success"}[5m])) /
sum(rate(dependency_calls_total[5m])) * 100
```

**Dependency call latency**:
```promql
histogram_quantile(0.95,
  rate(dependency_call_duration_seconds_bucket[5m])
)
```

**Dependency timeouts**:
```promql
sum(rate(dependency_calls_total{status="timeout"}[5m]))
```

## Time Comparisons

### Week-over-Week

**Current error rate vs last week**:
```promql
rate(http_requests_total{status=~"5.."}[5m]) /
rate(http_requests_total{status=~"5.."}[5m] offset 1w)
```

**Traffic change vs last week**:
```promql
sum(rate(http_requests_total[5m])) /
sum(rate(http_requests_total[5m] offset 1w))
```

### Day-over-Day

**Error rate change from yesterday**:
```promql
rate(http_requests_total{status=~"5.."}[5m]) -
rate(http_requests_total{status=~"5.."}[5m] offset 1d)
```

### Hour-over-Hour

**Latency increase in last hour**:
```promql
histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m])) -
histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m] offset 1h))
```

## Anomaly Detection

### Threshold Crossing

**Error rate above threshold**:
```promql
sum(rate(http_requests_total{status=~"5.."}[5m])) > 0.05
```

**Latency above threshold**:
```promql
histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m])) > 1.0
```

**Memory usage above threshold**:
```promql
process_resident_memory_bytes > 1e9  # 1GB
```

### Rate of Change

**Sudden traffic spike** (>50% increase):
```promql
(rate(http_requests_total[5m]) - rate(http_requests_total[5m] offset 10m)) /
rate(http_requests_total[5m] offset 10m) > 0.5
```

**Memory leak detection** (steady growth):
```promql
deriv(process_resident_memory_bytes[1h]) > 1e6  # 1MB per second growth
```

### Prediction

**Disk will fill in 24 hours**:
```promql
predict_linear(node_filesystem_free_bytes[1h], 24*3600) < 0
```

**Memory exhaustion prediction**:
```promql
predict_linear(process_resident_memory_bytes[1h], 3600) > 8e9  # Will hit 8GB in 1 hour
```

## Correlation Queries

### Multi-Metric Comparison

**Error rate + Latency correlation**:
```promql
# Query both together
rate(http_requests_total{status=~"5.."}[5m])
histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m]))
```

**Error rate + CPU correlation**:
```promql
# High error rate AND high CPU
rate(http_requests_total{status=~"5.."}[5m]) > 0.05
  and
(1 - avg(rate(node_cpu_seconds_total{mode="idle"}[5m]))) > 0.8
```

### Instance Comparison

**Compare instance metrics to find outliers**:
```promql
# CPU usage per instance
(1 - avg(rate(node_cpu_seconds_total{mode="idle"}[5m])) by (instance)) * 100
```

**Error rate by instance** (find problematic instance):
```promql
sum(rate(http_requests_total{status=~"5.."}[5m])) by (instance)
```

## Query Optimization

### Recording Rules

For frequently used expensive queries, create recording rules in Prometheus configuration:

```yaml
# recording_rules.yml
groups:
  - name: rca_metrics
    interval: 30s
    rules:
      - record: job:http_errors:rate5m
        expr: sum(rate(http_requests_total{status=~"5.."}[5m])) by (job)

      - record: job:http_latency:p95
        expr: histogram_quantile(0.95, sum(rate(http_request_duration_seconds_bucket[5m])) by (le, job))
```

Then query the pre-computed metric:
```promql
job:http_errors:rate5m{job="api"}
```

### Efficient Label Filtering

**Avoid**: High-cardinality label aggregation
```promql
# Bad: Aggregates across all user_ids (potentially millions)
sum(rate(requests[5m])) by (user_id)
```

**Prefer**: Low-cardinality label aggregation
```promql
# Good: Aggregates by service (low cardinality)
sum(rate(requests[5m])) by (service, status)
```

## Common Investigation Patterns

### Pattern 1: Error Rate Investigation

```promql
# 1. Overall error rate
sum(rate(http_requests_total{status=~"5.."}[5m]))

# 2. Error rate by endpoint (find problematic endpoint)
topk(5, sum(rate(http_requests_total{status=~"5.."}[5m])) by (endpoint))

# 3. Error rate by instance (find problematic instance)
sum(rate(http_requests_total{status=~"5.."}[5m])) by (instance)

# 4. Compare with last hour (sudden or gradual?)
rate(http_requests_total{status=~"5.."}[5m]) /
rate(http_requests_total{status=~"5.."}[5m] offset 1h)
```

### Pattern 2: Latency Investigation

```promql
# 1. Current p95 latency
histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m]))

# 2. Latency by endpoint
histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m]) by (le, endpoint))

# 3. Latency trend (last 6 hours)
histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m])[6h:])

# 4. Latency spike magnitude
histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m])) /
histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m] offset 1h))
```

### Pattern 3: Resource Exhaustion Investigation

```promql
# 1. CPU usage
(1 - avg(rate(node_cpu_seconds_total{mode="idle"}[5m]))) * 100

# 2. Memory usage
(node_memory_MemTotal_bytes - node_memory_MemAvailable_bytes) / node_memory_MemTotal_bytes * 100

# 3. Connection pool usage
(sum(db_connection_pool_active) / sum(db_connection_pool_max)) * 100

# 4. Disk usage
(node_filesystem_size_bytes - node_filesystem_free_bytes) / node_filesystem_size_bytes * 100
```

---

## Usage Tips

1. **Start broad, then narrow**: Begin with aggregated metrics, then filter by labels to find specific issues
2. **Use appropriate time ranges**: 5m for instant, 1h for trends, 1d for baselines
3. **Compare with baselines**: Use `offset` to compare with historical values
4. **Look for correlations**: Query multiple related metrics together
5. **Validate hypotheses**: Use metrics to confirm or refute root cause theories

Copy these queries and adapt label names and metric names to match your Prometheus setup.
