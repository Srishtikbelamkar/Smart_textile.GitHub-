import pandas as pd
import mysql.connector


# ============================================================
# 1. LOAD CSV FILE
# ============================================================

csv_file = r"C:\Users\hp\OneDrive\Desktop\mini project\Smart Textile Manufacturing Analytics\Smart_Textile.csv"

df = pd.read_csv(csv_file)

print("CSV loaded successfully!")
print("Total records:", len(df))
print(df.head())


# ============================================================
# 2. MYSQL CONNECTION
# ============================================================

connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="12345",
    database="smart_textile_db"
)

print("MySQL connected successfully!")


# ============================================================
# 3. CREATE CURSOR
# ============================================================

cursor = connection.cursor()

print("MySQL cursor created successfully!")
print("SMART TEXTILE MYSQL PROGRAM STARTED")


# ============================================================
# 4. CREATE TABLE
# ============================================================

create_table = """
CREATE TABLE IF NOT EXISTS Production_Data (

    Production_ID VARCHAR(50) PRIMARY KEY,
    Production_Date DATE,
    Shift VARCHAR(20),
    Product_Name VARCHAR(100),
    Fabric_Type VARCHAR(100),
    Machine_ID VARCHAR(50),
    Operator_ID VARCHAR(50),

    Planned_Qty INT,
    Produced_Qty INT,
    Good_Qty INT,
    Rejected_Qty INT,

    Production_Hours DECIMAL(10,2),
    Downtime_Hours DECIMAL(10,2),

    Raw_Material_Used_Kg DECIMAL(10,2),
    Wastage_Kg DECIMAL(10,2),

    Defect_Type VARCHAR(100),

    Production_Efficiency DECIMAL(10,2),
    Defect_Rate DECIMAL(10,2),
    Machine_Efficiency DECIMAL(10,2),
    Quality_Score DECIMAL(10,2),

    Quality_Level VARCHAR(50),
    Production_Status VARCHAR(50)
)
"""

cursor.execute(create_table)

print("Production_Data table created successfully!")


# ============================================================
# 5. REMOVE OLD DATA
# ============================================================

cursor.execute("TRUNCATE TABLE Production_Data")

connection.commit()

print("Old data removed successfully!")


# ============================================================
# 6. PREPARE DATE COLUMN
# ============================================================

df["Production_Date"] = pd.to_datetime(
    df["Production_Date"],
    errors="coerce"
)


# ============================================================
# 7. REPLACE EMPTY VALUES WITH NONE
# ============================================================

df = df.where(pd.notnull(df), None)


# ============================================================
# 8. INSERT QUERY
# ============================================================

insert_query = """
INSERT INTO Production_Data (
    Production_ID,
    Production_Date,
    Shift,
    Product_Name,
    Fabric_Type,
    Machine_ID,
    Operator_ID,
    Planned_Qty,
    Produced_Qty,
    Good_Qty,
    Rejected_Qty,
    Production_Hours,
    Downtime_Hours,
    Raw_Material_Used_Kg,
    Wastage_Kg,
    Defect_Type,
    Production_Efficiency,
    Defect_Rate,
    Machine_Efficiency,
    Quality_Score,
    Quality_Level,
    Production_Status
)
VALUES (
    %s, %s, %s, %s, %s, %s, %s,
    %s, %s, %s, %s,
    %s, %s,
    %s, %s,
    %s,
    %s, %s, %s, %s,
    %s, %s
)
"""


# ============================================================
# 9. CONVERT DATAFRAME TO TUPLES
# ============================================================

data = []

