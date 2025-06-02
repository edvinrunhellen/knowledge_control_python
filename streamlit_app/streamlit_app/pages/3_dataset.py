import streamlit as st
import pandas as pd

st.header("Översikt över dataset: diamonds.csv")
df = pd.read_csv("data/diamonds.csv")
st.write(df.head(100))
