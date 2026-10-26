-- ==============================================================================
-- SISTEMA DE GESTIÓN Y TRAZABILIDAD DE ÓRDENES DE TRABAJO (UNINORTE)
-- Script DML: Datos iniciales de prueba (Seeds)
-- ==============================================================================

-- 1. Inserción de Roles Base
INSERT INTO roles (id, name, description) VALUES
(1, 'ADMIN', 'Administrador general y recepcionista con acceso total al sistema'),
(2, 'TECNICO', 'Técnico de laboratorio y taller para diagnóstico, reparación y control de calidad')
ON CONFLICT (id) DO NOTHING;

-- 2. Inserción de Usuarios Iniciales
-- Contraseña para admin: admin123
-- Contraseña para tecnico: tecnico123
INSERT INTO users (id, role_id, username, email, password_hash, first_name, last_name, phone, is_active) VALUES
(1, 1, 'admin', 'admin@uninorte.edu.py', 'scrypt:32768:8:1$2LBmo1FOvQ3ktRH4$699d5643582726762b09850e93457c5e9d6e416fc4aba965e44dd7359347bb1ffb7c26a919bfa4d2b76bea2b37f59e71396588786b571b20df6f94b90dbf6bec', 'Carlos', 'Administrador', '0981111222', TRUE),
(2, 2, 'tecnico', 'tecnico@uninorte.edu.py', 'scrypt:32768:8:1$kYo0wrLcdHIGy64y$41a12629c01885591b4dfd73b9977a01938024d481d2073379cc36a5c3f96cd4bec425c8a49a6472484f04aa5c107544af63791073b7ef218d2b55db737f09f2', 'Lucas', 'Técnico Especialista', '0971333444', TRUE)
ON CONFLICT (id) DO NOTHING;

-- 3. Catálogo Inicial de Repuestos
INSERT INTO parts (id, code, name, description, category, cost_price, selling_price, stock_quantity, min_stock_alert) VALUES
(1, 'REP-SSD-512', 'Disco Sólido SSD 512GB NVMe M.2', 'Kingston PCIe 4.0 NVMe', 'Almacenamiento', 220000.00, 320000.00, 10, 2),
(2, 'REP-RAM-8GB', 'Memoria RAM DDR4 8GB 3200MHz', 'Crucial SODIMM para Notebook', 'Memoria', 150000.00, 210000.00, 15, 3),
(3, 'REP-BAT-L15', 'Batería Lenovo IdeaPad 3 / 5', 'Batería original de 3 celdas 45Wh', 'Baterías', 280000.00, 420000.00, 4, 1),
(4, 'REP-PNT-156', 'Pantalla LED 15.6 FHD 30 Pines Slim', 'Display IPS 1920x1080 sin marcos', 'Pantallas', 450000.00, 650000.00, 3, 1),
(5, 'REP-TER-PAST', 'Pasta Térmica Arctic MX-4 4g', 'Compuesto térmico de micropartículas de carbono', 'Insumos', 45000.00, 75000.00, 20, 5)
ON CONFLICT (id) DO NOTHING;

-- 4. Clientes de Prueba
INSERT INTO clients (id, document_number, first_name, last_name, phone, email, address, notes) VALUES
(1, '4567890', 'María', 'González Benítez', '0981987654', 'maria.gonzalez@gmail.com', 'Av. Mcal. López 1234, Asunción', 'Cliente frecuente'),
(2, '3890123', 'Jorge', 'Ramírez Almada', '0972456789', 'jorge.ramirez@hotmail.com', 'Palma e/ Chile, Asunción', 'Atención preferencial')
ON CONFLICT (id) DO NOTHING;

-- Ajustar los contadores seriales de PostgreSQL para evitar conflictos con futuros INSERT
SELECT setval('roles_id_seq', (SELECT MAX(id) FROM roles));
SELECT setval('users_id_seq', (SELECT MAX(id) FROM users));
SELECT setval('parts_id_seq', (SELECT MAX(id) FROM parts));
SELECT setval('clients_id_seq', (SELECT MAX(id) FROM clients));
