"""
Script de Inicialización de Base de Datos
Crea las tablas en PostgreSQL / SQLite y carga los datos semilla (Roles, Usuarios, Repuestos, Clientes).
"""
import sys
from app import create_app
from app.extensions import db
from app.models.user import Role, User
from app.models.client import Client
from app.models.inventory import Part

def initialize_database():
    app = create_app()
    with app.app_context():
        print("=" * 60)
        print("Iniciando creación de tablas en la base de datos...")
        print(f"URI de conexión: {app.config['SQLALCHEMY_DATABASE_URI']}")
        print("=" * 60)

        try:
            db.create_all()
            print("[OK] Tablas creadas exitosamente.")
        except Exception as e:
            print(f"[ERROR] Error al crear tablas: {e}")
            sys.exit(1)

        # Cargar datos semilla si no existen
        try:
            # 1. Roles
            admin_role = Role.query.filter_by(name='ADMIN').first()
            if not admin_role:
                admin_role = Role(id=1, name='ADMIN', description='Administrador y recepcionista')
                tech_role = Role(id=2, name='TECNICO', description='Técnico de laboratorio y reparación')
                db.session.add(admin_role)
                db.session.add(tech_role)
                db.session.commit()
                print("[OK] Roles iniciales registrados (ADMIN, TECNICO).")

            # 2. Usuarios
            admin_user = User.query.filter_by(username='admin').first()
            if not admin_user:
                admin_user = User(
                    role_id=1,
                    username='admin',
                    email='admin@uninorte.edu.py',
                    first_name='Carlos',
                    last_name='Administrador',
                    phone='0981111222'
                )
                admin_user.set_password('admin123')
                db.session.add(admin_user)

                tech_user = User(
                    role_id=2,
                    username='tecnico',
                    email='tecnico@uninorte.edu.py',
                    first_name='Lucas',
                    last_name='Técnico Especialista',
                    phone='0971333444'
                )
                tech_user.set_password('tecnico123')
                db.session.add(tech_user)

                db.session.commit()
                print("[OK] Usuarios iniciales creados:")
                print("    - Admin:   usuario 'admin'   / contraseña 'admin123'")
                print("    - Técnico: usuario 'tecnico' / contraseña 'tecnico123'")

            # 3. Repuestos iniciales
            if Part.query.count() == 0:
                parts = [
                    Part(code='REP-SSD-512', name='Disco Sólido SSD 512GB NVMe M.2', description='Kingston PCIe 4.0 NVMe', category='Almacenamiento', cost_price=220000, selling_price=320000, stock_quantity=10, min_stock_alert=2),
                    Part(code='REP-RAM-8GB', name='Memoria RAM DDR4 8GB 3200MHz', description='Crucial SODIMM para Notebook', category='Memoria', cost_price=150000, selling_price=210000, stock_quantity=15, min_stock_alert=3),
                    Part(code='REP-BAT-L15', name='Batería Lenovo IdeaPad 3 / 5', description='Batería original de 3 celdas 45Wh', category='Baterías', cost_price=280000, selling_price=420000, stock_quantity=4, min_stock_alert=1),
                    Part(code='REP-PNT-156', name='Pantalla LED 15.6 FHD 30 Pines Slim', description='Display IPS 1920x1080 sin marcos', category='Pantallas', cost_price=450000, selling_price=650000, stock_quantity=3, min_stock_alert=1),
                    Part(code='REP-TER-PAST', name='Pasta Térmica Arctic MX-4 4g', description='Compuesto térmico de alta disipación', category='Insumos', cost_price=45000, selling_price=75000, stock_quantity=20, min_stock_alert=5)
                ]
                db.session.bulk_save_objects(parts)
                db.session.commit()
                print("[OK] Catálogo inicial de repuestos cargado en inventario.")

            # 4. Clientes de prueba
            if Client.query.count() == 0:
                clients = [
                    Client(document_number='4567890', first_name='María', last_name='González Benítez', phone='0981987654', email='maria.gonzalez@gmail.com', address='Av. Mcal. López 1234, Asunción', notes='Cliente frecuente'),
                    Client(document_number='3890123', first_name='Jorge', last_name='Ramírez Almada', phone='0972456789', email='jorge.ramirez@hotmail.com', address='Palma e/ Chile, Asunción', notes='Atención preferencial')
                ]
                db.session.bulk_save_objects(clients)
                db.session.commit()
                print("[OK] Clientes de prueba registrados.")

            print("=" * 60)
            print("Base de datos lista para operar!")
            print("=" * 60)

        except Exception as e:
            db.session.rollback()
            print(f"[ERROR] Error durante la carga de datos semilla: {e}")

if __name__ == '__main__':
    initialize_database()
