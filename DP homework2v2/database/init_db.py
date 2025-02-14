from database.connection import init_db


def initialize_database() -> None:
    # with open("database/schemas.sql", "r") as schema_file:
    #     schema = schema_file.read()
    init_db()
    # connection = get_connection()
    # cursor = connection.cursor()
    # cursor.executescript(schema)
    # connection.commit()
