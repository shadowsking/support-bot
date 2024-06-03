import logging
import os

import dotenv
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType

from dialog_flow import detect_intent_by_text
from handlers import TelegramLogsHandler

logger = logging.getLogger(__name__)


def reply_text(event, api, message) -> None:
    api.messages.send(
        user_id=event.user_id, message=message, random_id=vk_api.utils.get_random_id()
    )


def main() -> None:
    dotenv.load_dotenv()

    logger.setLevel(logging.WARNING)
    handler = TelegramLogsHandler(
        os.environ["TELEGRAM_LOGGER_TOKEN"], os.environ["TELEGRAM_CHAT_ID"]
    )
    logger.addHandler(handler)

    vk_session = vk_api.VkApi(token=os.environ["VK_API_KEY"])
    long_poll = VkLongPoll(vk_session)
    api = vk_session.get_api()
    for event in long_poll.listen():
        if event.type != VkEventType.MESSAGE_NEW or not event.to_me:
            continue

        try:
            text = detect_intent_by_text(
                project_id=os.environ["GOOGLE_CLOUD_PROJECT"],
                session_id=event.message_id,
                text=event.text,
                language_code="ru-RU",
            )
            if not text:
                continue

            reply_text(event, api, text)
        except Exception as ex:
            logger.exception(ex)


if __name__ == "__main__":
    main()
