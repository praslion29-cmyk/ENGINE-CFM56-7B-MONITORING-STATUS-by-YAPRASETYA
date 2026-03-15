import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime
from PIL import Image

# =========================
# PAGE CONFIG
# =========================

st.set_page_config(
    page_title="CFM56-7B Engine Health Monitoring",
    page_icon="CFM_logo_Core_color.png",
    layout="wide"
)

# =========================
# LOGO
# =========================

try:
    logo = Image.open("CFM_logo_Core_color.png")
except:
    logo = None

col1, col2 = st.columns([1,6])

with col1:
    if logo:
        st.image(logo, width=120)

with col2:
    st.title("CFM56-7B ENGINE HEALTH MONITORING")
    st.subheader("Skywise Style Dashboard - Created by Y.A. Prasetya")

# =========================
# LIMIT ENGINE
# =========================

limits = {
"N1":102,
"N2":105,
"EGT":950,
"Fuel Flow":5200,
"Oil Pressure":60,
"Oil Temp":150,
"Vibration":4
}

# =========================
# SESSION DATA
# =========================

if "fleet_data" not in st.session_state:
    st.session_state.fleet_data = pd.DataFrame()

# =========================
# STATUS FUNCTION
# =========================

def check_status(value,limit):

    caution_limit = limit * 0.95

    if value > limit:
        return "WARNING","red"

    elif value >= caution_limit:
        return "CAUTION","orange"

    else:
        return "NORMAL","green"

# =========================
# HEALTH SCORE
# =========================

def calculate_health(params):

    score = 100

    for p,v in params.items():

        limit = limits[p]

        if v > limit:
            score -= 20

        elif v >= limit*0.95:
            score -= 10

    if score < 0:
        score = 0

    return score

# =========================
# SIDEBAR INPUT
# =========================

st.sidebar.header("Aircraft Information")

date = st.sidebar.date_input("Date", datetime.today())

aircraft = st.sidebar.text_input("Aircraft Registration")

engine = st.sidebar.text_input("Engine Number")

route = st.sidebar.text_input("Route")

# =========================
# ENGINE START
# =========================

st.sidebar.header("Engine Start Monitoring")

egt_start = st.sidebar.number_input("EGT Start (°C)",0)

if egt_start > 725:
    st.sidebar.error("HOT START - Maintenance Required")

# =========================
# TAKEOFF PARAMETERS
# =========================

st.sidebar.header("Takeoff Parameters")

N1 = st.sidebar.number_input("N1 (%)",0.0)

N2 = st.sidebar.number_input("N2 (%)",0.0)

EGT = st.sidebar.number_input("EGT Takeoff (°C)",0.0)

Fuel = st.sidebar.number_input("Fuel Flow (pph)",0.0)

OilP = st.sidebar.number_input("Oil Pressure (psi)",0.0)

OilT = st.sidebar.number_input("Oil Temp (°C)",0.0)

Vib = st.sidebar.number_input("Vibration (ips)",0.0)

params = {
"N1":N1,
"N2":N2,
"EGT":EGT,
"Fuel Flow":Fuel,
"Oil Pressure":OilP,
"Oil Temp":OilT,
"Vibration":Vib
}

# =========================
# EGT MARGIN
# =========================

egt_margin = limits["EGT"] - EGT

# =========================
# HEALTH SCORE
# =========================

health = calculate_health(params)

col1,col2 = st.columns(2)

col1.metric("EGT Margin",f"{egt_margin} °C")

col2.metric("Engine Health Score",health)

# =========================
# PARAMETER STATUS
# =========================

st.header("Engine Parameter Monitoring")

for p,v in params.items():

    status,color = check_status(v,limits[p])

    st.markdown(f"**{p} : {v} → :{color}[{status}]**")

# =========================
# POSSIBLE CAUSE
# =========================

st.header("Maintenance Recommendation")

alerts=[]

if EGT > limits["EGT"]:
    alerts.append(("High EGT","Possible hot section deterioration","Inspect turbine and combustor"))

if Fuel > limits["Fuel Flow"]:
    alerts.append(("High Fuel Flow","Possible combustion inefficiency","Check fuel nozzle and perform engine wash"))

if Vib > limits["Vibration"]:
    alerts.append(("High Vibration","Possible fan imbalance","Perform fan blade inspection"))

if OilT > limits["Oil Temp"]:
    alerts.append(("High Oil Temp","Oil cooling issue","Check oil cooler"))

for a in alerts:
    st.warning(f"""
Issue : {a[0]}

Possible Cause : {a[1]}

Recommendation : {a[2]}
""")

# =========================
# ADD AIRCRAFT
# =========================

if st.button("Add Aircraft Data"):

    new_data = {
    "Date":date,
    "Aircraft":aircraft,
    "Engine":engine,
    "Route":route,
    "EGT":EGT,
    "Fuel Flow":Fuel,
    "Vibration":Vib,
    "EGT Margin":egt_margin,
    "Health Score":health
    }

    st.session_state.fleet_data = pd.concat(
    [st.session_state.fleet_data,pd.DataFrame([new_data])],
    ignore_index=True
    )

    st.success("Aircraft Added to Monitoring Fleet")

# =========================
# FLEET OVERVIEW
# =========================

st.header("Fleet Monitoring")

if not st.session_state.fleet_data.empty:

    st.dataframe(st.session_state.fleet_data)

# =========================
# TREND GRAPH
# =========================

st.header("Engine Trend Monitoring")

if not st.session_state.fleet_data.empty:

    col1,col2,col3 = st.columns(3)

    with col1:

        fig = go.Figure()

        fig.add_trace(go.Scatter(
        y=st.session_state.fleet_data["EGT"],
        mode="lines+markers",
        name="EGT"))

        fig.update_layout(height=250,title="EGT Trend")

        st.plotly_chart(fig,use_container_width=True)

    with col2:

        fig = go.Figure()

        fig.add_trace(go.Scatter(
        y=st.session_state.fleet_data["Fuel Flow"],
        mode="lines+markers",
        name="Fuel Flow"))

        fig.update_layout(height=250,title="Fuel Flow Trend")

        st.plotly_chart(fig,use_container_width=True)

    with col3:

        fig = go.Figure()

        fig.add_trace(go.Scatter(
        y=st.session_state.fleet_data["Vibration"],
        mode="lines+markers",
        name="Vibration"))

        fig.update_layout(height=250,title="Vibration Trend")

        st.plotly_chart(fig,use_container_width=True)

# =========================
# EXPORT
# =========================

st.header("Export Data")

if st.button("Save CSV"):

    st.session_state.fleet_data.to_csv("engine_health_monitoring.csv",index=False)

    st.success("Data Saved")

if st.button("PRINT"):

    st.info("Use CTRL + P to print report")