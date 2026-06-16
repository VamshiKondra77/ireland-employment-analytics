import pandas as pd

df = pd.read_csv(r'C:\Users\hp\OneDrive\Desktop\ireland-employment-analytics\data\EHQ03.20260616T100616.csv', nrows=5)
print("Columns:", df.columns.tolist())
print("\nDtypes:")
print(df.dtypes)
print("\nFirst 5 rows:")
print(df.head(5))