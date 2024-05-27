import os
import random

import dotenv
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType


def echo(event, api):
    api.messages.send(
        user_id=event.user_id, message=event.text, random_id=random.randint(1, 1000)
    )


def listen_messages(token):
    vk_session = vk_api.VkApi(token=token)
    long_poll = VkLongPoll(vk_session)
    api = vk_session.get_api()
    for event in long_poll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            echo(event, api)


def main():
    dotenv.load_dotenv()

    listen_messages(os.environ["VK_API_KEY"])


if __name__ == "__main__":
    main()
