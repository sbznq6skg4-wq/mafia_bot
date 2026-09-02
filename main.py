import asyncio
import logging
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder

# Token va Admin ma'lumotlari
TOKEN = "8036652216:AAEou7rBzPHMTg8xHBkXLXREljZ28chb5R0"
ADMIN_ID = 4916990359211916  # Sening ID raqaming
ADMIN_USERNAME = "@sobirvss"

bot = Bot(token=TOKEN)
dp = Dispatcher()

# Vaqtinchalik baza
users_db = {}

def get_user(user_id: int):
    if user_id not in users_db:
        users_db[user_id] = {
            "money": 1000,
            "diamonds": 10,
            "wins": 0,
            "games": 0,
            "lang": "uz",
            "role_status": "free"
        }
    return users_db[user_id]

# 1. /start buyrug'i
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(text="🌐 Tilni tanlash / Язык / Lang", callback_data="set_lang"))
    builder.row(types.InlineKeyboardButton(text="➕ Guruhga qo'shish", url=f"https://t.me/{(await bot.get_me()).username}?startgroup=true"))
    builder.row(
        types.InlineKeyboardButton(text="👤 Profil", callback_data="profile"),
        types.InlineKeyboardButton(text="💎 Olmos & Do'kon", callback_data="shop")
    )
    builder.row(types.InlineKeyboardButton(text="⚔️ Boys vs Girls", callback_data="bvg_info"))

    text = (
        "<b>🔥 Premium Mafia Botiga Xush Kelibsiz!</b>\n\n"
        "Eng kuchli, noyob rollar va qiziqarli imkoniyatlarga ega o'yin.\n"
        "Mendan foydalanish uchun meni guruhingizga qo'shing!"
    )
    await message.answer(text, reply_markup=builder.as_markup(), parse_mode="HTML")

# 2. /profile buyrug'i
@dp.message(Command("profile"))
async def cmd_profile(message: types.Message):
    user = get_user(message.from_user.id)
    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(text="💳 Kartaga o'tkazish / Pay", callback_data="donate_info"))
    builder.row(types.InlineKeyboardButton(text="🔙 Ortga", callback_data="back_home"))

    text = (
        f"<b>👤 Foydalanuvchi Profili:</b>\n\n"
        f"💵 Dollar: <b>{user['money']}</b>\n"
        f"💎 Olmos: <b>{user['diamonds']}</b>\n"
        f"🏆 G'alaba: <b>{user['wins']}</b>\n"
        f"🎮 Barcha o'yinlar: <b>{user['games']}</b>\n"
        f"⭐ Status: <b>{user['role_status'].upper()}</b>\n\n"
        f"<i>Bog'lanish / Creator: {ADMIN_USERNAME}</i>"
    )
    await message.answer(text, reply_markup=builder.as_markup(), parse_mode="HTML")

# 3. /shop buyrug'i (Do'kon)
@dp.message(Command("shop"))
async def cmd_shop(message: types.Message):
    builder = InlineKeyboardBuilder()
    builder.row(
        types.InlineKeyboardButton(text="⭐ Telegram Stars orqali", callback_data="pay_stars"),
        types.InlineKeyboardButton(text="💳 Karta (Uzcard/Visa) orqali", callback_data="pay_card")
    )
    builder.row(types.InlineKeyboardButton(text="🔙 Ortga", callback_data="back_home"))

    text = (
        "<b>💎 Olmos va VIP Do'koniga Xush Kelibsiz!</b>\n\n"
        "O'yinda ustunlik qilish, VIP rollarni ochish va eksklyuziv imkoniyatlar uchun olmos sotib oling."
    )
    await message.answer(text, reply_markup=builder.as_markup(), parse_mode="HTML")

