import random
from abc import ABC, abstractmethod
from enum import Enum
from typing import Any, Dict, List, Optional, Type


class ClawLevel(Enum):
    NONE = 1
    SMALL = 2
    MEDIUM = 3
    BIG = 4


class Creature:
    movement_modes: Dict[str, Dict[str, int]] = {
        "flying": {
            "required_stamina": 80,
            "stamina_usage": 4,
            "speed": 8,
            "legs_needed": 0,
            "wings_needed": 2,
        },
        "running": {
            "required_stamina": 60,
            "stamina_usage": 4,
            "speed": 6,
            "legs_needed": 2,
            "wings_needed": 0,
        },
        "walking": {
            "required_stamina": 40,
            "stamina_usage": 2,
            "speed": 4,
            "legs_needed": 2,
            "wings_needed": 0,
        },
        "hopping": {
            "required_stamina": 20,
            "stamina_usage": 2,
            "speed": 3,
            "legs_needed": 1,
            "wings_needed": 0,
        },
        "crawling": {
            "required_stamina": 0,
            "stamina_usage": 1,
            "speed": 1,
            "legs_needed": 0,
            "wings_needed": 0,
        },
    }
    calculation_order: List[str] = ["add", "mult"]

    def __init__(
            self, upgrades_weight: Optional[Dict[str, int]] = None,
            upgrade_amount_weight: Optional[List[int]] = None,
            location: int = 0,
            stamina: int = 100,
            health: int = 100,
            min_upgrades: int = 0,
            max_upgrades: int = 3,

            attack_power: int = 2,
    ) -> None:
        if upgrade_amount_weight is None:
            upgrade_amount_weight = []
        if upgrades_weight is None:
            upgrades_weight = {}
        self.claw_multiplier: int = 1
        self.attack_power = attack_power
        self.location = location
        self.stamina = stamina
        self.health = health
        self.attributes: Dict[str, int] = {}
        self.min_upgrades = min_upgrades
        self.max_upgrades = max_upgrades

        # Initialize attributes
        self.initialize_legs()
        self.initialize_wings()
        self.initialize_claws()
        self.initialize_teeth()

        self.possible_upgrades = ["legs", "wings", "claws", "teeth"]

        self.upgrade_amount_weight = upgrade_amount_weight or [1] * (
                self.max_upgrades - self.min_upgrades + 1
        )
        self.upgrades_weight = upgrades_weight
        for upgrade in self.possible_upgrades:
            if upgrade not in self.upgrades_weight:
                self.upgrades_weight[upgrade] = 1

        self.predator = None
        self.prey = None

    def initialize_legs(self, initial_value: int = 0) -> None:
        self.attributes["legs"] = initial_value

    def initialize_wings(self, initial_value: int = 0) -> None:
        self.attributes["wings"] = initial_value

    def initialize_claws(self, initial_value: ClawLevel = ClawLevel.NONE) -> None:
        self.attributes["claws"] = initial_value.value
        self.claw_multiplier = 1

    def initialize_teeth(self, initial_value: int = 0) -> None:
        self.attributes["teeth"] = initial_value

    def evolve(self) -> None:
        """Randomly apply upgrades based on weighted probabilities."""
        # Determine the number of upgrades to apply
        min_upgrades = self.min_upgrades
        max_upgrades = self.max_upgrades
        # print(range(min_upgrades, max_upgrades + 1))
        # print("---------------------------------")
        # print(list(self.upgrade_amount_weight))
        num_upgrades = random.choices(
            range(min_upgrades, max_upgrades + 1),
            weights=list(self.upgrade_amount_weight),
            k=1,
        )[0]

        # Select upgrade names based on weights and available strategies
        selected_upgrades = random.choices(
            self.possible_upgrades,
            weights=[
                self.upgrades_weight.get(name, 1) for name in self.possible_upgrades
            ],
            k=num_upgrades,
        )

        # Apply each selected upgrade strategy
        for upgrade_name in selected_upgrades:
            # Use lowercase name to find the corresponding upgrade class
            strategy_class = UpgradeStrategy.registry.get(upgrade_name.lower())

            if strategy_class:
                strategy = strategy_class()
                strategy.apply_upgrade(self)
            else:
                print(f"Upgrade class for '{upgrade_name}' not found.")

    def choose_available_movement_options(self) -> list[str]:
        available_modes = [
            mode
            for mode, details in self.movement_modes.items()
            if self.stamina >= details["stamina_usage"]
               and self.attributes["legs"] >= details["legs_needed"]
               and self.attributes["wings"] >= details["wings_needed"]
               and self.stamina - details["stamina_usage"]
               >= details["required_stamina"]
        ]
        return available_modes

    def move(self) -> None:
        """Move the creature based on available stamina and attributes (legs, wings)."""
        available_modes = self.choose_available_movement_options()

        movement = self.choose_move(available_modes)

        self.location += movement["speed"]
        self.stamina -= movement["stamina_usage"]

    def choose_move(self, available_modes: list[str]) ->  dict[str, int]:
        best_mode = max(
            available_modes, key=lambda mode: self.movement_modes[mode]["speed"]
        )
        movement = self.movement_modes[best_mode]
        return movement

    def calculate_addition_bonus(self) -> int:
        # Calculate and return the additive bonus based on attributes
        return self.attributes["teeth"]  # Example: teeth bonus increases by 3

    def calculate_multiplication(self) -> int:
        return self.claw_multiplier

    def calculate_attack_damage(self) -> int:
        damage = self.attack_power
        for operation in self.calculation_order:
            if operation == "add":
                damage += self.calculate_addition_bonus()
            elif operation == "mult":
                damage *= self.calculate_multiplication()
        return damage


