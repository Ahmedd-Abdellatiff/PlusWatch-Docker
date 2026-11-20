import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    DATABASE_URL = os.getenv(
        "DATABASE_URL",
        "postgresql://pulseuser:your_password_here@db:5432/pulsewatch"
    )

    CHECK_INTERVAL = int(os.getenv("CHECK_INTERVAL", 60))

    REQUEST_TIMEOUT = int(os.getenv("REQUEST_TIMEOUT", 10))


settings = Settings()