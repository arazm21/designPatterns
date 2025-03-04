from abc import ABC, abstractmethod
from typing import Protocol


class Observer(Protocol):
    """Defines the Observer interface that must be
    implemented by all weather system components."""

    @abstractmethod
    def update(self, temperature: float, humidity: float, wind_speed: float) -> None:
        """Gets notified when weather data changes."""
        pass


class Subject(ABC):
    """Defines the Subject (Observable) interface."""

    def __init__(self) -> None:
        self._observers: list[Observer] = []  # Now part of the base class
    @abstractmethod
    def attach(self, observer: Observer) -> None:
        """Registers an observer."""
        pass

    @abstractmethod
    def detach(self, observer: Observer) -> None:
        """Unregisters an observer."""
        pass

    @abstractmethod
    def notify(self) -> None:
        """Notifies all registered observers."""
        pass
