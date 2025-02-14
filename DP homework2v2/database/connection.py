import sqlite3
from sqlite3.dbapi2 import Connection

_connection = None
_test_mode = False

def enable_test_mode() -> None:
    """Enable test mode to use an in-memory database."""
    global _test_mode
    _test_mode = True

def disable_test_mode() -> None:
    global _test_mode
    _test_mode = False


# making a test base in memory
def get_connection() -> Connection:
    """Get a SQLite connection."""
    global _connection
    if _connection is None:
        db_path = ":memory:" if _test_mode else "production.db"
        _connection = sqlite3.connect(db_path, check_same_thread=False)
    _connection.row_factory = sqlite3.Row  # Enable dictionary-like access
    return _connection

def init_db() -> None:
    """Initialize the database schema."""

    connection = get_connection()
    cursor = connection.cursor()
    cursor.executescript("""
        CREATE TABLE IF NOT EXISTS units (
            id TEXT PRIMARY KEY,
            name TEXT UNIQUE NOT NULL
        );
    """)
    cursor.executescript("""
            CREATE TABLE IF NOT EXISTS products (
            id TEXT PRIMARY KEY,        -- UUID for the product ID
            unit_id TEXT NOT NULL,      -- Foreign key to the units table
            name TEXT NOT NULL,         -- Name of the product
            barcode TEXT UNIQUE,        -- Unique barcode for the product
            price INTEGER NOT NULL     -- Price of the product in cents 
        ); 
    """)
    cursor.executescript("""
                CREATE TABLE IF NOT EXISTS receipt_products (
                receipt_id TEXT NOT NULL,
                product_id TEXT NOT NULL,
                quantity INTEGER NOT NULL,
                price INTEGER NOT NULL,
                total INTEGER NOT NULL
            );
    """)
    cursor.executescript("""
                    CREATE TABLE IF NOT EXISTS receipts (
                    id TEXT PRIMARY KEY,
                    status TEXT NOT NULL CHECK (status IN ('open', 'closed')),
                    total INTEGER NOT NULL DEFAULT 0
            );
    """)
    connection.commit()

def close_db() -> None:
    """Close the database connection."""
    global _connection
    if _connection:
        _connection.close()
        _connection = None

# # import sqlite3
# # from contextlib import contextmanager
# #
# # _connection = None
# #
# # def get_connection():
# #     global _connection
# #     if _connection is None:
# #         _connection = sqlite3.connect("pos.db", check_same_thread=False)
# #         _connection.row_factory = sqlite3.Row
# #     return _connection
# #
# # @contextmanager
# # def get_cursor():
# #     connection = get_connection()
# #     cursor = connection.cursor()
# #     try:
# #         yield cursor
# #         connection.commit()
# #     except:
# #         connection.rollback()
# #         raise
# import sqlite3
# from contextlib import contextmanager
# from pathlib import Path
#
# DB_PATH = Path("pos.db")
# _connection = None
#
# def get_connection():
#     global _connection
#     if _connection is None:
#         _connection = sqlite3.connect(DB_PATH, check_same_thread=False)
#         _connection.row_factory = sqlite3.Row
#     return _connection
#
#
# def init_db():
#     """Initializes the database schema."""
#     conn = get_connection()
#     with conn:
#         conn.executescript("""
#         CREATE TABLE IF NOT EXISTS units (
#             id TEXT PRIMARY KEY,
#             name TEXT UNIQUE NOT NULL
#         );
#         """)
#     print("Database initialized.")
#
# def close_db():
#     """Closes the database connection."""
#     global _connection
#     if _connection:
#         _connection.close()
#         _connection = None
#     print("Database connection closed.")
#
# @contextmanager
# def get_cursor():
#     connection = get_connection()
#     cursor = connection.cursor()
#     try:
#         yield cursor
#         connection.commit()
#     except:
#         connection.rollback()
#         raise