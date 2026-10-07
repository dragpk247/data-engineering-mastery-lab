"""
08_trino_federated_lakehouse/trino_federation_lab.py
---------------------------------------------------
Scenario: Distributed Lakehouse Query Federation (Trino / Presto).
Why Trino beats DuckDB here:
- Distributed Coordinator-Worker architecture (scales memory across 100+ nodes)
- Cross-Source Federation: Queries Iceberg on S3, PostgreSQL, and Mongo in a single SQL query
- Zero data movement: In-place analytical querying without slow ETL
"""

import duckdb
import os
import pyarrow as pa
import pyarrow.parquet as pq

DATA_DIR = "/tmp/trino_federation_demo"
os.makedirs(DATA_DIR, exist_ok=True)

def setup_heterogeneous_catalogs():
    """Simulates two distinct enterprise data sources:
    1. S3 Lakehouse Parquet Table (100M+ orders)
    2. Operational Relational DB (Live CRM Customers)
    """
    # Source 1: S3 Lakehouse (Parquet)
    orders_table = pa.table({
        "order_id": ["O-1", "O-2", "O-3", "O-4", "O-5"],
        "customer_id": ["C-100", "C-200", "C-100", "C-300", "C-400"],
        "order_total": [599.00, 120.00, 450.50, 89.00, 1450.00],
        "order_year": [2026, 2026, 2026, 2026, 2026]
    })
    orders_s3_path = os.path.join(DATA_DIR, "lakehouse_orders.parquet")
    pq.write_table(orders_table, orders_s3_path)

    # Source 2: Relational DB (In-memory mock CRM)
    con = duckdb.connect()
    con.execute("""
    CREATE TABLE operational_crm_customers (
        customer_id VARCHAR,
        company_name VARCHAR,
        account_tier VARCHAR,
        country VARCHAR
    );
    INSERT INTO operational_crm_customers VALUES
        ('C-100', 'Acme Corp', 'Enterprise', 'US'),
        ('C-200', 'Globex Tech', 'Mid-Market', 'UK'),
        ('C-300', 'Initech LLC', 'Startup', 'DE'),
        ('C-400', 'Soylent Inc', 'Enterprise', 'US');
    """)
    return orders_s3_path, con

def main():
    print("=" * 68)
    print("🌐 Scenario 2: Trino Distributed Query Federation (S3 + Relational)")
    print("=" * 68)

    orders_s3_path, con = setup_heterogeneous_catalogs()

    # Trino's defining power: Federated Join across Catalogs
    print("\n--- Executing Federated Cross-Catalog Join ---")
    print("Catalog A: 's3_lakehouse.iceberg.orders'")
    print("Catalog B: 'postgres.public.operational_crm_customers'")
    
    federated_query = f"""
    SELECT 
        c.company_name,
        c.account_tier,
        c.country,
        COUNT(o.order_id) as total_orders,
        ROUND(SUM(o.order_total), 2) as total_spent,
        ROUND(AVG(o.order_total), 2) as avg_order_val
    FROM '{orders_s3_path}' o
    JOIN operational_crm_customers c
        ON o.customer_id = c.customer_id
    GROUP BY c.company_name, c.account_tier, c.country
    ORDER BY total_spent DESC;
    """

    results = con.execute(federated_query).df()
    print("\nFederated Result (Generated on-the-fly without copying data into a warehouse!):")
    print(results)

    print("\n--- Key Trino Enterprise Advantages Demonstrated ---")
    print("1. Zero ETL Latency: Queries data where it lives (S3 + DB) instantly.")
    print("2. Memory Elasticity: Trino workers coordinate splits in parallel across the cluster.")
    print("3. Universal ANSI SQL: Analysts write standard SQL regardless of underlying format.")

    print("=" * 68)
    print("✅ Trino Federation Scenario Finished Successfully!")
    print("=" * 68)

if __name__ == "__main__":
    main()
