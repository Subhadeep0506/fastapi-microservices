import os

from dotenv import load_dotenv

from ..utils.infisical import InfisicalManagedCredentials

loaded_env = load_dotenv()

if not loaded_env:
    raise ValueError("Failed to load environment variables from .env file.")


class FastAPIConfig:
    creds = InfisicalManagedCredentials()
    creds_loaded = creds()
    if not creds_loaded:
        raise ValueError("Failed to fetch confiurations from Infisical.")
    DATABASE_URL: str = os.environ["DATABASE_URL"]
    ACCESS_TOKEN_EXPIRE_MINUTES = 30
    REFRESH_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7
    ALGORITHM = "HS256"
    JWT_SECRET_KEY = os.environ["JWT_SECRET_KEY"]
    JWT_REFRESH_SECRET_KEY = os.environ["JWT_REFRESH_SECRET_KEY"]
