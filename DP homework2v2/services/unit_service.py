from models.unit import Unit
from repositories.unit_repository import UnitRepository


class UnitService:
    def __init__(self, repository: UnitRepository):
        self.repository = repository

    def create_unit(self, name: str) -> Unit:
        """Create a new unit."""
        return self.repository.create_unit(name)

    def get_unit(self, unit_id: str) -> Unit:
        """Retrieve a unit by ID."""
        return self.repository.get_unit_by_id(unit_id)

    def list_units(self) -> list[Unit]:
        """List all units."""
        return self.repository.list_units()