class Prey(Creature):
    def __init__(
            self,
            min_location: int = 0,
            max_location: int = 500,
            stamina: int = 100,
            health: int = 100,
            min_upgrades: int = 0,
            max_upgrades: int = 3,
            upgrades_weight: Optional[Dict[str, int]] = None,
            upgrade_amount_weight: Optional[List[int]] = None
    ) -> None:
        # Set a random starting location within the given range
        random_location = random.randint(min_location, max_location)
        super().__init__(
            location=random_location,
            stamina=stamina,
            health=health,
            min_upgrades=min_upgrades,
            max_upgrades=max_upgrades,
            upgrades_weight=upgrades_weight,
            upgrade_amount_weight=upgrade_amount_weight,
        )


class Predator(Creature):
    def __init__(
            self,
            stamina: int = 100,
            health: int = 100,
            min_upgrades: int = 0,
            max_upgrades: int = 3,
            upgrades_weight: Optional[Dict[str, int]] = None,
            upgrade_amount_weight: Optional[List[int]] = None
    ) -> None:
        # Start the Predator at location 0
        super().__init__(
            location=0,
            stamina=stamina,
            health=health,
            min_upgrades=min_upgrades,
            max_upgrades=max_upgrades,
            upgrades_weight=upgrades_weight,
            upgrade_amount_weight=upgrade_amount_weight,
        )


class UpgradeStrategy(ABC):
    registry: Dict[str, Type['UpgradeStrategy']] = {}
    def __init_subclass__(cls: Type['UpgradeStrategy'],
                          **kwargs: dict[str, Any]) -> None:
        """Automatically register each subclass in the strategy registry."""
        super().__init_subclass__(**kwargs)
        cls.registry[cls.__name__.replace("Upgrade", "").lower()] = cls

    @abstractmethod
    def apply_upgrade(self, creature: Creature) -> None:
        """Each upgrade strategy will define how to apply itself to a creature."""
        pass


class LegsUpgrade(UpgradeStrategy):
    """Upgrade strategy to add legs to the creature."""

    def apply_upgrade(self, creature: Creature) -> None:
        # Increment legs by 1 each time this upgrade is applied
        creature.attributes["legs"] = creature.attributes.get("legs", 0) + 1
        # print(f"Legs upgraded to {creature.attributes['legs']}")


class WingsUpgrade(UpgradeStrategy):
    """Upgrade strategy to add wings to the creature."""

    def apply_upgrade(self, creature: Creature) -> None:
        # Increment wings by 1 each time this upgrade is applied
        creature.attributes["wings"] = creature.attributes.get("wings", 0) + 1
        # print(f"Wings upgraded to {creature.attributes['wings']}")


class ClawsUpgrade(UpgradeStrategy):
    # Define claw levels with an associated rank
    LEVELS = {ClawLevel.NONE.value: 1, ClawLevel.SMALL.value: 2,
              ClawLevel.MEDIUM.value: 3, ClawLevel.BIG.value: 4}

    def apply_upgrade(self, creature: Creature) -> None:
        # Get the creature's current claw level
        current_level = creature.attributes.get("claws", ClawLevel.NONE.value)
        current_rank = self.LEVELS.get(current_level, 1)

        # Randomly choose a new claw level
        new_level = random.choice(list(self.LEVELS.keys()))
        new_rank = self.LEVELS[new_level]

        # Apply the new level if it has a higher rank than the current level
        if new_rank > current_rank:
            creature.attributes["claws"] = new_level
            creature.claw_multiplier = new_rank


class TeethUpgrade(UpgradeStrategy):
    """Upgrade strategy to increase the sharpness of teeth."""

    SHARPNESS_LEVELS = [0, 3, 6, 9]

    def apply_upgrade(self, creature: Creature) -> None:
        # Randomly select a new sharpness level greater than 0, keeping the max achieved
        new_teeth = random.choice(self.SHARPNESS_LEVELS[1:])
        creature.attributes["teeth"] = max(
            creature.attributes.get("teeth", 0), new_teeth
        )
        # print(f"Teeth upgraded to {creature.attributes['teeth']}")
