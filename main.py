import asyncio
import logging
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder

# Token
TOKEN = "8036652216:AAEou7rBzPHMTg8xHBkXLXREljZ28chb5R0"

# O'zingning ID raqamingni shu yerga yozasan (masalan: 123456789)
# Agar ID raqamingni aniq bilmasang, botga /myid deb yozib bilib olasan va keyin shu yerga yozasan.
ADMIN_ID = 4916990359  # Bu yerga o'z ID raqamingni yoz (agar xato bo'lsa /myid orqali topib yozasan)
ADMIN_USERNAME = "@sobirvss"

bot = Bot(token=TOKEN)
dp = Dispatcher()

# Bazalar va Tarjimalar lug'ati
users_db = {}

TRANSLATIONS = {
    "uz": {
        "welcome": "<b>🔥 Premium Mafia Botiga Xush Kelibsiz!</b>\n\nEng kuchli, noyob rollar va qiziqarli imkoniyatlarga ega o'yin.",
        "profile": "<b>👤 Foydalanuvchi Profili:</b>\n\n💵 Dollar: <b>{money}</b>\n💎 Olmos: <b>{diamonds}</b>\n🏆 G'alaba: <b>{wins}</b>\n🎮 O'yinlar: <b>{games}</b>\n⭐ Status: <b>{status}</b>",
        "shop": "<b>💎 Olmos va VIP Do'koniga Xush Kelibsiz!</b>\n\nO'yinda ustunlik qilish uchun olmos sotib oling.",
        "lang_changed": "✅ Til O'zbek tiliga o'zgartirildi!",
        "btn_profile": "👤 Profil",
        "btn_shop": "💎 Olmos & Do'kon",
        "btn_lang": "🌐 Tilni tanlash",
        "btn_group": "➕ Guruhga qo'shish",
        "btn_bvg": "⚔️ Boys vs Girls",
        "btn_back": "🔙 Ortga",
        "btn_card": "💳 Karta orqali to'lov",
        "btn_stars": "⭐ Telegram Stars"
    },
    "ru": {
        "welcome": "<b>🔥 Добро пожаловать в Premium Mafia Bot!</b>\n\nЛучшая игра с уникальными ролями и возможностями.",
        "profile": "<b>👤 Профиль пользователя:</b>\n\n💵 Доллары: <b>{money}</b>\n💎 Алмазы: <b>{diamonds}</b>\n🏆 Победы: <b>{wins}</b>\n🎮 Игры: <b>{games}</b>\n⭐ Статус: <b>{status}</b>",
        "shop": "<b>💎 Магазин алмазов и VIP!</b>\n\nПокупайте алмазы для получения преимуществ.",
        "lang_changed": "✅ Язык изменен на Русский!",
        "btn_profile": "👤 Профиль",
        "btn_shop": "💎 Алмазы и Магазин",
        "btn_lang": "🌐 Выбрать язык",
        "btn_group": "➕ Добавить в группу",
        "btn_bvg": "⚔️ Парни против Девушек",
        "btn_back": "🔙 Назад",
        "btn_card": "💳 Оплата картой",
        "btn_stars": "⭐ Telegram Stars"
    },
    "en": {
        "welcome": "<b>🔥 Welcome to Premium Mafia Bot!</b>\n\nThe ultimate mafia game with unique roles and features.",
        "profile": "<b>👤 User Profile:</b>\n\n💵 Money: <b>{money}</b>\n💎 Diamonds: <b>{diamonds}</b>\n🏆 Wins: <b>{wins}</b>\n🎮 Games: <b>{games}</b>\n⭐ Status: <b>{status}</b>",
        "shop": "<b>💎 Diamond & VIP Shop!</b>\n\nBuy diamonds to get exclusive privileges.",
        "lang_changed": "✅ Language changed to English!",
        "btn_profile": "👤 Profile",
        "btn_shop": "💎 Diamonds & Shop",
        "btn_lang": "🌐 Change Language",
        "btn_group": "➕ Add to Group",
        "btn_bvg": "⚔️ Boys vs Girls",
        "btn_back": "🔙 Back",
        "btn_card": "💳 Pay via Card",
        "btn_stars": "⭐ Telegram Stars"
    }
}

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

