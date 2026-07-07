from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    DB_URL: str | None = None
    DB_HOST: str | None = None
    DB_PORT: int = 3306
    DB_NAME: str | None = None
    DB_USER: str | None = None
    DB_PASSWORD: str | None = None
    DB_SSL: bool = False
    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore"
    )

    @property
    def database_url(self) -> str:
        if self.DB_URL:
            return self.DB_URL

        missing = [
            name for name, value in {
                "DB_HOST": self.DB_HOST,
                "DB_NAME": self.DB_NAME,
                "DB_USER": self.DB_USER,
                "DB_PASSWORD": self.DB_PASSWORD,
            }.items()
            if not value
        ]

        if missing:
            raise ValueError(
                "Missing database configuration: " + ", ".join(missing)
            )

        return (
            f"mysql+pymysql://{self.DB_USER}:{self.DB_PASSWORD}"
            f"@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        )


settings = Settings()
