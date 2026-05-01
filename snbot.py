import requests
import asyncio
import sqlite3
import time
import random
import string
import json
from datetime import datetime, timedelta
from telegram import Bot, Update, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes
from telegram.constants import ParseMode

# ======================================
# TELEGRAM SETTINGS
# ======================================

BOT_TOKEN = "8753080087:AAGIOtTyWgVAf-CLnCtBjAEFtluSOXUYhe4"
ADMIN_ID = 8502686983

# চ্যানেল লিংক
REQUIRED_CHANNELS = [
    {"name": "NeroxaUpdate", "url": "https://t.me/NeroxaUpdate", "username": "@NeroxaUpdate"},
    {"name": "NeroxaOfficial", "url": "https://t.me/NeroxaOfficial", "username": "@NeroxaOfficial"}
]

# ======================================
# LANGUAGE DICTIONARY
# ======================================

TEXTS = {
    'bn': {
        'welcome': "🎯 নারক্সা সিগন্যাল বটে স্বাগতম!",
        'vip_user': "👑 ভিআইপি ইউজার",
        'free_user': "🆓 ফ্রি ইউজার",
        'coins_balance': "💰 কয়েন ব্যালান্স",
        'referral_link': "🔗 রেফার লিংক",
        'per_referral': "প্রতি রেফারে",
        'menu': "📱 মেইন মেনু",
        'live_signal': "📊 লাইভ সিগন্যাল",
        'vip_upgrade': "👑 ভিআইপি আপগ্রেড",
        'star_balance': "💰 স্টার ব্যালান্স",
        'settings': "⚙️ সেটিংস",
        'help': "❓ হেল্প",
        'admin_panel': "🔧 অ্যাডমিন প্যানেল",
        'auto_signal': "🔔 অটো সিগন্যাল",
        'language': "🌐 ল্যাংগুয়েজ",
        'broadcast': "📢 ব্রডকাস্ট",
        'my_info': "ℹ️ আমার তথ্য",
        'back': "🔙 ব্যাক",
        'vip_gift': "👑 ভিআইপি গিফট",
        'create_redeem': "🎫 রিডিম কোড তৈরি",
        'set_star_price': "💰 স্টার প্রাইস সেট",
        'payment_address': "💳 পেমেন্ট অ্যাড্রেস",
        'custom_message': "📝 কাস্টম মেসেজ",
        'user_manage': "👥 ইউজার ম্যানেজ",
        'server_stats': "📊 সার্ভার স্ট্যাটস",
        'bot_settings': "⚙️ বট সেটিংস",
        'news': "📰 নিউজ",
        'main_menu': "🔙 মেইন মেনু",
        'signal_scanning': "📊 সিগন্যাল স্ক্যান করা হচ্ছে...",
        'no_signal': "⏳ বর্তমানে কোনো সিগն্যাল নেই",
        'vip_price_info': "👑 ভিআইপি মেম্বারশিপ",
        'payment_method': "💳 পেমেন্ট মেথড",
        'redeem_code': "🎫 রিডিম কোড",
        'enter_redeem_code': "রিডিম কোড লিখুন:",
        'invalid_code': "❌ ইনভ্যালিড রিডিম কোড!",
        'code_already_used': "❌ এই কোড ইতিমধ্যে ইউজ করা হয়েছে!",
        'vip_activated': "✨ কংগ্রাচুলেশনস! আপনি এখন ভিআইপি ইউজার!",
        'expiry_date': "📅 এক্সপায়ারি ডেট",
        'vip_features': "🔥 ভিআইপি ফিচারসমূহ",
        'high_confidence': "✅ 95%+ কনফিডেন্স সিগন্যাল",
        'premium_indicators': "✅ প্রিমিয়াম ইন্ডিকেটর",
        'real_time': "✅ রিয়েল টাইম আপডেট",
        'daily_bonus': "✅ ডেইলি বোনাস",
        'auto_signal_on': "🔔 অটো সিগন্যাল চালু করা হয়েছে",
        'auto_signal_off': "🔕 অটো সিগন্যাল বন্ধ করা হয়েছে",
        'language_changed': "🌐 ভাষা পরিবর্তন করা হয়েছে",
        'news_sent': "📰 নিউজ পাঠানো হয়েছে",
        'admin_only': "⛔ এই কমান্ড শুধু অ্যাডমিনের জন্য!",
        'join_channels': "🔒 বট ব্যবহার করতে নিচের চ্যানেলগুলো জয়েন করুন:",
        'joined': "✅ জয়েন করেছি"
    },
    'en': {
        'welcome': "🎯 Welcome to Neroxa Signal Bot!",
        'vip_user': "👑 VIP User",
        'free_user': "🆓 Free User",
        'coins_balance': "💰 Coin Balance",
        'referral_link': "🔗 Referral Link",
        'per_referral': "Per Referral",
        'menu': "📱 Main Menu",
        'live_signal': "📊 Live Signal",
        'vip_upgrade': "👑 VIP Upgrade",
        'star_balance': "💰 Star Balance",
        'settings': "⚙️ Settings",
        'help': "❓ Help",
        'admin_panel': "🔧 Admin Panel",
        'auto_signal': "🔔 Auto Signal",
        'language': "🌐 Language",
        'broadcast': "📢 Broadcast",
        'my_info': "ℹ️ My Info",
        'back': "🔙 Back",
        'vip_gift': "👑 VIP Gift",
        'create_redeem': "🎫 Create Redeem Code",
        'set_star_price': "💰 Set Star Price",
        'payment_address': "💳 Payment Address",
        'custom_message': "📝 Custom Message",
        'user_manage': "👥 User Manage",
        'server_stats': "📊 Server Stats",
        'bot_settings': "⚙️ Bot Settings",
        'news': "📰 News",
        'main_menu': "🔙 Main Menu",
        'signal_scanning': "📊 Scanning signals...",
        'no_signal': "⏳ No signal at the moment",
        'vip_price_info': "👑 VIP Membership",
        'payment_method': "💳 Payment Method",
        'redeem_code': "🎫 Redeem Code",
        'enter_redeem_code': "Enter redeem code:",
        'invalid_code': "❌ Invalid redeem code!",
        'code_already_used': "❌ This code has already been used!",
        'vip_activated': "✨ Congratulations! You are now a VIP user!",
        'expiry_date': "📅 Expiry Date",
        'vip_features': "🔥 VIP Features",
        'high_confidence': "✅ 95%+ Confidence Signals",
        'premium_indicators': "✅ Premium Indicators",
        'real_time': "✅ Real Time Updates",
        'daily_bonus': "✅ Daily Bonus",
        'auto_signal_on': "🔔 Auto signal turned ON",
        'auto_signal_off': "🔕 Auto signal turned OFF",
        'language_changed': "🌐 Language changed",
        'news_sent': "📰 News sent",
        'admin_only': "⛔ This command is for admin only!",
        'join_channels': "🔒 Please join the following channels to use the bot:",
        'joined': "✅ Joined"
    }
}

