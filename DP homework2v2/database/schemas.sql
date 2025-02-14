CREATE TABLE IF NOT EXISTS units (
    id TEXT PRIMARY KEY,
    name TEXT UNIQUE NOT NULL
);
CREATE TABLE products (
    id TEXT PRIMARY KEY,        -- UUID for the product ID
    unit_id TEXT NOT NULL,      -- Foreign key to the units table
    name TEXT NOT NULL,         -- Name of the product
    barcode TEXT UNIQUE,        -- Unique barcode for the product
    price INTEGER NOT NULL,     -- Price of the product in cents (to avoid floating-point issues)
    FOREIGN KEY (unit_id) REFERENCES units(id) ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS receipts (
    id TEXT PRIMARY KEY,
    status TEXT NOT NULL CHECK (status IN ('open', 'closed')),
    total INTEGER NOT NULL DEFAULT 0
);


CREATE TABLE IF NOT EXISTS receipt_products (
    receipt_id TEXT NOT NULL,
    product_id TEXT NOT NULL,
    quantity INTEGER NOT NULL,
    price INTEGER NOT NULL,
    total INTEGER NOT NULL,
);
