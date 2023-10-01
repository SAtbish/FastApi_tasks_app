import os
from dotenv import load_dotenv

if not load_dotenv():
    print(
        "❗ Для корректной работы приложения необходим .env файл"
        "\n\nПуть до файла: ./<your_project>/.env"
        "\n\n📄 Структура файла 📄:"
        "\n# DB CONFIG"
        "\nDB_HOST={DB_HOST}"
        "\nDB_PORT={DB_PORT}"
        "\nDB_USER={DB_USER}"
        "\nDB_PSW={DB_PSW}"
        "\nDB_NAME={DB_NAME}"
        "\n\n#REDIS CONFIG"
        "\nREDIS_NAME={REDIS_NAME}"
        "\nREDIS_HOST={REDIS_HOST}"
        "\nREDIS_PORT={REDIS_PORT}"
        "\nREDIS_DB={REDIS_DB}"
        "\nREDISMAXPULL={REDISMAXPULL}"
        "\n\nTOKEN_UPDATE_TIME={TOKEN_UPDATE_TIME}"
        "\n\n#SMTP CONFIG"
        "\nEMAIL_SENDER={EMAIL_SENDER}"
        "\nSMTP_PASSWORD={SMTP_PASSWORD}"
    )

    exit(404)

DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_USER = os.getenv("DB_USER")
DB_PSW = os.getenv("DB_PSW")
DB_NAME = os.getenv("DB_NAME")

TOKEN_UPDATE_TIME = int(os.getenv("TOKEN_UPDATE_TIME"))

REDIS_NAME = os.getenv("REDIS_NAME")
REDIS_HOST = os.getenv("REDIS_HOST")
REDIS_PORT = os.getenv("REDIS_PORT")
REDIS_DB = os.getenv("REDIS_DB")
REDISMAXPULL = os.getenv("REDISMAXPULL")
REDIS_NOTIFICATIONS_KEY = os.getenv("REDIS_NOTIFICATIONS_KEY")

EMAIL_SENDER = os.getenv("EMAIL_SENDER")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")
