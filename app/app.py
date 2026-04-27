import streamlit as st
import sys
import os
import base64

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
from src.predict_pipeline import predict_price

st.set_page_config(page_title="CARS24 AI Valuation", layout="wide")

hero_path = os.path.join(BASE_DIR, "app", "assets", "hero_banner.png")
with open(hero_path, "rb") as img_file:
    hero_base64 = base64.b64encode(img_file.read()).decode()

st.markdown("""
<style>
#MainMenu {visibility:hidden;}
footer {visibility:hidden;}
header {visibility:hidden;}
.block-container {
    padding-top: 0.8rem;
    padding-left: 2rem;
    padding-right: 2rem;
    background:#f8fafc;
}
div.stButton > button {
    width:100%;
    height:54px;
    border-radius:14px;
    font-size:16px;
    font-weight:700;
    border:none;
    background: linear-gradient(90deg,#1d4ed8,#2563eb);
    color:white;
}
.white-card {
    background: rgba(255,255,255,0.96);
    padding: 22px;
    border-radius: 22px;
    box-shadow: 0px 10px 28px rgba(15,23,42,0.08);
    border:1px solid rgba(226,232,240,0.8);
}
.result-card {
    background: linear-gradient(135deg,#0f172a,#1d4ed8);
    color: white;
    padding: 22px;
    border-radius: 22px;
    box-shadow: 0px 10px 30px rgba(29,78,216,0.22);
    min-height: 190px;
}
.glass-card {
    background: rgba(255,255,255,0.9);
    padding:16px;
    border-radius:18px;
    box-shadow:0px 6px 18px rgba(15,23,42,0.06);
    border:1px solid rgba(226,232,240,0.8);
    text-align:center;
}
.insight-card {
    background: white;
    padding:20px;
    border-radius:18px;
    box-shadow:0px 6px 18px rgba(15,23,42,0.06);
    border:1px solid rgba(226,232,240,0.8);
    min-height:160px;
}
.section-title {
    font-size:14px;
    font-weight:700;
    color:#2563eb;
    letter-spacing:1px;
}
</style>
""", unsafe_allow_html=True)

st.markdown(f"""
<div style="
    background-image: linear-gradient(rgba(255,255,255,0.14), rgba(255,255,255,0.14)), url('data:image/png;base64,{hero_base64}');
    background-size: cover;
    background-position: center;
    height: 220px;
    border-radius: 24px;
    padding: 30px;
    display:flex;
    flex-direction:column;
    justify-content:center;
    box-shadow: 0px 12px 28px rgba(15,23,42,0.10);
">
    <div style="background:rgba(255,255,255,0.88); width:fit-content; padding:6px 14px; border-radius:20px; font-size:12px; font-weight:700; color:#1d4ed8;">PRODUCTION ML DEPLOYMENT INTERFACE</div>
    <h1 style="color:#0f172a; font-size:36px; margin-top:10px; margin-bottom:4px;">🚗 AI Powered Used Car Valuation Platform</h1>
    <p style="color:#1e293b; font-size:17px;">Enterprise-grade resale estimation driven by trained machine learning artifacts</p>
</div>
""", unsafe_allow_html=True)

st.markdown('<div style="height:18px"></div>', unsafe_allow_html=True)

left, right = st.columns([1.45, 0.55])

with left:
    st.markdown('<div class="white-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">VEHICLE INPUT MATRIX</div>', unsafe_allow_html=True)
    st.subheader("Vehicle Information")

    c1, c2, c3 = st.columns(3)
    with c1:
        make = st.selectbox("Brand", ['Maruti', 'Hyundai', 'Honda', 'Mahindra', 'Toyota', 'Tata', 'Ford', 'Renault', 'Others'])
        city = st.selectbox("Market City", ['Bangalore', 'Mumbai', 'Delhi', 'Chennai', 'Hyderabad', 'Pune', 'Kolkata', 'Ahmedabad', 'Jaipur', 'Lucknow', 'Others'])
        fueltype = st.selectbox("Fuel Type", ['Diesel', 'Petrol', 'Petrol + Cng'])
    with c2:
        model = st.selectbox("Model", ['Grand I10', 'Swift', 'Baleno', 'Wagon R 1.0', 'Elite I20','Alto 800', 'City', 'Creta', 'Celerio', 'Ecosport','Kwid', 'New  Wagon-R', 'Alto K10', 'Alto', 'Dzire', 'Others'])
        year = st.slider("Manufacturing Year", 2005, 2025, 2019)
        transmission = st.selectbox("Transmission", ['Automatic', 'Manual'])
    with c3:
        kilometerdriven = st.number_input("Kilometers Driven", 1000, 300000, 42000)
        ownernumber = st.selectbox("Owner Count", [1, 2, 3, 4])
        bodytype = st.selectbox("Body Segment", ['HATCHBACK', 'SUV', 'SEDAN', 'Sedan', 'Luxury SUV', 'Luxury Sedan'])

    d1,d2 = st.columns(2)
    with d1:
        isc24assured = st.selectbox("Certified Check", [1,0])
    with d2:
        registrationstate = st.selectbox("Registration State", ['Karnataka', 'Maharashtra', 'Delhi', 'Tamil Nadu', 'Telangana', 'Gujarat', 'Rajasthan', 'Uttar Pradesh', 'Others'])

    predict_btn = st.button("⚡ Generate AI Valuation")
    st.markdown('</div>', unsafe_allow_html=True)

