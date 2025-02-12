from database.connection import get_connection


def initialize_database() -> None:
    with open("database/schemas.sql", "r") as schema_file:
        schema = schema_file.read()
    connection = get_connection()
    cursor = connection.cursor()
    cursor.executescript(schema)
    connection.commit()
