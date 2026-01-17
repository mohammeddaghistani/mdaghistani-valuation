import pandas as pd
import math

def apply_taqeem_logic(comparables, target):
    """
    تطبيق منطق المقارنة الفنية وفق معايير الهيئة السعودية للمقيمين (تقييم).
    """
    adjusted_list = []
    
    for _, comp in comparables.iterrows():
        # 1. التعديلات النوعية (النشاط)
        act_adj = 1.05 if comp['النشاط الرئيسي'] == target['activity'] else 0.95
        
        # 2. التعديلات الزمنية (Time Adjustment)
        time_adj = 1.02  # افتراض تضخم سنوي 2% وفق السوق الحالي
        
        # 3. تعديل الموقع (المسافة من الحرم)
        dist_comp = math.sqrt((comp['lat']-21.4225)**2 + (comp['lon']-39.8262)**2)
        dist_target = math.sqrt((target['lat']-21.4225)**2 + (target['lon']-39.8262)**2)
        loc_adj = 1.10 if dist_target < dist_comp else 0.90 # ميزة القرب
        
        # القيمة المعدلة لكل مقارن
        adj_price = comp['القيمة السنوية للعقد'] * act_adj * time_adj * loc_adj
        adjusted_list.append(adj_price)
        
    return sum(adjusted_list) / len(adjusted_list)

def get_legal_grace_period(years):
    """المادة 24: فترة التجهيز (10% من مدة العقد، بحد أقصى 3 سنوات)"""
    return min(years * 0.10, 3.0)
