
import os
from pathlib import Path
from dotenv import load_dotenv
from sqlalchemy.engine import URL

base_dir = Path(__file__).resolve().parent.parent
load_dotenv(base_dir / ".env")

class Config:
    # La clave debe existir en el entorno
    SECRET_KEY = os.environ["SECRET_KEY"]

    # Protección de cookies
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"
    SESSION_COOKIE_SECURE = (
        os.environ.get("COOKIE_SECURE", "False").lower()
        == "true"
    )

    REMEMBER_COOKIE_HTTPONLY = True
    REMEMBER_COOKIE_SAMESITE = "Lax"
    REMEMBER_COOKIE_SECURE = SESSION_COOKIE_SECURE

    # Base de datos
    USE_SQLITE = os.environ.get(
        "USE_SQLITE_FALLBACK", "True"
    ).lower() in ("true", "1", "t")

    if USE_SQLITE:
        SQLALCHEMY_DATABASE_URI = (
            f"sqlite:///{base_dir / 'instance' / 'serviciotecnico.db'}"
        )
    else:
        SQLALCHEMY_DATABASE_URI = URL.create(
            drivername="postgresql+psycopg2",
            username=os.environ.get("DB_USER", "postgres"),
            password=os.environ["DB_PASSWORD"],
            host=os.environ.get("DB_HOST", "localhost"),
            port=int(os.environ.get("DB_PORT", "5432")),
            database=os.environ.get("DB_NAME", "serviciotecnico_db")
        )

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        "pool_pre_ping": True,
        "pool_recycle": 300,
    }

    QR_FOLDER = base_dir / "app" / "static" / "qr_codes"
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024
