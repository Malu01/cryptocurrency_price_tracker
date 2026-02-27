import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
from streamlit_autorefresh import st_autorefresh

# ---------------------------
# 1️⃣ Page Configuration
# ---------------------------
st.set_page_config(
    page_title="Crypto Live Tracker",
    layout="wide",
    page_icon="🚀"
)

st.title("🚀 Advanced Crypto Analytics Dashboard")

# ---------------------------
# 2️⃣ Sidebar Controls
# ---------------------------
st.sidebar.header("⚙ Dashboard Controls")

refresh_rate = st.sidebar.slider(
    "Auto Refresh (seconds)",
    min_value=5,
    max_value=300,
    value=60
)

sort_option = st.sidebar.selectbox(
    "Sort By",
    ["24h Change (High to Low)", "24h Change (Low to High)"]
)

# Auto refresh (Non-blocking)
st_autorefresh(interval=refresh_rate * 1000, key="datarefresh")

# ---------------------------
# 3️⃣ Load Data
# ---------------------------
@st.cache_data(ttl=60)
def load_data():
    try:
        df = pd.read_csv("crypto_prices.csv")

        if '24h Change' in df.columns:
            df['24h Change'] = (
                df['24h Change']
                .astype(str)
                .str.replace('%', '')
                .str.replace('+', '')
                .astype(float)
            )

        return df
    except:
        return pd.DataFrame()

data = load_data()

st.markdown(f"**Last Updated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

# ---------------------------
# 4️⃣ Process Data
# ---------------------------
if not data.empty:

    if sort_option == "24h Change (High to Low)":
        data = data.sort_values(by="24h Change", ascending=False)
    else:
        data = data.sort_values(by="24h Change", ascending=True)

    top_gainer = data.iloc[0]

    # ---------------------------
    # 5️⃣ Top Gainer Highlight
    # ---------------------------
    st.success(
        f"🏆 Top Performer: {top_gainer['Name']} "
        f"({top_gainer['24h Change']}%)"
    )

    st.divider()

    # ---------------------------
    # 6️⃣ Metrics Section
    # ---------------------------
    cols = st.columns(3)

    for i in range(min(3, len(data))):
        with cols[i]:
            st.metric(
                label=data.iloc[i]['Name'],
                value=data.iloc[i]['Market Cap'],
                delta=f"{data.iloc[i]['24h Change']}%"
            )

    st.divider()

    # ---------------------------
    # 7️⃣ Chart + Table Layout
    # ---------------------------
    col_chart, col_table = st.columns([2, 1])

    with col_chart:
        st.subheader("📊 24h Performance Analysis")

        fig = px.bar(
            data,
            x="Name",
            y="24h Change",
            color="24h Change",
            color_continuous_scale="RdYlGn",
            title="24h Percentage Change"
        )

        fig.update_layout(
            xaxis_title="Cryptocurrency",
            yaxis_title="Change (%)",
            height=500
        )

        st.plotly_chart(fig, use_container_width=True)

    with col_table:
        st.subheader("📋 Market Data Table")
        st.dataframe(
            data[['Name', '24h Change', 'Market Cap']],
            height=500
        )

    st.caption("🔄 Auto-refresh enabled")

else:
    st.warning("Waiting for data from scraper...")