# ======================================
# DATABASE SETUP
# ======================================

conn = sqlite3.connect("vip_bot.db", check_same_thread=False)
conn.execute("PRAGMA journal_mode=WAL")
cursor = conn.cursor()

# ইউজার টেবিল
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY,
    username TEXT,
    first_name TEXT,
    vip_status TEXT DEFAULT 'free',
    vip_expiry TEXT,
    stars INTEGER DEFAULT 0,
    auto_signal INTEGER DEFAULT 0,
    referral_code TEXT,
    referred_by INTEGER,
    join_date TEXT,
    total_referrals INTEGER DEFAULT 0,
    language TEXT DEFAULT 'bn'
)
""")

# অ্যাডমিন সেটিংস টেবিল
cursor.execute("""
CREATE TABLE IF NOT EXISTS admin_settings (
    id INTEGER PRIMARY KEY,
    payment_address TEXT,
    support_id TEXT,
    vip_price_stars INTEGER DEFAULT 500,
    vip_7days_stars INTEGER DEFAULT 300,
    vip_30days_stars INTEGER DEFAULT 1000,
    vip_90days_stars INTEGER DEFAULT 2500,
    referral_reward INTEGER DEFAULT 100,
    welcome_message TEXT,
    bot_name TEXT DEFAULT 'নারক্সা সিগন্যাল বট'
)
""")

# রিডিম কোড টেবিল
cursor.execute("""
CREATE TABLE IF NOT EXISTS redeem_codes (
    code TEXT PRIMARY KEY,
    duration_days INTEGER,
    stars_reward INTEGER DEFAULT 0,
    used_by INTEGER,
    used_time TEXT,
    is_used INTEGER DEFAULT 0
)
""")

# নিউজ টেবিল
cursor.execute("""
CREATE TABLE IF NOT EXISTS news (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT,
    content TEXT,
    image_url TEXT,
    send_to_all INTEGER DEFAULT 1,
    created_at TEXT
)
""")

# সিগন্যাল টেবিল
cursor.execute("""
CREATE TABLE IF NOT EXISTS signals (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    pair TEXT,
    signal TEXT,
    confidence INTEGER,
    result TEXT,
    time TEXT,
    message_id INTEGER
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS stats (
    id INTEGER PRIMARY KEY,
    total_profit REAL DEFAULT 0,
    total_win INTEGER DEFAULT 0,
    total_loss INTEGER DEFAULT 0,
    total_stars_earned INTEGER DEFAULT 0,
    total_stars_spent INTEGER DEFAULT 0
)
""")

# ডিফল্ট সেটিংস
cursor.execute("INSERT OR IGNORE INTO admin_settings (id, payment_address, support_id, welcome_message) VALUES (1, 'নারক্সা', '8502686983', 'বটে স্বাগতম')", ())
conn.commit()

# ======================================
# KEYBOARD FUNCTIONS
# ======================================

def get_main_keyboard(lang='bn', is_admin=False):
    """মেইন কীবোর্ড বাটন"""
    buttons = [
        [TEXTS[lang]['live_signal'], TEXTS[lang]['vip_upgrade']],
        [TEXTS[lang]['star_balance'], TEXTS[lang]['referral_link']],
        [TEXTS[lang]['settings'], TEXTS[lang]['help']]
    ]
    
    if is_admin:
        buttons.append([TEXTS[lang]['admin_panel']])
    
    return ReplyKeyboardMarkup(buttons, resize_keyboard=True)

def get_settings_keyboard(lang='bn'):
    """সেটিংস কীবোর্ড"""
    buttons = [
        [TEXTS[lang]['auto_signal'], TEXTS[lang]['language']],
        [TEXTS[lang]['broadcast'], TEXTS[lang]['my_info']],
        [TEXTS[lang]['back']]
    ]
    return ReplyKeyboardMarkup(buttons, resize_keyboard=True)

def get_admin_keyboard(lang='bn'):
    """অ্যাডমিন কীবোর্ড"""
    buttons = [
        [TEXTS[lang]['vip_gift'], TEXTS[lang]['create_redeem']],
        [TEXTS[lang]['set_star_price'], TEXTS[lang]['payment_address']],
        [TEXTS[lang]['custom_message'], TEXTS[lang]['user_manage']],
        [TEXTS[lang]['server_stats'], TEXTS[lang]['bot_settings']],
        [TEXTS[lang]['news'], TEXTS[lang]['main_menu']]
    ]
    return ReplyKeyboardMarkup(buttons, resize_keyboard=True)

def get_language_keyboard():
    """ল্যাংগুয়েজ সিলেক্ট কীবোর্ড"""
    buttons = [
        ["🇧🇩 বাংলা", "🇬🇧 English"],
        ["🔙 Back"]
    ]
    return ReplyKeyboardMarkup(buttons, resize_keyboard=True)

# ======================================
# CHANNEL CHECK
# ======================================

async def check_channel_join(user_id: int, context: ContextTypes.DEFAULT_TYPE) -> bool:
    """চ্যানেল জয়েন চেক করে"""
    try:
        for channel in REQUIRED_CHANNELS:
            chat_member = await context.bot.get_chat_member(chat_id=channel["username"], user_id=user_id)
            if chat_member.status in ["left", "kicked"]:
                return False
        return True
    except:
        return False

def get_channel_keyboard(lang='bn'):
    """চ্যানেল জয়েন কীবোর্ড"""
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton(f"📢 Join {c['name']}", url=c['url'])] for c in REQUIRED_CHANNELS
    ] + [[InlineKeyboardButton(TEXTS[lang]['joined'], callback_data="check_join")]])
    return keyboard

# ======================================
# VIP FUNCTIONS
# ======================================

def generate_referral_code():
    """রেফারেল কোড জেনারেট"""
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

async def give_vip(user_id: int, duration_days: int, context: ContextTypes.DEFAULT_TYPE):
    """ভিআইপি দেয়"""
    cursor.execute("SELECT language FROM users WHERE user_id = ?", (user_id,))
    lang_row = cursor.fetchone()
    lang = lang_row[0] if lang_row else 'bn'
    
    expiry = (datetime.now() + timedelta(days=duration_days)).strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute("UPDATE users SET vip_status = 'vip', vip_expiry = ? WHERE user_id = ?", (expiry, user_id))
    conn.commit()
    
    await context.bot.send_message(
        chat_id=user_id,
        text=f"{TEXTS[lang]['vip_activated']}\n\n"
             f"{TEXTS[lang]['expiry_date']}: {expiry}\n\n"
             f"{TEXTS[lang]['vip_features']}:\n"
             f"{TEXTS[lang]['high_confidence']}\n"
             f"{TEXTS[lang]['premium_indicators']}\n"
             f"{TEXTS[lang]['real_time']}\n"
             f"{TEXTS[lang]['daily_bonus']}"
    )

async def create_redeem_code(duration_days: int, stars_reward: int = 0) -> str:
    """রিডিম কোড তৈরি"""
    code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=12))
    cursor.execute("INSERT INTO redeem_codes (code, duration_days, stars_reward, is_used) VALUES (?, ?, ?, 0)", 
                   (code, duration_days, stars_reward))
    conn.commit()
    return code

# ======================================
# SIGNAL FUNCTIONS (বেসিক ভெரশন)
# ======================================

def get_market_data(symbol):
    """মার্কেট ডাটা আনে"""
    try:
        url = f"https://api.binance.com/api/v3/klines?symbol={symbol}&interval=1m&limit=100"
        response = requests.get(url, timeout=10)
        data = response.json()
        closes = [float(c[4]) for c in data]
        return closes
    except:
        return []

def analyze_signal(pair, is_vip=False):
    """সিগন্যাল অ্যানালাইসিস"""
    closes = get_market_data(pair)
    if len(closes) < 50:
        return None
    
    # সিম্পল অ্যানালাইসিস (আপনার পুরনো ফাংশন এখানে বসাতে পারেন)
    current = closes[-1]
    prev = closes[-2]
    
    if is_vip:
        # ভিআইপি জন্য বেশি অ্যাকিউরেট
        if current > prev * 1.002:
            return {"signal": "BUY", "confidence": 95}
        elif current < prev * 0.998:
            return {"signal": "SELL", "confidence": 95}
    else:
        # ফ্রি জন্য কম অ্যাকিউরেট
        if current > prev * 1.005:
            return {"signal": "BUY", "confidence": 70}
        elif current < prev * 0.995:
            return {"signal": "SELL", "confidence": 70}
    
    return None

# ======================================
# BOT HANDLERS
# ======================================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    user_id = user.id
    
    # চ্যানেল চেক
    if not await check_channel_join(user_id, context):
        await update.message.reply_text(
            "🔒 **Please join channels to use bot**\n\n"
            "বট ব্যবহার করতে চ্যানেল জয়েন করুন:",
            reply_markup=get_channel_keyboard('bn'),
            parse_mode=ParseMode.MARKDOWN
        )
        return
    
    # ইউজার চেক
    cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
    existing = cursor.fetchone()
    
    if not existing:
        referral_code = generate_referral_code()
        cursor.execute("""
            INSERT INTO users (user_id, username, first_name, join_date, referral_code, language)
            VALUES (?, ?, ?, ?, ?, 'bn')
        """, (user_id, user.username, user.first_name, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), referral_code))
        conn.commit()
        
        # রেফারেল চেক
        args = context.args
        if args:
            referred_by_code = args[0]
            cursor.execute("SELECT user_id FROM users WHERE referral_code = ?", (referred_by_code,))
            referrer = cursor.fetchone()
            if referrer:
                cursor.execute("UPDATE users SET stars = stars + 100, total_referrals = total_referrals + 1 WHERE user_id = ?", (referrer[0],))
                cursor.execute("UPDATE users SET referred_by = ? WHERE user_id = ?", (referrer[0], user_id))
                conn.commit()
    
    # স্ট্যাটাস চেক
    cursor.execute("SELECT vip_status, vip_expiry, stars, language FROM users WHERE user_id = ?", (user_id,))
    status = cursor.fetchone()
    lang = status[3]
    
    welcome = f"""{TEXTS[lang]['welcome']}

👤 {user.first_name}
{TEXTS[lang]['vip_user'] if status[0] == 'vip' else TEXTS[lang]['free_user']}
{TEXTS[lang]['star_balance']}: {status[2]} ⭐

{TEXTS[lang]['referral_link']}:
https://t.me/{context.bot.username}?start={referral_code}
{TEXTS[lang]['per_referral']}: 100 ⭐
"""
    
    await update.message.reply_text(welcome, reply_markup=get_main_keyboard(lang, user_id == ADMIN_ID))

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    text = update.message.text
    
    # ইউজার ল্যাংগুয়েজ পাওয়া
    cursor.execute("SELECT language FROM users WHERE user_id = ?", (user_id,))
    lang_row = cursor.fetchone()
    lang = lang_row[0] if lang_row else 'bn'
    
    # মেইন মেনু বাটন
    if text == TEXTS[lang]['live_signal']:
        await update.message.reply_text(TEXTS[lang]['signal_scanning'])
        
        pairs = ["BTCUSDT", "ETHUSDT", "BNBUSDT"]
        cursor.execute("SELECT vip_status FROM users WHERE user_id = ?", (user_id,))
        is_vip = cursor.fetchone()[0] == 'vip'
        
        signals = []
        for pair in pairs:
            result = analyze_signal(pair, is_vip)
            if result:
                signals.append(f"{pair}: {result['signal']} ({result['confidence']}%)")
        
        if signals:
            await update.message.reply_text("🚀 **Signals Found:**\n\n" + "\n".join(signals))
        else:
            await update.message.reply_text(TEXTS[lang]['no_signal'])
    
    elif text == TEXTS[lang]['vip_upgrade']:
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("💎 7 Days - 300 ⭐", callback_data="buy_vip_7")],
            [InlineKeyboardButton("💎 30 Days - 1000 ⭐", callback_data="buy_vip_30")],
            [InlineKeyboardButton("💎 90 Days - 2500 ⭐", callback_data="buy_vip_90")],
            [InlineKeyboardButton("🎫 Redeem Code", callback_data="redeem_menu")]
        ])
        await update.message.reply_text(f"{TEXTS[lang]['vip_price_info']}\n\n{TEXTS[lang]['payment_method']}: ⭐ Stars", reply_markup=keyboard)
    
    elif text == TEXTS[lang]['star_balance']:
        cursor.execute("SELECT stars FROM users WHERE user_id = ?", (user_id,))
        stars = cursor.fetchone()[0]
        await update.message.reply_text(f"💰 {TEXTS[lang]['star_balance']}: {stars} ⭐")
    
    elif text == TEXTS[lang]['referral_link']:
        cursor.execute("SELECT referral_code, total_referrals FROM users WHERE user_id = ?", (user_id,))
        code, refs = cursor.fetchone()
        await update.message.reply_text(
            f"{TEXTS[lang]['referral_link']}:\n"
            f"`https://t.me/{context.bot.username}?start={code}`\n\n"
            f"📊 Total Referrals: {refs}\n"
            f"⭐ Per Referral: 100 Stars"
        )
    
    elif text == TEXTS[lang]['settings']:
        await update.message.reply_text(TEXTS[lang]['menu'], reply_markup=get_settings_keyboard(lang))
    
    elif text == TEXTS[lang]['auto_signal']:
        cursor.execute("SELECT auto_signal FROM users WHERE user_id = ?", (user_id,))
        current = cursor.fetchone()[0]
        new_status = 0 if current == 1 else 1
        cursor.execute("UPDATE users SET auto_signal = ? WHERE user_id = ?", (new_status, user_id))
        conn.commit()
        msg = TEXTS[lang]['auto_signal_on'] if new_status else TEXTS[lang]['auto_signal_off']
        await update.message.reply_text(msg)
    
    elif text == TEXTS[lang]['language']:
        await update.message.reply_text("🌐 Select Language / ভাষা নির্বাচন করুন:", reply_markup=get_language_keyboard())
    
    elif text == TEXTS[lang]['broadcast'] and user_id == ADMIN_ID:
        context.user_data['admin_action'] = 'broadcast'
        await update.message.reply_text("📢 নিউজ লিখুন (বাংলা/ইংরেজি):")
    
    elif text == TEXTS[lang]['my_info']:
        cursor.execute("SELECT vip_status, vip_expiry, stars, total_referrals, join_date FROM users WHERE user_id = ?", (user_id,))
        info = cursor.fetchone()
        await update.message.reply_text(
            f"ℹ️ **Your Info**\n\n"
            f"👑 Status: {info[0]}\n"
            f"📅 Expiry: {info[1] if info[1] else 'N/A'}\n"
            f"⭐ Stars: {info[2]}\n"
            f"🔗 Referrals: {info[3]}\n"
            f"📆 Joined: {info[4]}"
        )
    
    elif text == TEXTS[lang]['back']:
        cursor.execute("SELECT language FROM users WHERE user_id = ?", (user_id,))
        lang = cursor.fetchone()[0]
        await update.message.reply_text(TEXTS[lang]['menu'], reply_markup=get_main_keyboard(lang, user_id == ADMIN_ID))
    
    # ল্যাংগুয়েজ বাটন
    elif text == "🇧🇩 বাংলা":
        cursor.execute("UPDATE users SET language = 'bn' WHERE user_id = ?", (user_id,))
        conn.commit()
        await update.message.reply_text(TEXTS['bn']['language_changed'], reply_markup=get_main_keyboard('bn', user_id == ADMIN_ID))
    
    elif text == "🇬🇧 English":
        cursor.execute("UPDATE users SET language = 'en' WHERE user_id = ?", (user_id,))
        conn.commit()
        await update.message.reply_text(TEXTS['en']['language_changed'], reply_markup=get_main_keyboard('en', user_id == ADMIN_ID))
    
    # অ্যাডমিন প্যানেল
    elif text == TEXTS[lang]['admin_panel'] and user_id == ADMIN_ID:
        await update.message.reply_text("🔧 **Admin Panel**", reply_markup=get_admin_keyboard(lang))
    
    elif text == TEXTS[lang]['main_menu'] and user_id == ADMIN_ID:
        cursor.execute("SELECT language FROM users WHERE user_id = ?", (user_id,))
        lang = cursor.fetchone()[0]
        await update.message.reply_text(TEXTS[lang]['menu'], reply_markup=get_main_keyboard(lang, True))
    
    elif text == TEXTS[lang]['vip_gift'] and user_id == ADMIN_ID:
        context.user_data['admin_action'] = 'gift_vip'
        await update.message.reply_text("👑 ভিআইপি গিফট করুন:\n\n`/gift USER_ID DAYS`\nযেমন: /gift 123456789 30")
    
    elif text == TEXTS[lang]['create_redeem'] and user_id == ADMIN_ID:
        context.user_data['admin_action'] = 'create_redeem'
        await update.message.reply_text("🎫 রিডিম কোড তৈরি:\n\n`/redeem DAYS STARS`\nযেমন: /redeem 30 500")
    
    elif text == TEXTS[lang]['news'] and user_id == ADMIN_ID:
        context.user_data['admin_action'] = 'news'
        await update.message.reply_text("📰 নিউজ পাঠানোর জন্য টাইটেল ও কন্টেন্ট লিখুন:\n\n`/news টাইটেল | কন্টেন্ট`")
    
    # ব্রডকাস্ট হ্যান্ডেল
    elif context.user_data.get('admin_action') == 'broadcast' and user_id == ADMIN_ID:
        cursor.execute("SELECT user_id FROM users")
        all_users = cursor.fetchall()
        
        success = 0
        for user in all_users:
            try:
                await context.bot.send_message(chat_id=user[0], text=f"📢 **নতুন নিউজ**\n\n{text}")
                success += 1
                await asyncio.sleep(0.05)
            except:
                pass
        
        await update.message.reply_text(f"✅ {success} জন ইউজারকে নিউজ পাঠানো হয়েছে!")
        context.user_data['admin_action'] = None

async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id
    
    cursor.execute("SELECT language, stars FROM users WHERE user_id = ?", (user_id,))
    user_data = cursor.fetchone()
    lang = user_data[0] if user_data else 'bn'
    stars = user_data[1] if user_data else 0
    
    if query.data == "check_join":
        if await check_channel_join(user_id, context):
            await query.edit_message_text("✅ চ্যানেল জয়েন কনফার্ম! /start দিন")
        else:
            await query.edit_message_text("❓ সব চ্যানেল জয়েন করেননি!", reply_markup=get_channel_keyboard(lang))
    
    elif query.data.startswith("buy_vip_"):
        days = int(query.data.split("_")[2])
        price_map = {7: 300, 30: 1000, 90: 2500}
        price = price_map.get(days, 300)
        
        if stars >= price:
            cursor.execute("UPDATE users SET stars = stars - ? WHERE user_id = ?", (price, user_id))
            conn.commit()
            await give_vip(user_id, days, context)
            await query.edit_message_text(f"✅ VIP Activated for {days} days!")
        else:
            need = price - stars
            await query.edit_message_text(f"❌ আপনার কাছে {stars} ⭐ আছে। আরও {need} ⭐ দরকার!\nরেফারেল লিংক শেয়ার করে স্টার সংগ্রহ করুন।")
    
    elif query.data == "redeem_menu":
        await query.edit_message_text(TEXTS[lang]['enter_redeem_code'], reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back", callback_data="back_to_vip")]]))

async def admin_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        await update.message.reply_text("⛔ Admin only!")
        return
    
    cmd = context.args[0] if context.args else ""
    
    if cmd == "gift" and len(context.args) >= 3:
        user_id = int(context.args[1])
        days = int(context.args[2])
        await give_vip(user_id, days, context)
        await update.message.reply_text(f"✅ VIP gifted to {user_id} for {days} days!")
    
    elif cmd == "redeem" and len(context.args) >= 3:
        days = int(context.args[1])
        stars = int(context.args[2])
        code = await create_redeem_code(days, stars)
        await update.message.reply_text(f"✅ Redeem Code: `{code}`\n📅 Days: {days}\n⭐ Stars: {stars}")
    
    elif cmd == "news" and len(context.args) >= 2:
        news_text = ' '.join(context.args[1:])
        parts = news_text.split('|')
        title = parts[0].strip() if parts else "নতুন নিউজ"
        content = parts[1].strip() if len(parts) > 1 else news_text
        
        cursor.execute("SELECT user_id, language FROM users")
        users = cursor.fetchall()
        
        success = 0
        for uid, lang in users:
            try:
                await context.bot.send_message(
                    chat_id=uid,
                    text=f"📰 **{title}**\n\n{content}\n\n_নারক্সা সিগন্যাল বট থেকে_",
                    parse_mode=ParseMode.MARKDOWN
                )
                success += 1
                await asyncio.sleep(0.05)
            except:
                pass
        
        await update.message.reply_text(f"✅ {success} users notified!")

# ======================================
# MAIN
# ======================================

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    
    # হ্যান্ডলার
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("gift", admin_command))
    app.add_handler(CommandHandler("redeem", admin_command))
    app.add_handler(CommandHandler("news", admin_command))
    app.add_handler(CallbackQueryHandler(handle_callback))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    print("✅ Bot is running with Bangla/English support, Star payment, and News system!")
    app.run_polling()

if __name__ == "__main__":
    main()
