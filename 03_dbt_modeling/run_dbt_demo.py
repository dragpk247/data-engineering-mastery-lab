"""
03_dbt_modeling/run_dbt_demo.py
-------------------------------
Runs dbt build and testing directly using dbt-duckdb.
Key concepts:
- Lineage execution: stg_orders (view) -> fct_customer_revenue (table)
- Automated data quality tests (unique, not_null)
"""

import subprocess
import os
import duckdb

def main():
    print("=" * 65)
    print("🧱 dbt (data build tool) Lab: SQL Modeling & Automated Tests")
    print("=" * 65)

    base_dir = os.path.dirname(os.path.abspath(__file__))
    profiles_dir = base_dir

    print("\n1. Running dbt run (Compiling & Building Models)...")
    cmd_run = ["dbt", "run", "--project-dir", base_dir, "--profiles-dir", profiles_dir]
    subprocess.run(cmd_run, check=True)

    print("\n2. Running dbt test (Executing Automated Quality Assertions)...")
    cmd_test = ["dbt", "test", "--project-dir", base_dir, "--profiles-dir", profiles_dir]
    subprocess.run(cmd_test, check=True)

    print("\n3. Querying Final Mart Table from DuckDB...")
    con = duckdb.connect("/tmp/dbt_ecommerce.duckdb")
    df = con.execute("SELECT * FROM fct_customer_revenue").df()
    print(df)

    print("=" * 65)
    print("✅ dbt Modeling Lab Finished Successfully!")
    print("=" * 65)

if __name__ == "__main__":
    main()
