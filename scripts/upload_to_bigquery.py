"""OPTIONAL: load the processed CSVs into Google BigQuery (free sandbox works), then connect Looker Studio to BigQuery.
Setup:  pip install google-cloud-bigquery pandas pyarrow ; gcloud auth application-default login
Usage:  python scripts/upload_to_bigquery.py --project YOUR_PROJECT_ID --dataset retail
Most beginners should skip this and use CSV File Upload in Looker Studio (see README).
"""
import argparse, os
import pandas as pd
from google.cloud import bigquery

ap = argparse.ArgumentParser()
ap.add_argument("--project", required=True); ap.add_argument("--dataset", default="retail")
a = ap.parse_args()
proc = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data", "processed")
client = bigquery.Client(project=a.project)
client.create_dataset(bigquery.Dataset(f"{a.project}.{a.dataset}"), exists_ok=True)
for name in ("retail_clean", "rfm_customers", "product_summary"):
    df = pd.read_csv(os.path.join(proc, name + ".csv"), dtype={"customer_id": str, "invoice_date": str,
                                                                "first_purchase_date": str, "last_purchase_date": str})
    if "invoice_datetime" in df: df["invoice_datetime"] = pd.to_datetime(df["invoice_datetime"])
    if "invoice_date" in df: df["invoice_date"] = pd.to_datetime(df["invoice_date"], format="%Y%m%d").dt.date
    job = client.load_table_from_dataframe(df, f"{a.project}.{a.dataset}.{name}",
                                           job_config=bigquery.LoadJobConfig(write_disposition="WRITE_TRUNCATE"))
    job.result(); print(f"Loaded {name}: {len(df):,} rows")
print("Done. In Looker Studio: Add data -> BigQuery -> choose project/dataset/table.")
