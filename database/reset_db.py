from database.base import Base
from database.connection import engine

# Import tất cả models để Base.metadata biết các table
from models import *


def reset_database():
    print("Dropping tables...")
    Base.metadata.drop_all(bind=engine)

    print("Creating tables...")
    Base.metadata.create_all(bind=engine)

    print("Done!")


if __name__ == "__main__":
    reset_database()