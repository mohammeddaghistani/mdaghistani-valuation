import streamlit as st
import pandas as pd
from core_valuation import apply_taqeem_logic, get_legal_grace_period
from report_engine import generate_formal_report

st.set_page_config(page_title="mdaghistani | v3.0", layout="wide")

# تنسيق CSS مخصص لتغيير شكل التطبيق تماماً
st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stButton>button { background-color: #1B4F72; color: white; border-radius: 5px; height: 3em; width: 100%; }
    .metric-card { background-color: white; padding: 20px; border-radius: 10px; box-shadow: 2px 2px 10px #eee; border-top: 5px solid #D4AF37; }
    </style>
""", unsafe_allow_html=True)

st.title("🕋 نظام mdaghistani للتحليل العقاري المتقدم")
st.markdown("---")

col_sidebar, col_main = st.columns([1, 2.5])

with col_sidebar:
    st.subheader("⚙️ بارامترات الموقع")
    lat = st.number_input("إحداثي العرض", value=21.4225, format="%.6f")
    lon = st.number_input("إحداثي الطول", value=39.8262, format="%.6f")
    activity = st.selectbox("النشاط المستهدف", ["الأنشطة الرياضية", "مواقف السيارات", "تجزئة", "تعليمي"])
    term = st.slider("مدة الاستثمار (سنة)", 5, 50, 20)

with col_main:
    if st.button("تشغيل خوارزمية التقييم (Comparison Matrix)"):
        # محاكاة لبيانات المقارنة من ملفك
        data = pd.read_csv("data.csv")
        data['dist'] = (data['lat']-lat)**2 + (data['lon']-lon)**2
        comparables = data.sort_values('dist').head(5)
        
        final_val = apply_taqeem_logic(comparables, {"lat": lat, "lon": lon, "activity": activity})
        grace = get_legal_grace_period(term)
        
        # عرض النتائج في كروت احترافية
        c1, c2 = st.columns(2)
        with c1:
            st.markdown(f"<div class='metric-card'><h4>قيمة الإيجار السنوي</h4><h2>{final_val:,.2f} ريال</h2></div>", unsafe_allow_html=True)
        with c2:
            st.markdown(f"<div class='metric-card'><h4>فترة التجهيز (المادة 24)</h4><h2>{grace} سنوات</h2></div>", unsafe_allow_html=True)
        
        # زر التحميل بصيغة رسمية
        pdf = generate_formal_report({"value": final_val, "basis": "Market Value", "grace": grace})
        st.download_button("📂 تصدير تقرير 'تقييم' الفني", pdf, "Valuation_Report.pdf")

st.markdown("---")
st.caption("تم تطوير هذا النظام ليتوافق مع تحديثات لائحة التصرف بالعقارات البلدية 1444هـ وسياسات الهيئة السعودية للمقيمين المعتمدين.")
