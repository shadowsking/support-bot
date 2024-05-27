import os
import random

import dotenv
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType

from dialog_flow import detect_intent_by_text


def reply_text(event, api, message) -> None:
    api.messages.send(
        user_id=event.user_id, message=message, random_id=random.randint(1, 1000)
    )


def listen_messages(token) -> None:
    vk_session = vk_api.VkApi(token=token)
    long_poll = VkLongPoll(vk_session)
    api = vk_session.get_api()
    for event in long_poll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            text = detect_intent_by_text(
                project_id=os.environ["GOOGLE_CLOUD_PROJECT"],
                session_id=event.message_id,
                text=event.text,
                language_code="ru-RU",
            )
            if not text:
                continue

            reply_text(event, api, text)


def main() -> None:
    dotenv.load_dotenv()

    listen_messages(os.environ["VK_API_KEY"])


if __name__ == "__main__":
    main()