def get_keyboard(lang="uz"):
    t = TRANSLATIONS.get(lang, TRANSLATIONS["uz"])
    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(text=t["btn_lang"], callback_data="set_lang"))
    bot_info = asyncio.run(bot.get_me()) if False else None # oddiy usul
    builder.row(types.InlineKeyboardButton(text=t["btn_group"], url=f"https://t.me/sobirvss_bot?startgroup=true")) #usernameni o'zingnikiga mosla
    builder.row(
        types.InlineKeyboardButton(text=t["btn_profile"], callback_data="profile"),
        types.InlineKeyboardButton(text=t["btn_shop"], callback_data="shop")
    )
    builder.row(types.InlineKeyboardButton(text=t["btn_bvg"], callback_data="bvg_info"))
    return builder.as_markup()

# ID ni aniqlash uchun buyruq
@dp.message(Command("myid"))
async def cmd_myid(message: types.Message):
    await message.reply(f"Sizning Telegram ID raqamingiz: <code>{message.from_user.id}</code>", parse_mode="HTML")

# Start
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    user = get_user(message.from_user.id)
    t = TRANSLATIONS[user["lang"]]
    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(text=t["btn_lang"], callback_data="set_lang"))
    builder.row(types.InlineKeyboardButton(text=t["btn_group"], url="https://t.me/sobirvss_bot?startgroup=true"))
    builder.row(
        types.InlineKeyboardButton(text=t["btn_profile"], callback_data="profile"),
        types.InlineKeyboardButton(text=t["btn_shop"], callback_data="shop")
    )
    builder.row(types.InlineKeyboardButton(text=t["btn_bvg"], callback_data="bvg_info"))

    await message.answer(t["welcome"], reply_markup=builder.as_markup(), parse_mode="HTML")

# Profil
@dp.message(Command("profile"))
async def cmd_profile(message: types.Message):
    user = get_user(message.from_user.id)
    t = TRANSLATIONS[user["lang"]]
    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(text=t["btn_card"], callback_data="pay_card"))
    builder.row(types.InlineKeyboardButton(text=t["btn_back"], callback_data="back_home"))

    text = t["profile"].format(
        money=user['money'], diamonds=user['diamonds'],
        wins=user['wins'], games=user['games'], status=user['role_status'].upper()
    ) + f"\n\n<i>Creator: {ADMIN_USERNAME}</i>"
    await message.answer(text, reply_markup=builder.as_markup(), parse_mode="HTML")

# Shop
@dp.message(Command("shop"))
async def cmd_shop(message: types.Message):
    user = get_user(message.from_user.id)
    t = TRANSLATIONS[user["lang"]]
    builder = InlineKeyboardBuilder()
    builder.row(
        types.InlineKeyboardButton(text=t["btn_stars"], callback_data="pay_stars"),
        types.InlineKeyboardButton(text=t["btn_card"], callback_data="pay_card")
    )
    builder.row(types.InlineKeyboardButton(text=t["btn_back"], callback_data="back_home"))
    await message.answer(t["shop"], reply_markup=builder.as_markup(), parse_mode="HTML")

# Admin panel
@dp.message(Command("admin"))
async def cmd_admin(message: types.Message):
    if message.from_user.id != ADMIN_ID:
        await message.reply(f"❌ Xatolik! Sizning ID ({message.from_user.id}) adminlar ro'yxatida yo'q. Botga /myid yozib ID raqamingizni aniqlang.")
        return
    
    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(text="📊 Statistikani ko'rish", callback_data="admin_stats"))
    await message.answer("<b>👑 Xush kelibsiz, Boss!</b>\nAdmin panel:", reply_markup=builder.as_markup(), parse_mode="HTML")

# Til tanlash menyusi
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
    t = TRANSLATIONS[lang]
    await callback.answer(t["lang_changed"], show_alert=True)
    
    # Asosiy oynani yangi tilda chiqarish
    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(text=t["btn_lang"], callback_data="set_lang"))
    builder.row(types.InlineKeyboardButton(text=t["btn_group"], url="https://t.me/sobirvss_bot?startgroup=true"))
    builder.row(
        types.InlineKeyboardButton(text=t["btn_profile"], callback_data="profile"),
        types.InlineKeyboardButton(text=t["btn_shop"], callback_data="shop")
    )
    builder.row(types.InlineKeyboardButton(text=t["btn_bvg"], callback_data="bvg_info"))
    await callback.message.edit_text(t["welcome"], reply_markup=builder.as_markup(), parse_mode="HTML")

