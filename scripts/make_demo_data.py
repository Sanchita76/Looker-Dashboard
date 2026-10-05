"""Fake data in the exact Online Retail format (data/raw/data.csv) for offline testing."""
import os
import numpy as np, pandas as pd

RAW = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data", "raw")
os.makedirs(RAW, exist_ok=True)
rng = np.random.default_rng(3)
products = [(f"{10000 + i}", d, round(float(rng.lognormal(1.1, .7)), 2)) for i, d in enumerate(
    ["WHITE HANGING HEART T-LIGHT HOLDER", "JUMBO BAG RED RETROSPOT", "REGENCY CAKESTAND 3 TIER", "PARTY BUNTING",
     "LUNCH BAG BLACK SKULL", "PAPER CHAIN KIT 50'S CHRISTMAS", "ASSORTED COLOUR BIRD ORNAMENT", "SET OF 3 CAKE TINS PANTRY DESIGN",
     "POPCORN HOLDER", "PACK OF 72 RETROSPOT CAKE CASES", "RABBIT NIGHT LIGHT", "VINTAGE DOILY JUMBO BAG RED",
     "STRAWBERRY CERAMIC TRINKET BOX", "HAND WARMER OWL DESIGN", "WOODEN FRAME ANTIQUE WHITE", "GARDENERS KNEELING PAD KEEP CALM"])]
countries = ["United Kingdom"] * 18 + ["Germany", "France", "EIRE", "Spain", "Netherlands", "Belgium", "Australia"]
rows = []
for inv in range(536365, 536365 + 4000):
    cid = int(rng.integers(12346, 12346 + 900)) if rng.random() > .2 else None
    ts = pd.Timestamp("2010-12-01") + pd.Timedelta(days=int(rng.integers(0, 365)), hours=int(rng.integers(8, 19)),
                                                   minutes=int(rng.integers(0, 60)))
    country = countries[int(rng.integers(len(countries)))]
    cancel = rng.random() < .02
    for _ in range(int(rng.integers(1, 6))):
        sc, desc, price = products[int(rng.integers(len(products)))]
        q = int(rng.choice([1, 2, 3, 6, 12, 24, 48]))
        rows.append(((f"C{inv}" if cancel else str(inv)), sc, desc, -q if cancel else q,
                     f"{ts.month}/{ts.day}/{ts.year} {ts.hour}:{ts.minute:02d}", price, cid, country))
df = pd.DataFrame(rows, columns=["InvoiceNo", "StockCode", "Description", "Quantity", "InvoiceDate", "UnitPrice",
                                 "CustomerID", "Country"])
df.loc[df.sample(20, random_state=1).index, "StockCode"] = "POST"
df.to_csv(os.path.join(RAW, "data.csv"), index=False, encoding="ISO-8859-1")
print("Demo data.csv written:", len(df), "rows")
