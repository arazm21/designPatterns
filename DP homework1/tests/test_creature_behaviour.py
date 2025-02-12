from __future__ import annotations

from game_simulation import (
    ClawLevel,
    Creature,
    LegsUpgrade,
    Predator,
    Prey,
    TeethUpgrade,
    WingsUpgrade,
)


def test_creature_init() -> None:
    creature = Creature()
    assert creature.health == 100
    assert creature.stamina == 100


def test_prey() -> None:
    prey = Prey(min_location=10, max_location=20)
    assert 20 >= prey.location >= 10
    assert prey.stamina == 100
    assert prey.health == 100


def test_predator() -> None:
    predator = Predator()
    assert predator.location == 0
    assert predator.stamina == 100
    assert predator.health == 100


def test_upgrades() -> None:
    creature = Creature(min_upgrades=1, max_upgrades=1)
    assert creature.attributes["legs"] == 0
    assert creature.attributes["teeth"] == 0
    assert creature.attributes["wings"] == 0
    assert creature.attributes["claws"] == ClawLevel.NONE.value


def test_legs_upgrade() -> None:
    # Test applying LegsUpgrade
    creature = Creature()
    legs_upgrade = LegsUpgrade()
    legs_upgrade.apply_upgrade(creature)
    assert creature.attributes["legs"] == 1 or creature.attributes["legs"] == 2


def test_wings_upgrade() -> None:
    # Test applying WingsUpgrade
    creature = Creature()
    wings_upgrade = WingsUpgrade()
    wings_upgrade.apply_upgrade(creature)
    assert creature.attributes["wings"] == 1 or creature.attributes["wings"] == 2


def test_teeth_upgrade() -> None:
    # Test applying TeethUpgrade, which keeps the maximum sharpness achieved
    creature = Creature()
    teeth_upgrade = TeethUpgrade()

    # Apply upgrade and ensure it raises teeth sharpness
    teeth_upgrade.apply_upgrade(creature)
    assert creature.attributes["teeth"] > 0

    # Check that another application only increases if new sharpness is higher
    current_teeth = creature.attributes["teeth"]
    teeth_upgrade.apply_upgrade(creature)
    assert creature.attributes["teeth"] >= current_teeth


def test_max_upgrade_levels() -> None:
    # Create a creature with high upgrade possibilities
    creature = Creature(
        min_upgrades=1, max_upgrades=1, upgrades_weight={}, upgrade_amount_weight=[]
    )

    # Run evolve multiple times to maximize upgrades
    for _ in range(1000):
        creature.evolve()

    # Now check if each attribute has reached its max level
    assert creature.attributes["legs"] >= 2
    assert creature.attributes["wings"] >= 2
    assert creature.attributes["claws"] == ClawLevel.BIG.value
    assert creature.attributes["teeth"] == 9


def test_weight_distribution() -> None:
    total_wings_upgrade = 0
    for _ in range(1000):
        creature = Creature(
            min_upgrades=1,
            max_upgrades=1,
            upgrades_weight={"wings": 50, "claws": 1, "teeth": 1, "legs": 1},
            upgrade_amount_weight=[],
        )

        # Run evolve multiple times to maximize upgrades

        creature.evolve()
        if creature.attributes["wings"] > 0:
            total_wings_upgrade += 1
    # print(total_wings_upgrade)
    assert total_wings_upgrade > 500


def test_amount_distribution() -> None:
    total_wings_upgrade = 0
    for _ in range(1000):
        creature = Creature(
            min_upgrades=1,
            max_upgrades=2,
            upgrades_weight={"wings": 500, "claws": 1, "teeth": 1, "legs": 1},
            upgrade_amount_weight=[1, 50],
        )

        # Run evolve multiple times to maximize upgrades

        creature.evolve()
        if creature.attributes["wings"] > 1:
            total_wings_upgrade += 1
    # print(total_wings_upgrade)
    assert total_wings_upgrade > 800
