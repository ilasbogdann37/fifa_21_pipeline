import pandas as pd
import duckdb

fotbal_df = pd.read_csv("football_data_clean.csv", low_memory=False)

print("📊 Conexiunea cu DuckDB este pregătită.")

query_gems = """
   SELECT
   Name,
   Age,
   POT,
   Value
   FROM fotbal_df
   WHERE POT > 85 AND Age <= 23 AND Value <= 10000000
   ORDER BY POT DESC;

"""

query_hype_vs_value = """
   SELECT
   Name,
   Wage,
   Hits
   FROM fotbal_df
   ORDER BY Hits DESC
   LIMIT 15

"""
query_bargain = """ 
    SELECT
    Name,
    Age,
    OVA,
    "Release Clause"

    FROM fotbal_df

    WHERE AGE >= 32 AND OVA >= 85 AND "Release Clause" < 25000000
    ORDER BY OVA DESC;

"""

query_team_valuation = """
SELECT 
    Club,
    COUNT(*) AS Players,
    SUM(Value) as Squad_Value
FROM fotbal_df
GROUP BY Club
ORDER BY Squad_Value DESC
LIMIT 10;



"""

gems= duckdb.query(query_gems).to_df()
value = duckdb.query(query_hype_vs_value).to_df()
bargain = duckdb.query(query_bargain).to_df()
team_valuation = duckdb.query(query_team_valuation).to_df()



import g4f  

tabel_echipe_text = team_valuation.to_markdown(index=False)

prompt = f"""
Ești un analist financiar de top din lumea fotbalului și lucrezi pentru FanDuel.
Iată un tabel cu top 10 cele mai valoroase echipe (loturi de jucători) extrase din baza noastră de date:

{tabel_echipe_text}

Te rog să generezi un raport scurt și dinamic (maximum 3 paragrafe) în limba română în care să analizezi aceste date. 
Menționează care este cea mai valoroasă echipă, ce sugerează numărul de jucători raportat la valoare și oferă un insight util pentru pariori.
"""

# 3. Apelăm modelul AI (folosim GPT-3.5 sau GPT-4 prin providerii gratuiți din g4f)
try:
    response = g4f.ChatCompletion.create(
        model=g4f.models.gpt_4, # Solicităm GPT-4
        messages=[{"role": "user", "content": prompt}],
    )
    
    print("\n📝 RAPORT GENERAT DE INTELIGENȚA ARTIFICIALĂ:")
    print("--------------------------------------------------")
    print(response)
    print("--------------------------------------------------")

except Exception as e:
    print(f"❌ A apărut o eroare la apelarea LLM-ului: {e}")