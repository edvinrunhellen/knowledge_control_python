import streamlit as st
import requests
from io import BytesIO
import streamlit as st

# Sidhuvud
st.title("💎 Välkommen till DiamondPicker")

st.header("🎯 Verktyget")
st.markdown("""
Verktyget finner diamanter i viktklassen **0.3–0.4 carat**, då detta segment:

- Är populärt i Norden  
- Har hög efterfrågan  
- Har god tillgång  
""")

st.header("✅ Urvalskriterier")
st.markdown("""
Endast diamanter som uppfyller följande kriterier visas:

- **Carat**: 0.3 – 0.4  
- **Clarity**: IF eller VVS1  
- **Color**: E, F eller G  
- **Cut**: Excellent  
""")

# Sektion: Dataset-information
st.header("📂 Datasetet: diamonds.csv")
st.markdown("""
Du kan ladda ner datasetet nedan och använda det""")


# URL till råfilen på GitHub (OBS! Använd råfil, inte visnings-URL)
url = "https://raw.githubusercontent.com/edvinrunhellen/DiamondLens/v2/streamlit_app/streamlit_app/data/diamonds.csv"

# Hämta innehållet
response = requests.get(url)
csv_bytes = BytesIO(response.content)

# Skapa nedladdningsknapp
st.download_button(
    label="⬇️ Ladda ner diamonds.csv",
    data=csv_bytes,
    file_name="diamonds.csv",
    mime="text/csv"
)

st.markdown("""eller ladda upp ditt egna dataset under fliken verktyg""")
