import streamlit as st
import pandas as pd
import numpy as np

st.title("DiamondPicker")



uploaded_file = st.file_uploader("Ladda upp din CSV-fil", type="csv")

def find_underpriced_diamonds(df):
    df_under_1ct = df[df['carat'] <= 0.5]

    # kvalitetskrav
    filtered = df_under_1ct[
        (df_under_1ct['carat'] >= 0.25) & (df_under_1ct['carat'] <= 0.5) &
        (df_under_1ct['clarity'].isin(['IF', 'VVS1'])) &
        (df_under_1ct['color'].isin(['E', 'F', 'G'])) &
        (df_under_1ct['cut'] == 'Excellent') &
        (df_under_1ct['price'] < 2000)
    ]

    bins = np.arange(0.3, 0.41, 0.01)
    labels = [f"{round(bins[i], 2)}–{round(bins[i+1], 2)}" for i in range(len(bins) - 1)]
    filtered['carat_interval'] = pd.cut(filtered['carat'], bins=bins, labels=labels, include_lowest=True)

    median_prices = filtered.groupby('carat_interval')['price'].median().reset_index()
    median_dict = median_prices.set_index('carat_interval')['price'].to_dict()

    # 10% under medianpris
    below_median_10 = []
    for idx, row in filtered.iterrows():
        interval = row['carat_interval']
        price = row['price']
        if pd.isna(interval) or interval not in median_dict:
            continue
        median = median_dict[interval]
        if price < median * 0.90:
            below_median_10.append({
                'index': idx,
                'carat': row['carat'],
                'price': float(price),
                'interval': interval,
                'median': float(median),
                'threshold_90pct': float(median * 0.90)
            })

    df_below_median_10 = pd.DataFrame(below_median_10)

    if df_below_median_10.empty:
        return df_below_median_10, 0, 0, 0

    total_price = df_below_median_10['price'].sum()
    total_median = df_below_median_10['median'].sum()
    difference = total_median - total_price

    return df_below_median_10, total_price, total_median, difference

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    # Filtrera bort nollvärden i x/y/z
    df = df[(df['x'] > 0) & (df['y'] > 0) & (df['z'] > 0)]
    df = df.dropna(subset=['x', 'y', 'z'])

    # Normalisera text
    df['cut'] = df['cut'].astype(str).str.title()
    df['clarity'] = df['clarity'].astype(str).str.upper()
    df['color'] = df['color'].astype(str).str.upper()

    # Gör så att klassicifesringssystemet är konsekvent
    cut_mapping = {
        'Ideal': 'Excellent',
        'Premium': 'Excellent',
        'Very Good': 'Very Good',
        'Excellent': 'Excellent',
        'Good': 'Good',
        'Fair': 'Fair',
        'Poor': 'Poor',
        'Shallow': 'Very Good',
        'Deep': 'Good',
        'Very Shallow': 'Fair',
        'Very Deep': 'Poor'
    }
    df['cut'] = df['cut'].replace(cut_mapping)

    valid_cuts = ['Excellent', 'Very Good', 'Good', 'Fair', 'Poor']
    df = df[df['cut'].isin(valid_cuts)]
    cut_order = ['Poor', 'Fair', 'Good', 'Very Good', 'Excellent']
    df['cut'] = pd.Categorical(df['cut'], categories=cut_order, ordered=True)

    # Kör analys
    results, total_price, total_median, difference = find_underpriced_diamonds(df)

    if results.empty:
        st.info("Inga matchande diamanter hittades.")
    else:
        st.success(f"Hittade {len(results)} stenar som är minst 10% under medianpris!")
        st.write(f"**Total faktisk pris:** {total_price:,.2f} USD")
        st.write(f"**Total medianpris:** {total_median:,.2f} USD")
        st.write(f"**Potentiell vinst:** {difference:,.2f} USD")
        st.dataframe(results)

