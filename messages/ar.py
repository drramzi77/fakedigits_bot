# messages/arabic.py

messages = {
    "language_selected_success": "✅ تم اختيار اللغة بنجاح.\n\nاضغط الزر أدناه للبدء.",
    "start_using_bot": "🚀 ابدأ",
    # =========================================================================
    #  General Messages (رسائل عامة)
    # =========================================================================
    "welcome_message": "أهلاً بك في بوت FakeDigits! 🤖\n\nيوفر لك البوت أرقامًا وهمية لمرة واحدة لتفعيل حساباتك على مختلف التطبيقات والخدمات.",
    "invalid_command": "أمر غير صالح. يرجى استخدام الأوامر الصحيحة.",
    "error_processing_request": "حدث خطأ أثناء معالجة طلبك. يرجى المحاولة مرة أخرى لاحقًا.",
    "choose_option": "اختر أحد الخيارات:", # يستخدم في main_menu
    "unrecognized_text_input": "👋 عفواً، لم أفهم طلبك. يرجى استخدام الأوامر أو الأزرار المتاحة.",
    "price_currency": "ر.س", # العملة الافتراضية
    "not_available": "لا يوجد", # يستخدم لليوزرنيم أو معلومات غير متوفرة
    "unknown_value_char": "❓", # يستخدم لحقول التاريخ أو المنصة أو الدولة غير المتوفرة


    # =========================================================================
    #  Main Dashboard & Menu Buttons (أزرار ولوحة التحكم الرئيسية)
    # =========================================================================
    "main_menu_title": "القائمة الرئيسية 🏠", # عنوان القائمة الرئيسية (إذا استخدمت في مكان ما)
    "buy_number_button": "شراء رقم 🛒",
    "profile_button": "ملفي الشخصي 👤",
    "offers_button": "العروض 🎁",
    "favorites_button": "المفضلة ❤️",
    "earn_credit_button": "اكسب رصيد 💰",
    "transfer_credit_button": "تحويل رصيد 💸",
    "help_button": "مساعدة ❓",
    "language_button": "English🌐العربية",
    "admin_panel_button": "لوحة التحكم ⚙️", # سيتم تفعيلها لاحقًا
    "available_platforms": "المنصات المتاحة الآن", # زر في الداشبورد
    "quick_search": "البحث السريع 🔎", # زر في الداشبورد
    "ready_numbers": "أرقام فورية جاهزة 🚀", # زر في الداشبورد
    "channel_button": "قناة البوت 📢", # زر في الداشبورد
    "become_agent_button": "كن وكيلًا معنا 🤝", # زر في الداشبورد
    "view_transfer_logs": "عرض التحويلات السابقة 📜", # زر للمشرفين في الداشبورد
    "admin_users": "إدارة المستخدمين 🛠️", # زر للمشرفين في الداشبورد
    "back_button_text": "🔙 العودة", # نص زر العودة العام
    "back_to_dashboard_button_text": "🔙 العودة للقائمة الرئيسية", # نص زر العودة من قائمة اختيار التطبيق الى لوحة التحكم الرئيسية


    # =========================================================================
    #  Dashboard Display Messages (رسائل عرض لوحة التحكم)
    # =========================================================================
    "dashboard_welcome": "👋 أهلاً بك يا <b>{display_name}</b> في لوحة تحكمك الرئيسية! 😊",
    "dashboard_id": "🆔 <b>ID:</b> <code>{user_id}</code>",
    # # تم التعديل على هذا السطر (إضافة {currency})
    "dashboard_balance": "💰 <b>الرصيد:</b> {balance} {currency}",
    "dashboard_channel_promo": "📢 اشترك في {channel_link}",
    "dashboard_choose_option": "🔽 اختر من القائمة التالية:",


    # =========================================================================
    #  Subscription Check (فحص الاشتراك)
    # =========================================================================
    "check_subscription_button": "🔁 تحقق من الاشتراك",
    "subscribe_to_channel": "اشترك في", # يستخدم مع اسم القناة
    "subscribed_success": "✅ تم التحقق من اشتراكك.\nاستخدم الأمر /plus للمتابعة.",
    "not_subscribed_channel": "📢 لضمان حصولك على الأرقام المميزة أولاً بأول، يرجى الاشتراك في القناة الرسمية للبوت.\n\n🔒 الاشتراك ضروري لتفعيل خدمات البوت والاستفادة الكاملة.\n👇 قم بالاشتراك ثم اضغط على زر 'تحقق من الاشتراك' بالأسفل: {channel_link}",
    "not_subscribed_channel_retry": "❗ لم نتمكن من التحقق من اشتراكك حتى الآن.\n✅ تأكد من أنك اشتركت في القناة المطلوبة.\n🔄 بعد الاشتراك، اضغط على الزر بالأسفل لإعادة التحقق: {channel_link}",


    # =========================================================================
    #  Error Handling Messages (رسائل معالجة الأخطاء)
    # =========================================================================
    "contact_support_button_error": "💬 تواصل مع الدعم",
    "back_to_main_menu_error": "🔙 العودة للقائمة الرئيسية", # لم يعد يستخدم بشكل مباشر في الكود الجديد، يستبدل بـ back_to_dashboard_button_text
    "error_processing_request_user": "❌ عذراً، حدث خطأ غير متوقع! 😔\nتم إبلاغ المسؤولين وسنعمل على إصلاحه بأسرع وقت.\n\n❓ يمكنك التواصل مع الدعم أو العودة للقائمة الرئيسية.",
    "bot_error_alert": "حدث خطأ في البوت!",
    "update_info": "التحديث",
    "error_details": "الخطأ",


    # =========================================================================
    #  Balance & Recharge (الرصيد والشحن)
    # =========================================================================
    "recharge_balance_button": "شحن رصيدي 💳", # زر في الداشبورد
    "withdraw_balance_button": "سحب الرصيد 🏧", # **تمت إضافة هذا السطر لحل المشكلة السابقة**
    "recharge_from_admin_button": "🧑‍💼 شحن من الإدارة",
    "recharge_welcome_message": "🟢 <b>مرحبًا بك في نظام شحن الرصيد!</b>\nيمكنك شحن حسابك في البوت باستخدام إحدى الطرق التالية:",
    "available_payment_methods": "💸 <b>طرق الدفع المتاحة:</b>",
    "payment_method_kareem": "🔹 كـريـم إيـداع / النجـم",
    "payment_method_vodafone": "🔹 فودافون كاش / تحويل مباشر",
    "payment_method_zain": "🔹 زين كاش / آسيا حوالة",
    "payment_method_crypto": "🔹 عملات رقمية: USDT / BTC / Payeer",
    "payment_method_paypal": "🔹 PayPal",
    "payment_method_other": "🔹 أي وسيلة أخرى يتم الاتفاق عليها",
    "send_proof_message": "📌 <i>يرجى إرسال إثبات الدفع إلى الإدارة مع معرفك التالي:</i>\n<code>{user_id}</code>",
    "contact_admin_message": "📞 <b>للتواصل مع الإدارة:</b> {admin_username}", # للمشرف الذي يتم التواصل معه
    "press_button_to_proceed": "📍 <b>اضغط على أحد الأزرار بالأسفل لإتمام العملية 👇</b>",
    "recharge_admin_title": "👨‍💼 <b>شحن من الإدارة</b>",
    "contact_dev_message": "يرجى التواصل مباشرة مع المطور عبر الرابط التالي:\n🔗 <a href='{dev_link}'>{dev_link}</a>",
    "send_proof_manual_recharge": "📤 أرسل له إثبات الدفع + معرفك في البوت، وسيتم شحن الرصيد يدويًا خلال دقائق.",
    "back_to_previous_menu": "🔙 يمكنك العودة باستخدام الزر أدناه.",
    "check_balance_button": "💰 رصيدي", # زر للتحقق من الرصيد فقط (في main_menu_kb)
    "my_balance_is": "💰 رصيدك الحالي هو: {balance} {currency}", # أمر /balance للمستخدم نفسه
    "my_balance_info": "👤 المستخدم: {name}\n🆔 المعرف: <code>{user_id}</code>\n💰 الرصيد الحالي: {balance} {currency}", # أمر /balance للمستخدم نفسه (تنسيق تفصيلي)
    "user_balance_info": "👤 المستخدم: {name}\n🆔 المعرف: <code>{user_id}</code>\n💰 الرصيد: {balance} {currency}", # أمر /balance للمشرف للاستعلام عن آخر
    "unknown_user_in_group": "غير معروف (ربما ليس في المجموعة)",
    "invalid_user_id_balance_command": "❌ أدخل معرفًا صالحًا مثل: /balance 123456789",
    "no_permission_to_view_others_balance": "❌ ليس لديك صلاحية لعرض رصيد الآخرين.",
    "admin_only_command": "❌ هذا الأمر مخصص فقط للمسؤولين.", # لأوامر /add_balance و /deduct_balance
    "add_balance_invalid_amount_format": "❌ الصيغة غير صحيحة للمبلغ. استخدم: /add_balance <user_id> <amount>",
    "add_balance_invalid_amount": "❌ أدخل مبلغًا صالحًا مثل: /add_balance 200",
    "add_balance_invalid_format": "❌ الصيغة غير صحيحة. استخدم: /add_balance <user_id> <amount> أو /add_balance <amount>",
    "amount_must_be_positive": "❌ المبلغ يجب أن يكون أكبر من صفر.",
    "invalid_user_id_after_clean": "❌ معرف المستخدم غير صالح أو فارغ بعد التنظيف.",
    "user_id_conversion_error": "❌ حدث خطأ في تحويل معرف المستخدم. يرجى التأكد من صلاحيته.",
    "balance_added_success": "✅ تم إضافة {amount} {currency} إلى رصيد المستخدم {user_id}.",
    "error_updating_balance": "❌ حدث خطأ أثناء تحديث الرصيد. يرجى مراجعة سجلات البوت.",
    "deduct_balance_invalid_format": "❌ الصيغة: /deduct_balance <user_id> <amount>",
    "deduct_balance_invalid_amount": "❌ أدخل مبلغًا صالحًا.",
    "insufficient_balance_deduct": "❌ الرصيد غير كافٍ. الرصيد الحالي: {current_balance} {currency}",
    "balance_deducted_success": "✅ تم خصم {amount} {currency} من المستخدم {user_id}.",
    "current_balance_prompt": "💰 رصيدك الحالي: {balance} {currency}", # **تمت إضافة هذا السطر**
    "balance_update_success": "✅ تم تحديث رصيد المستخدم {user_id} إلى {new_balance} {currency}.", # **تمت إضافة هذا السطر**


    # =========================================================================
    #  Withdraw Balance (سحب الرصيد)
    # =========================================================================
    "withdraw_balance_button_profile": "🏧 سحب الرصيد", # زر في صفحة البروفايل
    "withdraw_request_title": "🏧 <b>طلب سحب الرصيد</b>",
    "withdraw_instructions": "لضمان سرعة معالجة الطلب، يرجى إرسال بيانات التحويل بالتنسيق التالي:",
    "withdraw_full_name_field": "🔹 <b>الاسم الثلاثي:</b>",
    "withdraw_account_number_field": "🔹 <b>رقم الحساب أو المحفظة:</b>",
    "withdraw_type_field": "🔹 <b>نوع التحويل</b> (STC Pay / بنكي / حوالة):",
    "withdraw_amount_field": "🔹 <b>المبلغ المطلوب:</b>",
    "withdraw_review_notice": "📌 <i>سيتم مراجعة طلبك خلال 24 ساعة عمل كحد أقصى.</i>",
    "withdraw_contact_admin_prompt": "📞 في حال وجود أي مشكلة أو استفسار عاجل، يمكنك التواصل مباشرة مع الإدارة:",
    "contact_admin_button_withdraw": "📬 تواصل مع الإدارة",


    # =========================================================================
    #  Transfer Credit (تحويل الرصيد)
    # =========================================================================
    "transfer_successful": "تم تحويل {amount} 💵 بنجاح إلى المستخدم {receiver_id}.", # يستخدم في رسالة التأكيد بعد التحويل (مفاتيح قديمة لم تعد تستخدم مباشرة)
    "transfer_received": "لقد تلقيت تحويلاً بقيمة {amount} 💵 من المستخدم {sender_id}.", # يستخدم في رسالة التبليغ للمستلم (مفاتيح قديمة لم تعد تستخدم مباشرة)
    "enter_transfer_amount": "أدخل المبلغ الذي ترغب في تحويله (بالدولار):", # مفتاح قديم لم يعد يستخدم
    "invalid_amount": "مبلغ غير صالح. يرجى إدخال رقم موجب.", # مفتاح قديم لم يعد يستخدم
    "enter_receiver_id": "الآن، أدخل معرف المستخدم (ID) للمستقبل:", # مفتاح قديم لم يعد يستخدم
    "receiver_not_found": "المستخدم المستقبل غير موجود. يرجى التحقق من المعرف.", # مفتاح قديم لم يستخدم بعد في الكود
    "confirm_transfer": "هل أنت متأكد من تحويل {amount} 💵 إلى المستخدم {receiver_id}?", # مفتاح قديم لم يعد يستخدم
    "contact_support_button_transfer": "💬 تواصل مع الدعم", # مفتاح خاص بزر الدعم في التحويلات

    "admin_transfer_warning": "⚠️ هذا الخيار مخصص فقط للمستخدمين.\n🔋 لشحن رصيد مستخدم، استخدم القسم المخصص لذلك في لوحة التحكم.",
    "transfer_balance_too_low": "❌ - لا يمكنك تحويل الرصيد الآن.\n📊 - رصيدك الحالي: <b>{balance} {currency}</b>",
    "transfer_fee_info": "💸 - عمولة التحويل: <b>{fee_percentage}%</b>",
    "transfer_solution_prompt": "🔄 <b>ما الحل؟</b>",
    "transfer_solution_recharge": "1️⃣ قم بشحن رصيدك.",
    "transfer_solution_contact_support": "2️⃣ أو تواصل مع الدعم عبر الزر: 💬",
    "transfer_initial_prompt": "💰 رصيدك الحالي: <b>{balance} {currency}</b>\n\n🔁 <b>تحويل الرصيد</b>",
    "transfer_format_instruction": "📥 أرسل المعرف والمبلغ بالشكل التالي:",
    "transfer_example": "<code>123456789 20</code>",
    "transfer_id_explanation": "✅ <b>123456789</b>: معرف المستخدم",
    "transfer_amount_explanation": "✅ <b>20</b>: المبلغ المطلوب تحويله",
    "cancel_button": "❌ إلغاء", # هذا المفتاح عام، وربما كان موجوداً سابقاً
    "cancel_button_text": "❌ إلغاء", # **تمت إضافة هذا السطر**

    "transfer_invalid_format_error": "❌ الصيغة غير صحيحة. استخدم:\n<code>123456789 20</code>",
    "transfer_invalid_id_or_amount": "❌ تأكد من أن المعرف والمبلغ أرقام صحيحة.",
    "transfer_amount_must_be_positive": "❌ المبلغ يجب أن يكون أكبر من صفر.",
    "insufficient_balance_for_transfer": "❌ رصيدك غير كافٍ لإتمام التحويل المطلوب.\nرصيدك الحالي: {current_balance} {currency}\nالمطلوب: {required_amount} {currency}",

    "confirm_transfer_title": "🔁 <b>تأكيد تحويل الرصيد</b>",
    "transfer_amount_confirm": "✅ سيتم تحويل: <b>{amount} {currency}</b>",
    "transfer_target_id_confirm": "👤 إلى معرف: <code>{target_id}</code>",
    "transfer_fee_confirm": "💸 عمولة التحويل: <b>{fee} {currency}</b>",
    "transfer_total_deduction_confirm": "💰 إجمالي الخصم من رصيدك: <b>{total_deduction} {currency}</b>",
    "transfer_confirmation_warning": "⚠️ يرجى التأكد من صحة المعرف. لا يمكن التراجع عن هذه العملية.",
    "confirm_transfer_button": "✅ تأكيد التحويل",

    "transfer_expired_or_cancelled": "❌ انتهت صلاحية عملية التحويل أو تم إلغاؤها.",
    "transfer_details_missing": "❌ بيانات التحويل غير موجودة. يرجى البدء من جديد.",
    "insufficient_balance_after_check": "❌ عذراً، رصيدك أصبح غير كافٍ ({current_balance} {currency}) لإتمام التحويل المطلوب ({required_amount} {currency}).\nيرجى شحن رصيدك أو التواصل مع الدعم.",
    "transfer_successful_message": "✅ تم تحويل <b>{amount} {currency}</b> إلى المستخدم <b>{target_id}</b>.\n💸 تم خصم عمولة <b>{fee} {currency}</b>.\n💰 رصيدك الجديد: <b>{new_balance} {currency}</b>",
    "transfer_unexpected_error": "❌ حدث خطأ غير متوقع أثناء عملية التحويل بعد التأكيد. يرجى التواصل مع الدعم.",
    "transfer_cancelled_message": "❌ تم إلغاء عملية التحويل.",


    # =========================================================================
    #  Transfer Logs (سجل التحويلات) - Admin Only
    # =========================================================================
    "no_permission_alert": "❌ لا تملك صلاحية الوصول لهذا السجل.",
    "no_transfers_yet": "📭 لا يوجد أي تحويلات حتى الآن.",
    "recent_transfers_title": "<b>📊 آخر التحويلات بين المستخدمين:</b>",
    "transfer_log_entry": "🔁 <b>{sender_id}</b> ← <b>{receiver_id}</b>\n💸 المبلغ: <b>{amount} {currency}</b> | العمولة: <b>{fee} {currency}</b>\n📅 التاريخ: {date}\n— — — — — —",
    "clear_all_transfers_button": "🗑️ حذف الكل",
    "unauthorized_alert": "❌ غير مصرح لك.",
    "confirm_clear_transfers_message": "⚠️ هل أنت متأكد من حذف جميع سجل التحويلات؟ لا يمكن التراجع.\n\nاضغط للتأكيد:",
    "yes_delete_button": "✅ نعم، احذف",
    "transfers_cleared_success": "✅ تم حذف جميع سجل التحويلات.",


    # =========================================================================
    #  Buy Number (شراء الأرقام)
    # =========================================================================
    "choose_platform_to_use_number": "اختر المنصة التي تريد استخدام الرقم فيها:",
    "platform_selection_message": "🧭 أنت الآن في قسم: {platform}\nاختر نوع الرقم الذي ترغب به:",
    "country_selection_message": "🌍 اختر الدولة التي تريد شراء رقم {platform} منها:",
    "most_available_button": "🎯 الأكثر توفراً ({platform})",
    "random_country_button": "🚀 دولة عشوائية ({platform})",
    "region_arab": "🌍 العرب",
    "region_africa": "🌍 أفريقيا",
    "region_asia": "🌍 آسيا",
    "region_europe": "🌍 أوروبا",
    "region_america": "🌍 أمريكا",
    "region_australia": "🌍 أستراليا",
    "no_categories_available": "لا توجد فئات متاحة حالياً.",
    "no_countries_available": "لا توجد دول متاحة حالياً.",

    # Buy Number - Server & Purchase Details
    "server_button_label": "{emoji} {server_name} - 💰 {price} {currency} ({quantity} {available_text})",
    "available_quantity": "متاح",
    "add_to_favorites_button": "⭐️ أضف إلى المفضلة",
    "no_servers_available": "❗ لا توجد سيرفرات متاحة حاليًا لهذه الدولة أو المنصة.",
    "insufficient_balance_for_country": "❌ رصيدك غير كافٍ لشراء أي رقم من هذه السيرفرات.\nرصيدك الحالي: {balance} {currency}",
    "balance_and_server_count": "✅ رصيدك الحالي: {balance} {currency}\nعدد السيرفرات المتوفرة: {server_count}",
    "choose_server_prompt": "اختر السيرفر الذي ترغب بتجربته:",
    "server_not_found_message": "⚠️ لم يتم العثور على السيرفر المطلوب.",
    "no_numbers_available_server": "❌ عذراً، لا توجد أرقام متاحة حالياً في سيرفر <b>{server_name}</b> لـ <b>{platform}</b> في <b>{country_code}</b>.\n💰 رصيدك الحالي: {balance} {currency}",
    "insufficient_balance_recharge_prompt": "❌ رصيدك الحالي ({current_balance} {currency}) غير كافٍ لشراء هذا الرقم الذي يكلف {price} {currency}. يرجى شحن رصيدك.\n👇 يمكنك شحن رصيدك الآن:",
    "request_code_button": "💬 طلب الكود",
    "cancel_number_button": "❌ إلغاء الرقم",
    "purchase_success_message": "✅ <b>تم شراء الرقم بنجاح!</b>\n\n📱 <b>التطبيق:</b> {platform}\n🌍 <b>الدولة:</b> {country}\n💾 <b>السيرفر:</b> {server_name}\n💰 <b>السعر:</b> {price} {currency}\n🔢 <b>الرقم الخاص بك:</b> <code>{fake_number}</code>",
    "waiting_for_code_message": "⏳ <i>في انتظار الكود...</i>",
    "current_balance_info": "💡 رصيدك الحالي: {balance} {currency}",
    "no_numbers_available_platform": "❌ لا توجد أرقام متوفرة حالياً لهذه المنصة.",
    "no_numbers_available_random_country": "❌ عذراً، لا توجد أرقام متوفرة في الدولة العشوائية المختارة حالياً. يرجى المحاولة مرة أخرى.",
    "random_country_selected": "🎲 تم اختيار دولة عشوائية: {country_name}",
    "most_available_countries_message": "📦 الدول المتوفرة حالياً لـ {platform}:",
    "unrecognized_platform": "❌ لم يتم التعرف على المنصة.",
    "platform_whatsapp_text_input_key": "واتساب",
    "platform_telegram_text_input_key": "تليجرام",
    "no_platforms_available": "❌ لا توجد منصات متاحة حالياً بأي أرقام متوفرة.",
    "platform_country_count": "✅ {platform} - {count} دولة",
    "available_platforms_title": "📲 <b>المنصات المتاحة الآن:</b>",
    "choose_platform_prompt": "اختر المنصة لرؤية الأرقام المتوفرة:",
    "no_ready_numbers_available": "❌ لا توجد أرقام فورية جاهزة حالياً.",
    "ready_number_button_label": "{flag} {country_name} - {platform} 💰 {price} {currency} ({quantity} {available_text})",
    "ready_numbers_title": "⚡ <b>أرقام فورية جاهزة:</b>",
    "choose_number_prompt": "اختر رقمًا للشراء الفوري:",

    # Purchase Status & OTP
    "purchase_id": "معرف الشراء: {purchase_id}",
    "otp_number": "الرقم الخاص بك: {phone_number}\nكود التفعيل: {otp_code}",
    "waiting_for_otp": "جارٍ انتظار كود التفعيل... قد يستغرق الأمر بعض الوقت. يرجى عدم إغلاق هذه المحادثة.",
    "no_otp_received": "لم يتم استلام كود تفعيل لهذا الرقم خلال الوقت المحدد. يرجى المحاولة مع رقم آخر.",
    "otp_received_success": "تم استلام كود التفعيل بنجاح! 🥳",
    "otp_received_failure": "فشل استلام كود التفعيل 😞",
    "purchase_not_found": "❌ لم يتم العثور على هذا الرقم في سجل مشترياتك.",
    "code_already_sent": "✅ الكود لهذا الرقم ({fake_number}) تم إرساله مسبقاً. الكود الوهمي: <code>{fake_code}</code>",
    "not_available_code_text": "غير متوفر",
    "number_cancelled_cannot_request_code": "❌ هذا الرقم ({fake_number}) تم إلغاؤه مسبقاً. لا يمكن طلب الكود.",
    "code_sent_success": "✅ تم إرسال الكود بنجاح!\n\n🔢 الرقم: <code>{fake_number}</code>\n🔑 الكود الخاص بك: <code>{fake_code}</code>",
    "test_code_note": "⏳ <i>ملاحظة: هذا كود وهمي لأغراض الاختبار.</i>",

    # Cancel Purchase
    "purchase_not_found_to_cancel": "❌ لم يتم العثور على هذا الرقم في سجل مشترياتك.",
    "cannot_cancel_after_code": "❌ لا يمكن إلغاء الرقم بعد الحصول على الكود.",
    "number_already_cancelled": "❌ هذا الرقم ({fake_number}) تم إلغاؤه مسبقاً.",
    "number_cancelled_success": "✅ تم إلغاء الرقم <code>{fake_number}</code> بنجاح.\n💰 تم استرداد <b>{price} {currency}</b> إلى رصيدك.",
    "new_balance_info": "💡 رصيدك الجديد: {balance} {currency}",

    # =========================================================================
    #  Offers
    # =========================================================================
    "offers_message": "لا توجد عروض حالياً. تابعنا للمزيد من التحديثات!",
    "offer_button_label": "{flag} {country_name} - {price}{currency} 🚀",
    "platform_offers_title": "🔥⚡ <b>عروض {platform}</b>",
    "your_balance_info": "💰 <b>رصيدك:</b> {balance} {currency}",
    "available_countries_title": "🌍 <b>الدول المتوفرة حالياً:</b>",
    "general_offers_title": "🎯 <b>عروض الأرقام المتوفرة:</b>",
    "general_offers_whatsapp_telegram": "✅ عروض واتساب وتليجرام في جميع الدول",
    "general_offers_best_prices": "✅ أقل الأسعار لأفضل جودة",
    "choose_platform_for_offers_prompt": "👇 اختر المنصة التي تريد رؤية عروضها:",
    "whatsapp_offers_button": "🎯 عروض واتساب",
    "telegram_offers_button": "🎯 عروض تليجرام",


    # =========================================================================
    #  Profile
    # =========================================================================
    "profile_title": "ملفك الشخصي 👤",
    "your_balance": "رصيدك: {balance} 💵",
    "your_role": "الدور: {role}",
    "admin_role": "مشرف",
    "normal_user_role": "مستخدم عادي",
    "view_purchases_button": "عرض مشترياتي 📜",
    "profile_welcome": "👤 <b>مرحباً بك</b>",
    "profile_archive_intro": "هذا هو الأرشيف الخاص بحسابك:",
    "profile_name": "📛 الاسم: <b>{fullname}</b>",
    "profile_username": "📎 المعرف: <b>{username}</b>",
    "profile_id": "🆔 ID: <code>{user_id}</code>",
    "profile_registration_date": "📆 تاريخ التسجيل: {date}",
    "profile_current_balance": "💰 الرصيد الحالي: <b>{balance} {currency}</b>",
    "profile_total_orders": "📦 عدد الطلبات: <b>{total_orders}</b>",
    "profile_total_spent": "💸 الرصيد المستخدم: <b>{total_spent} {currency}</b>",
    "my_purchases_button": "🧾 صندوق مشترياتي",


    # =========================================================================
    #  My Purchases
    # =========================================================================
    "no_purchases_found": "🗃 لا توجد مشتريات محفوظة لحسابك.",
    "purchase_history_title": "📦 <b>سجل مشترياتك</b>:",
    "purchase_item_format": "• {platform} - {country_name} - {price} {currency}\n🕓 {date}",


    # =========================================================================
    #  Favorites
    # =========================================================================
    "favorites_title": "أرقامك المفضلة ❤️",
    "no_favorites": "ليس لديك أي أرقام مفضلة بعد.",
    "add_favorite_prompt": "أدخل معرف الدولة والفئة التي ترغب في إضافتها إلى المفضلة (مثال: US, WhatsApp):",
    "favorite_added": "تمت إضافة {country_name} - {category_name} إلى مفضلتك.",
    "favorite_already_exists": "{country_name} - {category_name} موجودة بالفعل في مفضلتك.",
    "remove_favorite_prompt": "اختر المفضلة التي تريد إزالتها:",
    "favorite_removed": "تمت إزالة المفضلة بنجاح.",
    "favorite_not_found": "المفضلة غير موجودة.",
    "no_favorites_yet": "⭐️ لا توجد أرقام مفضلة محفوظة لديك حالياً.",
    "favorites_list_title": "⭐️ <b>قائمة المفضلة الخاصة بك:</b>",
    "invalid_format_error": "❌ تنسيق غير صالح.",
    "favorite_entry_format": "{flag} {platform} - {country_name}",
    "favorite_added_success": "✅ تم إضافة الدولة إلى المفضلة.",
    "favorite_already_exists": "ℹ️ هذه الدولة موجودة مسبقاً في مفضلتك.",


    # =========================================================================
    #  Earn Credit / Referral
    # =========================================================================
    "earn_credit_message": "ادعُ أصدقاءك وانضم إلى برنامج الإحالة الخاص بنا!\nعندما يسجل صديقك باستخدام رابط الإحالة الخاص بك ويقوم بعملية شراء، ستحصل على نسبة من مشترياته كعمولة.",
    "your_referral_link": "رابط الإحالة الخاص بك: {referral_link}",
    "how_referral_works": "كيف يعمل نظام الإحالة؟\n1. شارك الرابط مع أصدقائك.\n2. عندما يقوم صديقك بالتسجيل والشراء، ستحصل على {commission_percentage}% من مشترياته.",
    "your_referrals_count": "عدد المدعوين: {count}",
    "view_referral_details_button": "تفاصيل الإحالات 📊",
    "earn_credit_title": "🎁 <b>اربح رصيد مجانًا!</b>",
    "earn_credit_description": "قم بدعوة أصدقائك باستخدام كود الإحالة الخاص بك، وكل من يسجّل عبر كودك ستحصل على رصيد تلقائيًا 💸",
    "your_referral_code": "🔗 <b>كودك:</b> <code>{referral_code}</code>",
    "your_reward": "💰 <b>مكافأتك:</b> {amount} {currency} عن كل صديق يستخدم كودك للتسجيل",
    "more_referrals_more_credit": "👥 كلما زاد عدد المدعوين، زاد رصيدك! شارك كودك في المجموعات والمنصات 👇",
    "copy_referral_code_button": "📤 نسخ كود الإحالة",
    "no_referrals_yet": "🚫 لا يوجد مدعوون حتى الآن.",
    "referrals_list_title": "📊 <b>المدعوون عبر كودك:</b>",
    "referral_entry": "👤 {name} — 🗓️ {joined_date}",
    "view_referrals_button": "عرض المدعوين 📊", # **تمت إضافة هذا السطر**


    # =========================================================================
    #  Agent Program
    # =========================================================================
    "agent_program_title": "🤝 <b>فرصتك لتكون وكيلًا معتمدًا لدينا!</b>",
    "agent_benefits_title": "✅ <b>مميزات الوكلاء:</b>",
    "agent_benefit_1": "• تسعيرات حصرية أقل من المستخدم العادي.",
    "agent_benefit_2": "• لوحة تحكم متقدمة لمتابعة المستخدمين.",
    "agent_benefit_3": "• ربح تلقائي من عمليات عملائك.",
    "agent_benefit_4": "• دعم فني مباشر وأولوية في الرد.",
    "agent_profit_example_title": "💼 <b>مثال على الربح:</b>",
    "agent_profit_example_scenario": "إذا أشرف الوكيل على 10 مستخدمين، وكل واحد استخدم رصيدًا بقيمة 50 {currency}:",
    "agent_monthly_profit": "🪙 <b>الربح الشهري:</b> {profit} {currency} (نسبة {commission_percentage}%)",
    "agent_terms_title": "📌 <b>الشروط:</b>",
    "agent_term_1": "• أن يكون لديك مستخدمين حقيقيين.",
    "agent_term_2": "• الالتزام بشروط الاستخدام.",
    "agent_call_to_action": "إذا كنت مهتمًا، اضغط على الزر أدناه وسنتواصل معك.",
    "send_agent_request_button": "📩 إرسال طلب الانضمام",
    "new_agent_request_title": "📬 <b>طلب وكيل جديد</b>",
    "agent_request_name": "👤 الاسم: {full_name}",
    "agent_request_username": "🆔 المعرف: @{username}",
    "agent_request_id": "🆔 ID: <code>{user_id}</code>",
    "agent_request_sent_success": "✅ تم إرسال طلبك إلى الإدارة بنجاح.",
    "agent_request_review_notice": "📌 سنقوم بمراجعة الطلب والتواصل معك قريبًا بإذن الله.",


    # =========================================================================
    #  Admin Panel
    # =========================================================================
    "admin_panel_title": "لوحة تحكم المشرف ⚙️",
    "not_admin_message": "عذراً، أنت لست مشرفاً.",
    "users_management_button": "إدارة المستخدمين",
    "servers_management_button": "إدارة السيرفرات",
    "add_balance_button": "إضافة رصيد لمستخدم",
    "subtract_balance_button": "خصم رصيد من مستخدم",
    "change_user_role_button": "تغيير دور المستخدم",
    "broadcast_message_button": "إرسال رسالة جماعية",
    "get_user_info_button": "معلومات المستخدم",
    "enter_user_id_for_action": "أدخل معرف المستخدم ({action_type}):",
    "enter_amount_for_balance_change": "أدخل المبلغ (بالدولار):",
    "user_balance_updated": "تم تحديث رصيد المستخدم {user_id} إلى {new_balance}.",
    "user_role_updated": "تم تحديث دور المستخدم {user_id} إلى {new_role}.",
    "user_not_found_in_db": "المستخدم غير موجود في قاعدة البيانات.",
    "invalid_role": "دور غير صالح. يجب أن يكون 'admin' أو 'user'.",
    "user_fallback_name": "مستخدم {user_id}",
    "no_matching_users": "❌ لا يوجد مستخدمون مطابقون.",
    "admin_user_management_title": "<b>👥 إدارة المستخدمين</b>",
    "banned_status": "🚫 محظور",
    "active_status": "✅ نشط",
    "admin_user_info_line": "👤 <b>{name}</b> | 🆔 {user_id}\n💰 {balance} {currency} | {status}",
    "edit_user_button": "✏️ تعديل",
    "ban_button": "✅ فك الحظر",
    "unban_button": "🚫 حظر",
    "delete_user_button": "🗑 حذف",
    "not_admin_search_permission": "❌ ليس لديك صلاحية للبحث في قائمة المستخدمين.",
    "enter_new_balance": "✏️ أرسل الآن الرصيد الجديد للمستخدم\n🆔 ID: <code>{user_id}</code>",
    "invalid_balance_input": "❌ الرجاء إدخال رقم صالح للرصيد.",
    "balance_conversion_error": "❌ حدث خطأ في تحويل الرصيد. الرجاء إدخال رقم.",
    "user_not_found_for_edit": "❌ لم يتم العثور على المستخدم المطلوب تعديل رصيده.",
    "user_status_updated": "✅ تم تحديث حالة المستخدم {user_id} إلى: {new_status}.",
    "user_not_found": "❌ المستخدم غير موجود.",
    "yes_delete_button": "✅ نعم، احذف",
    "confirm_delete_user_message": "⚠️ هل أنت متأكد من حذف المستخدم <code>{user_id}</code>؟ لا يمكن التراجع عن هذا الإجراء.",
    "user_deleted_success": "🗑️ تم حذف المستخدم <code>{user_id}</code> بنجاح.",
    "unbanned_text": "مفعل", # **تمت إضافة هذا السطر**
    "banned_text": "محظور",   # **تمت إضافة هذا السطر**


    # =========================================================================
    #  Quick Search (البحث السريع)
    # =========================================================================
    "quick_search_prompt": "🌹 مرحباً 😊\nDr\\Ramzi\n\n— قم بإرسال اسم الدولة (بالعربية أو الإنجليزية أو بالرمز 🇸🇦) للبحث عنها:\n\n──────────────",
    "country_not_found": "❌ لم يتم العثور على هذه الدولة. تأكد من كتابة الاسم بشكل صحيح.",
    "no_servers_available_country_quick_search": "❗ لا توجد سيرفرات متاحة حاليًا لهذه الدولة.",
    "quick_search_results": "📍 <b>الدولة:</b> {country_name}\n📱 <b>المنصة:</b> {platform}\n💰 <b>رصيدك:</b> {balance} {currency}",
    "choose_server_prompt": "اختر السيرفر الذي ترغب بتجربته:",


    # =========================================================================
    #  Language Selection (اختيار اللغة)
    # =========================================================================
    "select_your_language": "🌐 اختر اللغة التي تفضل استخدامها في البوت:\n\nChoose the bot language:",
    "language_arabic_button": "العربية",
    "language_english_button": "English",
    "language_changed_to_arabic": "✅ تم تعيين اللغة إلى العربية.",
    "language_changed_to_english": "✅ Language set to English.",


    # =========================================================================
    #  Help & Support (المساعدة والدعم)
    # =========================================================================
    "help_message": "مرحباً بك في قسم المساعدة!\n\nلشراء رقم، اضغط على 'شراء رقم' واتبع التعليمات. يمكنك شحن رصيدك عن طريق التواصل مع المشرف. للمزيد من المساعدة، يرجى التواصل مع الدعم الفني.",
    "help_menu_welcome_message": "🌹 مرحباً Dr\\Ramzi 😊\n⌁─━─━ ({bot_name}) ─━─━⌁",
    "contact_support_button": "📩 - التواصل مع الدعم",
    "usage_guide_button": "📄 - شرح الاستخدام",
    "faq_button": "❓ - الأسئلة الشائعة",

    "usage_guide_title": "📘 <b>شرح استخدام البوت</b>",
    "usage_step_1": "1️⃣ اضغط على زر 💎 شراء رقم في القائمة الرئيسية.",
    "usage_step_2": "2️⃣ اختر المنصة التي ترغب بتفعيل الرقم فيها (واتساب، تليجرام...)",
    "usage_step_3": "3️⃣ اختر الدولة ثم السيرفر المناسب حسب السعر والجودة.",
    "usage_step_4": "4️⃣ سيتم خصم الرصيد تلقائيًا وعرض الرقم لك.",
    "usage_step_5": "5️⃣ تابع الكود الذي يصلك مباشرة داخل البوت.",
    "usage_notes_title": "📌 ملاحظات:",
    "usage_note_1": "- تأكد من شحن رصيدك قبل الشراء.",
    "usage_note_2": "- الأسعار تختلف حسب السيرفر والدولة.",
    "usage_note_3": "- بعض الأرقام صالحة لفترة محدودة.",
    "usage_problem_contact_support": "⚠️ في حال واجهتك مشكلة تواصل مع الدعم.",
    "back_to_menu_note": "🔙 يمكنك العودة من الزر التالي.",

    "contact_support_title": "📞 <b>التواصل مع الدعم</b>",
    "contact_support_prompt": "لأي استفسار أو مشكلة:",
    "contact_support_link": "🔗 <a href='{support_link}'>{support_link}</a>",
    "contact_support_hours": "🕐 متاح من الساعة 10 صباحًا حتى 12 منتصف الليل.",
    "contact_support_tip": "📌 أرسل استفسارك مع صورة/شرح إن وُجد.",

    "faq_title": "❓ <b>الأسئلة الشائعة</b>",
    "faq_q1": "🟢 <b>هل الرقم يُستخدم مرة واحدة؟</b>",
    "faq_a1": "نعم، كل رقم يُستخدم لتفعيل حساب واحد فقط.",
    "faq_q2": "🟢 <b>ماذا لو لم يصلني الكود؟</b>",
    "faq_a2": "حاول مرة أخرى أو استخدم سيرفر مختلف.",
    "faq_q3": "🟢 <b>هل يمكن استرجاع الرصيد؟</b>",
    "faq_a3": "فقط في حال فشل العملية ولم يُستخدم الرقم.",
    "faq_more_questions": "📩 لمزيد من الأسئلة تواصل مع الدعم.",


    # =========================================================================
    #  Country Names (أسماء الدول)
    # =========================================================================
    "country_name_sa": "السعودية",
    "country_name_eg": "مصر",
    "country_name_ye": "اليمن",
    "country_name_dz": "الجزائر",
    "country_name_ma": "المغرب",
    "country_name_iq": "العراق",
    "country_name_sd": "السودان",
    "country_name_sy": "سوريا",
    "country_name_kw": "الكويت",
    "country_name_qa": "قطر",
    "country_name_ae": "الإمارات",
    "country_name_jo": "الأردن",
    "country_name_lb": "لبنان",
    "country_name_tn": "تونس",
    "country_name_ng": "نيجيريا",
    "country_name_ke": "كينيا",
    "country_name_gh": "غانا",
    "country_name_za": "جنوب أفريقيا",
    "country_name_et": "إثيوبيا",
    "country_name_tz": "تنزانيا",
    "country_name_in": "الهند",
    "country_name_pk": "باكستان",
    "country_name_id": "إندونيسيا",
    "country_name_th": "تايلاند",
    "country_name_my": "ماليزيا",
    "country_name_ph": "الفلبين",
    "country_name_uk": "بريطانيا",
    "country_name_fr": "فرنسا",
    "country_name_de": "ألمانيا",
    "country_name_es": "إسبانيا",
    "country_name_it": "إيطاليا",
    "country_name_nl": "هولندا",
    "country_name_us": "أمريكا",
    "country_name_br": "البرازيل",
    "country_name_ca": "كندا",
    "country_name_mx": "المكسيك",
    "country_name_co": "كولومبيا",
    "country_name_ar": "الأرجنتين",
    "country_name_au": "أستراليا",
    "country_name_nz": "نيوزيلندا",

    "start_message": "مرحباً بك في بوت الأرقام الوهمية! اختر لغتك المفضلة:",
    "choose_language": "الرجاء اختيار لغتك المفضلة 🌐:",
    # ... (المزيد من الرسائل)
    "category_menu_message": "الرجاء اختيار الفئة:",
    "select_country_message": "الرجاء اختيار الدولة:",
    "no_servers_available_for_country": "عذراً، لا توجد سيرفرات متاحة لهذه الدولة حالياً. الرجاء المحاولة بدولة أخرى.",
    "select_server_message": "الرجاء اختيار السيرفر:",
    "balance_insufficient": "رصيدك غير كافٍ لإتمام هذه العملية. رصيدك الحالي: {balance} {currency}. يرجى الشحن والمحاولة مرة أخرى.",
    "purchase_success": "تم شراء الرقم بنجاح!\nالرقم: <code>{number}</code>\nالسعر: {price} {currency}\nملاحظة: إذا لم يصل الكود، يمكنك طلب رقم آخر أو التواصل مع الدعم.",
    "error_processing_request_user": "حدث خطأ أثناء معالجة طلبك. الرجاء المحاولة مرة أخرى لاحقاً أو التواصل مع الدعم.",
    "no_numbers_available_in_server": "عذراً، لا توجد أرقام متاحة في السيرفر المختار حالياً. يرجى اختيار سيرفر آخر أو دولة أخرى.",
    "failed_to_get_number": "عذراً، فشل الحصول على رقم من مزود الخدمة. يرجى المحاولة مرة أخرى.",
    "number_expired_or_no_code": "لم يتم استلام الكود لهذا الرقم أو انتهت صلاحيته. يرجى تجربة رقم آخر أو التواصل مع الدعم.",
    "processing_request": "جارٍ معالجة طلبك... الرجاء الانتظار قليلاً.",
    "fetching_data": "جارٍ جلب البيانات... الرجاء الانتظار.",
    "request_cancelled": "تم إلغاء العملية.",
    "not_allowed_in_channel": "عذراً، لا يُسمح باستخدام البوت في هذه القناة. يرجى استخدامه في الدردشة الخاصة.",
    "offers_title": "✨ العروض المتاحة ✨",
    "no_offers_available": "عذراً، لا توجد عروض متاحة حالياً.",
    "available_offers_list": "قائمة العروض المتاحة:",
    "offer_entry": "- {platform} - {country} - {server_name}: {price} {currency} ({quantity} متاح)",
    "your_balance_is": "رصيدك الحالي: {balance} {currency}.",
    "all_offers_button": "جميع العروض",
    "whatsapp_offers_button": "عروض واتساب",
    "telegram_offers_button": "عروض تليجرام",
    "general_offers_title": "🎁 عروض الأرقام المميزة 🎁",
    "general_offers_whatsapp_telegram": "تصفح أفضل عروض أرقام الواتساب والتليجرام بأسعار لا تقبل المنافسة.",
    "general_offers_best_prices": "نقدم لك أفضل الأسعار على الأرقام المؤقتة المتاحة حالياً.",
    "choose_platform_for_offers_prompt": "الرجاء اختيار المنصة لعرض العروض:",
    "offer_button_label_new": "{flag} {country_name} - {platform} - {price} {currency} ({quantity} متاح)",
    "view_more_offers_button": "عرض المزيد من العروض...",

}