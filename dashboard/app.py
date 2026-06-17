import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px
import plotly.graph_objects as go

# -------------------------------
# PAGE CONFIG
# -------------------------------

st.set_page_config(
    page_title="AI Manufacturing Dashboard",
    layout="wide"
)

st.title("🏭 AI-Based Manufacturing Breakdown Detection System")
st.subheader("Predictive Maintenance Dashboard")

# -------------------------------
# DATABASE CONNECTION
# -------------------------------

try:
    conn = sqlite3.connect("database/machine.db")
    df = pd.read_sql_query(
        "SELECT * FROM MachineData",
        conn
    )

except Exception as e:
    st.error(f"Database Error: {e}")
    st.stop()

# -------------------------------
# CHECK DATA
# -------------------------------

if len(df) == 0:
    st.warning("No machine data found in database.")
    st.stop()

# -------------------------------
# LATEST READING
# -------------------------------

latest = df.iloc[-1]

st.header("📡 Latest Machine Reading")

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Temperature (°C)",
    round(latest["temperature"], 2)
)

col2.metric(
    "Vibration",
    round(latest["vibration"], 2)
)

col3.metric(
    "RPM",
    round(latest["rpm"], 2)
)

col4.metric(
    "Pressure",
    round(latest["pressure"], 2)
)

# -------------------------------
# MACHINE STATUS
# -------------------------------

st.header("🤖 Machine Health Status")

prediction = latest["prediction"]

# Handle both numeric and text values

if prediction == 0 or str(prediction).upper() == "HEALTHY":

    st.success("✅ MACHINE HEALTHY")

elif prediction == 1 or str(prediction).upper() == "WARNING":

    st.warning("⚠ MAINTENANCE REQUIRED SOON")

else:

    st.error("🚨 FAILURE RISK DETECTED")

# -------------------------------
# RISK SCORE
# -------------------------------

risk_score = 0

if latest["temperature"] > 75:
    risk_score += 30

if latest["vibration"] > 2:
    risk_score += 30

if latest["rpm"] < 1000:
    risk_score += 40

risk_score = min(risk_score, 100)

st.header("📊 Machine Risk Score")

fig_gauge = go.Figure(
    go.Indicator(
        mode="gauge+number",
        value=risk_score,
        title={"text": "Risk Level (%)"},
        gauge={
            "axis": {"range": [0, 100]}
        }
    )
)

st.plotly_chart(
    fig_gauge,
    use_container_width=True
)

# -------------------------------
# FAILURE ANALYTICS
# -------------------------------

st.header("📈 Failure Analytics")

total_records = len(df)

failure_df = df[
    (df["prediction"] == 2)
    |
    (df["prediction"].astype(str).str.upper() == "FAILURE")
]

failure_count = len(failure_df)

failure_rate = (
    failure_count / total_records
) * 100

colA, colB, colC = st.columns(3)

colA.metric(
    "Total Records",
    total_records
)

colB.metric(
    "Failures",
    failure_count
)

colC.metric(
    "Failure Rate %",
    round(failure_rate, 2)
)

# -------------------------------
# STATUS DISTRIBUTION
# -------------------------------

st.header("🥧 Machine Status Distribution")

status_counts = (
    df["prediction"]
    .astype(str)
    .value_counts()
)

fig_pie = px.pie(
    values=status_counts.values,
    names=status_counts.index,
    title="Status Distribution"
)

st.plotly_chart(
    fig_pie,
    use_container_width=True
)

# -------------------------------
# TEMPERATURE TREND
# -------------------------------

st.header("🌡 Temperature Trend")

fig_temp = px.line(
    df,
    x="timestamp",
    y="temperature",
    title="Temperature vs Time"
)

st.plotly_chart(
    fig_temp,
    use_container_width=True
)

# -------------------------------
# VIBRATION TREND
# -------------------------------

st.header("📳 Vibration Trend")

fig_vib = px.line(
    df,
    x="timestamp",
    y="vibration",
    title="Vibration vs Time"
)

st.plotly_chart(
    fig_vib,
    use_container_width=True
)

# -------------------------------
# RPM TREND
# -------------------------------

st.header("⚙ RPM Trend")

fig_rpm = px.line(
    df,
    x="timestamp",
    y="rpm",
    title="RPM vs Time"
)

st.plotly_chart(
    fig_rpm,
    use_container_width=True
)

# -------------------------------
# PRESSURE TREND
# -------------------------------

st.header("🛢 Pressure Trend")

fig_pressure = px.line(
    df,
    x="timestamp",
    y="pressure",
    title="Pressure vs Time"
)

st.plotly_chart(
    fig_pressure,
    use_container_width=True
)

# -------------------------------
# AVERAGE MACHINE PERFORMANCE
# -------------------------------

st.header("📋 Average Machine Performance")

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Avg Temp",
    round(df["temperature"].mean(), 2)
)

col2.metric(
    "Avg Vibration",
    round(df["vibration"].mean(), 2)
)

col3.metric(
    "Avg RPM",
    round(df["rpm"].mean(), 2)
)

col4.metric(
    "Avg Pressure",
    round(df["pressure"].mean(), 2)
)

# -------------------------------
# CORRELATION MATRIX
# -------------------------------

st.header("🔍 Sensor Correlation Matrix")

corr = df[
    [
        "temperature",
        "vibration",
        "rpm",
        "pressure",
        "runtime"
    ]
].corr()

fig_corr = px.imshow(
    corr,
    text_auto=True,
    title="Correlation Heatmap"
)

st.plotly_chart(
    fig_corr,
    use_container_width=True
)

# -------------------------------
# MAINTENANCE RECOMMENDATION
# -------------------------------

st.header("🛠 Maintenance Recommendations")

recommendations = []

if latest["temperature"] > 75:
    recommendations.append(
        "Inspect Cooling System"
    )

if latest["vibration"] > 2:
    recommendations.append(
        "Check Bearings and Alignment"
    )

if latest["rpm"] < 1000:
    recommendations.append(
        "Inspect Motor Drive"
    )

if latest["pressure"] > 8:
    recommendations.append(
        "Check Pressure Valve"
    )

if len(recommendations) == 0:

    st.success(
        "No Maintenance Required"
    )

else:

    for rec in recommendations:
        st.warning(rec)

# -------------------------------
# ALERT SYSTEM
# -------------------------------

st.header("🚨 Alert System")

if risk_score >= 80:

    st.error(
        "CRITICAL ALERT: Machine Breakdown Possible!"
    )

elif risk_score >= 50:

    st.warning(
        "WARNING: Machine Requires Inspection"
    )

else:

    st.success(
        "Machine Operating Normally"
    )

# -------------------------------
# HISTORICAL DATA
# -------------------------------

st.header("📜 Historical Machine Data")

st.dataframe(
    df.tail(50),
    use_container_width=True
)

# -------------------------------
# FOOTER
# -------------------------------

st.markdown("---")

st.write(
    "AI Smart Manufacturing Machine Downtime Prediction System"
)