for _, row in df.iterrows():

    values = (
        row["Production_ID"],

        row["Production_Date"].date()
        if row["Production_Date"] is not None
        else None,

        row["Shift"],
        row["Product_Name"],
        row["Fabric_Type"],
        row["Machine_ID"],
        row["Operator_ID"],

        row["Planned_Qty"],
        row["Produced_Qty"],
        row["Good_Qty"],
        row["Rejected_Qty"],

        row["Production_Hours"],
        row["Downtime_Hours"],

        row["Raw_Material_Used_Kg"],
        row["Wastage_Kg"],

        row["Defect_Type"],

        row["Production_Efficiency"],
        row["Defect_Rate"],
        row["Machine_Efficiency"],
        row["Quality_Score"],

        row["Quality_Level"],
        row["Production_Status"]
    )

    data.append(values)


# ============================================================
# 10. INSERT ALL RECORDS - ONLY ONCE
# ============================================================

cursor.executemany(
    insert_query,
    data
)

connection.commit()

print("All records inserted successfully!")


# ============================================================
# 11. CHECK TOTAL RECORDS
# ============================================================

cursor.execute("""
SELECT COUNT(*) FROM Production_Data
""")

total_records = cursor.fetchone()[0]

print("Total records in MySQL:", total_records)


# ============================================================
# 12. YEAR-WISE ANALYSIS
# ============================================================

print("\nYEAR-WISE PRODUCTION")
print("=" * 60)

cursor.execute("""
SELECT
    YEAR(Production_Date) AS Year,
    SUM(Produced_Qty) AS Produced_Qty,
    SUM(Good_Qty) AS Good_Qty,
    SUM(Rejected_Qty) AS Rejected_Qty,
    ROUND(AVG(Production_Efficiency), 2)
        AS Production_Efficiency
FROM Production_Data
GROUP BY YEAR(Production_Date)
ORDER BY Year
""")

for row in cursor.fetchall():
    print(row)


# ============================================================
# 13. MACHINE ANALYSIS
# ============================================================

print("\nMACHINE ANALYSIS")
print("=" * 60)

cursor.execute("""
SELECT
    Machine_ID,
    SUM(Produced_Qty) AS Produced_Qty,
    ROUND(AVG(Machine_Efficiency), 2)
        AS Machine_Efficiency,
    ROUND(AVG(Defect_Rate), 2)
        AS Defect_Rate
FROM Production_Data
GROUP BY Machine_ID
ORDER BY Machine_ID
""")

for row in cursor.fetchall():
    print(row)


# ============================================================
# 14. SHIFT ANALYSIS
# ============================================================

print("\nSHIFT ANALYSIS")
print("=" * 60)

cursor.execute("""
SELECT
    Shift,
    SUM(Produced_Qty) AS Produced_Qty,
    SUM(Good_Qty) AS Good_Qty,
    SUM(Rejected_Qty) AS Rejected_Qty,
    ROUND(AVG(Production_Efficiency), 2)
        AS Production_Efficiency
FROM Production_Data
GROUP BY Shift
""")

for row in cursor.fetchall():
    print(row)


# ============================================================
# 15. PRODUCT ANALYSIS
# ============================================================

print("\nPRODUCT ANALYSIS")
print("=" * 60)

cursor.execute("""
SELECT
    Product_Name,
    SUM(Produced_Qty) AS Produced_Qty,
    SUM(Good_Qty) AS Good_Qty,
    SUM(Rejected_Qty) AS Rejected_Qty,
    ROUND(AVG(Quality_Score), 2)
        AS Quality_Score
FROM Production_Data
GROUP BY Product_Name
ORDER BY Produced_Qty DESC
""")

for row in cursor.fetchall():
    print(row)


# ============================================================
# 16. FABRIC ANALYSIS
# ============================================================

print("\nFABRIC ANALYSIS")
print("=" * 60)

cursor.execute("""
SELECT
    Fabric_Type,
    SUM(Produced_Qty) AS Produced_Qty,
    SUM(Wastage_Kg) AS Wastage_Kg,
    ROUND(AVG(Quality_Score), 2)
        AS Quality_Score
FROM Production_Data
GROUP BY Fabric_Type
""")

for row in cursor.fetchall():
    print(row)


