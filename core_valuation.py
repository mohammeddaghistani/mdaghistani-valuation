import math

def apply_taqeem_logic(df, target):
    """تطبيق مصفوفة التعديلات الكمية وفق دليل تقييم العقارات البلدية ص 34"""
    df = df.copy()
    # حساب المسافة التقريبية
    df['dist'] = df.apply(lambda r: math.sqrt((r['lat']-target['lat'])**2 + (r['lon']-target['lon'])**2), axis=1)
    # اختيار أفضل 5 مقارنات
    comps = df.sort_values('dist').head(5)
    
    adjusted_prices = []
    for _, row in comps.iterrows():
        base = row['القيمة السنوية للعقد']
        adj = 1.0
        # تعديل النشاط (ص 34)
        if str(row['النشاط الرئيسي']).strip() == target['activity'].strip():
            adj += 0.10
        else:
            adj -= 0.05
        # تعديل الموقع (القرب من الحرم)
        dist_haram_comp = math.sqrt((row['lat']-21.4225)**2 + (row['lon']-39.8262)**2)
        dist_haram_target = math.sqrt((target['lat']-21.4225)**2 + (target['lon']-39.8262)**2)
        if dist_haram_target < dist_haram_comp:
            adj += 0.07
            
        adjusted_prices.append(base * adj)
    return sum(adjusted_prices) / len(adjusted_prices)

def get_legal_grace_period(years):
    """المادة 24: 10% من مدة العقد بحد أقصى 3 سنوات"""
    return min(years * 0.10, 3.0)
