import math

def apply_taqeem_logic(df, target):
    """
    تطبيق مصفوفة التعديلات الكمية (Quantitative Adjustments)
    وفق دليل تقييم العقارات البلدية ص 34.
    """
    # حساب المسافة لكل مقارن عن العقار المستهدف
    df = df.copy()
    df['distance'] = df.apply(lambda r: math.sqrt((r['lat']-target['lat'])**2 + (r['lon']-target['lon'])**2), axis=1)
    
    # اختيار أقرب 5 مقارنات (Comparables)
    comps = df.sort_values('distance').head(5)
    
    adjusted_prices = []
    for _, row in comps.iterrows():
        base_price = row['القيمة السنوية للعقد']
        adjustment_factor = 1.0
        
        # 1. تعديل النشاط (0.10+ إذا تطابق، 0.05- إذا اختلف)
        if str(row['النشاط الرئيسي']).strip() == target['activity'].strip():
            adjustment_factor += 0.10
        else:
            adjustment_factor -= 0.05
            
        # 2. تعديل الموقع (القرب من الحرم كميزة تنافسية)
        dist_to_haram_comp = math.sqrt((row['lat']-21.4225)**2 + (row['lon']-39.8262)**2)
        dist_to_haram_target = math.sqrt((target['lat']-21.4225)**2 + (target['lon']-39.8262)**2)
        
        if dist_to_haram_target < dist_to_haram_comp:
            adjustment_factor += 0.07  # العقار الهدف موقعه أفضل
            
        adjusted_prices.append(base_price * adjustment_factor)
        
    return sum(adjusted_prices) / len(adjusted_prices)

def get_legal_grace_period(years):
    # تطبيق المادة 24 من اللائحة التنفيذية
    return min(years * 0.10, 3.0)
