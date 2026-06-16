import snowflake.connector
import pandas as pd
import os
import numpy as np

# Snowflake connection
conn = snowflake.connector.connect(
    account='VQPUKTO-CK76732',
    user='VAMSHIKONDRA077',
    password='Vamshi@1234567',
    role='ACCOUNTADMIN',
    warehouse='COMPUTE_WH',
    database='IRELAND_ANALYTICS',
    schema='RAW'
)

cursor = conn.cursor()
print("✅ Connected to Snowflake successfully!")

# ── Create RAW tables ──────────────────────────

cursor.execute("""
CREATE OR REPLACE TABLE IRELAND_ANALYTICS.RAW.RAW_EARNINGS_BY_SECTOR (
    STATISTIC_LABEL     VARCHAR,
    QUARTER             VARCHAR,
    ECONOMIC_SECTOR     VARCHAR,
    TYPE_OF_EMPLOYEE    VARCHAR,
    UNIT                VARCHAR,
    VALUE               FLOAT
)
""")
print("✅ RAW_EARNINGS_BY_SECTOR table created!")

cursor.execute("""
CREATE OR REPLACE TABLE IRELAND_ANALYTICS.RAW.RAW_WEEKLY_EARNINGS (
    STATISTIC_LABEL     VARCHAR,
    QUARTER             VARCHAR,
    ECONOMIC_SECTOR     VARCHAR,
    UNIT                VARCHAR,
    VALUE               FLOAT
)
""")
print("✅ RAW_WEEKLY_EARNINGS table created!")

cursor.execute("""
CREATE OR REPLACE TABLE IRELAND_ANALYTICS.RAW.RAW_PUBLIC_PRIVATE (
    STATISTIC_LABEL     VARCHAR,
    QUARTER             VARCHAR,
    SECTOR_TYPE         VARCHAR,
    UNIT                VARCHAR,
    VALUE               FLOAT
)
""")
print("✅ RAW_PUBLIC_PRIVATE table created!")

# ── Load function ──────────────────────────────

data_path = r"C:\Users\hp\OneDrive\Desktop\ireland-employment-analytics\data"

def load_csv(filepath, table_name):
    print(f"\nLoading {os.path.basename(filepath)} into {table_name}...")
    df = pd.read_csv(filepath, encoding='utf-8', low_memory=False)
    
    # Clean column names
    df.columns = [c.strip().upper()
                   .replace(' ', '_')
                   .replace('-', '_')
                   .replace('.', '_') 
                  for c in df.columns]
    
    # Replace NaN with None so Snowflake gets NULL
    df = df.where(pd.notnull(df), None)
    
    print(f"  Columns: {df.columns.tolist()}")
    print(f"  Rows: {len(df):,}")
    
    rows = []
    for row in df.itertuples(index=False):
        clean_row = tuple(
            None if (v is np.nan or v != v) else v 
            for v in row
        )
        rows.append(clean_row)
    
    placeholders = ','.join(['%s'] * len(df.columns))
    batch_size = 5000
    total = 0
    
    for i in range(0, len(rows), batch_size):
        batch = rows[i:i+batch_size]
        cursor.executemany(
            f"INSERT INTO IRELAND_ANALYTICS.RAW.{table_name} VALUES ({placeholders})",
            batch
        )
        total += len(batch)
        print(f"  Progress: {total:,} / {len(rows):,} rows", end='\r')
    
    print(f"\n✅ {total:,} rows loaded into {table_name}!")

# ── Load all 3 files ───────────────────────────

load_csv(
    os.path.join(data_path, 'EHQ03.20260616T100616.csv'),
    'RAW_EARNINGS_BY_SECTOR'
)

load_csv(
    os.path.join(data_path, 'EHQ15.20260616T100642.csv'),
    'RAW_WEEKLY_EARNINGS'
)

load_csv(
    os.path.join(data_path, 'EHQ08.20260616T100606.csv'),
    'RAW_PUBLIC_PRIVATE'
)

# ── Verify row counts ──────────────────────────
print("\n📊 Final row counts in Snowflake:")
for table in ['RAW_EARNINGS_BY_SECTOR', 'RAW_WEEKLY_EARNINGS', 'RAW_PUBLIC_PRIVATE']:
    cursor.execute(f"SELECT COUNT(*) FROM IRELAND_ANALYTICS.RAW.{table}")
    count = cursor.fetchone()[0]
    print(f"  {table}: {count:,} rows")

cursor.close()
conn.close()
print("\n✅ Bronze layer complete!")