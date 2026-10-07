"""
11_b2b_data_sharing/b2b_sharing_demo.py
---------------------------------------
Demonstrates B2B Cross-Platform Sharing:
- Simulating Delta Sharing credential handshake
- Remote zero-download querying via HTTP/S3 Parquet endpoints
"""

import duckdb
import pyarrow as pa
import pyarrow.parquet as pq
import os
import json

DATA_DIR = "/tmp/b2b_sharing_demo"
os.makedirs(DATA_DIR, exist_ok=True)

def setup_shared_b2b_dataset():
    """Simulates a vendor preparing a zero-copy shared dataset for a partner."""
    export_file = os.path.join(DATA_DIR, "b2b_partner_stream.parquet")
    table = pa.table({
        "partner_id": ["P-10", "P-10", "P-10", "P-20"],
        "client_name": ["Apex Logistics", "Apex Logistics", "Apex Logistics", "Summit Retail"],
        "metric_date": ["2026-10-01", "2026-10-02", "2026-10-03", "2026-10-01"],
        "delivered_volume": [14200, 16800, 15900, 8900],
        "sla_on_time_pct": [99.2, 98.9, 99.5, 95.1]
    })
    pq.write_table(table, export_file)
    return export_file

def main():
    print("=" * 68)
    print("🤝 Module 11: B2B Cross-Platform Fast Data Sharing Demo")
    print("=" * 68)

    export_file = setup_shared_b2b_dataset()

    # 1. Delta Sharing Credential Simulation
    print("\n--- 1. Delta Sharing Security Token (config.share) ---")
    mock_share_profile = {
        "shareCredentialsVersion": 1,
        "endpoint": "https://sharing.datalake.enterprise.io/delta-sharing/",
        "bearerToken": "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.partner_b2b_scoped_token"
    }
    print(json.dumps(mock_share_profile, indent=2))
    print("Partner uses this token in Python, PowerBI, or Excel to query live tables.")

    # 2. Remote Client Direct Querying
    print("\n--- 2. Partner Queries Live Dataset on Different Stack ---")
    print("Partner runs standard SQL directly against vendor storage with 0 ETL:")
    
    con = duckdb.connect()
    partner_query = f"""
    SELECT 
        client_name,
        COUNT(*) as total_reporting_days,
        SUM(delivered_volume) as total_volume_delivered,
        ROUND(AVG(sla_on_time_pct), 2) as avg_sla_score
    FROM '{export_file}'
    WHERE partner_id = 'P-10'
    GROUP BY client_name;
    """
    
    partner_results = con.execute(partner_query).df()
    print(partner_results)

    print("\n--- Why This Beats Legacy SFTP/ETL ---")
    print("1. Instant Availability: Access granted in minutes via token / pre-signed URL.")
    print("2. Zero Data Duplication: Partner queries live storage without copying files.")
    print("3. Granular Revocation: Vendor revokes bearer token or S3 URL anytime.")

    print("=" * 68)
    print("✅ B2B Fast Sharing Demo Finished Successfully!")
    print("=" * 68)

if __name__ == "__main__":
    main()
