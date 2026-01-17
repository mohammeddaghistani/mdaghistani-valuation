import streamlit as st
import pandas as pd
import sqlite3
import os
import pydeck as pdk
from datetime import datetime
from core_valuation import apply_valuation_matrix, get_grace_period
from report_engine import generate_professional_report

st.set_page_config(page_title="mdaghistani | تقييم مكة", layout="wide")

# تحميل البيانات (Streamlit Cloud يحتاج قراءة مباشرة من CSV)
@st.cache_data
def load_data():
    df = pd.read_csv("data.csv")
    df['القيمة السنوية للعقد'] = pd.to_numeric(df['القيمة السنوية للعقد'], errors='coerce').fillna(0)
    # استخراج الإحداثيات (كود مبسط للسحابة)
    def extract_coords(url):
        match = re.search(r'([-?\d\.]+),([-?\d\.]+)', str(url))
        return (float(match.group(1)), float(match.group(2))) if match else (None, None)
    # ملاحظة: يفضل أن يكون ملف data.csv يحتوي على أعمدة lat, lon جاهزة لتسريع السحابة
    return df

st.title("🕋 mdaghistani - نظام التقييم العقاري البلدي")
st.markdown("---")

tab1, tab2 = st.tabs(["🎯 محرك التقييم", "📊 خريطة الصفقات"])

with tab1:
    c1, c2 = st.columns([1, 1.5])
    with c1:
        st.subheader("📋 مدخلات العقار")
        lat = st.number_input("Lat", value=21.4225, format="%.6f")
        lon = st.number_input("Lon", value=39.8262, format="%.6f")
        act = st.selectbox("النشاط", ["الأنشطة الرياضية", "مواقف السيارات", "تجزئة"])
        years = st.slider("مدة العقد", 1, 50, 15)
        
    with c2:
        if st.button("تحليل القيمة المقارنة", use_container_width=True):
            df = load_data()
            # مصفوفة التعديلات
            df_final = apply_valuation_matrix(df.head(10), {"lat": lat, "lon": lon, "activity": act})
            val = df_final['adjusted_price'].mean()
            grace = get_grace_period(years)

            st.metric("الإيجار السوقي السنوي", f"{val:,.2f} ريال")
            st.info(f"فترة التجهيز الموصى بها (المادة 24): {grace} سنوات")
            
            # تصدير التقرير
            pdf = generate_professional_report({
                "value": val, "date": datetime.now().strftime("%Y-%m-%d"),
                "grace": grace, "basis": "Market Rent", "report_id": "MD-2026"
            })
            st.download_button("📥 تحميل تقرير 'تقييم' المعتمد", pdf, "mdaghistani_report.pdf")

with tab2:
    st.subheader("توزيع صفقات مكة المكرمة")
    # عرض خريطة تفاعلية لصفقات داغستاني
    st.write("سيتم عرض الخريطة بناءً على إحداثيات ملف data.csv")
