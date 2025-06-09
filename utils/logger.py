import logging
import os
from datetime import datetime

def setup_logging():
    """
    يقوم بتهيئة نظام التسجيل (logging) للبوت.
    - يسجل الرسائل في ملف log.txt داخل مجلد 'logs/'.
    - يعرض الرسائل في وحدة التحكم (console).
    """
    log_directory = "logs"
    if not os.path.exists(log_directory):
        os.makedirs(log_directory)

    log_filename = datetime.now().strftime("%Y-%m-%d") + ".log"
    log_filepath = os.path.join(log_directory, log_filename)

    # تكوين المٌسجل الرئيسي (root logger)
    logging.basicConfig(
        level=logging.INFO,  # المستويات: DEBUG, INFO, WARNING, ERROR, CRITICAL
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
        handlers=[
            logging.FileHandler(log_filepath, encoding='utf-8'),
            logging.StreamHandler()
        ]
    )
    # تعطيل تسجيل بعض المكتبات التي قد تكون صاخبة جداً
    logging.getLogger('httpx').setLevel(logging.WARNING)
    logging.getLogger('telegram').setLevel(logging.WARNING)
    logging.getLogger('telegram.ext').setLevel(logging.WARNING)

    logging.info("تم تهيئة نظام التسجيل بنجاح.")

# يمكنك استدعاء هذه الدالة مرة واحدة عند بدء تشغيل البوت.
# مثال:
# if __name__ == "__main__":
#     setup_logging()
#     logging.info("هذه رسالة معلومات.")
#     logging.warning("هذا تحذير!")
#     logging.error("هذا خطأ!")