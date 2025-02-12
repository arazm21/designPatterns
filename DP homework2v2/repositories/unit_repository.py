
from uuid import uuid4

from database.connection import get_connection
from models.unit import Unit


class UnitRepository:
    @staticmethod
    def create_unit(name: str) -> Unit:
        """Create a new unit in the database."""
        connection = get_connection()
        cursor = connection.cursor()

        # Check if the unit already exists
        cursor.execute("SELECT id FROM units WHERE name = ?", (name,))
        if cursor.fetchone():
            raise ValueError(f"Unit with name<{name}> already exists.")

        # Generate a new UUID and insert the unit
        unit_id = uuid4()
        cursor.execute("INSERT INTO units (id, name) "
                       "VALUES (?, ?)", (str(unit_id), name))
        connection.commit()

        # Return the created unit
        return Unit(id=unit_id, name=name)

    @staticmethod
    def get_unit_by_id(unit_id: str) -> Unit:
        """Retrieve a unit by its ID."""
        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute("SELECT id, name FROM units WHERE id = ?", (unit_id,))
        row = cursor.fetchone()
        if not row:

            raise ValueError(f"Unit with id<{unit_id}> does not exist.")

        return Unit(id=row["id"], name=row["name"])


    @staticmethod
    def list_units() -> list[Unit]:
        """Retrieve all units from the database."""
        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute("SELECT id, name FROM units")
        rows = cursor.fetchall()

        # Convert rows to a list of Unit instances
        units = [Unit(id=row["id"], name=row["name"]) for row in rows]

        return units

# from typing import List, Optional
# from uuid import UUID
# from database.connection import get_cursor
# from models.unit import Unit
#
# class UnitRepository:
#     def create_unit(self, unit: Unit) -> None:
#         with get_cursor() as cursor:
#             cursor.execute(
#                 "INSERT INTO units (id, name) VALUES (?, ?)",
#                 (str(unit.id), unit.name),
#             )
#
#     def get_unit_by_id(self, unit_id: UUID) -> Optional[Unit]:
#         with get_cursor() as cursor:
#             cursor.execute("SELECT id, name FROM units WHERE id = ?", (str(unit_id),))
#             row = cursor.fetchone()
#             return Unit(id=row["id"], name=row["name"]) if row else None
#
#     def get_unit_by_name(self, name: str) -> Optional[Unit]:
#         with get_cursor() as cursor:
#             cursor.execute("SELECT id, name FROM units WHERE name = ?", (name,))
#             row = cursor.fetchone()
#             return Unit(id=row["id"], name=row["name"]) if row else None
#
#     def list_units(self) -> List[Unit]:
#         with get_cursor() as cursor:
#             cursor.execute("SELECT id, name FROM units")
#             rows = cursor.fetchall()
#             return [Unit(id=row["id"], name=row["name"]) for row in rows]
