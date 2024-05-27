import logging
import os

import dotenv
from telegram import Update, ForceReply
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    CallbackContext,
)

from dialog_flow import detect_intent_by_text

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

logger = logging.getLogger(__name__)


def start(update: Update, context: CallbackContext) -> None:
    user = update.effective_user
    update.message.reply_markdown_v2(
        rf"Hi {user.mention_markdown_v2()}\!",
        reply_markup=ForceReply(selective=True),
    )


def help_command(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("Help!")


def reply_text(update: Update, context: CallbackContext) -> None:
    text = detect_intent_by_text(
        project_id=os.environ["GOOGLE_CLOUD_PROJECT"],
        session_id=update.message.chat_id,
        text=update.message.text,
        language_code="ru-RU",
    )
    if not text:
        return

    update.message.reply_text(text)


def main() -> None:
    dotenv.load_dotenv()
    updater = Updater(os.getenv("TELEGRAM_TOKEN"))

    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_command))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, reply_text))

    updater.start_polling()

    updater.idle()


if __name__ == "__main__":
    main()
