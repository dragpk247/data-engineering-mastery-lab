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

| Module | Technology | Real-World Scenario | Run Command |
| :--- | :--- | :--- | :--- |
| **[`01_duckdb_analytics/`](./01_duckdb_analytics/)** | **DuckDB** | In-process columnar SQL over local Parquet files with zero cloud spend. | `uv run python 01_duckdb_analytics/duckdb_lab.py` |
| **[`02_polars_dataframes/`](./02_polars_dataframes/)** | **Polars** | Multi-threaded Rust DataFrames, Lazy execution, and predicate pushdown. | `uv run python 02_polars_dataframes/polars_lab.py` |
| **[`03_dbt_modeling/`](./03_dbt_modeling/)** | **dbt (Core)** | Production SQL modeling: Staging views, Marts tables, tests & documentation. | `uv run python 03_dbt_modeling/run_dbt_demo.py` |
| **[`04_kafka_streaming/`](./04_kafka_streaming/)** | **Kafka Pattern** | Real-time event streaming: topic partitioning, consumer groups, offsets. | `uv run python 04_kafka_streaming/streaming_events.py` |
| **[`05_lakehouse_formats/`](./05_lakehouse_formats/)** | **Delta Lake** | Lakehouse open table formats: ACID transactions, commit log & time-travel. | `uv run python 05_lakehouse_formats/delta_acid_lab.py` |
| **[`06_dagster_orchestration/`](./06_dagster_orchestration/)** | **Dagster** | Modern asset-based orchestration: `@asset` graphs and automated DAG runs. | `uv run python 06_dagster_orchestration/dagster_pipeline.py` |
| **[`07_clickhouse_realtime_olap/`](./07_clickhouse_realtime_olap/)** | **ClickHouse** | **Scenario 1:** Real-time high-concurrency telemetry, P99 metrics & Materialized Views. | `uv run python 07_clickhouse_realtime_olap/clickhouse_telemetry_lab.py` |
| **[`08_trino_federated_lakehouse/`](./08_trino_federated_lakehouse/)** | **Trino (Presto)** | **Scenario 2:** Distributed query federation across S3 Lakehouse & Operational DBs without ETL. | `uv run python 08_trino_federated_lakehouse/trino_federation_lab.py` |
| **[`09_enterprise_warehouse_patterns/`](./09_enterprise_warehouse_patterns/)** | **Snowflake / BigQuery** | **Scenario 3:** Enterprise cloud warehouse: Zero-Copy Cloning, micro-partition pruning & time-travel. | `uv run python 09_enterprise_warehouse_patterns/warehouse_patterns_lab.py` |


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
