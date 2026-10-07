# 🚀 Modern Data Engineering Mastery Lab

A complete, production-grade learning curriculum covering the **essential job-ready tools** demanded by top data engineering teams in 2026.

---

## 🗺️ The Modern Data Engineering Ecosystem

```
 ┌────────────────────────────────────────────────────────────────────────┐
 │                      JOB-READY ECOSYSTEM MAP                           │
 ├───────────────────┬────────────────────────────┬───────────────────────┤
 │ 1. In-Process SQL │ 2. Rust DataFrames         │ 3. Transformation     │
 │   • DuckDB        │   • Polars                 │   • dbt (Core)        │
 │   (Fast columnar) │   (Multi-threaded speed)   │   (SQL Data Modeling) │
 ├───────────────────┼────────────────────────────┼───────────────────────┤
 │ 4. Real-Time Event│ 5. Open Table Formats      │ 6. Orchestration      │
 │   • Kafka         │   • Delta Lake & Iceberg   │   • Dagster           │
 │   (Pub/Sub stream)│   (ACID & Time Travel)     │   (Asset-Based DAGs)  │
 └───────────────────┴────────────────────────────┴───────────────────────┘
```

---

## 📂 Modules & Hands-On Labs

| Module | Technology | Real-World Purpose & Lab |
| :--- | :--- | :--- |
| **[`01_duckdb_analytics/`](./01_duckdb_analytics/)** | **DuckDB** | Fast analytical querying directly over Parquet files without spinning up clusters. |
| **[`02_polars_dataframes/`](./02_polars_dataframes/)** | **Polars** | The blazing-fast Rust DataFrame library replacing Pandas. Features lazy execution and query optimization. |
| **[`03_dbt_modeling/`](./03_dbt_modeling/)** | **dbt (data build tool)** | SQL transformation, schema testing, and documentation across Staging and Marts layers. |
| **[`04_kafka_streaming/`](./04_kafka_streaming/)** | **Apache Kafka** | Real-time event streaming: Topic creation, partitioned producers, consumer groups, and offset tracking. |
| **[`05_lakehouse_formats/`](./05_lakehouse_formats/)** | **Delta Lake** | Lakehouse table format with ACID transactions, time-travel history queries, and schema evolution. |
| **[`06_dagster_orchestration/`](./06_dagster_orchestration/)** | **Dagster** | Modern asset-based orchestration: Automate and schedule end-to-end data dependencies. |

---

## ⚡ Running Any Module (Powered by `uv`)

Every module in this repository is pre-configured to run instantly using `uv`:

```bash
# Clone the repository
git clone https://github.com/dragpk247/data-engineering-mastery-lab.git
cd data-engineering-mastery-lab

# Module 1: DuckDB Analytics
uv run python 01_duckdb_analytics/duckdb_lab.py

# Module 2: Polars DataFrames (Fast Rust Engine)
uv run python 02_polars_dataframes/polars_lab.py

# Module 3: dbt Data Modeling Simulation
uv run python 03_dbt_modeling/run_dbt_demo.py

# Module 4: Real-time Event Streaming (Kafka Pattern)
uv run python 04_kafka_streaming/streaming_events.py

# Module 5: Delta Lake ACID & Time Travel
uv run python 05_lakehouse_formats/delta_acid_lab.py

# Module 6: Dagster Software-Defined Assets
uv run python 06_dagster_orchestration/dagster_pipeline.py
```
