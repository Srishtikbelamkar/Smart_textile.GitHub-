import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

# ============================================================
# SMART TEXTILE MANUFACTURING ANALYTICS
# ============================================================

FILE = "Smart_Textile.csv"

os.makedirs("data", exist_ok=True)
os.makedirs("graphs", exist_ok=True)

# ---------------- LOAD DATA ----------------

df = pd.read_csv(FILE)

df["Production_Date"] = pd.to_datetime(
    df["Production_Date"], errors="coerce"
)

numeric_cols = [
    "Planned_Qty",
    "Produced_Qty",
    "Good_Qty",
    "Rejected_Qty",
    "Production_Hours",
    "Downtime_Hours",
    "Raw_Material_Used_Kg",
    "Wastage_Kg",
    "Production_Efficiency",
    "Defect_Rate",
    "Machine_Efficiency",
    "Quality_Score"
]

for col in numeric_cols:
    df[col] = pd.to_numeric(df[col], errors="coerce")

df["Year"] = df["Production_Date"].dt.year
df["Month"] = df["Production_Date"].dt.month
df["Month_Name"] = df["Production_Date"].dt.strftime("%B")

print("\nSMART TEXTILE MANUFACTURING ANALYTICS")
print("=" * 70)

print("Total Records:", len(df))
print("Date From:", df["Production_Date"].min().date())
print("Date To:", df["Production_Date"].max().date())

# ============================================================
# ALL DATASET RECORDS
# ============================================================

print("\nFULL DATASET")
print("=" * 70)
print(df.to_string(index=False))

# ============================================================
# KPI
# ============================================================

print("\nKEY PERFORMANCE INDICATORS")
print("=" * 70)

print("Total Planned Quantity      :", f"{df['Planned_Qty'].sum():,.0f}")
print("Total Produced Quantity     :", f"{df['Produced_Qty'].sum():,.0f}")
print("Total Good Quantity         :", f"{df['Good_Qty'].sum():,.0f}")
print("Total Rejected Quantity     :", f"{df['Rejected_Qty'].sum():,.0f}")
print("Total Wastage               :", f"{df['Wastage_Kg'].sum():,.2f} Kg")
print("Average Production Efficiency:", f"{df['Production_Efficiency'].mean():.2f}%")
print("Average Machine Efficiency   :", f"{df['Machine_Efficiency'].mean():.2f}%")
print("Average Defect Rate          :", f"{df['Defect_Rate'].mean():.2f}%")
print("Average Quality Score        :", f"{df['Quality_Score'].mean():.2f}")

# ============================================================
# YEAR ANALYSIS
# ============================================================

print("\nYEAR ANALYSIS")
print("=" * 70)

year_analysis = df.groupby("Year").agg(
    Planned_Qty=("Planned_Qty", "sum"),
    Produced_Qty=("Produced_Qty", "sum"),
    Good_Qty=("Good_Qty", "sum"),
    Rejected_Qty=("Rejected_Qty", "sum"),
    Production_Efficiency=("Production_Efficiency", "mean"),
    Defect_Rate=("Defect_Rate", "mean"),
    Machine_Efficiency=("Machine_Efficiency", "mean"),
    Quality_Score=("Quality_Score", "mean")
).round(2)

print(year_analysis)


# ============================================================
# MONTH ANALYSIS
# ============================================================

print("\nMONTH ANALYSIS")
print("=" * 70)

month_analysis = df.groupby(["Year", "Month", "Month_Name"]).agg(
    Produced_Qty=("Produced_Qty", "sum"),
    Good_Qty=("Good_Qty", "sum"),
    Rejected_Qty=("Rejected_Qty", "sum"),
    Production_Efficiency=("Production_Efficiency", "mean"),
    Defect_Rate=("Defect_Rate", "mean"),
    Quality_Score=("Quality_Score", "mean")
).round(2)

print(month_analysis)

# ============================================================
# MACHINE ANALYSIS
# ============================================================

print("\nMACHINE ANALYSIS")
print("=" * 70)

machine_analysis = df.groupby("Machine_ID").agg(
    Produced_Qty=("Produced_Qty", "sum"),
    Good_Qty=("Good_Qty", "sum"),
    Rejected_Qty=("Rejected_Qty", "sum"),
    Production_Efficiency=("Production_Efficiency", "mean"),
    Machine_Efficiency=("Machine_Efficiency", "mean"),
    Defect_Rate=("Defect_Rate", "mean"),
    Quality_Score=("Quality_Score", "mean"),
    Downtime_Hours=("Downtime_Hours", "sum")
).round(2)

print(machine_analysis)

# ============================================================
# SHIFT ANALYSIS
# ============================================================

print("\nSHIFT ANALYSIS")
print("=" * 70)

