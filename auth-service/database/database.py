import sys

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from ..config.config import FastAPIConfig

engine = create_engine(
    FastAPIConfig.DATABASE_URL,
    connect_args={
        "sslmode": "require",
        "sslrootcert": FastAPIConfig.CERTIFICATE_PATH,
    },
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
# Base.metadata.create_all(bind=engine)
