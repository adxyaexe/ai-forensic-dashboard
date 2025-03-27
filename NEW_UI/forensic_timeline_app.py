import streamlit as st
import pandas as pd
import plotly.express as px

# ✅ MUST BE FIRST
st.set_page_config(page_title="Forensic Timeline Dashboard", layout="centered")

# ✅ Full CSV path (update this if needed)
CSV_PATH = "C:/Users/Adirhya Kesav/Desktop/DFIS/ForensicTImeline/NEW_UI/forensic_timeline_updated_from_refs.csv"

# ✅ Load the dataset
@st.cache_data
def load_data():
    return pd.read_csv(CSV_PATH, parse_dates=["Timestamp"])

df = load_data()

st.title("🕵️ Forensic Timeline Viewer")

# Sidebar filters
st.sidebar.header("🔎 Filters")

selected_sources = st.sidebar.multiselect("Source:", df["Source"].unique(), default=df["Source"].unique())
selected_event_types = st.sidebar.multiselect("Event Type:", df["Event Type"].unique(), default=df["Event Type"].unique())
date_range = st.sidebar.date_input("Date Range:", [df["Timestamp"].min().date(), df["Timestamp"].max().date()])

# Apply filters
filtered_df = df[
    (df["Source"].isin(selected_sources)) &
    (df["Event Type"].isin(selected_event_types)) &
    (df["Timestamp"].dt.date >= date_range[0]) &
    (df["Timestamp"].dt.date <= date_range[1])
]

# Summary
st.markdown(f"### Showing {len(filtered_df)} Events")
st.write(f"Unique Executables: {filtered_df['Executable/Task'].nunique()} | Unique Logon IDs: {filtered_df['Logon ID'].nunique()}")

# Chart type selection
chart_type = st.radio("Choose Timeline View:", ["Scatter Plot (Detailed)", "Line Graph (Event Frequency)"])

if chart_type == "Scatter Plot (Detailed)":
    fig = px.scatter(
        filtered_df,
        x="Timestamp",
        y="Event Type",
        color="Source",
        title="Timeline of Events",
        height=400,
        hover_data=["Executable/Task", "Logon ID", "Event ID"]
    )
    st.plotly_chart(fig, use_container_width=True)
else:
    # Aggregate events by hour
    freq_df = filtered_df.copy()
    freq_df["Hour"] = freq_df["Timestamp"].dt.floor("H")
    event_counts = freq_df.groupby(["Hour", "Event Type"]).size().reset_index(name="Count")

    fig = px.line(
        event_counts,
        x="Hour",
        y="Count",
        color="Event Type",
        title="Event Frequency Over Time",
        markers=True
    )
    st.plotly_chart(fig, use_container_width=True)

# Show full table
#st.markdown("### Event Log Table")
#st.dataframe(filtered_df, use_container_width=True)