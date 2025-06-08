import json
import os
import logging

logger = logging.getLogger(__name__)

def load_json_file(file_path: str, default_data=None):
    """
    يُحمّل البيانات من ملف JSON. إذا لم يتم العثور على الملف أو كان تالفًا، يُرجع default_data.
    """
    if default_data is None:
        default_data = {} # الافتراضي هو قاموس فارغ إذا لم يُحدد

    if not os.path.exists(file_path):
        logger.warning(f"ملف JSON '{file_path}' غير موجود. سيتم إرجاع بيانات افتراضية.")
        return default_data
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError:
        logger.error(f"خطأ في قراءة ملف JSON '{file_path}'. الملف قد يكون تالفًا. سيتم إرجاع بيانات افتراضية.", exc_info=True)
        return default_data
    except IOError as e:
        logger.error(f"خطأ في الوصول إلى ملف JSON '{file_path}' أثناء التحميل: {e}", exc_info=True)
        return default_data
    except Exception as e:
        logger.error(f"خطأ غير متوقع عند تحميل ملف JSON '{file_path}': {e}", exc_info=True)
        return default_data

def save_json_file(file_path: str, data):
    """
    يُحفظ البيانات إلى ملف JSON.
    """
    try:
        # ✅ تأكد من وجود المجلد
        os.makedirs(os.path.dirname(file_path), exist_ok=True) # ✅ تم إضافة هذا السطر
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        logger.info(f"تم حفظ البيانات في ملف JSON '{file_path}'.")
    except IOError as e:
        logger.error(f"خطأ في الوصول إلى ملف JSON '{file_path}' أثناء الحفظ: {e}", exc_info=True)
    except Exception as e:
        logger.error(f"خطأ غير متوقع عند حفظ ملف JSON '{file_path}': {e}", exc_info=True)