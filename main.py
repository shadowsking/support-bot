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


def echo(update: Update, context: CallbackContext) -> None:
    text = detect_intent_by_text(
        project_id=os.environ["DIALOG_FLOW_PROJECT_ID"],
        session_id=1,
        text=update.message.text,
        language_code="ru-RU",
    )
    update.message.reply_text(text)


def main() -> None:
    dotenv.load_dotenv()
    updater = Updater(os.getenv("TELEGRAM_TOKEN"))

    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_command))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))

    updater.start_polling()

    updater.idle()


if __name__ == "__main__":
    main()
