import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# Ladda och städa datan
df = pd.read_csv("data/diamonds.csv")
df = df[(df['x'] > 0) & (df['y'] > 0) & (df['z'] > 0)]
df = df.dropna(subset=['x', 'y', 'z'])

cut_mapping = {
    "Ideal": "Excellent",
    "Premium": "Excellent",
    "Very Good": "Very Good",
    "Good": "Good",
    "Fair": "Fair",
    "Poor": "Poor",
    "Shallow": "Very Good",
    "Deep": "Good",
    "Very Shallow": "Fair",
    "Very Deep": "Poor"
}

df["cut"] = df['cut'].astype(str).replace(cut_mapping)
valid_cuts = ["Excellent", "Very Good", "Good", "Fair", "Poor"]
df = df[df["cut"].isin(valid_cuts)]
cut_order = ["Poor", "Fair", "Good", "Very Good", "Excellent"]
df['cut'] = pd.Categorical(df["cut"], categories=cut_order, ordered=True)

# Streamlit-utskrifter
st.title("📊 Översikt av DiamondPicker")

st.markdown("""
**Dataanalysen har bidragit med 5 huvudsakliga faktorer till verktygets funktion:**

1. Analysen har identifierat caratintervall där caratpriset är som absolut billigast.  
2. Analysen har tagit marknadens efterfrågan i beaktning sett till kvalitet och storlek.
3. Analysen har identifierat caratintervall med högst volatilitet, dvs. högst potential till avkastning.  
4. Analysen har identifierat medianpriser för caratintervallen marknaden efterfrågar.    
5. Analysen har beräknat underprissatta diamanter i dessa caratintervall.  
""")

st.subheader("1. Genomsnittligt pris per carat per caratintervall")


# Skapa caratintervall
bins = [0, 0.25, 0.5, 0.75, 1.0, 1.25, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 5.0]
labels = ["0-0.25", "0.25-0.5", "0.5-0.75", "0.75-1.0", "1.0-1.25", "1.25-1.5", 
          "1.5-2.0", "2.0-2.5", "2.5-3.0", "3.0-3.5", "3.5-4.0", "4.0-5.0"]
df['carat_range'] = pd.cut(df['carat'], bins=bins, labels=labels)

# Beräkna pris per carat
df['price_per_carat'] = df['price'] / df['carat']

# Pivot-tabeller
pivot_ppc = df.pivot_table(index='carat_range', values='price_per_carat', aggfunc='mean')
pivot_total_price = df.pivot_table(index='carat_range', values='price', aggfunc='mean')

# Kombinera och sortera
combined = pivot_ppc.join(pivot_total_price, rsuffix='_total')
combined.columns = ['avg_price_per_carat', 'avg_total_price']
top3_value = combined.sort_values('avg_price_per_carat').head(3)

# Rita heatmap
fig, ax = plt.subplots(figsize=(8, 6))
sns.heatmap(pivot_ppc, annot=True, fmt=".0f", cmap='YlGnBu', linewidths=0.5, ax=ax)
ax.set_title("Genomsnittligt pris per carat per caratintervall")
ax.set_xlabel("Genomsnittligt pris per carat")
ax.set_ylabel("Caratintervall")
st.pyplot(fig)

st.write("Från denna visualisering ser vi att priset per carat generellt är lägre när hela stenen väger mellan 0–0.25 carat. De absolut dyraste stenarna per carat återfinns i intervallet 2.0–2.5 carat. Detta beror troligen på en korrelation mellan tillgång och efterfrågan. Större diamanter, alltså över 1.0 carat, är mer sällsynta vilket leder till ett kraftigt prisuppsving.")


# Visa topp 3 mest prisvärda intervall
st.write("Topp 3 mest prisvärda caratintervall")
st.dataframe(top3_value)

st.subheader("2. Efterfrågan på marknaden")

st.write("Efter att ha studerat marknaden har vi identifierat att attributen color och clarity har en mindre påverkan på priset. Många kunder kan inte urskilja skillnaden mellan färgerna D till G trots att de prissätts olika. Detta ger möjligheten att köpa in G diamanter billigare men ändå erbjuda liknande kvalite. När det gäller clarity är skillnaden också visuellt marginell men prisskillnaden kan vara stor. Sett till den nordiska marknaden ser vi dessutom att efterfrågan är större i caratintervallet 0.3-0-4. Dessa upplevs och är prisvärda sett till caratpriset. De finns dessutom  större volym av stenar i detta intervall vilket medför en högre köpomsättning. ")

st.subheader("3. Volatilitet i priser i olika caratintervall 0.2-0.5")

# Läs in datan
df = pd.read_csv("data/diamonds.csv")
df = df[(df['x'] > 0) & (df['y'] > 0) & (df['z'] > 0)]

# Filtrera till diamanter <= 0.5 ct
df_under_1ct = df[df["carat"] <= 0.5]

# Filtrera på specifika kvalitetskriterier
filtered = df_under_1ct[
    (df_under_1ct["carat"] >= 0.25) &
    (df_under_1ct["clarity"].isin(["IF", "VVS1"])) &
    (df_under_1ct["color"].isin(["E", "F", "G"])) &
    (df_under_1ct["cut"] == 'Excellent') &
    (df_under_1ct["price"] < 2000)
]


