import streamlit as st
import pandas as pd
import duckdb
import g4f

# Configurarea paginii web
st.set_page_config(page_title="FanDuel Sports Analytics Dashboard", layout="wide")

st.title("⚽ FanDuel GenAI Sports Data Pipeline")
st.subheader("Dashboard inteligent de analiză și rezumate automate bazate pe AI")

# Funcție pentru încărcarea datelor (folosește cache-ul Streamlit ca să nu reîncarce la fiecare click)
@st.cache_data
def load_data():
    return pd.read_csv("football_data_clean.csv", low_memory=False)

try:
    fotbal_df = load_data()
    st.success("✅ Datele curate au fost încărcate cu succes din pipeline-ul ETL!")
except FileNotFoundError:
    st.error("❌ Nu am găsit 'football_data_clean.csv'. Rulează mai întâi scriptul 'clean_data.py'.")
    st.stop()

# --- INTERFAȚA CU UTILIZATORUL (TABS) ---
tab1, tab2, tab3 = st.tabs(["💎 Tineri Subvalorați", "🔥 Hype vs Salarii", "🏢 Valoarea Echipelor"])

# --- TAB 1: GEMS ---
with tab1:
    st.header("Top Tineri de Viitor Subevaluați")
    st.write("Jucători de maximum 23 de ani, cu potențial uriaș (POT > 85) și preț accesibil.")
    
    query_gems = """
       SELECT Name, Age, Club, POT, Value 
       FROM fotbal_df 
       WHERE POT > 85 AND Age <= 23 AND Value <= 10000000 
       ORDER BY POT DESC LIMIT 15;
    """
    gems_df = duckdb.query(query_gems).to_df()
    st.dataframe(gems_df, use_container_width=True)

# --- TAB 2: HYPE VS VALUE ---
with tab2:
    st.header("Corelația Hype (Hits) vs Salarii (Wage)")
    st.write("Cei mai căutați/populari jucători de pe platformă.")
    
    query_hype = """
       SELECT Name, Club, Wage, Hits 
       FROM fotbal_df 
       ORDER BY Hits DESC LIMIT 15;
    """
    hype_df = duckdb.query(query_hype).to_df()
    st.dataframe(hype_df, use_container_width=True)

# --- TAB 3: TEAM VALUATION ---
with tab3:
    st.header("Top 10 Cele Mai Valoroase Echipe")
    
    query_team = """
        SELECT Club, COUNT(*) AS Jucatori, SUM(Value) as Valoare_Lot_Euro
        FROM fotbal_df
        WHERE Club != 'No Club'
        GROUP BY Club
        ORDER BY Valoare_Lot_Euro DESC LIMIT 10;
    """
    team_df = duckdb.query(query_team).to_df()
    
    # Împărțim ecranul în două coloane: stânga tabelul, dreapta AI-ul
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.dataframe(team_df, use_container_width=True)
        
    with col2:
        st.subheader("🤖 Analiza Generată de AI")
        if st.button("Generează Raport Financiar"):
            with st.spinner("Inteligența Artificială analizează datele din tabel..."):
                tabel_text = team_df.to_markdown(index=False)
                prompt = f"""
                Ești un analist financiar de top de la FanDuel. Analizează acest tabel Markdown cu top 10 echipe valoroase:
                {tabel_text}
                Oferă un raport scurt, dinamic și structurat în limba română (maximum 3 paragrafe).
                Adaugă la final un sfat/insight util pentru pariori bazat pe aceste evaluări.
                """
                try:
                    response = g4f.ChatCompletion.create(
                        model=g4f.models.gpt_4,
                        messages=[{"role": "user", "content": prompt}]
                    )
                    st.markdown(response)
                except Exception as e:
                    st.error(f"Eroare la generarea raportului AI: {e}")