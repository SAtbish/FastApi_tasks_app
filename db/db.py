import os

from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase
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
    )

    exit(404)

DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_USER = os.getenv("DB_USER")
DB_PSW = os.getenv("DB_PSW")
DB_NAME = os.getenv("DB_NAME")


engine = create_async_engine(f"postgresql+asyncpg://{DB_USER}:{DB_PSW}@{DB_HOST}:{DB_PORT}/{DB_NAME}")
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)


class Base(DeclarativeBase):
    pass


async def get_async_session():
    async with async_session_maker() as session:
        yield session
