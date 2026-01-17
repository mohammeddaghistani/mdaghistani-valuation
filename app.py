import streamlit as st
import pandas as pd
import pydeck as pdk
import os
from core_valuation import apply_taqeem_logic, get_legal_grace_period
from report_engine import generate_formal_report

# إعدادات المتصفح والجوال
st.set_page_config(page_title="mdaghistani | التقييم العقاري", layout="wide", initial_sidebar_state="collapsed")

# تصميم فخم (CSS) متوافق مع الجوال
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Kufi+Arabic:wght@400;700&display=swap');
    html, body, [class*="css"] { font-family: 'Noto Kufi Arabic', sans-serif; direction: rtl; text-align: right; }
    .main { background-color: #fcfcfc; }
    .stButton>button { 
        background: linear-gradient(135deg, #1a4731 0%, #2d5a44 100%); 
        color: white; border: None; padding: 15px; border-radius: 12px; width: 100%; font-weight: bold; box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    .card { 
        background: white; padding: 20px; border-radius: 15px; border-right: 8px solid #c5a059; 
        box-shadow: 0 2px 10px rgba(0,0,0,0.05); margin-bottom: 20px;
    }
    [data-testid="stHeader"] { background: rgba(0,0,0,0); }
    </style>
""", unsafe_allow_html=True)

# عرض الشعار في الأعلى (تأكد من وجود logo.png في GitHub)
if os.path.exists("logo.png"):
    col_logo, _ = st.columns([1, 4])
    with col_logo:
        st.image("logo.png", width=150)

st.title("🕋 منصة mdaghistani الاستشارية")
st.caption("نظام تقييم معتمد وفق لائحة العقارات البلدية ومعايير (تقييم)")

# التحميل الآمن للبيانات
@st.cache_data
def load_data():
    try:
        return pd.read_csv("data.csv")
    except:
        return pd.DataFrame()

# الواجهة الرئيسية
with st.container():
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("🔍 معطيات التقييم الفني")
    c1, c2 = st.columns(2)
    with c1:
        lat = st.number_input("خط العرض", value=21.4225, format="%.6f")
        act = st.selectbox("النشاط", ["الأنشطة الرياضية", "مواقف السيارات", "تجزئة", "صحي"])
    with c2:
        lon = st.number_input("خط الطول", value=39.8262, format="%.6f")
        term = st.slider("مدة العقد (سنوات)", 1, 50, 20)
    
    if st.button("بدء تحليل القيمة السوقية"):
        df = load_data()
        if not df.empty:
            final_val = apply_taqeem_logic(df, {"lat": lat, "lon": lon, "activity": act})
            grace = get_legal_grace_period(term)
            
            st.markdown("---")
            res_col1, res_col2 = st.columns(2)
            with res_col1:
                st.markdown(f"<div style='text-align:center;'><h3>الإيجار السنوي</h3><h1 style='color:#1a4731;'>{final_val:,.2f} ريال</h1></div>", unsafe_allow_html=True)
            with res_col2:
                st.markdown(f"<div style='text-align:center;'><h3>فترة التجهيز</h3><h1 style='color:#c5a059;'>{grace} سنوات</h1></div>", unsafe_allow_html=True)
            
            # تصدير التقرير الفاخر
            pdf = generate_formal_report({"value": final_val, "grace": grace, "act": act})
            st.download_button("📥 تحميل التقرير الرسمي المعتمد", pdf, "mdaghistani_valuation.pdf")
    st.markdown("</div>", unsafe_allow_html=True)

# خريطة تفاعلية أسفل الصفحة
st.subheader("📍 النطاق الجغرافي للصفقات")
df_map = load_data()
if not df_map.empty:
    st.pydeck_chart(pdk.Deck(
        layers=[pdk.Layer('ScatterplotLayer', data=df_map, get_position='[lon, lat]', get_color='[26, 71, 49, 160]', get_radius=200)],
        initial_view_state=pdk.ViewState(latitude=21.4225, longitude=39.8262, zoom=11)
    ))
