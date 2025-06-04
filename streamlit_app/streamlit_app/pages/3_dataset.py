import streamlit as st
import pandas as pd
import pandas as pd
import requests
from io import BytesIO
import streamlit as st

st.header("Översikt över dataset: /data/diamonds.csv")

st.write("Notera att datan inte är hanterad efter datakvalite. Detta är endast en översikt över det råa datasetet.")


# GitHub raw URL till CSV-filen
url = "https://raw.githubusercontent.com/edvinrunhellen/DiamondLens/v2/streamlit_app/streamlit_app/data/diamonds.csv"

# Hämta innehållet som bytes
response = requests.get(url)
csv_bytes = BytesIO(response.content)

# Läs in filen som DataFrame
df = pd.read_csv(csv_bytes)

# Visa DataFrame
st.write("📊 Förhandsvisning av data:", df.head())

# Ladda ner-knapp
st.download_button(
    label="⬇️ Ladda ner diamonds.csv",
    data=csv_bytes,
    file_name="diamonds.csv",
    mime="text/csv"
)
