import sqlite3
import os

import pandas as pd

from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer

import matplotlib.pyplot as plt

DB = "nifty100.db"

OUTPUT = "output"
REPORTS = "reports"

os.makedirs(OUTPUT, exist_ok=True)
os.makedirs(REPORTS, exist_ok=True)


conn = sqlite3.connect(DB)

ratios = pd.read_sql("SELECT * FROM financial_ratios", conn)

companies = pd.read_sql(
    """
    SELECT
        c.id,
        c.company_name,
        s.broad_sector
    FROM companies c
    LEFT JOIN sectors s
        ON c.id = s.company_id
    """,
    conn,
)

conn.close()
# ============================================================
# LATEST YEAR KPIs
# ============================================================

latest = ratios.sort_values("year").groupby("company_id").tail(1)

# Merge with company information
df = latest.merge(companies, left_on="company_id", right_on="id", how="left")

# ============================================================
# FEATURES FOR CLUSTERING
# ============================================================

features = [
    "return_on_equity_pct",
    "debt_to_equity",
    "operating_profit_margin_pct",
    "free_cash_flow_cr",
    "interest_coverage",
]
# ============================================================
# CHECK REQUIRED COLUMNS
# ============================================================

print("=" * 60)
print("Checking Required Columns")
print("=" * 60)

missing = [col for col in features if col not in df.columns]

if missing:

    print("Missing columns:", missing)
    exit()

print("All required columns found.")

print("=" * 60)

# ============================================================
# IMPUTE MISSING VALUES USING SECTOR MEDIAN
# ============================================================

for col in features:

    if col in df.columns:

        df[col] = df.groupby("broad_sector")[col].transform(
            lambda x: x.fillna(x.median())
        )

# Fill any remaining missing values with overall median
imputer = SimpleImputer(strategy="median")

X = pd.DataFrame(imputer.fit_transform(df[features]), columns=features)

print("Rows available for clustering :", len(X))
# ============================================================
# STANDARDIZE FEATURES
# ============================================================

scaler = StandardScaler()

X_scaled = scaler.fit_transform(X)

print("=" * 60)
print("Feature Scaling Completed")
print("=" * 60)

# ============================================================
# ELBOW METHOD
# ============================================================

inertia = []

k_values = range(2, 11)

for k in k_values:

    model = KMeans(n_clusters=k, random_state=42, n_init=10)

    model.fit(X_scaled)

    inertia.append(model.inertia_)

# ============================================================
# SAVE ELBOW PLOT
# ============================================================

plt.figure(figsize=(8, 5))

plt.plot(list(k_values), inertia, marker="o", linewidth=2)

plt.title("KMeans Elbow Plot")

plt.xlabel("Number of Clusters (k)")

plt.ylabel("Inertia")

plt.grid(True)

plt.tight_layout()

plt.savefig("reports/elbow_plot.png", dpi=300)

plt.close()

print("Saved : reports/elbow_plot.png")
# ============================================================
# FINAL KMEANS MODEL
# ============================================================

kmeans = KMeans(n_clusters=5, random_state=42, n_init=10)

clusters = kmeans.fit_predict(X_scaled)

df["cluster_id"] = clusters

# ============================================================
# DISTANCE FROM CENTROID
# ============================================================

distances = kmeans.transform(X_scaled)

df["distance_from_centroid"] = [
    distances[i][cluster] for i, cluster in enumerate(clusters)
]

# ============================================================
# CLUSTER NAMES
# ============================================================

cluster_names = {
    0: "High-Quality Compounders",
    1: "Defensive Dividend Payers",
    2: "Value Cyclicals",
    3: "Emerging Growth",
    4: "Distressed / Turnaround",
}

df["cluster_name"] = df["cluster_id"].map(cluster_names)

# ============================================================
# SAVE OUTPUT
# ============================================================

output = df[
    [
        "company_id",
        "company_name",
        "broad_sector",
        "cluster_id",
        "cluster_name",
        "distance_from_centroid",
    ]
].copy()

output["distance_from_centroid"] = output["distance_from_centroid"].round(4)

output.to_csv("output/cluster_labels.csv", index=False)

print("=" * 60)
print("KMeans Clustering Completed")
print("=" * 60)
print("Companies Clustered :", len(output))
print("Clusters :", output["cluster_id"].nunique())
print("Output : output/cluster_labels.csv")
print("Elbow Plot : reports/elbow_plot.png")
print("=" * 60)