# ============================================================
# 17. OPERATOR ANALYSIS
# ============================================================

print("\nOPERATOR ANALYSIS")
print("=" * 60)

cursor.execute("""
SELECT
    Operator_ID,
    SUM(Produced_Qty) AS Produced_Qty,
    ROUND(AVG(Production_Efficiency), 2)
        AS Production_Efficiency,
    ROUND(AVG(Quality_Score), 2)
        AS Quality_Score
FROM Production_Data
GROUP BY Operator_ID
ORDER BY Produced_Qty DESC
""")

for row in cursor.fetchall():
    print(row)


# ============================================================
# 18. DEFECT ANALYSIS
# ============================================================

print("\nDEFECT ANALYSIS")
print("=" * 60)

cursor.execute("""
SELECT
    Defect_Type,
    COUNT(*) AS Records,
    SUM(Rejected_Qty) AS Rejected_Qty,
    ROUND(AVG(Defect_Rate), 2)
        AS Defect_Rate
FROM Production_Data
GROUP BY Defect_Type
ORDER BY Rejected_Qty DESC
""")

for row in cursor.fetchall():
    print(row)


# ============================================================
# 19. QUALITY ANALYSIS
# ============================================================

print("\nQUALITY ANALYSIS")
print("=" * 60)

cursor.execute("""
SELECT
    Quality_Level,
    COUNT(*) AS Records,
    SUM(Good_Qty) AS Good_Qty,
    SUM(Rejected_Qty) AS Rejected_Qty,
    ROUND(AVG(Quality_Score), 2)
        AS Quality_Score
FROM Production_Data
GROUP BY Quality_Level
ORDER BY Quality_Score DESC
""")

for row in cursor.fetchall():
    print(row)


# ============================================================
# 20. PRODUCTION STATUS ANALYSIS
# ============================================================

print("\nPRODUCTION STATUS ANALYSIS")
print("=" * 60)

cursor.execute("""
SELECT
    Production_Status,
    COUNT(*) AS Records,
    SUM(Produced_Qty) AS Produced_Qty,
    SUM(Good_Qty) AS Good_Qty,
    SUM(Rejected_Qty) AS Rejected_Qty
FROM Production_Data
GROUP BY Production_Status
""")

for row in cursor.fetchall():
    print(row)


# ============================================================
# 21. OVERALL KPI
# ============================================================

print("\nOVERALL PRODUCTION KPI")
print("=" * 60)

cursor.execute("""
SELECT
    SUM(Planned_Qty) AS Total_Planned,
    SUM(Produced_Qty) AS Total_Produced,
    SUM(Good_Qty) AS Total_Good,
    SUM(Rejected_Qty) AS Total_Rejected,

    ROUND(AVG(Production_Efficiency), 2)
        AS Avg_Production_Efficiency,

    ROUND(AVG(Machine_Efficiency), 2)
        AS Avg_Machine_Efficiency,

    ROUND(AVG(Defect_Rate), 2)
        AS Avg_Defect_Rate,

    ROUND(AVG(Quality_Score), 2)
        AS Avg_Quality_Score,

    ROUND(SUM(Wastage_Kg), 2)
        AS Total_Wastage_Kg

FROM Production_Data
""")

kpi = cursor.fetchone()

print("Total Planned:", kpi[0])
print("Total Produced:", kpi[1])
print("Total Good:", kpi[2])
print("Total Rejected:", kpi[3])
print("Average Production Efficiency:", kpi[4])
print("Average Machine Efficiency:", kpi[5])
print("Average Defect Rate:", kpi[6])
print("Average Quality Score:", kpi[7])
print("Total Wastage Kg:", kpi[8])


# ============================================================
# 22. CLOSE CONNECTION
# ============================================================

cursor.close()
connection.close()

print("\n" + "=" * 60)
print("SMART TEXTILE MYSQL ANALYSIS COMPLETED")
print("=" * 60)