import streamlit as st
import requests
import json
import pandas as pd
import plotly.express as px
import os
import sys
from pathlib import Path

# Add parent directory to path to import config
sys.path.insert(0, str(Path(__file__).parent.parent))
from config import SERVER_IP, SERVER_PORT, API_URL

# Stream URL
STREAM_URL = f"http://{SERVER_IP}:{SERVER_PORT}/stream"

# Streamlit setup
st.set_page_config(page_title="PUB Realtime Dashboard", layout="wide")
st.title("🔴 Real-Time PUB Demand Dashboard")
st.markdown(f"**Stream URL:** `{STREAM_URL}`")

plot_placeholder = st.empty()
table_placeholder = st.empty()

data_buffer = []

view = st.sidebar.selectbox(
    "📊 View Mode",
    [
        "Today",
        "All Dates",
        "Average",
        "Today vs Average",
        "Latest 7 Days",
        "Latest Records",
    ],
)


def sse_events(url):
    """Server-Sent Events reader"""
    try:
        with requests.get(url, stream=True, timeout=30) as r:
            for line in r.iter_lines():
                if line:
                    decoded = line.decode("utf-8")
                    if decoded.startswith("data:"):
                        yield decoded.replace("data:", "").strip()
    except requests.exceptions.RequestException as e:
        st.error(f"❌ Connection error: {e}")


# Main loop
try:
    for payload in sse_events(STREAM_URL):
        record = json.loads(payload)
        data_buffer.append(record)

        df = pd.DataFrame(data_buffer)

        if "Date" in df.columns:
            df["Date"] = pd.to_datetime(df["Date"])
        if "Hour" in df.columns:
            df["Hour"] = pd.to_numeric(df["Hour"], errors="coerce")

            # View 1: Today only
            if view == "Today":
                latest_date = df["Date"].max()
                df_today = df[df["Date"] == latest_date]

                fig = px.line(
                    df_today,
                    x="Hour",
                    y="Ontario Demand",
                    title=f"Ontario Demand — {latest_date.date()}",
                    markers=True,
                )
                plot_placeholder.plotly_chart(fig, use_container_width=True)
                table_placeholder.dataframe(df_today.tail(10))

            # View 2: All dates
            elif view == "All Dates":
                fig = px.line(
                    df,
                    x="Hour",
                    y="Ontario Demand",
                    color=df["Date"].dt.date.astype(str),
                    title="Ontario Demand by Hour — All Dates",
                )
                plot_placeholder.plotly_chart(fig, use_container_width=True)
                table_placeholder.dataframe(df.tail(10))

            # View 3: Average profile
            elif view == "Average":
                df_avg = df.groupby("Hour")["Ontario Demand"].mean().reset_index()

                fig = px.line(
                    df_avg,
                    x="Hour",
                    y="Ontario Demand",
                    title="Average Ontario Demand by Hour",
                    markers=True,
                )
                plot_placeholder.plotly_chart(fig, use_container_width=True)
                table_placeholder.dataframe(df_avg)

            # View 4: Latest 7 days
            elif view == "Latest 7 Days":
                latest_date = df["Date"].max()
                cutoff = latest_date - pd.Timedelta(days=7)
                df_7 = df[df["Date"] >= cutoff]

                fig = px.line(
                    df_7,
                    x="Hour",
                    y="Ontario Demand",
                    color=df_7["Date"].dt.date.astype(str),
                    title="Ontario Demand — Last 7 Days",
                )
                plot_placeholder.plotly_chart(fig, use_container_width=True)
                table_placeholder.dataframe(df_7.tail(20))

            # View 5: Today vs Average
            elif view == "Today vs Average":
                latest_date = df["Date"].max()
                df_today = df[df["Date"] == latest_date]
                df_avg = df.groupby("Hour")["Ontario Demand"].mean().reset_index()

                fig = px.line(
                    df_today,
                    x="Hour",
                    y="Ontario Demand",
                    title=f"Ontario Demand — Today ({latest_date.date()}) vs Average",
                    markers=True,
                )
                fig.add_scatter(
                    x=df_avg["Hour"],
                    y=df_avg["Ontario Demand"],
                    mode="lines+markers",
                    name="Average",
                )

                plot_placeholder.plotly_chart(fig, use_container_width=True)
                table_placeholder.dataframe(df_today.tail(10))

            # View 6: Latest records table
            elif view == "Latest Records":
                plot_placeholder.empty()
                table_placeholder.dataframe(df.tail(25))

except KeyboardInterrupt:
    st.info("Stream stopped by user")
except Exception as e:
    st.error(f"❌ Error: {e}")