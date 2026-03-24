# ==========================================
# FINSECURE EXECUTIVE – FINAL MERGED VERSION
# UI (Neon Glass) + Real Model Logic
# ==========================================

import streamlit as st
import pandas as pd
import pickle
import plotly.graph_objects as go

# ==========================================
# PAGE CONFIG
# ==========================================
st.set_page_config(
    page_title="FinSecure Executive",
    page_icon="🏦",
    layout="wide"
)

# ==========================================
# ADVANCED NEON & GLASSMORPHISM CSS
# ==========================================
st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=Inter:wght@300;500&display=swap');

.stApp {
    background: radial-gradient(circle at center, #001233 0%, #000000 100%);
    color: #e0e0e0;
    font-family: 'Inter', sans-serif;
}

h1, h2, h3, .logo-text {
    font-family: 'Orbitron', sans-serif !important;
    letter-spacing: 2px;
}

/* Hide default header */
header {visibility: hidden;}

/* Glassmorphism Card */
.glass-card {
    background: rgba(10, 25, 47, 0.7);
    border: 1px solid rgba(0, 212, 255, 0.3);
    border-radius: 15px;
    padding: 25px;
    backdrop-filter: blur(12px);
    box-shadow: 0 0 25px rgba(0, 212, 255, 0.1);
    margin-bottom: 20px;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background-color: rgba(2, 12, 27, 0.95);
    border-right: 1px solid #00d4ff;
}

/* Buttons */
div.stButton > button {
    background: linear-gradient(45deg, #0072ff, #00d4ff);
    color: white;
    border: none;
    border-radius: 6px;
    font-weight: bold;
    text-transform: uppercase;
    width: 100%;
    transition: 0.3s;
    box-shadow: 0 0 12px rgba(0, 212, 255, 0.4);
}

div.stButton > button:hover {
    box-shadow: 0 0 30px rgba(0, 212, 255, 0.8);
    transform: translateY(-2px);
}

/* Inputs */
.stTextInput input, .stSelectbox div, .stNumberInput input {
    background-color: rgba(0, 0, 0, 0.4) !important;
    color: white !important;
    border: 1px solid rgba(0, 212, 255, 0.3) !important;
}

/* Header */
.header-container {
    text-align: center;
    padding: 20px;
    border-bottom: 2px solid #00d4ff;
    margin-bottom: 30px;
    box-shadow: 0 10px 15px -10px rgba(0, 212, 255, 0.5);
}

</style>
""", unsafe_allow_html=True)

# ==========================================
# HEADER
# ==========================================
st.markdown("""
<div class="header-container">
    <div style="font-size: 24px; color: #d4af37; font-weight: bold;">🏦 FinSecure Executive</div>
    <div style="font-size: 42px; color: #ffffff; font-weight: 700;">Fraud Detection Platform</div>
</div>
""", unsafe_allow_html=True)

# ==========================================
# LOAD REAL MODEL
# ==========================================
with open("fraud_model.pkl", "rb") as f:
    model = pickle.load(f)

with open("label_encoders.pkl", "rb") as f:
    label_encoders = pickle.load(f)

# ==========================================
# SIDEBAR
# ==========================================
with st.sidebar:
    st.markdown("### System Status")
    st.markdown('<div style="color: #00ff00; font-weight: bold;">● Model Active</div>', unsafe_allow_html=True)
    st.markdown("---")
    st.caption("Executive Risk Engine v4.1")
    st.caption("Live Prediction Mode")

# ==========================================
# MAIN LAYOUT
# ==========================================
left, right = st.columns([1.5, 1])
input_data = {}

# ==========================================
# REAL INPUT FORM (UNCHANGED LOGIC)
# ==========================================
with left:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown("### Transaction Details")

    features = model.feature_names_in_
    cols = st.columns(2)

    for i, feature in enumerate(features):
        column = cols[i % 2]
        with column:
            if feature in label_encoders:
                options = label_encoders[feature].classes_
                selected = st.selectbox(feature, options)
                encoded = label_encoders[feature].transform([selected])[0]
                input_data[feature] = encoded
            else:
                input_data[feature] = st.number_input(feature, value=0.0)

    st.markdown("<br>", unsafe_allow_html=True)
    predict_btn = st.button("Run Executive Risk Analysis")

    st.markdown('</div>', unsafe_allow_html=True)

# ==========================================
# RISK ASSESSMENT SECTION
# ==========================================
with right:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown("### Risk Assessment")

    if predict_btn:
        input_df = pd.DataFrame([input_data])
        prediction = model.predict(input_df)[0]
        probability = model.predict_proba(input_df)[0][1]
        risk_value = probability * 100

        status_text = "High Risk Transaction" if prediction == 1 else "Transaction Appears Safe"
        status_color = "#FF4B4B" if prediction == 1 else "#00ff88"

    else:
        risk_value = 0
        status_text = "Awaiting Analysis..."
        status_color = "#00d4ff"

    # Gauge
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=risk_value,
        number={'suffix': "%", 'font': {'color': 'white', 'size': 50}},
        gauge={
            'axis': {'range': [0, 100], 'tickcolor': "white"},
            'bar': {'color': "#ffffff"},
            'bgcolor': "rgba(0,0,0,0)",
            'steps': [
                {'range': [0, 40], 'color': "#00ff00"},
                {'range': [40, 70], 'color': "#ffa500"},
                {'range': [70, 100], 'color': "#ff0000"}
            ],
        }
    ))

    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font={'color': "white", 'family': "Orbitron"},
        height=320,
        margin=dict(l=20, r=20, t=40, b=20)
    )

    st.plotly_chart(fig, use_container_width=True)

    st.markdown(f"""
        <div style="text-align: center; margin-top: -15px;">
            <p style="color: {status_color}; font-size: 24px; font-weight: bold; font-family: 'Orbitron';">
                {status_text}
            </p>
        </div>
    """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

# ==========================================
# FOOTER
# ==========================================
st.markdown("""
<div style="text-align: center; color: rgba(255,255,255,0.3); font-size: 12px; margin-top: 50px;">
    © 2026 FinSecure Executive | Confidential Board-Level System | Powered by Executive Risk Engine v4.1
</div>
""", unsafe_allow_html=True)