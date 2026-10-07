"""
06_dagster_orchestration/dagster_pipeline.py
--------------------------------------------
Demonstrates Dagster: Modern Asset-Based Orchestration.
Key concepts:
- Software-Defined Assets (@asset)
- Automatic dependency tracking (upstream -> downstream)
- Programmatic materialization and asset health tracking
"""

from dagster import asset, materialize, Definitions
import polars as pl

@asset
def raw_marketing_leads() -> pl.DataFrame:
    """Bronze Asset: Raw leads extracted from marketing webhooks."""
    print("Ingesting raw marketing leads...")
    return pl.DataFrame({
        "lead_id": ["L1", "L2", "L3", "L4", "L5"],
        "email": ["lead1@corp.com", "lead2@corp.com", None, "lead4@corp.com", "lead5@corp.com"],
        "company_size": [50, 500, 10, 2500, 15],
        "country": ["US", "UK", "US", "US", "DE"]
    })

@asset
def cleaned_enterprise_leads(raw_marketing_leads: pl.DataFrame) -> pl.DataFrame:
    """Silver Asset: Filters valid emails and enterprise-tier companies."""
    print("Cleaning and qualifying enterprise leads...")
    return raw_marketing_leads \
        .filter(pl.col("email").is_not_null()) \
        .filter(pl.col("company_size") >= 100) \
        .with_columns(is_enterprise=pl.lit(True))

@asset
def executive_leads_summary(cleaned_enterprise_leads: pl.DataFrame) -> pl.DataFrame:
    """Gold Asset: Aggregated country summary for sales leadership."""
    print("Generating executive lead aggregates...")
    return cleaned_enterprise_leads \
        .group_by("country") \
        .agg(
            qualified_enterprise_count=pl.len(),
            avg_company_headcount=pl.col("company_size").mean().round(1)
        )

defs = Definitions(assets=[raw_marketing_leads, cleaned_enterprise_leads, executive_leads_summary])

def main():
    print("=" * 65)
    print("⚙️ Dagster Lab: Modern Asset-Based Pipeline Orchestration")
    print("=" * 65)

    print("\nTriggering Asset Graph Materialization (DAG Execution)...")
    result = materialize([raw_marketing_leads, cleaned_enterprise_leads, executive_leads_summary])

    print(f"\nExecution Success: {result.success}")
    
    # Materialize and display the final gold asset
    final_gold = executive_leads_summary(cleaned_enterprise_leads(raw_marketing_leads()))
    print("\n--- Final Materialized Asset Output: executive_leads_summary ---")
    print(final_gold)

    print("=" * 65)
    print("✅ Dagster Orchestration Lab Finished Successfully!")
    print("=" * 65)

if __name__ == "__main__":
    main()
