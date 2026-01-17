import streamlit as st
import pandas as pd
import pydeck as pdk
import os
from core_valuation import apply_taqeem_logic, get_legal_grace_period

# إعداد الصفحة للجوال والكمبيوتر
st.set_page_config(page_title="mdaghistani | منصة التقييم", layout="wide")

# تنسيق بصري فخم
st.markdown("""
    <style>
    .main { background-color: #f4f7f6; }
    .stButton>button { 
        background: linear-gradient(135deg, #1e4d3a 0%, #0d2b1e 100%); 
        color: white; border-radius: 12px; height: 50px; border: none; font-size: 18px;
    }
    .result-card { 
        background-color: white; padding: 25px; border-radius: 15px; 
        border-right: 10px solid #c5a059; box-shadow: 0 4px 15px rgba(0,0,0,0.05);
    }
    </style>
""", unsafe_allow_html=True)

# عرض الشعار
if os.path.exists("logo.png"):
    st.image("logo.png", width=180)
else:
    st.title("🏛️ mdaghistani")

st.subheader("نظام التقييم العقاري الاستشاري")

# تحميل البيانات
@st.cache_data
def load_data():
    if os.path.exists("data.csv"):
        return pd.read_csv("data.csv")
    return pd.DataFrame()

# المحتوى الرئيسي
col1, col2 = st.columns([1, 1.5])

with col1:
    st.markdown("### 📍 معطيات الموقع")
    lat = st.number_input("خط العرض", value=21.4225, format="%.6f")
    lon = st.number_input("خط الطول", value=39.8262, format="%.6f")
    act = st.selectbox("النشاط", ["الأنشطة الرياضية", "مواقف السيارات", "تجزئة"])
    years = st.slider("مدة العقد", 1, 50, 20)

with col2:
    if st.button("تشغيل التحليل الفني"):
        df = load_data()
        if not df.empty:
            val = apply_taqeem_logic(df, {"lat": lat, "lon": lon, "activity": act})
            grace = get_legal_grace_period(years)
            
            st.markdown(f"""
                <div class="result-card">
                    <p style="color:#666; margin:0;">القيمة الإيجارية السنوية التقديرية</p>
                    <h1 style="color:#1e4d3a;">{val:,.2f} ريال</h1>
                    <hr>
                    <p style="color:#666; margin:0;">فترة التجهيز (المادة 24)</p>
                    <h2 style="color:#c5a059;">{grace} سنوات</h2>
                </div>
            """, unsafe_allow_html=True)

# خريطة احترافية
st.markdown("### 🗺️ النطاق الجغرافي")
df_map = load_data()
if not df_map.empty:
    st.pydeck_chart(pdk.Deck(
        initial_view_state=pdk.ViewState(latitude=21.4225, longitude=39.8262, zoom=11),
        layers=[pdk.Layer('ScatterplotLayer', data=df_map, get_position='[lon, lat]', get_color='[30, 77, 58, 160]', get_radius=200)]
    ))