@dp.callback_query(F.data == "profile")
async def show_profile_cb(callback: types.CallbackQuery):
    user = get_user(callback.from_user.id)
    t = TRANSLATIONS[user["lang"]]
    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(text=t["btn_card"], callback_data="pay_card"))
    builder.row(types.InlineKeyboardButton(text=t["btn_back"], callback_data="back_home"))

    text = t["profile"].format(
        money=user['money'], diamonds=user['diamonds'],
        wins=user['wins'], games=user['games'], status=user['role_status'].upper()
    ) + f"\n\n<i>Creator: {ADMIN_USERNAME}</i>"
    await callback.message.edit_text(text, reply_markup=builder.as_markup(), parse_mode="HTML")
    await callback.answer()

@dp.callback_query(F.data == "shop")
async def shop_menu_cb(callback: types.CallbackQuery):
    user = get_user(callback.from_user.id)
    t = TRANSLATIONS[user["lang"]]
    builder = InlineKeyboardBuilder()
    builder.row(
        types.InlineKeyboardButton(text=t["btn_stars"], callback_data="pay_stars"),
        types.InlineKeyboardButton(text=t["btn_card"], callback_data="pay_card")
    )
    builder.row(types.InlineKeyboardButton(text=t["btn_back"], callback_data="back_home"))
    await callback.message.edit_text(t["shop"], reply_markup=builder.as_markup(), parse_mode="HTML")
    await callback.answer()

@dp.callback_query(F.data == "pay_card")
async def pay_card_info(callback: types.CallbackQuery):
    user = get_user(callback.from_user.id)
    t = TRANSLATIONS[user["lang"]]
    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(text=t["btn_back"], callback_data="shop"))
    
    text = (
        "<b>💳 Karta orqali to'lov qilish / Payment via Card:</b>\n\n"
        "Quyidagi kartalarga to'lov qilib, chekni adminga yuboring:\n\n"
        f"🇺🇿 <b>Uzcard:</b> <code>9860160623296383</code>\n"
        f"🌍 <b>Visa:</b> <code>4916990359211916</code>\n\n"
        f"👤 <b>Admin:</b> {ADMIN_USERNAME}"
    )
    await callback.message.edit_text(text, reply_markup=builder.as_markup(), parse_mode="HTML")
    await callback.answer()

@dp.callback_query(F.data == "bvg_info")
async def bvg_info_cb(callback: types.CallbackQuery):
    user = get_user(callback.from_user.id)
    t = TRANSLATIONS[user["lang"]]
    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(text=t["btn_back"], callback_data="back_home"))
    text = "<b>⚔️ Boys vs Girls (O'g'il bolalar Qizlarga qarshi)</b>\n\nBu rejim guruhda ishlaydi! Jamoalar bo'linib jang qilishadi."
    await callback.message.edit_text(text, reply_markup=builder.as_markup(), parse_mode="HTML")
    await callback.answer()

@dp.callback_query(F.data == "back_home")
async def back_home_handler(callback: types.CallbackQuery):
    user = get_user(callback.from_user.id)
    t = TRANSLATIONS[user["lang"]]
    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(text=t["btn_lang"], callback_data="set_lang"))
    builder.row(types.InlineKeyboardButton(text=t["btn_group"], url="https://t.me/sobirvss_bot?startgroup=true"))
    builder.row(
        types.InlineKeyboardButton(text=t["btn_profile"], callback_data="profile"),
        types.InlineKeyboardButton(text=t["btn_shop"], callback_data="shop")
    )
    builder.row(types.InlineKeyboardButton(text=t["btn_bvg"], callback_data="bvg_info"))
    await callback.message.edit_text(t["welcome"], reply_markup=builder.as_markup(), parse_mode="HTML")
    await callback.answer()

async def main():
    logging.basicConfig(level=logging.INFO)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
