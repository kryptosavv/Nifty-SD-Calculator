import streamlit as st
import numpy as np
from datetime import date

# --- Page Configuration ---
st.set_page_config(page_title="Nifty Expiry Range Calculator", page_icon="📈")

# --- Title and Description ---
st.title("📈 Nifty 50 Expected Move Calculator")
st.markdown("""
This tool calculates the expected trading range for Nifty 50 based on **Implied Volatility (IV)**.
It provides levels for 1 SD (68%), 2 SD (95%), and 3 SD (99.7%).
""")

st.markdown("---")

# --- Sidebar Inputs ---
st.sidebar.header("1. Enter Market Data")

spot_price = st.sidebar.number_input(
    "Current Nifty Spot Price", 
    min_value=10000.0, 
    value=24000.0, 
    step=10.0,
    format="%.2f"
)

iv = st.sidebar.number_input(
    "ATM Implied Volatility (IV) %", 
    min_value=1.0, 
    max_value=100.0, 
    value=12.5, 
    step=0.1,
    help="Check the Option Chain for the IV of the ATM strike."
)

st.sidebar.header("2. Expiry Settings")

input_method = st.sidebar.radio("Select Input Method:", ["Select Date", "Enter Days Manually"])

if input_method == "Select Date":
    expiry_date = st.sidebar.date_input("Select Expiry Date", min_value=date.today())
    today = date.today()
    dte = (expiry_date - today).days
else:
    dte = st.sidebar.number_input("Days to Expiry (DTE)", min_value=0, value=7, step=1)

# --- Calculation Logic ---
if dte > 0:
    # 1 Standard Deviation (68% Probability)
    sd_1_points = spot_price * (iv / 100) * np.sqrt(dte / 365)
    upper_1sd = spot_price + sd_1_points
    lower_1sd = spot_price - sd_1_points

    # 2 Standard Deviation (95% Probability)
    sd_2_points = sd_1_points * 2
    upper_2sd = spot_price + sd_2_points
    lower_2sd = spot_price - sd_2_points

    # 3 Standard Deviation (99.7% Probability)
    sd_3_points = sd_1_points * 3
    upper_3sd = spot_price + sd_3_points
    lower_3sd = spot_price - sd_3_points

    # --- Main Display ---
    st.header(f"Results for {dte} Days to Expiry")

    # Row 1: 1 SD
    st.markdown("### 1 Standard Deviation (68% Probability)")
    st.caption("The most likely range for the market.")
    col1, col2, col3 = st.columns(3)
    col1.metric("Bearish Limit", f"{lower_1sd:,.0f}", delta=f"-{sd_1_points:.0f} pts")
    col2.metric("Expected Move", f"±{sd_1_points:.0f} pts")
    col3.metric("Bullish Limit", f"{upper_1sd:,.0f}", delta=f"+{sd_1_points:.0f} pts")
    
    st.markdown("---")

    # Row 2: 2 SD
    st.markdown("### 2 Standard Deviations (95% Probability)")
    st.caption("Often used by option sellers as a 'safe' zone.")
    colA, colB, colC = st.columns(3)
    colA.metric("Bearish Limit", f"{lower_2sd:,.0f}", delta=f"-{sd_2_points:.0f} pts", delta_color="inverse")
    colB.metric("Expected Move", f"±{sd_2_points:.0f} pts")
    colC.metric("Bullish Limit", f"{upper_2sd:,.0f}", delta=f"+{sd_2_points:.0f} pts", delta_color="normal")

    st.markdown("---")

    # Row 3: 3 SD (New Addition)
    st.markdown("### 3 Standard Deviations (99.7% Probability)")
    st.caption("Extreme outlier events. Price rarely breaches these levels.")
    colX, colY, colZ = st.columns(3)
    colX.metric("Bearish Limit", f"{lower_3sd:,.0f}", delta=f"-{sd_3_points:.0f} pts", delta_color="inverse")
    colY.metric("Expected Move", f"±{sd_3_points:.0f} pts")
    colZ.metric("Bullish Limit", f"{upper_3sd:,.0f}", delta=f"+{sd_3_points:.0f} pts", delta_color="normal")

    # --- Visual Representation ---
    st.markdown("### 📊 Range Visualization")
    
    # Text visualization of the levels
    st.text(f"UPPER 3SD: {upper_3sd:,.0f} (Extreme Resistance)")
    st.text(f"UPPER 2SD: {upper_2sd:,.0f}")
    st.text(f"UPPER 1SD: {upper_1sd:,.0f}")
    st.text(f"   SPOT  : {spot_price:,.0f}")
    st.text(f"LOWER 1SD: {lower_1sd:,.0f}")
    st.text(f"LOWER 2SD: {lower_2sd:,.0f}")
    st.text(f"LOWER 3SD: {lower_3sd:,.0f} (Extreme Support)")

else:
    st.warning("Days to Expiry must be greater than 0.")

# --- Footer ---
st.sidebar.markdown("---")
st.sidebar.markdown("**Formulas Used:**")
st.sidebar.latex(r"1SD = Spot \times IV \times \sqrt{\frac{DTE}{365}}")
st.sidebar.latex(r"2SD = 1SD \times 2")
st.sidebar.latex(r"3SD = 1SD \times 3")