shift_analysis = df.groupby("Shift").agg(
    Produced_Qty=("Produced_Qty", "sum"),
    Good_Qty=("Good_Qty", "sum"),
    Rejected_Qty=("Rejected_Qty", "sum"),
    Production_Efficiency=("Production_Efficiency", "mean"),
    Defect_Rate=("Defect_Rate", "mean"),
    Quality_Score=("Quality_Score", "mean")
).round(2)

print(shift_analysis)

# ============================================================
# PRODUCT ANALYSIS
# ============================================================

print("\nPRODUCT ANALYSIS")
print("=" * 70)

product_analysis = df.groupby("Product_Name").agg(
    Produced_Qty=("Produced_Qty", "sum"),
    Good_Qty=("Good_Qty", "sum"),
    Rejected_Qty=("Rejected_Qty", "sum"),
    Production_Efficiency=("Production_Efficiency", "mean"),
    Defect_Rate=("Defect_Rate", "mean"),
    Quality_Score=("Quality_Score", "mean")
).round(2)

print(product_analysis)

# ============================================================
# FABRIC ANALYSIS
# ============================================================

print("\nFABRIC ANALYSIS")
print("=" * 70)

fabric_analysis = df.groupby("Fabric_Type").agg(
    Produced_Qty=("Produced_Qty", "sum"),
    Good_Qty=("Good_Qty", "sum"),
    Rejected_Qty=("Rejected_Qty", "sum"),
    Production_Efficiency=("Production_Efficiency", "mean"),
    Defect_Rate=("Defect_Rate", "mean"),
    Quality_Score=("Quality_Score", "mean")
).round(2)

print(fabric_analysis)

# ============================================================
# OPERATOR ANALYSIS
# ============================================================

print("\nOPERATOR ANALYSIS")
print("=" * 70)

operator_analysis = df.groupby("Operator_ID").agg(
    Produced_Qty=("Produced_Qty", "sum"),
    Good_Qty=("Good_Qty", "sum"),
    Rejected_Qty=("Rejected_Qty", "sum"),
    Production_Efficiency=("Production_Efficiency", "mean"),
    Defect_Rate=("Defect_Rate", "mean"),
    Quality_Score=("Quality_Score", "mean")
).round(2)

print(operator_analysis)

# ============================================================
# DEFECT ANALYSIS
# ============================================================

print("\nDEFECT ANALYSIS")
print("=" * 70)

defect_analysis = df.groupby("Defect_Type").agg(
    Occurrences=("Defect_Type", "count"),
    Rejected_Qty=("Rejected_Qty", "sum"),
    Defect_Rate=("Defect_Rate", "mean"),
    Quality_Score=("Quality_Score", "mean")
).sort_values(
    "Occurrences", ascending=False
).round(2)

print(defect_analysis)


# ============================================================
# QUALITY ANALYSIS
# ============================================================

print("\nQUALITY ANALYSIS")
print("=" * 70)

quality_analysis = df.groupby("Quality_Level").agg(
    Records=("Quality_Level", "count"),
    Produced_Qty=("Produced_Qty", "sum"),
    Good_Qty=("Good_Qty", "sum"),
    Rejected_Qty=("Rejected_Qty", "sum"),
    Quality_Score=("Quality_Score", "mean"),
    Defect_Rate=("Defect_Rate", "mean")
).sort_values(
    "Records", ascending=False
).round(2)

print(quality_analysis)

# ============================================================
# PRODUCTION STATUS ANALYSIS
# ============================================================

print("\nPRODUCTION STATUS ANALYSIS")
print("=" * 70)

status_analysis = df.groupby("Production_Status").agg(
    Records=("Production_Status", "count"),
    Planned_Qty=("Planned_Qty", "sum"),
    Produced_Qty=("Produced_Qty", "sum"),
    Good_Qty=("Good_Qty", "sum"),
    Rejected_Qty=("Rejected_Qty", "sum"),
    Production_Efficiency=("Production_Efficiency", "mean"),
    Defect_Rate=("Defect_Rate", "mean"),
    Quality_Score=("Quality_Score", "mean")
).round(2)

print(status_analysis)

# ============================================================
# SAVE ALL ANALYSIS
# ============================================================

with pd.ExcelWriter(
    "Smart_Textile_Analysis.xlsx",
    engine="openpyxl"
) as writer:

    year_analysis.to_excel(writer, sheet_name="Year_Analysis")
    month_analysis.to_excel(writer, sheet_name="Month_Analysis")
    machine_analysis.to_excel(writer, sheet_name="Machine_Analysis")
    shift_analysis.to_excel(writer, sheet_name="Shift_Analysis")
    product_analysis.to_excel(writer, sheet_name="Product_Analysis")
    fabric_analysis.to_excel(writer, sheet_name="Fabric_Analysis")
    operator_analysis.to_excel(writer, sheet_name="Operator_Analysis")
    defect_analysis.to_excel(writer, sheet_name="Defect_Analysis")
    quality_analysis.to_excel(writer, sheet_name="Quality_Analysis")