predicted_price = None
segment = "Awaiting Analysis"
demand = "--"
score = 0
conf = "--"
insight1 = "Run valuation to receive depreciation intelligence."
insight2 = "Run valuation to receive market liquidity intelligence."
insight3 = "Run valuation to receive AI recommendation."

age = 2026-year
score = max(52, 100 - (age*3) - (kilometerdriven/5000) - (ownernumber*4))
score = round(score,1)

if predict_btn:
    user_input = {
        'make': make,'model': model,'city': city,'year': year,'fueltype': fueltype,
        'kilometerdriven': kilometerdriven,'ownernumber': ownernumber,'transmission': transmission,
        'bodytype': bodytype,'isc24assured': isc24assured,'registrationstate': registrationstate
    }
    predicted_price = predict_price(user_input)

    if predicted_price >= 900000:
        segment = "⭐ Premium Resale Segment"
        demand = "High Buyer Demand"
    elif predicted_price >= 600000:
        segment = "✅ Fair Market Segment"
        demand = "Stable Buyer Demand"
    else:
        segment = "💡 Budget Resale Segment"
        demand = "Practical Buyer Demand"

    if score >= 80:
        conf = "High Confidence"
    elif score >= 65:
        conf = "Moderate Confidence"
    else:
        conf = "Cautious Confidence"

    depr = round((age*2.8) + (kilometerdriven/12000),1)
    insight1 = f"Vehicle age of {age} years and {kilometerdriven:,} km usage contribute approximately {depr}% depreciation pressure on resale retention."

    insight2 = f"{make} {model} in {city} falls under {demand.lower()} where brand liquidity and urban demand improve market discoverability."

    if isc24assured == 1 and ownernumber == 1:
        insight3 = "Single owner certified profile significantly improves buyer trust score and supports stronger resale negotiation potential."
    elif ownernumber >= 3:
        insight3 = "Higher ownership count introduces trust discounting, reducing premium buyer confidence during resale decisioning."
    else:
        insight3 = "Balanced ownership and certification profile positions this vehicle in an average trust-driven resale bracket."

with right:
    price_display = "₹ --" if predicted_price is None else f"₹ {predicted_price:,.0f}"
    st.markdown(f'''<div class="result-card">
    <div style="font-size:13px; font-weight:700; opacity:0.9;">LIVE VALUATION OUTPUT</div>
    <h3 style="margin-top:8px;">Estimated Market Price</h3>
    <h1 style="margin-top:4px;">{price_display}</h1>
    <p style="font-size:17px; font-weight:600;">{segment}</p>
    <p>{demand}</p>
    <p><b>AI Confidence:</b> {conf}</p>
    </div>''', unsafe_allow_html=True)

    st.markdown('<div style="height:14px"></div>', unsafe_allow_html=True)
    st.markdown(f'<div class="glass-card"><div style="font-size:13px;color:#2563eb;font-weight:700;">VEHICLE HEALTH SCORE</div><h1 style="color:#0f172a;">{score}/100</h1></div>', unsafe_allow_html=True)

st.markdown('<div style="height:18px"></div>', unsafe_allow_html=True)

m1,m2,m3,m4 = st.columns(4)
usage = "Low Usage" if kilometerdriven < 40000 else "Moderate Usage" if kilometerdriven < 80000 else "High Usage"
own = "Single Owner" if ownernumber == 1 else "Multi Owner"
cert = "Certified" if isc24assured == 1 else "Non Certified"
with m1:
    st.markdown(f'<div class="glass-card"><div style="font-size:12px;color:#64748b;">Vehicle Age</div><h3>{2026-year} Years</h3></div>', unsafe_allow_html=True)
with m2:
    st.markdown(f'<div class="glass-card"><div style="font-size:12px;color:#64748b;">Usage Profile</div><h3>{usage}</h3></div>', unsafe_allow_html=True)
with m3:
    st.markdown(f'<div class="glass-card"><div style="font-size:12px;color:#64748b;">Ownership</div><h3>{own}</h3></div>', unsafe_allow_html=True)
with m4:
    st.markdown(f'<div class="glass-card"><div style="font-size:12px;color:#64748b;">Certification</div><h3>{cert}</h3></div>', unsafe_allow_html=True)

st.markdown('<div style="height:18px"></div>', unsafe_allow_html=True)

a1,a2,a3 = st.columns(3)
with a1:
    st.markdown(f'<div class="insight-card"><h4>📉 Depreciation Insight</h4><p>{insight1}</p></div>', unsafe_allow_html=True)
with a2:
    st.markdown(f'<div class="insight-card"><h4>📈 Market Demand Intelligence</h4><p>{insight2}</p></div>', unsafe_allow_html=True)
with a3:
    st.markdown(f'<div class="insight-card"><h4>🤖 AI Recommendation</h4><p>{insight3}</p></div>', unsafe_allow_html=True)
