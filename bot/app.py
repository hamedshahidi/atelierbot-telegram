import os
import asyncio
import logging

from dotenv import load_dotenv

from aiogram import Bot, Dispatcher, F, Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

load_dotenv()

# ---- Logging (see what's happening) ----
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s"
)
log = logging.getLogger("atelierbot")

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_CHAT_ID = os.getenv("ADMIN_CHAT_ID")

if not BOT_TOKEN:
    raise RuntimeError("BOT_TOKEN is required in .env")

bot = Bot(BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
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


# ---------- Commands ----------

@router.message(CommandStart())
async def on_start(message: Message):
    # Track source param if present
    parts = message.text.split(" ", 1)
    source = parts[1] if len(parts) > 1 else ""
    log.info(f"/start from @{message.from_user.username} id={message.from_user.id} source='{source}'")

    welcome_fa = (
        "سلام 🌿 خوش اومدی به آتلیه شما!\n"
        "از دکمه‌های زیر انتخاب کن:"
    )
    await message.answer(welcome_fa, reply_markup=main_menu_kb())

    # Optional admin ping
    if ADMIN_CHAT_ID:
        try:
            await bot.send_message(
                int(ADMIN_CHAT_ID),
                f"👤 Start by @{message.from_user.username or 'user'} (id: {message.from_user.id}) source: {source}"
            )
        except Exception as e:
            log.warning(f"Failed to notify admin: {e}")


@router.message(Command("ping"))
async def on_ping(message: Message):
    await message.answer("pong ✅")


# Quick text trigger to reopen menu
@router.message(F.text.lower() == "menu")
async def on_menu_text(message: Message):
    await message.answer("منوی اصلی:", reply_markup=main_menu_kb())


# ---------- Callback handlers ----------

@router.callback_query(F.data == "menu:packages")
async def cb_packages(call: CallbackQuery):
    await call.answer()  # acknowledge
    text = (
        "📦 <b>پکیج‌ها</b>\n"
        "نوع مراسم رو انتخاب کن:"
    )
    kb = InlineKeyboardBuilder()
    kb.button(text="💍 عروسی", callback_data="pkg:wedding")
    kb.button(text="🎉 تولد", callback_data="pkg:birthday")
    kb.button(text="🧑‍🎨 پرتره", callback_data="pkg:portrait")
    kb.button(text="⬅️ بازگشت", callback_data="menu:home")
    kb.adjust(2, 2)
    await call.message.edit_text(text, reply_markup=kb.as_markup())


@router.callback_query(F.data == "menu:samples")
async def cb_samples(call: CallbackQuery):
    await call.answer()
    text = (
        "🖼 <b>نمونه‌کارها</b>\n"
        "سبک مورد نظر رو انتخاب کن تا آلبوم تلگرام باز بشه."
    )
    kb = InlineKeyboardBuilder()
    # TODO: replace with your real channel post URLs
    kb.button(text="💍 عروسی کلاسیک", url="https://t.me/YourChannel/1")
    kb.button(text="🏙 شهری تهران", url="https://t.me/YourChannel/2")
    kb.button(text="🏜 کویر", url="https://t.me/YourChannel/3")
    kb.button(text="🌲 جنگل شمال", url="https://t.me/YourChannel/4")
    kb.button(text="⬅️ بازگشت", callback_data="menu:home")
    kb.adjust(2, 2, 1)
    await call.message.edit_text(text, reply_markup=kb.as_markup())


@router.callback_query(F.data == "menu:booking")
async def cb_booking(call: CallbackQuery):
    await call.answer()
    text = (
        "🗓 <b>رزرو تاریخ</b>\n"
        "یکی از گزینه‌ها رو انتخاب کن (نسخه ساده)."
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
    await call.answer()
    text = (
        "📞 <b>تماس</b>\n"
        "برای تماس مستقیم: tel:+989000000000\n\n"
        "یا از طریق دکمه زیر شماره‌ت رو ارسال کن تا باهات تماس بگیریم."
    )
    kb = InlineKeyboardBuilder()
    kb.button(text="⬅️ بازگشت", callback_data="menu:home")
    await call.message.edit_text(text, reply_markup=kb.as_markup())


@router.callback_query(F.data == "menu:home")
async def cb_home(call: CallbackQuery):
    await call.answer()
    await call.message.edit_text("منوی اصلی:", reply_markup=main_menu_kb())


# ---------- App entry ----------

async def main():
    # sanity check: token & identity
    me = await bot.get_me()
    log.info(f"Starting polling as @{me.username} (id={me.id})")
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        log.info("Bot stopped.")
