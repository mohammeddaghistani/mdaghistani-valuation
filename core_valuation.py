import pandas as pd
import re
import math

def apply_valuation_matrix(results, target_data):
    """تطبيق مصفوفة التعديلات الكمية وفق دليل تقييم ص 34"""
    adjusted_results = results.copy()
    
    def calculate_adjustment(row):
        adj = 1.0
        # 1. تعديل النشاط (أعلى وأفضل استخدام)
        if str(row['النشاط الرئيسي']).strip() == target_data['activity'].strip():
            adj += 0.10  # ميزة تطابق النشاط
        else:
            adj -= 0.05  # خصم اختلاف النشاط
            
        # 2. تعديل الموقع (القرب من الحرم كمعيار مكة)
        target_dist = math.sqrt((target_data['lat']-21.4225)**2 + (target_data['lon']-39.8262)**2)
        comp_dist = math.sqrt((row['lat']-21.4225)**2 + (row['lon']-39.8262)**2)
        if target_dist < comp_dist: adj += 0.08 # ميزة الموقع الأفضل للهدف
        
        return adj

    adjusted_results['factor'] = adjusted_results.apply(calculate_adjustment, axis=1)
    adjusted_results['adjusted_price'] = adjusted_results['القيمة السنوية للعقد'] * adjusted_results['factor']
    return adjusted_results

def get_grace_period(duration):
    """فترة التجهيز - المادة 24 (10% من العقد بحد أقصى 3 سنوات)"""
    return min(duration * 0.10, 3.0)
