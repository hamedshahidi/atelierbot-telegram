import os
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram import Router
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.enums import ParseMode
import asyncio
from dotenv import load_dotenv

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_CHAT_ID = os.getenv("ADMIN_CHAT_ID")

if not BOT_TOKEN:
    raise RuntimeError("BOT_TOKEN is required in .env")

bot = Bot(BOT_TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher()
router = Router()
dp.include_router(router)

def main_menu_kb():
    kb = InlineKeyboardBuilder()
    kb.button(text="📦 پکیج‌ها", callback_data="menu:packages")
    kb.button(text="🖼 نمونه‌کارها", callback_data="menu:samples")
    kb.button(text="🗓 رزرو تاریخ", callback_data="menu:booking")
    kb.button(text="📞 تماس", callback_data="menu:contact")
    kb.adjust(2, 2)
    return kb.as_markup()

@router.message(CommandStart())
async def on_start(message: Message):
    source = message.text.split(" ", 1)[1] if len(message.text.split(" ", 1)) > 1 else ""
    welcome_fa = (
        "سلام 🌿 خوش اومدی به آتلیه شما!\n"
        "از دکمه‌های زیر انتخاب کن:\n"
        "📦 پکیج‌ها | 🖼 نمونه‌کارها | 🗓 رزرو تاریخ | 📞 تماس"
    )
    await message.answer(welcome_fa, reply_markup=main_menu_kb())
    # Optional: notify admin about new start
    try:
        if ADMIN_CHAT_ID:
            await bot.send_message(int(ADMIN_CHAT_ID), f"👤 Start: @{message.from_user.username} (source: {source})")
    except Exception:
        pass

@router.callback_query(F.data == "menu:packages")
async def cb_packages(call: CallbackQuery):
    text = (
        "📦 <b>پکیج‌ها</b>\n"
        "نوع مراسم رو انتخاب کن:\n"
        "• عروسی\n• تولد\n• پرتره"
    )
    kb = InlineKeyboardBuilder()
    kb.button(text="💍 عروسی", callback_data="pkg:wedding")
    kb.button(text="🎉 تولد", callback_data="pkg:birthday")
    kb.button(text="🧑‍🎨 پرتره", callback_data="pkg:portrait")
    kb.button(text="⬅️ بازگشت", callback_data="menu:home")
    kb.adjust(2, 1, 1)
    await call.message.edit_text(text, reply_markup=kb.as_markup())

@router.callback_query(F.data == "menu:samples")
async def cb_samples(call: CallbackQuery):
    text = (
        "🖼 <b>نمونه‌کارها</b>\n"
        "سبک مورد نظر رو انتخاب کن تا آلبوم تلگرام باز بشه."
    )
    kb = InlineKeyboardBuilder()
    kb.button(text="💍 عروسی کلاسیک", url="https://t.me/YourChannel/1")
    kb.button(text="🏙 شهری تهران", url="https://t.me/YourChannel/2")
    kb.button(text="🏜 کویر", url="https://t.me/YourChannel/3")
    kb.button(text="🌲 جنگل شمال", url="https://t.me/YourChannel/4")
    kb.button(text="⬅️ بازگشت", callback_data="menu:home")
    kb.adjust(2, 2, 1)
    await call.message.edit_text(text, reply_markup=kb.as_markup())

@router.callback_query(F.data == "menu:booking")
async def cb_booking(call: CallbackQuery):
    text = (
        "🗓 <b>رزرو تاریخ</b>\n"
        "لطفاً نوع مراسم و شهر رو در پیام بعدی بفرست یا از گزینه‌های زیر انتخاب کن."
    )
    kb = InlineKeyboardBuilder()
    kb.button(text="💍 عروسی", callback_data="book:type:wedding")
    kb.button(text="🎉 تولد", callback_data="book:type:birthday")
    kb.button(text="🧑‍🎨 پرتره", callback_data="book:type:portrait")
    kb.button(text="⬅️ بازگشت", callback_data="menu:home")
    kb.adjust(3, 1)
    await call.message.edit_text(text, reply_markup=kb.as_markup())

@router.callback_query(F.data == "menu:contact")
async def cb_contact(call: CallbackQuery):
    text = (
        "📞 <b>تماس</b>\n"
        "برای تماس مستقیم:\n"
        "tel:+989000000000\n\n"
        "یا از طریق دکمه زیر شماره‌ت رو ارسال کن تا باهات تماس بگیریم."
    )
    # Telegram request_contact works with ReplyKeyboard, not Inline; here we give tel link.
    kb = InlineKeyboardBuilder()
    kb.button(text="⬅️ بازگشت", callback_data="menu:home")
    await call.message.edit_text(text, reply_markup=kb.as_markup())

@router.callback_query(F.data == "menu:home")
async def cb_home(call: CallbackQuery):
    await call.message.edit_text("منوی اصلی:", reply_markup=main_menu_kb())

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

