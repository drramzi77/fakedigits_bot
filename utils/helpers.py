# utils/helpers.py (ملف جديد)

def get_flag(country_code: str) -> str:
    """
    يحول رمز كود الدولة (مثل 'sa') إلى رمز تعبيري للعلم (مثل '🇸🇦').
    """
    try:
        # التأكد من أن country_code مكون من حرفين فقط للتحويل الصحيح للعلم
        if len(country_code) == 2:
            return ''.join([chr(0x1F1E6 + (ord(c.upper()) - ord('A'))) for c in country_code])
        else:
            return "🏳️" # علم أبيض أو رمز افتراضي إذا لم يكن كود دولة صالح
    except Exception:
        return "🏳️" # علم أبيض في حال حدوث خطأ