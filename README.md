# support-bot
Vk и [telegram](t.me/MyCloudSupportBot) чат-боты, который отвечают на типичные вопросы.
Используется [DialogFlow](https://dialogflow.cloud.google.com/#/getStarted) для обработки текстовых запросов.

![support_bot](https://github.com/shadowsking/support-bot/assets/21194893/108cdaa8-2950-4160-ac5c-72abb851b637)

### Установка

```bash
git clone https://github.com/shadowsking/support-bot.git
```

Создайте виртуальное окружение

Windows:
```bash
python3 -m venv venv
source venv/scripts/activate
```
Linux:
```bash
python3 -m venv venv
source venv/bin/activate
```

Установите зависимости
```bash
pip install -r requirements.txt
```

Создайте '.env' файл и установите следующие аргументы:
- TELEGRAM_TOKEN
- TELEGRAM_LOGGER_TOKEN
- TELEGRAM_CHAT_ID
- VK_API_KEY
- GOOGLE_CLOUD_PROJECT
- GOOGLE_APPLICATION_CREDENTIALS

### Запуск

#### Обучение
Для обучения модели нужно заполнить questions.json и запустить:
```bash
python dialog_flow.py -f questions.json
```

#### Telegram бот:
```bash
python telegram_bot.py
```

##### VK бот:
```bash
python vk_bot.py
```
