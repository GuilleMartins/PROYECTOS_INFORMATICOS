import os
from pathlib import Path
from dotenv import load_dotenv

# Cargar variables de entorno desde .env
base_dir = Path(__file__).resolve().parent.parent
load_dotenv(base_dir / '.env')

class Config:
    # Seguridad
    SECRET_KEY = os.environ.get('SECRET_KEY', 'clave-dev-uninorte-segura-2026')
    
    # Parámetros de conexión a Base de Datos
    DB_USER = os.environ.get('DB_USER', 'postgres')
    DB_PASSWORD = os.environ.get('DB_PASSWORD', 'postgres')
    DB_HOST = os.environ.get('DB_HOST', 'localhost')
    DB_PORT = os.environ.get('DB_PORT', '5432')
    DB_NAME = os.environ.get('DB_NAME', 'serviciotecnico_db')
    USE_SQLITE = os.environ.get('USE_SQLITE_FALLBACK', 'False').lower() in ('true', '1', 't')

    # URL de SQLAlchemy
    if USE_SQLITE:
        SQLALCHEMY_DATABASE_URI = f"sqlite:///{base_dir / 'instance' / 'serviciotecnico.db'}"
    else:
        SQLALCHEMY_DATABASE_URI = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_pre_ping': True,
        'pool_recycle': 300,
    }

    # Directorio para almacenar códigos QR
    QR_FOLDER = base_dir / 'app' / 'static' / 'qr_codes'
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16 MB max upload
