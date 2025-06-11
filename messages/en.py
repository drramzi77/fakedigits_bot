# messages/english.py

messages = {
    "language_selected_success": "✅ Language selected successfully.\n\nPress the button below to start.",
    "start_using_bot": "🚀 Start",
    # =========================================================================
    #  General Messages
    # =========================================================================
    "welcome_message": "Welcome to FakeDigits Bot! 🤖\n\nThis bot provides you with one-time virtual numbers for activating your accounts on various applications and services.",
    "invalid_command": "Invalid command. Please use correct commands.",
    "error_processing_request": "An error occurred while processing your request. Please try again later.",
    "choose_option": "Choose an option:", # used in main_menu
    "unrecognized_text_input": "👋 Sorry, I didn't understand your request. Please use available commands or buttons.",
    "price_currency": "SAR", # Default currency
    "not_available": "N/A", # Used for username or unavailable info
    "unknown_value_char": "❓", # Used for unavailable date/platform/country fields


    # =========================================================================
    #  Main Dashboard & Menu Buttons
    # =========================================================================
    "main_menu_title": "Main Menu 🏠", # Dashboard title (if used somewhere)
    "buy_number_button": "Buy Number 🛒",
    "profile_button": "My Profile 👤",
    "offers_button": "Offers 🎁",
    "favorites_button": "Favorites ❤️",
    "earn_credit_button": "Earn Credit 💰",
    "transfer_credit_button": "Transfer Credit 💸",
    "help_button": "Help ❓",
    "language_button": "English🌐العربية",
    "admin_panel_button": "Admin Panel ⚙️", # (will be activated later)
    "available_platforms": "Available Platforms", # Button on dashboard
    "quick_search": "Quick Search 🔎", # Button on dashboard
    "ready_numbers": "Ready Numbers 🚀", # Button on dashboard
    "channel_button": "Bot Channel 📢", # Button on dashboard
    "become_agent_button": "Become an Agent 🤝", # Button on dashboard
    "view_transfer_logs": "View Transfer Logs 📜", # Button for admins on dashboard
    "admin_users": "Admin Users 🛠️", # Button for admins on dashboard
    "back_button_text": "🔙 Back", # General back button text
    "back_to_dashboard_button_text": "🔙 Back to Main Dashboard", # Back button from app selection to main dashboard


    # =========================================================================
    #  Dashboard Display Messages
    # =========================================================================
    "dashboard_welcome": "👋 Welcome, <b>{display_name}</b>, to your main dashboard! 😊",
    "dashboard_id": "🆔 <b>ID:</b> <code>{user_id}</code>",
    # # تم التعديل على هذا السطر (إضافة {currency})
    "dashboard_balance": "💰 <b>Balance:</b> {balance} {currency}",
    "dashboard_channel_promo": "📢 Subscribe to {channel_link}",
    "dashboard_choose_option": "🔽 Choose from the following menu:",


    # =========================================================================
    #  Subscription Check
    # =========================================================================
    "check_subscription_button": "🔁 Check Subscription",
    "subscribe_to_channel": "Subscribe to", # used with channel name
    "subscribed_success": "✅ Subscription verified.\nUse /plus to proceed.",
    "not_subscribed_channel": "📢 To ensure you get premium numbers first, please subscribe to the bot's official channel.\n\n🔒 Subscription is required to activate bot services and full access.\n👇 Subscribe then click 'Check Subscription' below: {channel_link}",
    "not_subscribed_channel_retry": "❗ We couldn't verify your subscription yet.\n✅ Make sure you have subscribed to the required channel.\n🔄 After subscribing, click the button below to re-verify: {channel_link}",


    # =========================================================================
    #  Error Handling Messages
    # =========================================================================
    "contact_support_button_error": "💬 Contact Support",
    "back_to_main_menu_error": "🔙 Back to Main Menu", # (not used directly, replaced by back_to_dashboard_button_text)
    "error_processing_request_user": "❌ Sorry, an unexpected error occurred! 😔\nAdmins have been notified and we'll fix it as soon as possible.\n\n❓ You can contact support or return to the main menu.",
    "bot_error_alert": "Bot Error!",
    "update_info": "Update",
    "error_details": "Error",


    # =========================================================================
    #  Balance & Recharge
    # =========================================================================
    "recharge_balance_button": "Recharge Balance 💳", # Button on dashboard
    "withdraw_balance_button": "Withdraw Balance 🏧", # **تمت إضافة هذا السطر لحل المشكلة السابقة**
    "recharge_from_admin_button": "🧑‍💼 Recharge from Admin",
    "recharge_welcome_message": "🟢 <b>Welcome to the Balance Recharge System!</b>\nYou can recharge your bot account using one of the following methods:",
    "available_payment_methods": "💸 <b>Available Payment Methods:</b>",
    "payment_method_kareem": "🔹 Kareem Eidaa / Al-Najm",
    "payment_method_vodafone": "🔹 Vodafone Cash / Direct Transfer",
    "payment_method_zain": "🔹 Zain Cash / Asia Hawala",
    "payment_method_crypto": "🔹 Cryptocurrencies: USDT / BTC / Payeer",
    "payment_method_paypal": "🔹 PayPal",
    "payment_method_other": "🔹 Any other agreed method",
    "send_proof_message": "📌 <i>Please send payment proof to the admin with your ID:</i>\n<code>{user_id}</code>",
    "contact_admin_message": "📞 <b>To contact Admin:</b> {admin_username}", # For the admin to be contacted
    "press_button_to_proceed": "📍 <b>Click one of the buttons below to proceed 👇</b>",
    "recharge_admin_title": "👨‍💼 <b>Recharge from Admin</b>",
    "contact_dev_message": "Please contact the developer directly via the following link:\n🔗 <a href='{dev_link}'>{dev_link}</a>",
    "send_proof_manual_recharge": "📤 Send him payment proof + your bot ID, and your balance will be manually recharged within minutes.",
    "back_to_previous_menu": "🔙 You can go back using the button below.",
    "check_balance_button": "💰 My Balance", # Button to check balance only (in main_menu_kb)
    "my_balance_is": "💰 Your current balance is: {balance} {currency}", # /balance command for user itself
    "my_balance_info": "👤 User: {name}\n🆔 ID: <code>{user_id}</code>\n💰 Current Balance: {balance} {currency}", # /balance command for user itself (detailed format)
    "user_balance_info": "👤 User: {name}\n🆔 ID: <code>{user_id}</code>\n💰 Balance: {balance} {currency}", # /balance command for admin to query other users
    "unknown_user_in_group": "Unknown (perhaps not in group)",
    "invalid_user_id_balance_command": "❌ Enter a valid ID like: /balance 123456789",
    "no_permission_to_view_others_balance": "❌ You do not have permission to view others' balances.",
    "admin_only_command": "❌ This command is for administrators only.", # For /add_balance and /deduct_balance commands
    "add_balance_invalid_amount_format": "❌ Incorrect amount format. Use: /add_balance <user_id> <amount>",
    "add_balance_invalid_amount": "❌ Enter a valid amount like: /add_balance 200",
    "add_balance_invalid_format": "❌ Incorrect format. Use: /add_balance <user_id> <amount> or /add_balance <amount>",
    "amount_must_be_positive": "❌ Amount must be greater than zero.",
    "invalid_user_id_after_clean": "❌ User ID is invalid or empty after cleaning.",
    "user_id_conversion_error": "❌ Error converting user ID. Please ensure its validity.",
    "balance_added_success": "✅ {amount} {currency} added to user {user_id}'s balance.",
    "error_updating_balance": "❌ An error occurred while updating the balance. Please check bot logs.",
    "deduct_balance_invalid_format": "❌ Format: /deduct_balance <user_id> <amount>",
    "deduct_balance_invalid_amount": "❌ Enter a valid amount.",
    "insufficient_balance_deduct": "❌ Insufficient balance. Current balance: {current_balance} {currency}",
    "balance_deducted_success": "✅ {amount} {currency} deducted from user {user_id}.",
    "current_balance_prompt": "💰 Your current balance: {balance} {currency}", # **تمت إضافة هذا السطر**
    "balance_update_success": "✅ User {user_id}'s balance updated to {new_balance} {currency}.", # **تمت إضافة هذا السطر**


    # =========================================================================
    #  Withdraw Balance
    # =========================================================================
    "withdraw_balance_button_profile": "🏧 Withdraw Balance", # Button on profile page
    "withdraw_request_title": "🏧 <b>Balance Withdrawal Request</b>",
    "withdraw_instructions": "To ensure quick processing of your request, please send transfer details in the following format:",
    "withdraw_full_name_field": "🔹 <b>Full Name:</b>",
    "withdraw_account_number_field": "🔹 <b>Account or Wallet Number:</b>",
    "withdraw_type_field": "🔹 <b>Transfer Type</b> (STC Pay / Bank / Remittance):",
    "withdraw_amount_field": "🔹 <b>Requested Amount:</b>",
    "withdraw_review_notice": "📌 <i>Your request will be reviewed within a maximum of 24 business hours.</i>",
    "withdraw_contact_admin_prompt": "📞 In case of any urgent issue or inquiry, you can directly contact the administration:",
    "contact_admin_button_withdraw": "📬 Contact Admin",


    # =========================================================================
    #  Transfer Credit
    # =========================================================================
    "transfer_successful": "Successfully transferred {amount} 💵 to user {receiver_id}.", # (old key, not used directly now)
    "transfer_received": "You have received a transfer of {amount} 💵 from user {sender_id}.", # (old key, not used directly now)
    "enter_transfer_amount": "Enter the amount you wish to transfer (in USD):", # (old key)
    "invalid_amount": "Invalid amount. Please enter a positive number.", # (old key)
    "enter_receiver_id": "Now, enter the recipient's User ID:", # (old key)
    "receiver_not_found": "Recipient user not found. Please verify the ID.", # (not used yet)
    "confirm_transfer": "Are you sure you want to transfer {amount} 💵 to user {receiver_id}?", # (old key)
    "contact_support_button_transfer": "💬 Contact Support", # Specific button for support in transfers

    "admin_transfer_warning": "⚠️ This option is for users only.\n🔋 To recharge a user's balance, use the dedicated section in the admin panel.",
    "transfer_balance_too_low": "❌ - You cannot transfer balance now.\n📊 - Your current balance: <b>{balance} {currency}</b>",
    "transfer_fee_info": "💸 - Transfer fee: <b>{fee_percentage}%</b>",
    "transfer_solution_prompt": "🔄 <b>What to do?</b>",
    "transfer_solution_recharge": "1️⃣ Recharge your balance.",
    "transfer_solution_contact_support": "2️⃣ Or contact support via the button: 💬",
    "transfer_initial_prompt": "💰 Your current balance: <b>{balance} {currency}</b>\n\n🔁 <b>Balance Transfer</b>",
    "transfer_format_instruction": "📥 Send the ID and amount in the following format:",
    "transfer_example": "<code>123456789 20</code>",
    "transfer_id_explanation": "✅ <b>123456789</b>: User ID",
    "transfer_amount_explanation": "✅ <b>20</b>: Amount to transfer",
    "cancel_button": "❌ Cancel", # General cancel button, might be used in other contexts as well
    "cancel_button_text": "❌ Cancel", # **تمت إضافة هذا السطر**

    "transfer_invalid_format_error": "❌ Incorrect format. Use:\n<code>123456789 20</code>",
    "transfer_invalid_id_or_amount": "❌ Make sure the ID and amount are valid numbers.",
    "cannot_transfer_to_self": "❌ You cannot transfer balance to yourself.",
    "transfer_amount_must_be_positive": "❌ Amount must be greater than zero.",
    "insufficient_balance_for_transfer": "❌ Your balance is insufficient for the requested transfer.\nYour current balance: {current_balance} {currency}\nRequired: {required_amount} {currency}",

    "confirm_transfer_title": "🔁 <b>Confirm Balance Transfer</b>",
    "transfer_amount_confirm": "✅ Will transfer: <b>{amount} {currency}</b>",
    "transfer_target_id_confirm": "👤 To ID: <code>{target_id}</code>",
    "transfer_fee_confirm": "💸 Transfer Fee: <b>{fee} {currency}</b>",
    "transfer_total_deduction_confirm": "💰 Total deduction from your balance: <b>{total_deduction} {currency}</b>",
    "transfer_confirmation_warning": "⚠️ Please verify the ID. This operation cannot be undone.",
    "confirm_transfer_button": "✅ Confirm Transfer",

    "transfer_expired_or_cancelled": "❌ Transfer operation expired or cancelled.",
    "transfer_details_missing": "❌ Transfer details are missing. Please start over.",
    "insufficient_balance_after_check": "❌ Sorry, your balance is now insufficient ({current_balance} {currency}) to complete the requested transfer ({required_amount} {currency}).\nPlease recharge your balance or contact support.",
    "transfer_successful_message": "✅ Successfully transferred <b>{amount} {currency}</b> to user <b>{target_id}</b>.\n💸 A fee of <b>{fee} {currency}</b> was deducted.\n💰 Your new balance: <b>{new_balance} {currency}</b>",
    "transfer_unexpected_error": "❌ An unexpected error occurred during the transfer after confirmation. Please contact support.",
    "transfer_cancelled_message": "❌ Transfer operation cancelled.",


    # =========================================================================
    #  Transfer Logs (Admin Only)
    # =========================================================================
    "no_permission_alert": "❌ You do not have permission to access this log.", # For admins only
    "no_transfers_yet": "📭 No transfers yet.",
    "recent_transfers_title": "<b>📊 Recent Transfers Between Users:</b>",
    "transfer_log_entry": "🔁 <b>{sender_id}</b> ← <b>{receiver_id}</b>\n💸 Amount: <b>{amount} {currency}</b> | Fee: <b>{fee} {currency}</b>\n📅 Date: {date}\n— — — — — —",
    "clear_all_transfers_button": "🗑️ Clear All",
    "unauthorized_alert": "❌ Unauthorized.", # For admins only
    "confirm_clear_transfers_message": "⚠️ Are you sure you want to delete all transfer logs? This action cannot be undone.\n\nClick to confirm:",
    "yes_delete_button": "✅ Yes, Delete",
    "transfers_cleared_success": "✅ All transfer logs have been deleted.",


    # =========================================================================
    #  Buy Number
    # =========================================================================
    "choose_platform_to_use_number": "Choose the platform you want to use the number for:",
    "platform_selection_message": "🧭 You are now in: {platform}\nChoose the number type you want:",
    "country_selection_message": "🌍 Select the country you want to buy a {platform} number from:",
    "most_available_button": "🎯 Most Available ({platform})",
    "random_country_button": "🚀 Random Country ({platform})",
    "region_arab": "🌍 Arabs",
    "region_africa": "🌍 Africa",
    "region_asia": "🌍 Asia",
    "region_europe": "🌍 Europe",
    "region_america": "🌍 America",
    "region_australia": "🌍 Australia",
    "no_categories_available": "No categories available at the moment.",
    "no_countries_available": "No countries available at the moment.",

    # Buy Number - Server & Purchase Details
    "server_button_label": "{emoji} {server_name} - 💰 {price} {currency} ({quantity} {available_text})",
    "available_quantity": "available",
    "add_to_favorites_button": "⭐️ Add to Favorites",
    "no_servers_available": "❗ No servers currently available for this country or platform.",
    "insufficient_balance_for_country": "❌ Your balance is insufficient to purchase any number from these servers.\nYour current balance: {balance} {currency}",
    "balance_and_server_count": "✅ Your current balance: {balance} {currency}\nAvailable servers count: {server_count}",
    "choose_server_prompt": "Choose the server you want to try:",
    "server_not_found_message": "⚠️ The requested server was not found.",
    "no_numbers_available_server": "❌ Sorry, no numbers are currently available in server <b>{server_name}</b> for <b>{platform}</b> in <b>{country_code}</b>.\n💰 Your current balance: {balance} {currency}",
    "insufficient_balance_recharge_prompt": "❌ Your current balance ({current_balance} {currency}) is insufficient to purchase this number costing {price} {currency}. Please recharge your balance.\n👇 You can recharge your balance now:",
    "request_code_button": "💬 Request Code",
    "cancel_number_button": "❌ Cancel Number",
    "purchase_success_message": "✅ <b>Number purchased successfully!</b>\n\n📱 <b>App:</b> {platform}\n🌍 <b>Country:</b> {country}\n💾 <b>Server:</b> {server_name}\n💰 <b>Price:</b> {price} {currency}\n🔢 <b>Your Number:</b> <code>{fake_number}</code>",
    "waiting_for_code_message": "⏳ <i>Waiting for code...</i>",
    "current_balance_info": "💡 Your current balance: {balance} {currency}",
    "no_numbers_available_platform": "❌ No numbers currently available for this platform.",
    "no_numbers_available_random_country": "❌ Sorry, no numbers are available in the randomly selected country at the moment. Please try again.",
    "random_country_selected": "🎲 Random country selected: {country_name}",
    "most_available_countries_message": "📦 Countries currently available for {platform}:",
    "unrecognized_platform": "❌ Platform not recognized.",
    "platform_whatsapp_text_input_key": "whatsapp",
    "platform_telegram_text_input_key": "telegram",
    "no_platforms_available": "❌ No platforms currently available with any numbers.",
    "platform_country_count": "✅ {platform} - {count} countries",
    "available_platforms_title": "📲 <b>Available Platforms:</b>",
    "choose_platform_prompt": "Choose the platform to see available numbers:",
    "no_ready_numbers_available": "❌ No instant numbers ready at the moment.",
    "ready_number_button_label": "{flag} {country_name} - {platform} 💰 {price} {currency} ({quantity} {available_text})",
    "ready_numbers_title": "⚡ <b>Instant Ready Numbers:</b>",
    "choose_number_prompt": "Choose a number for instant purchase:",

    # Purchase Status & OTP
    "purchase_id": "Purchase ID: {purchase_id}",
    "otp_number": "Your number: {phone_number}\nOTP Code: {otp_code}",
    "waiting_for_otp": "Waiting for OTP code... This might take some time. Please do not close this chat.",
    "no_otp_received": "No OTP code was received for this number within the specified time. Please try another number.",
    "otp_received_success": "OTP code received successfully! 🥳",
    "otp_received_failure": "Failed to receive OTP code 😞",
    "purchase_not_found": "❌ This number was not found in your purchase history.",
    "code_already_sent": "✅ Code for this number ({fake_number}) has already been sent. Virtual Code: <code>{fake_code}</code>",
    "not_available_code_text": "N/A",
    "number_cancelled_cannot_request_code": "❌ This number ({fake_number}) has been cancelled. Cannot request code.",
    "code_sent_success": "✅ Code sent successfully!\n\n🔢 Number: <code>{fake_number}</code>\n🔑 Your Code: <code>{fake_code}</code>",
    "test_code_note": "⏳ <i>Note: This is a virtual code for testing purposes.</i>",

    # Cancel Purchase
    "purchase_not_found_to_cancel": "❌ This number was not found in your purchase history.",
    "cannot_cancel_after_code": "❌ Cannot cancel the number after receiving the code.",
    "number_already_cancelled": "❌ This number ({fake_number}) has already been cancelled.",
    "number_cancelled_success": "✅ Number <code>{fake_number}</code> cancelled successfully.\n💰 <b>{price} {currency}</b> refunded to your balance.",
    "new_balance_info": "💡 Your new balance: {balance} {currency}",

    # =========================================================================
    #  Offers
    # =========================================================================
    "offers_message": "No offers available at the moment. Stay tuned for updates!",
    "offer_button_label": "{flag} {country_name} - {price}{currency} 🚀",
    "platform_offers_title": "🔥⚡ <b>{platform} Offers</b>",
    "your_balance_info": "💰 <b>Your Balance:</b> {balance} {currency}",
    "available_countries_title": "🌍 <b>Currently Available Countries:</b>",
    "general_offers_title": "🎯 <b>Available Number Offers:</b>",
    "general_offers_whatsapp_telegram": "✅ WhatsApp and Telegram offers in all countries",
    "general_offers_best_prices": "✅ Lowest prices for best quality",
    "choose_platform_for_offers_prompt": "👇 Choose the platform you want to see offers for:",
    "whatsapp_offers_button": "🎯 WhatsApp Offers",
    "telegram_offers_button": "🎯 Telegram Offers",


    # =========================================================================
    #  Profile
    # =========================================================================
    "profile_title": "Your Profile 👤",
    "your_balance": "Your balance: {balance} 💵",
    "your_role": "Role: {role}",
    "admin_role": "Admin",
    "normal_user_role": "Normal User",
    "view_purchases_button": "View My Purchases 📜",
    "profile_welcome": "👤 <b>Welcome</b>",
    "profile_archive_intro": "This is your account archive:",
    "profile_name": "📛 Name: <b>{fullname}</b>",
    "profile_username": "📎 Username: <b>{username}</b>",
    "profile_id": "🆔 ID: <code>{user_id}</code>",
    "profile_registration_date": "📆 Registration Date: {date}",
    "profile_current_balance": "💰 Current Balance: <b>{balance} {currency}</b>",
    "profile_total_orders": "📦 Total Orders: <b>{total_orders}</b>",
    "profile_total_spent": "💸 Total Spent: <b>{total_spent} {currency}</b>",
    "my_purchases_button": "🧾 My Purchases",


    # =========================================================================
    #  My Purchases
    # =========================================================================
    "no_purchases_found": "🗃 No purchases saved for your account.",
    "purchase_history_title": "📦 <b>Your Purchase History</b>:",
    "purchase_item_format": "• {platform} - {country_name} - {price} {currency}\n🕓 {date}",


    # =========================================================================
    #  Favorites
    # =========================================================================
    "favorites_title": "Your Favorites ❤️",
    "no_favorites": "You don't have any favorite numbers yet.",
    "add_favorite_prompt": "Enter the Country ID and Category ID you want to add to favorites (e.g., US, WhatsApp):",
    "favorite_added": "{country_name} - {category_name} added to your favorites.",
    "favorite_already_exists": "{country_name} - {category_name} already exists in your favorites.",
    "remove_favorite_prompt": "Select the favorite you want to remove:",
    "favorite_removed": "Favorite removed successfully.",
    "favorite_not_found": "Favorite not found.",
    "no_favorites_yet": "⭐️ You don't have any favorite numbers saved yet.",
    "favorites_list_title": "⭐️ <b>Your Favorites List:</b>",
    "invalid_format_error": "❌ Invalid format.",
    "favorite_entry_format": "{flag} {platform} - {country_name}",
    "favorite_added_success": "✅ Country added to favorites.",
    "favorite_already_exists": "ℹ️ This country is already in your favorites.",


    # =========================================================================
    #  Earn Credit / Referral
    # =========================================================================
    "earn_credit_message": "Invite your friends and join our referral program!\nWhen your friend signs up using your referral link and makes a purchase, you'll earn a percentage of their purchases as commission.",
    "your_referral_link": "Your referral link: {referral_link}",
    "how_referral_works": "How the referral system works?\n1. Share the link with your friends.\n2. When your friend signs up and makes a purchase, you'll get {commission_percentage}% of their purchases.",
    "your_referrals_count": "Number of referrals: {count}",
    "view_referral_details_button": "Referral Details 📊",
    "earn_credit_title": "🎁 <b>Earn Free Credit!</b>",
    "earn_credit_description": "Invite your friends using your referral code, and for every friend who signs up through your code, you'll automatically receive credit 💸",
    "your_referral_code": "🔗 <b>Your Code:</b> <code>{referral_code}</code>",
    "your_reward": "💰 <b>Your Reward:</b> {amount} {currency} for each friend who uses your code to sign up",
    "more_referrals_more_credit": "👥 The more referrals, the more credit! Share your code in groups and platforms 👇",
    "copy_referral_code_button": "📤 Copy Referral Code",
    "no_referrals_yet": "🚫 No referrals yet.",
    "referrals_list_title": "📊 <b>Your Referrals:</b>",
    "referral_entry": "👤 {name} — 🗓️ {joined_date}",
    "view_referrals_button": "View Referrals 📊", # **تمت إضافة هذا السطر**


    # =========================================================================
    #  Agent Program
    # =========================================================================
    "agent_program_title": "🤝 <b>Your chance to become an authorized agent!</b>",
    "agent_benefits_title": "✅ <b>Agent Benefits:</b>",
    "agent_benefit_1": "• Exclusive pricing lower than regular users.",
    "agent_benefit_2": "• Advanced control panel to monitor users.",
    "agent_benefit_3": "• Automatic earnings from your clients' operations.",
    "agent_benefit_4": "• Direct technical support and priority response.",
    "agent_profit_example_title": "💼 <b>Profit Example:</b>",
    "agent_profit_example_scenario": "If an agent oversees 10 users, and each user spends 50 {currency}:",
    "agent_monthly_profit": "🪙 <b>Monthly Profit:</b> {profit} {currency} ({commission_percentage}% commission)",
    "agent_terms_title": "📌 <b>Terms:</b>",
    "agent_term_1": "• You must have real users.",
    "agent_term_2": "• Adherence to terms of service.",
    "agent_call_to_action": "If you are interested, click the button below and we will contact you.",
    "send_agent_request_button": "📩 Send Application",
    "new_agent_request_title": "📬 <b>New Agent Request</b>",
    "agent_request_name": "👤 Name: {full_name}",
    "agent_request_username": "🆔 Username: @{username}",
    "agent_request_id": "🆔 ID: <code>{user_id}</code>",
    "agent_request_sent_success": "✅ Your application has been sent to the administration successfully.",
    "agent_request_review_notice": "📌 We will review the application and contact you soon, God willing.",


    # =========================================================================
    #  Admin Panel
    # =========================================================================
    "admin_panel_title": "Admin Panel ⚙️",
    "not_admin_message": "Sorry, you are not an admin.",
    "users_management_button": "User Management",
    "servers_management_button": "Server Management",
    "add_balance_button": "Add Balance to User",
    "subtract_balance_button": "Subtract Balance from User",
    "change_user_role_button": "Change User Role",
    "broadcast_message_button": "Broadcast Message",
    "get_user_info_button": "Get User Info",
    "enter_user_id_for_action": "Enter User ID for {action_type}:",
    "enter_amount_for_balance_change": "Enter amount (in USD):",
    "user_balance_updated": "User {user_id}'s balance updated to {new_balance}.",
    "user_role_updated": "User {user_id}'s role updated to {new_role}.",
    "user_not_found_in_db": "User not found in database.",
    "invalid_role": "Invalid role. Must be 'admin' or 'user'.",
    "user_fallback_name": "User {user_id}",
    "no_matching_users": "❌ No matching users.",
    "admin_user_management_title": "<b>👥 User Management</b>",
    "banned_status": "🚫 Banned",
    "active_status": "✅ Active",
    "admin_user_info_line": "👤 <b>{name}</b> | 🆔 {user_id}\n💰 {balance} {currency} | {status}",
    "edit_user_button": "✏️ Edit",
    "ban_button": "✅ Unban",
    "unban_button": "🚫 Ban",
    "delete_user_button": "🗑 Delete",
    "not_admin_search_permission": "❌ You do not have permission to search the user list.",
    "enter_new_balance": "✏️ Send new balance for user now\n🆔 ID: <code>{user_id}</code>",
    "invalid_balance_input": "❌ Please enter a valid number for the balance.",
    "balance_conversion_error": "❌ Error converting balance. Please enter a number.",
    "user_not_found_for_edit": "❌ User whose balance you want to edit was not found.",
    "user_status_updated": "✅ User {user_id}'s status updated to: {new_status}.",
    "user_not_found": "❌ User not found.",
    "yes_delete_button": "✅ Yes, Delete",
    "confirm_delete_user_message": "⚠️ Are you sure you want to delete user <code>{user_id}</code>? This action cannot be undone.",
    "user_deleted_success": "🗑️ User <code>{user_id}</code> deleted successfully.",
    "unbanned_text": "Active", # **تمت إضافة هذا السطر**
    "banned_text": "Banned",   # **تمت إضافة هذا السطر**


    # =========================================================================
    #  Quick Search
    # =========================================================================
    "quick_search_prompt": "🌹 Hello 😊\nDr\\Ramzi\n\n— Please send the country name (in Arabic, English, or by flag emoji 🇸🇦) to search for it:\n\n──────────────",
    "country_not_found": "❌ This country was not found. Make sure the name is spelled correctly.",
    "no_servers_available_country_quick_search": "❗ No servers currently available for this country.",
    "quick_search_results": "📍 <b>Country:</b> {country_name}\n📱 <b>Platform:</b> {platform}\n💰 <b>Your Balance:</b> {balance} {currency}",
    "choose_server_prompt": "Choose the appropriate server to try:",


    # =========================================================================
    #  Language Selection
    # =========================================================================
    "select_your_language": "🌐 Choose the language you prefer for the bot:\n\nاختر اللغة التي تفضل استخدامها في البوت:",
    "language_arabic_button": "العربية",
    "language_english_button": "English",
    "language_changed_to_arabic": "✅ Language set to Arabic.",
    "language_changed_to_english": "✅ Language set to English.",


    # =========================================================================
    #  Help & Support
    # =========================================================================
    "help_message": "Welcome to the help section!\n\nTo buy a number, click 'Buy Number' and follow the instructions. You can recharge your balance by contacting the admin. For more help, please contact technical support.",
    "help_menu_welcome_message": "🌹 Welcome Dr\\Ramzi 😊\n⌁─━─━ ({bot_name}) ─━─━⌁",
    "contact_support_button": "📩 - Contact Support",
    "usage_guide_button": "📄 - Usage Guide",
    "faq_button": "❓ - FAQ",

    "usage_guide_title": "📘 <b>Bot Usage Guide</b>",
    "usage_step_1": "1️⃣ Click the 💎 Buy Number button in the main menu.",
    "usage_step_2": "2️⃣ Choose the platform you want to activate the number for (WhatsApp, Telegram...)",
    "usage_step_3": "3️⃣ Choose the country then the appropriate server based on price and quality.",
    "usage_step_4": "4️⃣ Your balance will be automatically deducted and the number displayed.",
    "usage_step_5": "5️⃣ Follow the code that reaches you directly inside the bot.",
    "usage_notes_title": "📌 Notes:",
    "usage_note_1": "- Make sure to recharge your balance before purchasing.",
    "usage_note_2": "- Prices vary by server and country.",
    "usage_note_3": "- Some numbers are valid for a limited period.",
    "usage_problem_contact_support": "⚠️ If you encounter a problem, contact support.",
    "back_to_menu_note": "🔙 You can go back using the button below.",

    "contact_support_title": "📞 <b>Contact Support</b>",
    "contact_support_prompt": "For any inquiries or issues:",
    "contact_support_link": "🔗 <a href='{support_link}'>{support_link}</a>",
    "contact_support_hours": "🕐 Available from 10 AM to 12 AM.",
    "contact_support_tip": "📌 Send your inquiry with a picture/explanation if available.",

    "faq_title": "❓ <b>Frequently Asked Questions</b>",
    "faq_q1": "🟢 <b>Is the number for one-time use?</b>",
    "faq_a1": "Yes, each number is used to activate only one account.",
    "faq_q2": "🟢 <b>What if I don't receive the code?</b>",
    "faq_a2": "Try again or use a different server.",
    "faq_q3": "🟢 <b>Can I get a refund?</b>",
    "faq_a3": "Only if the operation failed and the number was not used.",
    "faq_more_questions": "📩 For more questions, contact support.",


    # =========================================================================
    #  Country Names
    # =========================================================================
    "country_name_sa": "Saudi Arabia",
    "country_name_eg": "Egypt",
    "country_name_ye": "Yemen",
    "country_name_dz": "Algeria",
    "country_name_ma": "Morocco",
    "country_name_iq": "Iraq",
    "country_name_sd": "Sudan",
    "country_name_sy": "Syria",
    "country_name_kw": "Kuwait",
    "country_name_qa": "Qatar",
    "country_name_ae": "UAE",
    "country_name_jo": "Jordan",
    "country_name_lb": "Lebanon",
    "country_name_tn": "Tunisia",
    "country_name_ng": "Nigeria",
    "country_name_ke": "Kenya",
    "country_name_gh": "Ghana",
    "country_name_za": "South Africa",
    "country_name_et": "Ethiopia",
    "country_name_tz": "Tanzania",
    "country_name_in": "India",
    "country_name_pk": "Pakistan",
    "country_name_id": "Indonesia",
    "country_name_th": "Thailand",
    "country_name_my": "Malaysia",
    "country_name_ph": "Philippines",
    "country_name_uk": "United Kingdom",
    "country_name_fr": "France",
    "country_name_de": "Germany",
    "country_name_es": "Spain",
    "country_name_it": "Italy",
    "country_name_nl": "Netherlands",
    "country_name_us": "USA",
    "country_name_br": "Brazil",
    "country_name_ca": "Canada",
    "country_name_mx": "Mexico",
    "country_name_co": "Colombia",
    "country_name_ar": "Argentina",
    "country_name_au": "Australia",
    "country_name_nz": "New Zealand",
}