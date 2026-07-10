import streamlit as st
import pandas as pd
import duckdb
import g4f


st.set_page_config(page_title="Sports Analytics Dashboard", layout="wide")

st.title("⚽ Sports Data Pipeline")
st.subheader("Dashboard inteligent de analiză și rezumate automate bazate pe AI")


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
tab1, tab2, tab3, tab4 = st.tabs([
    "💎 Tineri Subvalorați", 
    "🔥 Hype vs Salarii", 
    "👵 Veteran Bargains", 
    "🏢 Valoarea Echipelor"
])

# --- TAB 1: GEMS ---
with tab1:
    st.header("Top Tineri de Viitor Subevaluați")
    st.write("Jucători de maximum 23 de ani, cu potențial uriaș (POT > 85) și preț accesibil (Value <= 10M).")
    
    query_gems = """
       SELECT Name, Age, Club, POT, Value 
       FROM fotbal_df 
       WHERE POT > 85 AND Age <= 23 AND Value <= 10000000 
       ORDER BY POT DESC LIMIT 15;
    """
    gems_df = duckdb.query(query_gems).to_df()
    
    col1, col2 = st.columns([1, 1])
    with col1:
        st.dataframe(gems_df, use_container_width=True)
    with col2:
        st.subheader("🤖 Analiză AI: Scouting Report")
        if st.button("Generează Raport Scouting", key="btn_gems"):
            with st.spinner("AI-ul analizează talentele..."):
                tabel_text = gems_df.to_markdown(index=False)
                prompt = f"""
                Ești un scout de top. Analizează acest tabel cu tineri subevaluați:
                {tabel_text}
                Generează un raport scurt (max 3 paragrafe) în limba română. Scoate în evidență jucătorii cu cel mai bun raport Calitate/Preț și oferă un sfat pentru utilizatorii de Fantasy Sports.
                """
                try:
                    response = g4f.ChatCompletion.create(model=g4f.models.gpt_4, messages=[{"role": "user", "content": prompt}])
                    st.markdown(response)
                except Exception as e:
                    st.error(f"Eroare AI: {e}")

# --- TAB 2: HYPE VS VALUE ---
with tab2:
    st.header("Corelația Hype (Hits) vs Salarii (Wage)")
    st.write("Cei mai căutați/populari jucători de pe platformă ordonați după numărul de vizualizări.")
    
    query_hype = """
       SELECT Name, Wage, Hits 
       FROM fotbal_df 
       ORDER BY Hits DESC LIMIT 15;
    """
    hype_df = duckdb.query(query_hype).to_df()
    
    col1, col2 = st.columns([1, 1])
    with col1:
        st.dataframe(hype_df, use_container_width=True)
    with col2:
        st.subheader("🤖 Analiză AI: Market Sentiment")
        if st.button("Generează Raport Popularitate", key="btn_hype"):
            with st.spinner("AI-ul analizează hype-ul comunității..."):
                tabel_text = hype_df.to_markdown(index=False)
                prompt = f"""
                Ești un analist de marketing sportiv. Analizează această corelație între vizualizări (Hits) și salarii (Wage):
                {tabel_text}
                Generează un raport scurt (max 3 paragrafe) în limba română. Explică dacă jucătorii foarte căutați își justifică salariul sau dacă sunt doar supraevaluați (hype comercial), oferind un insight pentru piața de pariuri.
                """
                try:
                    response = g4f.ChatCompletion.create(model=g4f.models.gpt_4, messages=[{"role": "user", "content": prompt}])
                    st.markdown(response)
                except Exception as e:
                    st.error(f"Eroare AI: {e}")

# --- TAB 3: VETERAN BARGAINS ---
with tab3:
    st.header("Veterani de Top la Preț Redus")
    st.write("Jucători de peste 32 de ani care mențin un rating mare (OVA >= 85), dar au o clauză mică.")
    
    query_bargain = """ 
        SELECT Name, Age, OVA, "Release Clause"
        FROM fotbal_df
        WHERE Age >= 32 AND OVA >= 85 AND "Release Clause" < 25000000
        ORDER BY OVA DESC;
    """
    bargain_df = duckdb.query(query_bargain).to_df()
    
    col1, col2 = st.columns([1, 1])
    with col1:
        st.dataframe(bargain_df, use_container_width=True)
    with col2:
        st.subheader("🤖 Analiză AI: Value Experience")
        if st.button("Generează Raport Veterani", key="btn_bargain"):
            with st.spinner("AI-ul analizează veteranii..."):
                tabel_text = bargain_df.to_markdown(index=False)
                prompt = f"""
                Ești un manager sportiv axat pe eficientizarea bugetelor. Analizează acest tabel cu veterani valoroși:
                {tabel_text}
                Generează un raport scurt (max 3 paragrafe) în limba română. Explică de ce acești jucători experimentați reprezintă oportunități pe termen scurt, în ciuda vârstei, și cum poate profita un parior de pe urma lor.
                """
                try:
                    response = g4f.ChatCompletion.create(model=g4f.models.gpt_4, messages=[{"role": "user", "content": prompt}])
                    st.markdown(response)
                except Exception as e:
                    st.error(f"Eroare AI: {e}")

# --- TAB 4: TEAM VALUATION ---
with tab4:
    st.header("Top 10 Cele Mai Valoroase Echipe")
    st.write("Valoarea totală cumulată a loturilor per club sportiv (excluzând jucătorii fără club).")
    
    query_team = """
        SELECT Club, COUNT(*) AS Players, SUM(Value) as Squad_Value
        FROM fotbal_df
        WHERE Club != 'No Club'
        GROUP BY Club
        ORDER BY Squad_Value DESC LIMIT 10;
    """
    team_df = duckdb.query(query_team).to_df()
    
    col1, col2 = st.columns([1, 1])
    with col1:
        st.dataframe(team_df, use_container_width=True)
    with col2:
        st.subheader("🤖 Analiză AI: Financial Report")
        if st.button("Generează Raport Financiar Echipe", key="btn_team"):
            with st.spinner("AI-ul analizează cluburile..."):
                tabel_text = team_df.to_markdown(index=False)
                prompt = f"""
                Ești un analist financiar din lumea fotbalului și lucrezi pentru. Analizează acest tabel cu top 10 cele mai valoroase echipe:
                {tabel_text}
                Te rog să generezi un raport scurt și dinamic (maximum 3 paragrafe) în limba română în care să analizezi aceste date. 
                Menționează care este cea mai valoroasă echipă, ce sugerează numărul de jucători raportat la valoare și oferă un insight util pentru pariori.
                """
                try:
                    response = g4f.ChatCompletion.create(model=g4f.models.gpt_4, messages=[{"role": "user", "content": prompt}])
                    st.markdown(response)
                except Exception as e:
                    st.error(f"Eroare AI: {e}")