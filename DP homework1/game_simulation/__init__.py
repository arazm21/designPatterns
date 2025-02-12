from .creature_classes import (
    ClawLevel,
    ClawsUpgrade,
    Creature,
    LegsUpgrade,
    Predator,
    Prey,
    TeethUpgrade,
    WingsUpgrade,
)
from .simulate_game import Game

__all__ = ["Creature", "Prey", "Predator",
           "Game", "TeethUpgrade", "ClawsUpgrade", "WingsUpgrade",
           "LegsUpgrade","ClawLevel"]


# Specify the public API of game_simulation
