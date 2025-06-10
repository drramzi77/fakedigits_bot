# utils/i18n.py

import importlib
import os
import logging
from config import DEFAULT_LANGUAGE, MESSAGES_PATH

logger = logging.getLogger(__name__)

# # تم حذف قاموس LANG_FILE_MAP هنا لأنه لم يعد ضرورياً بعد إعادة تسمية الملفات

def get_messages(lang_code: str = DEFAULT_LANGUAGE) -> dict:
    """
    Loads messages for a given language code.
    Falls back to DEFAULT_LANGUAGE if the specified language is not found.
    """
    try:
        # # ستحاول استيراد messages.ar أو messages.en مباشرة
        module_name_to_import = f"{MESSAGES_PATH}.{lang_code}"
        
        # # التحقق مما إذا كان الملف موجودًا بالفعل قبل محاولة الاستيراد
        # # هذا المسار سيشير الآن إلى: fakedigits_bot/messages/ar.py
        file_path_check = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            '..',
            MESSAGES_PATH,
            f"{lang_code}.py" # # تم تعديل هذا السطر ليستخدم lang_code مباشرة
        )

        if not os.path.exists(file_path_check):
            logger.warning(f"Language file '{file_path_check}' not found. Falling back to default language '{DEFAULT_LANGUAGE}'.")
            
            # # محاولة تحميل اللغة الافتراضية إذا لم يتم العثور على الملف المحدد
            module_name_to_import = f"{MESSAGES_PATH}.{DEFAULT_LANGUAGE}"
            
            default_file_path_check = os.path.join(
                os.path.dirname(os.path.abspath(__file__)), '..', MESSAGES_PATH, f"{DEFAULT_LANGUAGE}.py"
            )
            if not os.path.exists(default_file_path_check):
                logger.critical(f"FATAL ERROR: Default language file '{default_file_path_check}' not found either. Bot may not function correctly.")
                return {}

        module = importlib.import_module(module_name_to_import)
        
        if not hasattr(module, 'messages') or not isinstance(module.messages, dict):
            logger.error(f"Language module '{module_name_to_import}' does not contain a 'messages' dictionary. Falling back to default.")
            module = importlib.import_module(f"{MESSAGES_PATH}.{DEFAULT_LANGUAGE}")
            return module.messages

        return module.messages

    except (ImportError, AttributeError) as e:
        logger.error(f"Error loading messages for language '{lang_code}' (attempted to import '{module_name_to_import}'): {e}. Falling back to default language '{DEFAULT_LANGUAGE}'.")
        try:
            default_module = importlib.import_module(f"{MESSAGES_PATH}.{DEFAULT_LANGUAGE}")
            return default_module.messages
        except (ImportError, AttributeError) as default_e:
            logger.critical(f"FATAL ERROR: Could not load default language messages ({DEFAULT_LANGUAGE}): {default_e}. Bot may not function correctly.")
            return {}