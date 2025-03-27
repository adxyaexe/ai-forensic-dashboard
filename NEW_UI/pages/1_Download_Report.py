import streamlit as st
import pandas as pd

st.set_page_config(page_title="Download Report", layout="centered")
st.title("📄 Download Forensic Report")

# Load data (update path if needed)
@st.cache_data
def load_data():
    return pd.read_csv("C:/Users/Adirhya Kesav/Desktop/DFIS/ForensicTImeline/NEW_UI/forensic_timeline_updated_from_refs.csv", parse_dates=["Timestamp"])

df = load_data()

# Sidebar filters
st.sidebar.header("Filter Before Export")
source_filter = st.sidebar.multiselect("Select Source(s)", df["Source"].unique(), default=df["Source"].unique())
event_filter = st.sidebar.multiselect("Select Event Type(s)", df["Event Type"].unique(), default=df["Event Type"].unique())

# Apply filters
filtered_df = df[(df["Source"].isin(source_filter)) & (df["Event Type"].isin(event_filter))]

# Report Summary
st.markdown("### 🧠 Report Summary")
st.write(f"**Total Events:** {len(filtered_df)}")

# Event Type Distribution
event_counts = filtered_df["Event Type"].value_counts()
st.write("**Event Type Breakdown:**")
st.dataframe(event_counts.rename("Count"))

# Top 5 Executables
top_executables = filtered_df["Executable/Task"].value_counts().head(5)
st.write("**Top 5 Most Frequent Executables:**")
st.dataframe(top_executables.rename("Executions"))

# Anomaly summary if available
if "AnomalyFlag" in filtered_df.columns:
    anomaly_count = filtered_df["AnomalyFlag"].apply(lambda x: 1 if "Anomaly" in str(x) else 0).sum()
    st.write(f"**🚨 Anomalies Detected:** {anomaly_count}")

# Data preview
st.markdown("### 📋 Filtered Data Preview")
st.dataframe(filtered_df, use_container_width=True)

# Download CSV
csv = filtered_df.to_csv(index=False).encode("utf-8")
st.download_button("⬇️ Download Filtered CSV", csv, "filtered_forensic_report.csv", "text/csv")
