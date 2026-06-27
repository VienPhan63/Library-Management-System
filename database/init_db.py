from database.base import Base
from database.connection import engine

# Import tất cả model
from models import *

def create_tables():
    print("Creating tables...")

    Base.metadata.create_all(bind=engine)

    print("Done.")

if __name__ == "__main__":
    create_tables()