# 4. /olmos buyrug'i
@dp.message(Command("olmos"))
async def cmd_olmos(message: types.Message):
    user = get_user(message.from_user.id)
    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(text="💎 Olmos sotib olish", callback_data="shop"))
    
    text = (
        f"<b>💎 Sizning Olmos Balansingiz:</b> {user['diamonds']} ta\n\n"
        "Olmoslar orqali maxsus VIP rollarni ochishingiz va o'yinda imtiyozlarga ega bo'lishingiz mumkin!"
    )
    await message.answer(text, reply_markup=builder.as_markup(), parse_mode="HTML")

# 5. /admin buyrug'i (Faqat senga ishlaydi)
@dp.message(Command("admin"))
async def cmd_admin(message: types.Message):
    if message.from_user.id != ADMIN_ID:
        await message.reply("❌ Bu buyruq faqat bot egasi uchun!")
        return
    
    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(text="📊 Bot Statistikasi", callback_data="admin_stats"))
    builder.row(types.InlineKeyboardButton(text="📢 Global Xabar", callback_data="admin_broadcast"))
    
    text = (
        "<b>👑 Xush kelibsiz, Boss!</b>\n\n"
        "Admin boshqaruv panelidasiz. Kerakli bo'limni tanlang:"
    )
    await message.answer(text, reply_markup=builder.as_markup(), parse_mode="HTML")

# 6. /pay buyrug'i (Reply orqali pul o'tkazish)
@dp.message(Command("pay"))
async def cmd_pay(message: types.Message):
    if not message.reply_to_message:
        await message.reply("⚠️ Pul o'tkazish uchun o'sha odamning xabariga reply qilib yozing! Masalan: <code>/pay 100</code>", parse_mode="HTML")
        return
    
    try:
        args = message.text.split()
        amount = int(args[1])
    except (IndexError, ValueError):
        await message.reply("⚠️ Noto'g'ri format! Ishlatish: <code>/pay [summa]</code>", parse_mode="HTML")
        return

    sender_id = message.from_user.id
    receiver_id = message.reply_to_message.from_user.id

    if sender_id == receiver_id:
        await message.reply("❌ O'zingizga pul o'tkaza olmaysiz!")
        return

    sender = get_user(sender_id)
    if sender["money"] < amount:
        await message.reply("❌ Hisobingizda yetarli mablag' yo'q!")
        return

    receiver = get_user(receiver_id)
    sender["money"] -= amount
    receiver["money"] += amount

    await message.reply(f"✅ Muvaffaqiyatli! <b>{amount}</b> dollar {message.reply_to_message.from_user.first_name} ga o'tkazildi.", parse_mode="HTML")

# --- CALLBACK QUERY HANDLERS (Tugmalar uchun) ---

@dp.callback_query(F.data == "set_lang")
async def choose_lang(callback: types.CallbackQuery):
    builder = InlineKeyboardBuilder()
    builder.row(
        types.InlineKeyboardButton(text="🇺🇿 O'zbekcha", callback_data="lang_uz"),
        types.InlineKeyboardButton(text="🇷🇺 Русский", callback_data="lang_ru"),
        types.InlineKeyboardButton(text="🇬🇧 English", callback_data="lang_en")
    )
    builder.row(types.InlineKeyboardButton(text="🔙 Ortga", callback_data="back_home"))
    await callback.message.edit_text("<b>Tilni tanlang / Выберите язык / Choose language:</b>", reply_markup=builder.as_markup(), parse_mode="HTML")
    await callback.answer()

@dp.callback_query(F.data.startswith("lang_"))
async def set_lang(callback: types.CallbackQuery):
    lang = callback.data.split("_")[1]
    user = get_user(callback.from_user.id)
    user["lang"] = lang
    await callback.answer("✅ Saqlandi!")
    await back_home_handler(callback)

