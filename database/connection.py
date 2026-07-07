from sqlalchemy import create_engine

from config.settings import settings

DATABASE_URL = settings.database_url

engine = create_engine(
    DATABASE_URL,

    echo=False,

    pool_pre_ping=True,

    pool_recycle=3600,

    connect_args={"ssl": {}} if settings.DB_SSL else {},

    future=True
)