print("\nAnalysis saved successfully!")
print("File: Smart_Textile_Analysis.xlsx")

# ============================================================
# GRAPHS
# ============================================================

# ============================================================
# 1. PRODUCTION TREND
# ============================================================
# ============================================================
# 1. PRODUCTION TREND
# ============================================================

# Create a copy so the original analysis is not affected
trend = month_analysis.reset_index().copy()

# Create date from Year and Month
trend["Date"] = pd.to_datetime(
    trend["Year"].astype(str) + "-" +
    trend["Month"].astype(str) + "-01"
)

# Sort by date
trend = trend.sort_values("Date")

# Create graph
plt.figure(figsize=(14, 6))

plt.plot(
    trend["Date"],
    trend["Produced_Qty"],
    marker="o",
    linewidth=2
)

plt.title("Monthly Production Trend")
plt.xlabel("Year / Month")
plt.ylabel("Produced Quantity")

plt.xticks(rotation=45)
plt.grid(True, alpha=0.3)

plt.tight_layout()

# Save graph
plt.savefig(
    "graphs/production_trend.png",
    dpi=300,
    bbox_inches="tight"
)

# SHOW GRAPH IN VS CODE
plt.show()

plt.close()


# ============================================================
# 2. YEARLY PRODUCTION
# ============================================================

plt.figure(figsize=(10, 6))

plt.bar(
    year_analysis.index.astype(str),
    year_analysis["Produced_Qty"]
)

plt.title("Year-wise Production")
plt.xlabel("Year")
plt.ylabel("Produced Quantity")
plt.grid(axis="y", alpha=0.3)
plt.tight_layout()

plt.savefig(
    "graphs/yearly_production.png",
    dpi=300
)

plt.show()   # Displays the graph

plt.close()

# ============================================================
# 3. MACHINE EFFICIENCY
# ============================================================

machine = machine_analysis.reset_index()

plt.figure(figsize=(10, 6))

plt.bar(
    machine["Machine_ID"],
    machine["Machine_Efficiency"]
)

plt.title("Machine-wise Efficiency")
plt.xlabel("Machine ID")
plt.ylabel("Efficiency (%)")
plt.ylim(0, 100)
plt.grid(axis="y", alpha=0.3)
plt.tight_layout()

plt.savefig(
    "graphs/machine_efficiency.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()
plt.close()


# ============================================================
# 4. SHIFT PRODUCTION
# ============================================================

shift = shift_analysis.reset_index()

plt.figure(figsize=(9, 6))

plt.bar(
    shift["Shift"],
    shift["Produced_Qty"]
)

plt.title("Shift-wise Production")
plt.xlabel("Shift")
plt.ylabel("Produced Quantity")
plt.grid(axis="y", alpha=0.3)
plt.tight_layout()

plt.savefig(
    "graphs/shift_production.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()
plt.close()

# ============================================================
# 5. DEFECT ANALYSIS
# ============================================================

defect = defect_analysis.reset_index()

plt.figure(figsize=(10, 7))

plt.barh(
    defect["Defect_Type"],
    defect["Rejected_Qty"]
)

plt.title("Defect-wise Rejected Quantity")
plt.xlabel("Rejected Quantity")
plt.ylabel("Defect Type")
plt.tight_layout()

plt.savefig(
    "graphs/defect_analysis.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()
plt.close()

# ============================================================
# 6. WASTAGE TREND
# ============================================================

# Create monthly wastage analysis
monthly = df.groupby(
    ["Year", "Month"]
).agg(
    Wastage_Kg=("Wastage_Kg", "sum")
).reset_index()

monthly["Production_Date"] = pd.to_datetime(
    monthly["Year"].astype(str) + "-" +
    monthly["Month"].astype(str) + "-01"
)

monthly = monthly.sort_values("Production_Date")

plt.figure(figsize=(14, 6))

plt.plot(
    monthly["Production_Date"],
    monthly["Wastage_Kg"],
    marker="o",
    linewidth=2
)

plt.title("Monthly Material Wastage")
plt.xlabel("Date")
plt.ylabel("Wastage (Kg)")
plt.xticks(rotation=45)
plt.grid(True, alpha=0.3)
plt.tight_layout()

plt.savefig(
    "graphs/wastage_trend.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()
plt.close()

# ============================================================
# 7. QUALITY DISTRIBUTION
# ============================================================

quality_count = df["Quality_Level"].value_counts()

plt.figure(figsize=(8, 8))

plt.pie(
    quality_count.values,
    labels=quality_count.index,
    autopct="%1.1f%%",
    startangle=90
)

plt.title("Quality Level Distribution")
plt.tight_layout()

plt.savefig(
    "graphs/quality_distribution.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()
plt.close()

# ============================================================
# PROJECT COMPLETED
# ============================================================

print("\n" + "=" * 70)
print("PROJECT COMPLETED SUCCESSFULLY")
print("=" * 70)


print("Graphs Folder   : graphs/")