import pandas as pd

print("🔍 Începem faza de explorare a datelor...")
df = pd.read_csv("football_data.csv")

# 1. Vedem toate cele 77 de coloane și tipul lor de date
print("\n--- Toate coloanele din dataset ---")
# Dezactivăm trunchierea din Pandas ca să le vedem pe toate
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

# Afișăm coloanele, tipul lor și câte valori non-null au
print(df.info())

# 2. Verificăm unde avem cele mai multe valori lipsă (NaN)
print("\n--- Top coloane cu valori lipsă (NaN) ---")
missing_values = df.isnull().sum()
missing_values = missing_values[missing_values > 0].sort_values(ascending=False)
print(missing_values.head(20))

# 3. Să vedem câteva statistici rapide pe coloanele numerice
print("\n--- Statistici descriptive de bază ---")
print(df.describe(include='all').head(3)) # ne uităm doar la primele rânduri de statistici