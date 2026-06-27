from sqlalchemy import text

from database.session import SessionLocal


def test_connection():
    session = SessionLocal()

    try:
        result = session.execute(text("SELECT 1"))

        print(result.scalar())

        print("Connected successfully!")

    finally:
        session.close()


if __name__ == "__main__":
    test_connection()