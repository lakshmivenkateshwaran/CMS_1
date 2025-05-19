from dotenv import load_dotenv
import os

load_dotenv()  # Load env variables

class Settings:
    MAIL_USERNAME = os.getenv("MAIL_USERNAME")
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")
    MAIL_FROM = os.getenv("MAIL_FROM")
    MAIL_FROM_NAME = os.getenv("MAIL_FROM_NAME")
    MAIL_PORT = int(os.getenv("MAIL_PORT", 587))
    MAIL_SERVER = os.getenv("MAIL_SERVER")
    MAIL_STARTTLS = os.getenv("MAIL_STARTTLS", "True") == "True"
    MAIL_SSL_TLS = os.getenv("MAIL_SSL_TLS", "False") == "True"
    USE_CREDENTIALS = os.getenv("USE_CREDENTIALS", "True") == "True"
    VALIDATE_CERTS = os.getenv("VALIDATE_CERTS", "True") == "True"
    SECRET_KEY = os.getenv("SECRET_KEY", "default_secret_key")

settings = Settings()
