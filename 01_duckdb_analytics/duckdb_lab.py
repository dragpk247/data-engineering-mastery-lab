"""
01_duckdb_analytics/duckdb_lab.py
---------------------------------
Demonstrates DuckDB: The in-process columnar SQL OLAP engine.
Key concepts:
- Zero-copy querying directly over Parquet files
- Advanced analytical SQL (Window functions, CTEs)
- Direct export to partitioned Parquet
"""

import os
import duckdb
import pyarrow as pa
import pyarrow.parquet as pq

DATA_DIR = "/tmp/duckdb_lab_data"
os.makedirs(DATA_DIR, exist_ok=True)
parquet_file = os.path.join(DATA_DIR, "transactions.parquet")

def generate_mock_data():
    """Creates a sample Parquet dataset to demonstrate external querying."""
    table = pa.table({
        "tx_id": ["T1", "T2", "T3", "T4", "T5", "T6", "T7", "T8"],
        "user_id": ["U10", "U20", "U10", "U30", "U20", "U10", "U40", "U30"],
        "region": ["NA", "EU", "NA", "APAC", "EU", "NA", "LATAM", "APAC"],
        "amount": [120.50, 45.00, 310.25, 89.90, 520.00, 15.00, 75.50, 190.00],
        "category": ["Cloud", "SaaS", "Hardware", "Cloud", "Hardware", "SaaS", "Cloud", "SaaS"]
    })
    pq.write_table(table, parquet_file)
    print(f"Generated mock Parquet file at: {parquet_file}")

def main():
    print("=" * 65)
    print("🦆 DuckDB Analytics Lab: Fast Columnar In-Process SQL")
    print("=" * 65)

    generate_mock_data()
    con = duckdb.connect() # In-memory database instance

    # 1. Querying raw Parquet files directly using SQL (No ingestion needed!)
    print("\n--- 1. Query directly from Parquet file ---")
    query_direct = f"SELECT * FROM '{parquet_file}' LIMIT 5"
    print(con.execute(query_direct).df())

    # 2. Aggregations & High-Speed Analytics
    print("\n--- 2. Revenue & Average Transaction by Region ---")
    agg_sql = f"""
    SELECT 
        region,
        COUNT(tx_id) AS total_transactions,
        ROUND(SUM(amount), 2) AS total_revenue,
        ROUND(AVG(amount), 2) AS avg_ticket_size
    FROM '{parquet_file}'
    GROUP BY region
    ORDER BY total_revenue DESC
    """
    print(con.execute(agg_sql).df())

    # 3. Window Functions: Ranking Top Spenders per Region
    print("\n--- 3. Top Spending Users Ranked per Region (Window Function) ---")
    window_sql = f"""
    WITH ranked_spend AS (
        SELECT 
            user_id,
            region,
            amount,
            DENSE_RANK() OVER (PARTITION BY region ORDER BY amount DESC) as rank_in_region
        FROM '{parquet_file}'
    )
    SELECT * FROM ranked_spend WHERE rank_in_region = 1
    """
    print(con.execute(window_sql).df())

    # 4. Direct Parquet Export
    output_summary = os.path.join(DATA_DIR, "regional_summary.parquet")
    con.execute(f"COPY ({agg_sql}) TO '{output_summary}' (FORMAT PARQUET)")
    print(f"\n✅ Analytical summary exported directly to Parquet: {output_summary}")

    print("=" * 65)
    print("✅ DuckDB Lab Finished Successfully!")
    print("=" * 65)

if __name__ == "__main__":
    main()
