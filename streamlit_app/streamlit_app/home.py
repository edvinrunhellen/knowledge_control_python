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

with open("data/diamonds.csv", "rb") as f:
    st.download_button("⬇️ Ladda ner diamonds.csv", f, file_name="diamonds.csv", mime="text/csv")

st.markdown("""eller ladda upp ditt egna dataset under fliken verktyg""")
