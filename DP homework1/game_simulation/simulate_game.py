from typing import Dict, List, Optional

from game_simulation.creature_classes import Predator, Prey


class Game:
    def __init__(
            self,
            upgrades_weight: Optional[Dict[str, int]] = None,
            upgrade_amount_weight: Optional[List[int]] = None,
            min_upgrades_predator: int = 0,
            max_upgrades_predator: int = 3,
            min_upgrades_prey: int = 0,
            max_upgrades_prey: int = 3,
            max_prey_location: int = 500,
            predator_stamina: int = 100,
            prey_stamina: int = 100,
    ) -> None:

        self.min_upgrades_predator = min_upgrades_predator
        self.max_upgrades_predator = max_upgrades_predator
        self.min_upgrades_prey = min_upgrades_prey
        self.max_upgrades_prey = max_upgrades_prey
        self.max_prey_location = max_prey_location
        self.upgrades_weight = upgrades_weight
        self.upgrade_amount_weight = upgrade_amount_weight
        self.predator = Predator()
        self.prey = Prey()
        self.fight_order = ["prey", "predator"]
        self.predator_stamina = predator_stamina
        self.prey_stamina = prey_stamina
    def setup_game(self) -> None:
        """Initialize predator and prey with random positions and attributes."""
        # Evolve a random predator at location 0
        self.predator = Predator(
            stamina=self.predator_stamina,
            health=100,
            min_upgrades=self.min_upgrades_predator,
            max_upgrades=self.max_upgrades_predator,
            upgrades_weight=self.upgrades_weight,
            upgrade_amount_weight=self.upgrade_amount_weight,
        )
        self.predator.evolve()

        print(f"  Predator location: {self.predator.location}")
        print(f"  Attributes: {self.predator.attributes}\n")
        self.prey = Prey(
            stamina=self.prey_stamina,
            health=100,
            min_upgrades=self.min_upgrades_prey,
            max_upgrades=self.max_upgrades_prey,
            min_location=0,
            max_location=self.max_prey_location,
            upgrades_weight=self.upgrades_weight,
            upgrade_amount_weight=self.upgrade_amount_weight,
        )
        self.prey.evolve()
        print(f"  Prey location: {self.prey.location}")
        print(f"  Attributes: {self.prey.attributes}\n")

    def chase_phase(self) -> bool:
        while self.predator.stamina > 0 and self.predator.location < self.prey.location:
            if self.prey.stamina > 0:
                self.prey.move()
            self.predator.move()
        if not (self.predator.location < self.prey.location):
            return True
        print("Pray ran into infinity")
        return False  # Predator failed to catch prey

    def fight_phase(self) -> str:
        while self.predator.health > 0:
            damage = self.predator.calculate_attack_damage()
            self.prey.health -= damage
            if self.prey.health <= 0:
                print("Some R-rated things have happened")
                return "predator"
            damage = self.prey.calculate_attack_damage()
            self.predator.health -= damage
        print("Pray ran into infinity")
        return "prey"

    def simulate_entire_game(self) -> str:
        """Run the entire setup and simulation sequence."""
        self.setup_game()

        # Run the chase and, if successful, proceed to fight phase
        if self.chase_phase():
            return self.fight_phase()
        return "prey"


if __name__ == "__main__":
    total_game_number = 100
    prey_victories = 0
    for _ in range(total_game_number):
        game = Game(
            min_upgrades_predator=4,
            max_upgrades_predator=4,
            min_upgrades_prey=1,
            max_upgrades_prey=2,
            max_prey_location=500,
            predator_stamina=300,
            prey_stamina=100
        )
        if game.simulate_entire_game() == "prey":
            prey_victories += 1
    print(f"  Prey victories: {prey_victories}")
    print(f"  Predator victories: {total_game_number - prey_victories}")
