import os

import dotenv
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType


def listen_messages(token):
    vk_session = vk_api.VkApi(token=token)
    long_poll = VkLongPoll(vk_session)

    for event in long_poll.listen():
        if event.type == VkEventType.MESSAGE_NEW:
            if event.to_me:
                print("Для меня от:", event.user_id)
            else:
                print("От меня для:", event.user_id)

            print("Текст:", event.text)


def main():
    dotenv.load_dotenv()

    listen_messages(os.environ["VK_API_KEY"])


if __name__ == "__main__":
    main()
