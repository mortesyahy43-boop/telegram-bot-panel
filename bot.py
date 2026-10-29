import os
import logging

from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
)

logging.basicConfig(level=logging.INFO)

TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID", "0"))

users = set()


def main_menu():
    keyboard = [
        [
            InlineKeyboardButton("👤 حساب کاربری", callback_data="profile"),
            InlineKeyboardButton("ℹ️ درباره ما", callback_data="about"),
        ],
        [
            InlineKeyboardButton("📞 پشتیبانی", callback_data="support"),
        ],
    ]
    return InlineKeyboardMarkup(keyboard)


async def start(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):
    user = update.effective_user
    users.add(user.id)

    await update.message.reply_text(
        f"سلام {user.first_name} عزیز! 👋\n\n"
        "به ربات ما خوش اومدی 🤖\n"
        "از منوی زیر استفاده کن:",
        reply_markup=main_menu(),
    )


async def button_handler(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):
    query = update.callback_query
    await query.answer()

    if query.data == "profile":
        await query.edit_message_text(
            f"👤 حساب کاربری\n\n"
            f"شناسه شما: {query.from_user.id}",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton(
                    "🔙 بازگشت",
                    callback_data="home",
                )]
            ]),
        )

    elif query.data == "about":
        await query.edit_message_text(
            "🤖 این ربات با پایتون ساخته شده است.",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton(
                    "🔙 بازگشت",
                    callback_data="home",
                )]
            ]),
        )

    elif query.data == "support":
        await query.edit_message_text(
            "📞 برای پشتیبانی با مدیر ربات تماس بگیر.",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton(
                    "🔙 بازگشت",
                    callback_data="home",
                )]
            ]),
        )

    elif query.data == "home":
        await query.edit_message_text(
            "🏠 منوی اصلی ربات:",
            reply_markup=main_menu(),
        )


async def admin(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):
    if update.effective_user.id != ADMIN_ID or ADMIN_ID == 0:
        await update.message.reply_text(
            "⛔ شما اجازه دسترسی ندارید."
        )
        return

    await update.message.reply_text(
        f"⚙️ پنل مدیریت\n\n"
        f"👥 کاربران ثبت‌شده از زمان اجرای ربات: {len(users)}"
    )


def main():
    if not TOKEN:
        raise RuntimeError(
            "لطفاً متغیر محیطی BOT_TOKEN را تنظیم کنید."
        )

    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("admin", admin))
    app.add_handler(
        CallbackQueryHandler(button_handler)
    )

    print("Bot is running...")
    app.run_polling()


if __name__ == "__main__":
    main()