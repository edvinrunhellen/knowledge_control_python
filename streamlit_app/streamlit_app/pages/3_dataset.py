import streamlit as st
import pandas as pd

st.header("Översikt över dataset: /data/diamonds.csv")

st.write("Notera att datan inte är hanterad efter datakvalite")

df = pd.read_csv("data/diamonds.csv")
st.write(df.head(100))
