import streamlit as st
import pandas as pd
import re
import pydeck as pdk
from datetime import datetime
from core_valuation import apply_valuation_matrix, get_grace_period
from report_engine import generate_professional_report

st.set_page_config(page_title="mdaghistani | تقييم مكة", layout="wide")

# دالة ذكية لتحميل ومعالجة البيانات من CSV
@st.cache_data
def load_and_clean_data():
    df = pd.read_csv("data.csv")
    df['القيمة السنوية للعقد'] = pd.to_numeric(df['القيمة السنوية للعقد'], errors='coerce').fillna(0)
    def extract_coords(url):
        match = re.search(r'([-?\d\.]+),([-?\d\.]+)', str(url))
        return (float(match.group(1)), float(match.group(2))) if match else (None, None)
    if 'lat' not in df.columns:
        df[['lat', 'lon']] = df['رابط الموقع'].apply(lambda x: pd.Series(extract_coords(x)))
    return df[df['lat'].notna()]

st.sidebar.title("mdaghistani System")
st.title("🕋 نظام الخبير العقاري mdaghistani")
st.caption("متوافق مع لائحة التصرف بالعقارات البلدية ومعايير (تقييم) 2026")

tab1, tab2 = st.tabs(["🎯 محرك التقييم المعتمد", "🔥 خريطة التركز السعري"])

with tab1:
    c1, c2 = st.columns([1, 1.5])
    with c1:
        st.subheader("📍 معطيات العقار")
        lat = st.number_input("Lat", value=21.4225, format="%.6f")
        lon = st.number_input("Lon", value=39.8262, format="%.6f")
        act = st.selectbox("النشاط", ["الأنشطة الرياضية", "مواقف السيارات", "تجزئة"])
        years = st.slider("مدة الاستثمار (سنوات)", 1, 50, 15)
        
    with c2:
        if st.button("تحليل القيمة المقارنة", use_container_width=True):
            data = load_and_clean_data()
            # جلب أقرب 10 صفقات وتطبيق المصفوفة
            subset = data.copy()
            subset['dist'] = (subset['lat']-lat)**2 + (subset['lon']-lon)**2
            top_deals = subset.sort_values('dist').head(10)
            
            df_final = apply_valuation_matrix(top_deals, {"lat": lat, "lon": lon, "activity": act})
            val = df_final['adjusted_price'].mean()
            grace = get_grace_period(years)

            # بطاقة النتيجة
            st.markdown(f"""
                <div style="background-color:#fffdf5; padding:25px; border-radius:15px; border-right:10px solid #d4af37;">
                    <h2 style="color:#d4af37; margin:0;">{val:,.2f} ريال</h2>
                    <p style="color:#5d4037;">الإيجار السوقي السنوي المقترح</p>
                    <p style="color:#8d6e63; font-size:14px;">فترة التجهيز (المادة 24): {grace} سنوات</p>
                </div>
            """, unsafe_allow_html=True)
            
            pdf = generate_professional_report({
                "value": val, "date": datetime.now().strftime("%Y-%m-%d"),
                "grace": grace, "basis": "Market Rent", "report_id": f"MD-{datetime.now().year}"
            })
            st.download_button("📥 تحميل التقرير الرسمي (PDF)", pdf, "mdaghistani_valuation.pdf")

with tab2:
    st.subheader("تحليل تركز القيم في مكة")
    map_data = load_and_clean_data()
    st.pydeck_chart(pdk.Deck(
        layers=[pdk.Layer('HeatmapLayer', data=map_data, get_position='[lon, lat]', get_weight='القيمة السنوية للعقد', radius_pixels=50)],
        initial_view_state=pdk.ViewState(latitude=21.4225, longitude=39.8262, zoom=11)
    ))
