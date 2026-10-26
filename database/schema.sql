-- ==============================================================================
-- SISTEMA DE GESTIÓN Y TRAZABILIDAD DE ÓRDENES DE TRABAJO (UNINORTE)
-- Script DDL: Creación de Esquema de Base de Datos PostgreSQL
-- ==============================================================================

-- 1. Tabla de Roles de Usuario
CREATE TABLE IF NOT EXISTS roles (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) UNIQUE NOT NULL,
    description VARCHAR(255),
    created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 2. Tabla de Usuarios del Sistema (Administradores, Recepcionistas, Técnicos)
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    role_id INTEGER NOT NULL REFERENCES roles(id) ON DELETE RESTRICT,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(120) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    phone VARCHAR(30),
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 3. Tabla de Clientes
CREATE TABLE IF NOT EXISTS clients (
    id SERIAL PRIMARY KEY,
    document_number VARCHAR(30) UNIQUE NOT NULL, -- Cédula de Identidad o RUC
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    phone VARCHAR(30) NOT NULL,
    email VARCHAR(120),
    address TEXT,
    notes TEXT,
    created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 4. Tabla de Equipos
CREATE TABLE IF NOT EXISTS equipment (
    id SERIAL PRIMARY KEY,
    client_id INTEGER NOT NULL REFERENCES clients(id) ON DELETE RESTRICT,
    equipment_type VARCHAR(50) NOT NULL,   -- Notebook, PC Torre, Smartphone, Impresora, etc.
    brand VARCHAR(60) NOT NULL,
    model VARCHAR(80) NOT NULL,
    serial_number VARCHAR(100),
    physical_condition TEXT,              -- Estado estético al ingresar (rayones, faltantes)
    accessories TEXT,                     -- Cargador, funda, cable USB, etc.
    created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 5. Tabla Principal de Órdenes de Trabajo
CREATE TABLE IF NOT EXISTS orders (
    id SERIAL PRIMARY KEY,
    order_number VARCHAR(20) UNIQUE NOT NULL,          -- Ej: OT-2026-0001
    public_token VARCHAR(36) UNIQUE NOT NULL,          -- UUID v4 para el QR y acceso público seguro
    client_id INTEGER NOT NULL REFERENCES clients(id) ON DELETE RESTRICT,
    equipment_id INTEGER NOT NULL REFERENCES equipment(id) ON DELETE RESTRICT,
    created_by_user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE RESTRICT,
    assigned_tech_id INTEGER REFERENCES users(id) ON DELETE SET NULL,
    reported_failure TEXT NOT NULL,                    -- Problema reportado por el cliente
    current_status VARCHAR(40) NOT NULL DEFAULT 'RECIBIDO', 
    -- Estados permitidos:
    -- RECIBIDO, EN_DIAGNOSTICO, PENDIENTE_APROBACION, PRESUPUESTO_APROBADO, 
    -- EN_REPARACION, EN_CONTROL_CALIDAD, LISTO_ENTREGA, ENTREGADO, CANCELADO
    priority VARCHAR(20) NOT NULL DEFAULT 'NORMAL',    -- BAJA, NORMAL, ALTA, URGENTE
    entry_date TIMESTAMP WITHOUT TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    estimated_delivery_date DATE,
    completion_date TIMESTAMP WITHOUT TIME ZONE,
    delivery_date TIMESTAMP WITHOUT TIME ZONE,
    qr_code_path VARCHAR(255),
    created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Índices para optimizar búsquedas frecuentes
CREATE INDEX IF NOT EXISTS idx_orders_public_token ON orders(public_token);
CREATE INDEX IF NOT EXISTS idx_orders_status ON orders(current_status);
CREATE INDEX IF NOT EXISTS idx_orders_client ON orders(client_id);
CREATE INDEX IF NOT EXISTS idx_orders_tech ON orders(assigned_tech_id);

-- 6. Tabla de Diagnóstico Técnico
CREATE TABLE IF NOT EXISTS diagnostics (
    id SERIAL PRIMARY KEY,
    order_id INTEGER UNIQUE NOT NULL REFERENCES orders(id) ON DELETE CASCADE,
    technician_id INTEGER NOT NULL REFERENCES users(id) ON DELETE RESTRICT,
    findings TEXT NOT NULL,                            -- Diagnóstico detallado
    proposed_solution TEXT NOT NULL,                   -- Trabajos requeridos
    technical_notes TEXT,                              -- Notas internas del técnico
    diagnostic_date TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 7. Tabla de Presupuestos
CREATE TABLE IF NOT EXISTS budgets (
    id SERIAL PRIMARY KEY,
    order_id INTEGER UNIQUE NOT NULL REFERENCES orders(id) ON DELETE CASCADE,
    diagnostic_id INTEGER REFERENCES diagnostics(id) ON DELETE CASCADE,
    total_parts NUMERIC(12, 2) NOT NULL DEFAULT 0.00,
    total_labor NUMERIC(12, 2) NOT NULL DEFAULT 0.00,
    total_amount NUMERIC(12, 2) NOT NULL DEFAULT 0.00,
    status VARCHAR(30) NOT NULL DEFAULT 'PENDIENTE',   -- PENDIENTE, APROBADO, RECHAZADO
    client_notes TEXT,
    decision_date TIMESTAMP WITHOUT TIME ZONE,
    decision_channel VARCHAR(50),                      -- 'PORTAL_QR', 'PRESENCIAL', 'TELEFONICO'
    decision_ip VARCHAR(45),                           -- Registro de auditoría IP
    created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 8. Tabla de Repuestos (Catálogo de Inventario)
CREATE TABLE IF NOT EXISTS parts (
    id SERIAL PRIMARY KEY,
    code VARCHAR(50) UNIQUE NOT NULL,                  -- Código de referencia (ej. REP-PNT-01)
    name VARCHAR(150) NOT NULL,
    description TEXT,
    category VARCHAR(60),
    cost_price NUMERIC(12, 2) NOT NULL DEFAULT 0.00,
    selling_price NUMERIC(12, 2) NOT NULL DEFAULT 0.00,
    stock_quantity INTEGER NOT NULL DEFAULT 0,
    min_stock_alert INTEGER NOT NULL DEFAULT 2,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT chk_stock_non_negative CHECK (stock_quantity >= 0)
);

-- 9. Tabla de Repuestos Utilizados en Presupuesto / Orden
CREATE TABLE IF NOT EXISTS order_parts (
    id SERIAL PRIMARY KEY,
    budget_id INTEGER NOT NULL REFERENCES budgets(id) ON DELETE CASCADE,
    part_id INTEGER NOT NULL REFERENCES parts(id) ON DELETE RESTRICT,
    quantity INTEGER NOT NULL DEFAULT 1,
    unit_price NUMERIC(12, 2) NOT NULL,
    subtotal NUMERIC(12, 2) NOT NULL,
    is_consumed BOOLEAN NOT NULL DEFAULT FALSE,        -- True si ya se descontó del stock real
    created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT chk_qty_positive CHECK (quantity > 0)
);

-- 10. Tabla de Mano de Obra en Presupuesto
CREATE TABLE IF NOT EXISTS order_labor (
    id SERIAL PRIMARY KEY,
    budget_id INTEGER NOT NULL REFERENCES budgets(id) ON DELETE CASCADE,
    description VARCHAR(200) NOT NULL,
    estimated_hours NUMERIC(5, 2),
    price NUMERIC(12, 2) NOT NULL,
    created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 11. Tabla de Movimientos de Inventario (Kardex Básico)
CREATE TABLE IF NOT EXISTS inventory_movements (
    id SERIAL PRIMARY KEY,
    part_id INTEGER NOT NULL REFERENCES parts(id) ON DELETE RESTRICT,
    movement_type VARCHAR(30) NOT NULL,                -- 'ENTRADA', 'SALIDA_REPARACION', 'AJUSTE'
    quantity INTEGER NOT NULL,
    order_id INTEGER REFERENCES orders(id) ON DELETE SET NULL,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE RESTRICT,
    notes TEXT,
    created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 12. Tabla de Historial y Trazabilidad de Estados (Inmutable)
CREATE TABLE IF NOT EXISTS order_status_history (
    id SERIAL PRIMARY KEY,
    order_id INTEGER NOT NULL REFERENCES orders(id) ON DELETE CASCADE,
    previous_status VARCHAR(40),
    new_status VARCHAR(40) NOT NULL,
    changed_by_user_id INTEGER REFERENCES users(id) ON DELETE SET NULL,
    changed_by_role VARCHAR(40) NOT NULL,              -- 'ADMIN', 'RECEPCIONISTA', 'TECNICO', 'CLIENTE_QR'
    observation TEXT,
    created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_history_order ON order_status_history(order_id);

-- 13. Tabla de Control de Calidad
CREATE TABLE IF NOT EXISTS quality_controls (
    id SERIAL PRIMARY KEY,
    order_id INTEGER UNIQUE NOT NULL REFERENCES orders(id) ON DELETE CASCADE,
    technician_id INTEGER NOT NULL REFERENCES users(id) ON DELETE RESTRICT,
    tests_performed TEXT NOT NULL,                     -- Lista de pruebas efectuadas
    is_approved BOOLEAN NOT NULL,                      -- True = Pasa control, False = Rechazado
    observations TEXT,
    check_date TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 14. Tabla de Entrega de Equipos
CREATE TABLE IF NOT EXISTS deliveries (
    id SERIAL PRIMARY KEY,
    order_id INTEGER UNIQUE NOT NULL REFERENCES orders(id) ON DELETE CASCADE,
    delivered_by_user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE RESTRICT,
    receiver_name VARCHAR(120) NOT NULL,               -- Nombre y Apellido de quien retira
    receiver_document VARCHAR(30) NOT NULL,            -- Cédula de Identidad de quien retira
    delivery_notes TEXT,
    delivered_at TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP
);
