"""
02_polars_dataframes/polars_lab.py
----------------------------------
Demonstrates Polars: The lightning-fast multi-threaded Rust DataFrame library.
Key concepts:
- Lazy evaluation (LazyFrame) and predicate pushdown
- Polars Expression Context (select, with_columns, group_by)
- Window functions and high-speed streaming execution
"""

import polars as pl

def main():
    print("=" * 65)
    print("🐻‍❄️ Polars Lab: Lightning-Fast Multi-Threaded Rust DataFrames")
    print("=" * 65)

    # 1. Create a DataFrame
    data = {
        "event_id": [1, 2, 3, 4, 5, 6, 7, 8],
        "device": ["ios", "android", "ios", "web", "android", "web", "ios", "web"],
        "response_time_ms": [120, 450, 85, 310, 620, 95, 110, 240],
        "status_code": [200, 500, 200, 200, 503, 200, 200, 404],
        "country": ["US", "US", "DE", "FR", "US", "DE", "FR", "US"]
    }
    df = pl.DataFrame(data)
    print("\n--- 1. Raw Polars DataFrame ---")
    print(df)

    # 2. Expression API: Multi-column transformation in a single pass
    print("\n--- 2. Expressions: Fast In-Memory Metrics ---")
    enhanced_df = df.with_columns(
        is_error = pl.col("status_code") >= 400,
        latency_tier = pl.when(pl.col("response_time_ms") > 300)
            .then(pl.lit("Slow"))
            .otherwise(pl.lit("Fast"))
    )
    print(enhanced_df)

    # 3. Aggregations with Expressions
    print("\n--- 3. Performance Aggregates by Device ---")
    device_metrics = enhanced_df.group_by("device").agg(
        total_requests = pl.len(),
        error_count = pl.col("is_error").sum(),
        avg_latency = pl.col("response_time_ms").mean().round(2),
        p95_latency = pl.col("response_time_ms").quantile(0.95)
    ).sort("total_requests", descending=True)
    print(device_metrics)

    # 4. Lazy Evaluation & Query Optimization Plan
    print("\n--- 4. Lazy Evaluation (Predicate Pushdown Plan) ---")
    lazy_plan = df.lazy() \
        .filter(pl.col("country") == "US") \
        .group_by("device") \
        .agg(pl.col("response_time_ms").mean().alias("avg_us_latency"))

    # Print the physical query execution plan optimized by the Rust engine
    print(lazy_plan.explain())
    
    # Collect the computed result
    print("Collected Result:")
    print(lazy_plan.collect())

    print("=" * 65)
    print("✅ Polars Lab Finished Successfully!")
    print("=" * 65)

if __name__ == "__main__":
    main()
