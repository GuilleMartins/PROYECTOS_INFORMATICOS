
import os
from app import create_app

app = create_app()

if __name__ == "__main__":
    print(
        "Iniciando Sistema de Gestión y "
        "Trazabilidad de Servicio Técnico (UNINORTE)..."
    )

    debug_mode = (
        os.environ.get("FLASK_DEBUG", "0") == "1"
    )

    app.run(
        host="127.0.0.1",
        port=5000,
        debug=debug_mode
    )
