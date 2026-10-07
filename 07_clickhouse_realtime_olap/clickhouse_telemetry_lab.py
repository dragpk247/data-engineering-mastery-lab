"""
07_clickhouse_realtime_olap/clickhouse_telemetry_lab.py
-------------------------------------------------------
Scenario: Real-Time High-Throughput Telemetry & Sub-Second Dashboards.
Why ClickHouse beats DuckDB here:
- Built for continuous streaming ingestion (100k+ inserts/second)
- Real-time Materialized Views pre-aggregate data on write
- Sub-10ms response times on billions of time-series rows
"""

import time
import random
from collections import defaultdict
import duckdb # Used here as a local columnar mock execution environment for ClickHouse MergeTree simulation

def main():
    print("=" * 68)
    print("⚡ Scenario 1: Real-Time High-Concurrency OLAP (ClickHouse Engine)")
    print("=" * 68)

    con = duckdb.connect()

    # 1. Define the ClickHouse MergeTree Table Structure
    print("\n--- 1. Creating ClickHouse-style MergeTree Engine Table ---")
    con.execute("""
    CREATE TABLE server_telemetry (
        timestamp TIMESTAMP,
        server_id VARCHAR,
        region VARCHAR,
        cpu_usage DOUBLE,
        memory_usage DOUBLE,
        latency_ms DOUBLE
    );
    """)

    # 2. Simulate High-Throughput Batch Ingestion (e.g. from Kafka/Vector)
    print("Ingesting 50,000 live infrastructure telemetry events...")
    start_time = time.time()
    
    servers = ["srv-prod-us-1", "srv-prod-us-2", "srv-prod-eu-1", "srv-prod-ap-1"]
    regions = ["us-east", "us-east", "eu-central", "ap-southeast"]
    
    con.execute("""
    INSERT INTO server_telemetry
    SELECT 
        TIMESTAMP '2026-10-07 10:00:00' + INTERVAL (random() * 3600) SECOND,
        ['srv-prod-us-1', 'srv-prod-us-2', 'srv-prod-eu-1', 'srv-prod-ap-1'][CAST(floor(random() * 4) + 1 AS INT)],
        ['us-east', 'us-east', 'eu-central', 'ap-southeast'][CAST(floor(random() * 4) + 1 AS INT)],
        ROUND(random() * 100, 2),
        ROUND(random() * 100, 2),
        ROUND(20 + random() * 480, 2)
    FROM range(50000);
    """)
    ingest_duration = (time.time() - start_time) * 1000
    print(f"✅ Ingested 50,000 records in {ingest_duration:.2f} ms")

    # 3. ClickHouse Powerhouse Feature: Instant Percentiles (P95, P99 Latency)
    print("\n--- 2. Sub-Second P95 & P99 Latency Calculation by Region ---")
    query_start = time.time()
    telemetry_kpis = con.execute("""
    SELECT 
        region,
        COUNT(*) as total_samples,
        ROUND(AVG(cpu_usage), 1) as avg_cpu_pct,
        ROUND(AVG(memory_usage), 1) as avg_mem_pct,
        ROUND(QUANTILE_CONT(latency_ms, 0.50), 2) as p50_latency,
        ROUND(QUANTILE_CONT(latency_ms, 0.95), 2) as p95_latency,
        ROUND(QUANTILE_CONT(latency_ms, 0.99), 2) as p99_latency
    FROM server_telemetry
    GROUP BY region
    ORDER BY p99_latency DESC;
    """).df()
    query_duration = (time.time() - query_start) * 1000

    print(telemetry_kpis)
    print(f"⚡ Query executed in {query_duration:.2f} ms across 50,000 data points!")

    # 4. Materialized View Pattern: Pre-aggregating data for sub-millisecond dashboards
    print("\n--- 3. ClickHouse Materialized View Simulation ---")
    con.execute("""
    CREATE TABLE mv_hourly_server_rollups AS
    SELECT 
        DATE_TRUNC('hour', timestamp) as window_hour,
        server_id,
        COUNT(*) as sample_count,
        ROUND(MAX(latency_ms), 2) as max_spike_latency
    FROM server_telemetry
    GROUP BY window_hour, server_id;
    """)
    print("Pre-aggregated Materialized View Table (Instant Dashboard Queries):")
    print(con.execute("SELECT * FROM mv_hourly_server_rollups LIMIT 5").df())

    print("=" * 68)
    print("✅ ClickHouse Telemetry Scenario Finished Successfully!")
    print("=" * 68)

if __name__ == "__main__":
    main()
