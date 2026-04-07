from dataclasses import dataclass
import os


@dataclass
class Settings:
    app_name: str = "SuburbRank"
    environment: str = os.getenv("ENVIRONMENT", "development")
    database_url: str = os.getenv("DATABASE_URL", "sqlite:///./suburbrank.db")
    stripe_secret_key: str = os.getenv("STRIPE_SECRET_KEY", "")
    stripe_price_id: str = os.getenv("STRIPE_PRICE_ID", "")
    stripe_webhook_secret: str = os.getenv("STRIPE_WEBHOOK_SECRET", "")
    app_base_url: str = os.getenv("APP_BASE_URL", "http://localhost:8000")


settings = Settings()
