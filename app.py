import streamlit as st
import time
from bandwidth import get_bandwidth_data
import plotly.graph_objects as go
from datetime import datetime

st.set_page_config(page_title="Bandwidth Monitor", layout="wide")
st.title("📶 Real-Time Bandwidth Monitor")

WINDOW = 50  # rolling window size

# Store history for graph
if "history" not in st.session_state:
    st.session_state.history = {}  # {ip: {"x": [], "y": []}}

placeholder = st.empty()

while True:
    data = get_bandwidth_data(duration=1)

    # Remove TOTAL if present
    if "TOTAL" in data:
        del data["TOTAL"]

    # Update history
    for ip, stats in data.items():
        kb = stats["total_kb"]

        if ip not in st.session_state.history:
            st.session_state.history[ip] = {"x": [], "y": [], "counter": 0}

        # Increase counter
        st.session_state.history[ip]["counter"] += 1

        # Append the counter value as time (1, 2, 3...)
        st.session_state.history[ip]["x"].append(st.session_state.history[ip]["counter"])
        st.session_state.history[ip]["y"].append(kb)

        # Keep last 50 points
        st.session_state.history[ip]["x"] = st.session_state.history[ip]["x"][-WINDOW:]
        st.session_state.history[ip]["y"] = st.session_state.history[ip]["y"][-WINDOW:]


    # Build combined graph
    fig = go.Figure()

    for ip, logs in st.session_state.history.items():
        fig.add_trace(go.Scatter(
            x=logs["x"],
            y=logs["y"],
            mode="lines",
            name=ip,   # <-- this shows IP in legend
            line=dict(width=2)
        ))

    fig.update_layout(
        title="📡 Bandwidth Usage Per IP",
        xaxis_title="Time(s)",
        yaxis_title="KB/s",
        height=500,
        margin=dict(l=20, r=20, t=40, b=20),
        legend_title="Devices (IP Addresses)"
    )

    placeholder.plotly_chart(fig, use_container_width=True)

    time.sleep(1)
