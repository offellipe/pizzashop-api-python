CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT NOT NULL,
    password TEXT NOT NULL,
    role TEXT NOT NULL CHECK (role IN ('admin', 'customer', 'manager')),
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT users_email_unique UNIQUE (email)
);

CREATE TABLE restaurants (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    description TEXT NOT NULL,
    manager_id INTEGER, -- Tipo da chave estrangeira
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (manager_id) REFERENCES users(id) -- Declaração da chave estrangeira
);

CREATE TABLE products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    description TEXT,
    price_in_cents INTEGER NOT NULL,
    restaurant_id INTEGER, -- Tipo da chave estrangeira
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (restaurant_id) REFERENCES restaurants(id) -- Declaração da chave estrangeira
);

CREATE TYPE order_status AS ENUM ('pending', 'processing', 'delivering', 'delivered', 'canceled');

CREATE TABLE orders (
    id TEXT PRIMARY KEY DEFAULT createId(),
    customer_id TEXT REFERENCES users(id) ON DELETE SET NULL,
    restaurant_id TEXT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    status order_status NOT NULL DEFAULT 'pending',
    total_in_cents INTEGER NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE evaluations (
    id TEXT PRIMARY KEY,
    customer_id TEXT NOT NULL,
    restaurant_id TEXT NOT NULL,
    rate INTEGER NOT NULL,
    comment TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL,
    FOREIGN KEY (customer_id) REFERENCES users (id),
    FOREIGN KEY (restaurant_id) REFERENCES restaurants (id)
);

CREATE TABLE order_items (
    id TEXT PRIMARY KEY,
    order_id TEXT NOT NULL,
    product_id TEXT,
    quantity INTEGER NOT NULL DEFAULT 1,
    price_in_cents INTEGER NOT NULL,
    FOREIGN KEY (order_id) REFERENCES orders (id) ON DELETE CASCADE,
    FOREIGN KEY (product_id) REFERENCES products (id) ON DELETE SET NULL
);