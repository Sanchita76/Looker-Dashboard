"""Clean the Online Retail data and build 3 files for Looker Studio:
   retail_clean.csv  - one row per invoice line (main data source)
   rfm_customers.csv - one row per customer with RFM scores/segments (second source, blend on customer_id)
   product_summary.csv - one row per product
Usage: python scripts/prepare_data.py
"""
import os, sys
import numpy as np, pandas as pd

BASE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data")
RAW, OUT = os.path.join(BASE, "raw", "data.csv"), os.path.join(BASE, "processed")
NON_PRODUCT = {"POST", "D", "M", "DOT", "CRUK", "BANK CHARGES", "AMAZONFEE", "S", "B", "PADS", "C2"}


def main():
    if not os.path.exists(RAW):
        sys.exit(f"Missing {RAW}\nRun scripts/download_data.py, or download data.csv from Kaggle into data/raw, "
                 "or run scripts/make_demo_data.py")
    os.makedirs(OUT, exist_ok=True)
    df = pd.read_csv(RAW, encoding="ISO-8859-1", dtype={"InvoiceNo": str, "StockCode": str})
    n0 = len(df)
    df.columns = [c.strip() for c in df.columns]
    df = df.rename(columns={"InvoiceNo": "invoice_no", "StockCode": "stock_code", "Description": "description",
                            "Quantity": "quantity", "InvoiceDate": "invoice_datetime", "UnitPrice": "unit_price",
                            "CustomerID": "customer_id", "Country": "country"})
    df["invoice_datetime"] = pd.to_datetime(df["invoice_datetime"], format="mixed", dayfirst=False)
    df["description"] = df["description"].fillna("").str.strip().str.title()
    df = df.drop_duplicates()
    df = df[df["unit_price"] > 0]                      # drop free/adjustment rows
    df["is_guest"] = df["customer_id"].isna().astype(int)
    df["customer_id"] = df["customer_id"].apply(lambda x: "" if pd.isna(x) else str(int(x)))
    df["is_cancellation"] = df["invoice_no"].str.startswith("C").astype(int)
    df["is_non_product"] = df["stock_code"].str.upper().isin(NON_PRODUCT).astype(int)
    df["revenue"] = (df["quantity"] * df["unit_price"]).round(2)
    dt = df["invoice_datetime"]
    df["invoice_date"] = dt.dt.strftime("%Y%m%d")                # Looker Studio type: Date (YYYYMMDD)
    df["invoice_datetime"] = dt.dt.strftime("%Y-%m-%d %H:%M:%S")
    df["year_month"] = dt.dt.strftime("%Y-%m")
    df["weekday"] = dt.dt.strftime("%a"); df["weekday_num"] = dt.dt.weekday + 1
    df["hour"] = dt.dt.hour
    df["is_uk"] = (df["country"] == "United Kingdom").astype(int)
    cols = ["invoice_no", "stock_code", "description", "quantity", "unit_price", "revenue", "customer_id", "country",
            "invoice_date", "invoice_datetime", "year_month", "weekday", "weekday_num", "hour", "is_cancellation",
            "is_guest", "is_non_product", "is_uk"]
    clean = df[cols]
    clean.to_csv(os.path.join(OUT, "retail_clean.csv"), index=False)
    print(f"retail_clean.csv: {len(clean):,} rows (from {n0:,} raw)")

    # ---------------- RFM per customer (sales only, known customers) ----------------
    s = df[(df["is_cancellation"] == 0) & (df["customer_id"] != "") & (df["is_non_product"] == 0)].copy()
    s["_dt"] = pd.to_datetime(s["invoice_datetime"])
    snap = s["_dt"].max() + pd.Timedelta(days=1)
    rfm = s.groupby("customer_id").agg(
        country=("country", "first"), first_purchase=("_dt", "min"), last_purchase=("_dt", "max"),
        frequency=("invoice_no", "nunique"), monetary=("revenue", "sum"), items=("quantity", "sum")).reset_index()
    rfm["recency_days"] = (snap - rfm["last_purchase"]).dt.days
    rfm["monetary"] = rfm["monetary"].round(2)
    rfm["avg_order_value"] = (rfm["monetary"] / rfm["frequency"]).round(2)
    rfm["r_score"] = pd.qcut(rfm["recency_days"].rank(method="first"), 5, labels=[5, 4, 3, 2, 1]).astype(int)
    rfm["f_score"] = pd.qcut(rfm["frequency"].rank(method="first"), 5, labels=[1, 2, 3, 4, 5]).astype(int)
    rfm["m_score"] = pd.qcut(rfm["monetary"].rank(method="first"), 5, labels=[1, 2, 3, 4, 5]).astype(int)

    def seg(r):
        if r.r_score >= 4 and r.f_score >= 4: return "Champions"
        if r.r_score >= 3 and r.f_score >= 3: return "Loyal"
        if r.r_score >= 4 and r.f_score <= 2: return "New / Promising"
        if r.r_score <= 2 and r.f_score >= 4: return "Can't Lose Them"
        if r.r_score <= 2 and r.f_score >= 2: return "At Risk"
        if r.r_score <= 2: return "Lost"
        return "Need Attention"
    rfm["segment"] = rfm.apply(seg, axis=1)
    for c in ("first_purchase", "last_purchase"):
        rfm[c + "_date"] = rfm[c].dt.strftime("%Y%m%d"); rfm = rfm.drop(columns=[c])
    rfm.to_csv(os.path.join(OUT, "rfm_customers.csv"), index=False)
    print(f"rfm_customers.csv: {len(rfm):,} customers")

    # ---------------- product summary ----------------
    p = s.groupby(["stock_code"]).agg(description=("description", lambda x: x.mode().iat[0]),
                                      units=("quantity", "sum"), revenue=("revenue", "sum"),
                                      orders=("invoice_no", "nunique"), customers=("customer_id", "nunique"),
                                      avg_price=("unit_price", "mean")).reset_index()
    p[["revenue", "avg_price"]] = p[["revenue", "avg_price"]].round(2)
    p.to_csv(os.path.join(OUT, "product_summary.csv"), index=False)
    print(f"product_summary.csv: {len(p):,} products")
    size = os.path.getsize(os.path.join(OUT, "retail_clean.csv")) / 1e6
    print(f"retail_clean.csv size: {size:.1f} MB (Looker Studio file upload limit: 100 MB)")


if __name__ == "__main__":
    main()
