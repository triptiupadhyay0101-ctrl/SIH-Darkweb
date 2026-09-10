import os

from dotenv import load_dotenv
from sqlalchemy import create_engine

load_dotenv()


DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError(
        "DATABASE_URL is not set. Please create a .env file."
    )


engine = create_engine(
    DATABASE_URL
)


def test_connection():
    with engine.connect():
        print("Database connection successful!")


if __name__ == "__main__":
    test_connection()