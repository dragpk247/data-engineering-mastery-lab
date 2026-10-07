"""
09_enterprise_warehouse_patterns/warehouse_patterns_lab.py
----------------------------------------------------------
Scenario: Enterprise Cloud Data Warehouse (Snowflake & BigQuery Patterns).
Why enterprises choose Snowflake/BigQuery over DuckDB:
- Zero-Copy Cloning (Instant dev/stage branches of 50TB data with $0 extra storage)
- Micro-Partition Pruning & Automated Metadata Clustering
- Virtual Warehouse Elasticity (Auto-suspend when idle, scale to 128 nodes in seconds)
- Automated Time-Travel and Undrop Protection
"""

import duckdb
import time

def main():
    print("=" * 68)
    print("❄️ Scenario 3: Enterprise Cloud Data Warehouse Patterns (Snowflake)")
    print("=" * 68)

    con = duckdb.connect()

    # 1. Production Table Creation with Clustering
    print("\n--- 1. Creating Clustered Production Table (Micro-Partitioning Pattern) ---")
    con.execute("""
    CREATE TABLE prod_financial_ledger (
        tx_id VARCHAR,
        account_id VARCHAR,
        tx_type VARCHAR,
        amount DOUBLE,
        tx_time TIMESTAMP
    );

    INSERT INTO prod_financial_ledger VALUES
        ('TX-01', 'ACC-A', 'DEPOSIT', 50000.0, '2026-10-07 09:00:00'),
        ('TX-02', 'ACC-B', 'WITHDRAWAL', 1200.0, '2026-10-07 09:15:00'),
        ('TX-03', 'ACC-A', 'TRANSFER', 8500.0, '2026-10-07 09:30:00');
    """)
    print("Production Ledger Table:")
    print(con.execute("SELECT * FROM prod_financial_ledger").df())

    # 2. Snowflake Superpower: Zero-Copy Cloning Simulation
    print("\n--- 2. Zero-Copy Cloning: CREATE TABLE dev_ledger CLONE prod_ledger ---")
    print("In Snowflake, metadata pointers are cloned instantly in ~100ms with 0 storage duplication.")
    # In-memory metadata clone simulation
    con.execute("CREATE TABLE dev_experimental_ledger AS SELECT * FROM prod_financial_ledger;")
    
    # Developers can modify dev table without mutating production!
    con.execute("UPDATE dev_experimental_ledger SET amount = 999999.0 WHERE tx_id = 'TX-01';")
    
    print("\nDev Table (Modified by Engineer for testing):")
    print(con.execute("SELECT * FROM dev_experimental_ledger").df())
    
    print("\nProduction Table (Completely untouched & safe):")
    print(con.execute("SELECT * FROM prod_financial_ledger").df())

    # 3. Micro-Partition Pruning (Metadata Search without Reading Storage)
    print("\n--- 3. Micro-Partition Metadata Pruning ---")
    print("Snowflake maintains min/max values for every 50-500MB micro-partition.")
    pruned_query = """
    EXPLAIN 
    SELECT * FROM prod_financial_ledger 
    WHERE tx_time >= '2026-10-07 09:00:00' AND tx_type = 'DEPOSIT';
    """
    print("Execution Plan showing Filter Pushdown & Partition Pruning:")
    print(con.execute(pruned_query).df()["explain_value"].iloc[0])

    print("=" * 68)
    print("✅ Enterprise Data Warehouse Scenario Finished Successfully!")
    print("=" * 68)

if __name__ == "__main__":
    main()
