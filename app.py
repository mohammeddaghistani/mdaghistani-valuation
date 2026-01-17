import streamlit as st
import pandas as pd
import pydeck as pdk
from datetime import datetime
import re
from core_valuation import apply_taqeem_logic, get_legal_grace_period
from report_engine import generate_formal_report

# 1. إعدادات الصفحة والجماليات (تم نقلها لتجنب الخطأ)
st.set_page_config(page_title="نظام mdaghistani للتقييم", layout="wide")

def apply_custom_style():
    st.markdown("""
        <style>
        .main { background-color: #f8f9fa; }
        .stButton>button { background-color: #1a4731; color: white; border-radius: 8px; font-weight: bold; }
        .metric-container { 
            background-color: white; padding: 25px; border-radius: 12px; 
            box-shadow: 0 4px 12px rgba(0,0,0,0.05); border-top: 6px solid #c5a059;
            text-align: center;
        }
        </style>
    """, unsafe_allow_html=True)

# 2. دالة تحميل البيانات (المتسببة في الخطأ السابق تم إصلاح وضعها)
@st.cache_data
def load_and_prepare_data():
    try:
        df = pd.read_csv("data.csv")
        df['القيمة السنوية للعقد'] = pd.to_numeric(df['القيمة السنوية للعقد'], errors='coerce').fillna(0)
        # معالجة الإحداثيات إذا لم تكن موجودة كأعمدة
        if 'lat' not in df.columns:
            def extract_lat_lon(url):
                match = re.search(r'([-?\d\.]+),([-?\d\.]+)', str(url))
                return (float(match.group(1)), float(match.group(2))) if match else (None, None)
            df[['lat', 'lon']] = df['رابط الموقع'].apply(lambda x: pd.Series(extract_lat_lon(x)))
        return df[df['lat'].notna()]
    except Exception as e:
        st.error(f"خطأ في قراءة ملف data.csv: {e}")
        return pd.DataFrame()

# 3. واجهة المستخدم
apply_custom_style()
st.title("🕋 منصة mdaghistani للتحليل والتقييم العقاري")
st.caption("إصدار احترافي متوافق مع معايير الهيئة السعودية للمقيمين المعتمدين 2026")

tab1, tab2 = st.tabs(["🎯 محرك التقييم الفني", "🗺️ تحليل النطاق الجغرافي"])

with tab1:
    col_input, col_result = st.columns([1, 2])
    
    with col_input:
        st.subheader("📋 معطيات العقار")
        lat_in = st.number_input("خط العرض (Latitude)", value=21.4225, format="%.6f")
        lon_in = st.number_input("خط الطول (Longitude)", value=39.8262, format="%.6f")
        act_in = st.selectbox("نوع النشاط البلدي", ["الأنشطة الرياضية", "مواقف السيارات", "تجزئة", "خدمي"])
        years_in = st.slider("مدة العقد الاستثماري", 1, 50, 15)
        
    with col_result:
        if st.button("تحليل القيمة السوقية وتشغيل مصفوفة التعديلات", use_container_width=True):
            raw_data = load_and_prepare_data()
            if not raw_data.empty:
                # منطق المقارنة الفنية
                final_val = apply_taqeem_logic(raw_data, {"lat": lat_in, "lon": lon_in, "activity": act_in})
                grace_period = get_legal_grace_period(years_in)
                
                # عرض النتائج بشكل لائق
                res_c1, res_c2 = st.columns(2)
                with res_c1:
                    st.markdown(f"""<div class='metric-container'>
                        <p style='color:#666;'>الإيجار السنوي التقديري</p>
                        <h2 style='color:#1a4731;'>{final_val:,.2f} ريال</h2>
                    </div>""", unsafe_allow_html=True)
                with res_c2:
                    st.markdown(f"""<div class='metric-container'>
                        <p style='color:#666;'>فترة التجهيز (المادة 24)</p>
                        <h2 style='color:#c5a059;'>{grace_period} سنوات</h2>
                    </div>""", unsafe_allow_html=True)
                
                # تصدير التقرير
                pdf_file = generate_formal_report({"value": final_val, "grace": grace_period, "date": datetime.now().strftime("%Y-%m-%d")})
                st.download_button("📂 تحميل تقرير التقييم المعتمد (PDF)", pdf_file, "Mdaghistani_Report.pdf")

with tab2:
    st.subheader("خريطة التركز السعري (Heatmap) لمدينة مكة")
    map_df = load_and_prepare_data()
    if not map_df.empty:
        st.pydeck_chart(pdk.Deck(
            map_style='mapbox://styles/mapbox/light-v9',
            initial_view_state=pdk.ViewState(latitude=21.4225, longitude=39.8262, zoom=11, pitch=45),
            layers=[pdk.Layer('HeatmapLayer', data=map_df, get_position='[lon, lat]', get_weight='القيمة السنوية للعقد', radius_pixels=40)]
        ))