@dp.callback_query(F.data == "profile")
async def show_profile_cb(callback: types.CallbackQuery):
    user = get_user(callback.from_user.id)
    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(text="💳 Kartaga o'tkazish / Pay", callback_data="donate_info"))
    builder.row(types.InlineKeyboardButton(text="🔙 Ortga", callback_data="back_home"))

    text = (
        f"<b>👤 Foydalanuvchi Profili:</b>\n\n"
        f"💵 Dollar: <b>{user['money']}</b>\n"
        f"💎 Olmos: <b>{user['diamonds']}</b>\n"
        f"🏆 G'alaba: <b>{user['wins']}</b>\n"
        f"🎮 Barcha o'yinlar: <b>{user['games']}</b>\n"
        f"⭐ Status: <b>{user['role_status'].upper()}</b>\n\n"
        f"<i>Bog'lanish / Creator: {ADMIN_USERNAME}</i>"
    )
    await callback.message.edit_text(text, reply_markup=builder.as_markup(), parse_mode="HTML")
    await callback.answer()

@dp.callback_query(F.data == "shop")
async def shop_menu_cb(callback: types.CallbackQuery):
    builder = InlineKeyboardBuilder()
    builder.row(
        types.InlineKeyboardButton(text="⭐ Telegram Stars orqali", callback_data="pay_stars"),
        types.InlineKeyboardButton(text="💳 Karta (Uzcard/Visa) orqali", callback_data="pay_card")
    )
    builder.row(types.InlineKeyboardButton(text="🔙 Ortga", callback_data="back_home"))

    text = (
        "<b>💎 Olmos va VIP Do'koniga Xush Kelibsiz!</b>\n\n"
        "O'yinda ustunlik qilish va VIP rollarni ochish uchun olmos sotib oling."
    )
    await callback.message.edit_text(text, reply_markup=builder.as_markup(), parse_mode="HTML")
    await callback.answer()

@dp.callback_query(F.data == "pay_card")
async def pay_card_info(callback: types.CallbackQuery):
    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(text="🔙 Ortga", callback_data="shop"))
    
    text = (
        "<b>💳 Karta orqali to'lov qilish:</b>\n\n"
        "Quyidagi kartalarga to'lov qilib, chekni adminga yuboring:\n\n"
        f"🇺🇿 <b>Uzcard:</b> <code>9860160623296383</code>\n"
        f"🌍 <b>Visa:</b> <code>4916990359211916</code>\n\n"
        f"👤 <b>Admin:</b> {ADMIN_USERNAME}"
    )
    await callback.message.edit_text(text, reply_markup=builder.as_markup(), parse_mode="HTML")
    await callback.answer()

@dp.callback_query(F.data == "admin_stats")
async def admin_stats(callback: types.CallbackQuery):
    if callback.from_user.id != ADMIN_ID:
        await callback.answer("Ruxsat yo'q!", show_alert=True)
        return
    total_users = len(users_db)
    await callback.answer(f"📊 Botdagi jami foydalanuvchilar: {total_users} ta", show_alert=True)

@dp.callback_query(F.data == "back_home")
async def back_home_handler(callback: types.CallbackQuery):
    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(text="🌐 Tilni tanlash / Язык / Lang", callback_data="set_lang"))
    builder.row(types.InlineKeyboardButton(text="➕ Guruhga qo'shish", url=f"https://t.me/{(await bot.get_me()).username}?startgroup=true"))
    builder.row(
        types.InlineKeyboardButton(text="👤 Profil", callback_data="profile"),
        types.InlineKeyboardButton(text="💎 Olmos & Do'kon", callback_data="shop")
    )
    builder.row(types.InlineKeyboardButton(text="⚔️ Boys vs Girls", callback_data="bvg_info"))

    text = (
        "<b>🔥 Premium Mafia Botiga Xush Kelibsiz!</b>\n\n"
        "Eng kuchli, noyob rollar va qiziqarli imkoniyatlarga ega o'yin."
    )
    await callback.message.edit_text(text, reply_markup=builder.as_markup(), parse_mode="HTML")
    await callback.answer()

async def main():
    logging.basicConfig(level=logging.INFO)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
