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
        "\nTOKEN_UPDATE_TIME={TOKEN_UPDATE_TIME}"
    )

    exit(404)

DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_USER = os.getenv("DB_USER")
DB_PSW = os.getenv("DB_PSW")
DB_NAME = os.getenv("DB_NAME")

TOKEN_UPDATE_TIME = int(os.getenv("TOKEN_UPDATE_TIME"))