df = pd.read_csv("data/diamonds.csv")
df = df[(df['x'] > 0) & (df['y'] > 0) & (df['z'] > 0)]

# Standardisera 'cut'
cut_mapping = {
    "Ideal": "Excellent",
    "Premium": "Excellent",
    "Very Good": "Very Good",
    "Good": "Good",
    "Fair": "Fair",
    "Poor": "Poor",
    "Shallow": "Very Good",
    "Deep": "Good",
    "Very Shallow": "Fair",
    "Very Deep": "Poor"
}
df["cut"] = df['cut'].astype(str).replace(cut_mapping)
valid_cuts = ["Excellent", "Very Good", "Good", "Fair", "Poor"]
df = df[df["cut"].isin(valid_cuts)]
cut_order = ["Poor", "Fair", "Good", "Very Good", "Excellent"]
df['cut'] = pd.Categorical(df["cut"], categories=cut_order, ordered=True)

# 🧱 2. Filtrera 0.25–0.5 carat med kvalitetskriterier
df_under_05ct = df[df["carat"] <= 0.5]
filtered = df_under_05ct[
    (df_under_05ct["carat"] >= 0.25) &
    (df_under_05ct["clarity"].isin(["IF", "VVS1"])) &
    (df_under_05ct["color"].isin(["E", "F", "G"])) &
    (df_under_05ct["cut"] == 'Excellent') &
    (df_under_05ct["price"] < 2000)
]

fig1, ax1 = plt.subplots(figsize=(10, 6))
ax1.scatter(df_under_05ct["carat"], df_under_05ct["price"], color="lightgray", label="Alla diamanter", alpha=0.5)
ax1.scatter(filtered["carat"], filtered["price"], color="red", label="Matchande diamanter", alpha=0.8)
ax1.set_xlabel("Carat")
ax1.set_ylabel("Pris (USD)")
ax1.set_title("Pris vs Carat (0.25–0.5 ct)")
ax1.legend()
ax1.grid(True)
st.pyplot(fig1)

st.markdown("""
            **Vad vi ser:**

Från denna scatterplot ser vi att diamanterna i intervallet mellan 0.20 och 0.50 carat är relativt koncentrerade i pris, men att det samtidigt finns stenar som uppfyller våra kvalitetskriterier och som kan köpas till ett lägre pris. Exempelvis kan vi under 0.28 carat identifiera en diamant som är billigare än övriga i samma kategori.

**Detta innebär följande:**

Prisvolatiliteten ökar tydligt redan vid 0.30 till 0.40 carat. Genom att beräkna medianpriset för varje caratintervall kan vi filtrera ut de stenar som ligger under medianen och därmed identifiera potentiella köplägen med högre sannolikhet för avkastning. Det tyder på att rätt köpbeslut inom detta spann kan vara särskilt lönsamt.

**Ur ett affärsperspektiv:**

Från affärsperspektiv ser vi att störst potential finns i intervallet mellan 0.30 och 0.40 carat. Här finns flest stenar och volatiliteten i pris är högst, vilket innebär större möjligheter att göra fynd. Däremot är chanserna till lönsam affär lägre i t.ex. 0.47-caratintervallet eftersom antalet tillgängliga stenar är färre. Vi väljer därför att sortera bort dessa ur analysen för att fokusera på de intervall där utbudet och möjligheterna till vinst är som störst.
            
            
            """)


st.subheader("4. Medianpris för caratintervallen 0.3 - 0-4")

bins = np.arange(0.3, 0.41, 0.01)  
labels = [f"{round(bins[i], 2)}–{round(bins[i+1], 2)}" for i in range(len(bins) - 1)]

# Skapa ny kolumn med intervallbaserade carat-grupper
filtered["carat_interval"] = pd.cut(filtered["carat"], bins=bins, labels=labels, include_lowest=True)

# Räkna medianpris för varje intervall
median_prices = filtered.groupby("carat_interval")["price"].median().reset_index()


fig, ax = plt.subplots(figsize=(10, 5))
ax.bar(median_prices["carat_interval"], median_prices["price"], color="red", alpha=0.8)
ax.set_xlabel("Carat-intervall 0.01 steg")
ax.set_ylabel("Medianpris")
ax.set_title("Medianpris för filtrerade diamanter 0.3–0.4 carat")
ax.grid(axis='y')


st.pyplot(fig)
            
st.subheader("5. Diamanter <10% under medianpris")

median_dict = median_prices.set_index("carat_interval")["price"].to_dict()

# Hitta diamanter som ligger 10% under medianen i sitt intervall
below_median_10 = []

for idx, row in filtered.iterrows():
    interval = row["carat_interval"]
    price = row["price"]
    
    if pd.isna(interval) or interval not in median_dict:
        continue
    
    median = median_dict[interval]
    if price < median * 0.90:
        below_median_10.append({
            "index": idx,
            "carat": row["carat"],
            "price": price,
            "interval": interval,
            "median": median,
            "buy for:": median * 0.90
        })

# Konvertera till DataFrame
df_below_median_10 = pd.DataFrame(below_median_10)


st.write(f"Antal diamanter: **{len(df_below_median_10)}**")

# Visa tabell
st.dataframe(df_below_median_10)