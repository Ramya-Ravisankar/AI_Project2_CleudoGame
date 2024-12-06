import unittest
from classes.room import Room
from classes.character import Character
from classes.weapon import Weapon
from game_logic import GameLogic

class TestAccusationLogic(unittest.TestCase):
    def setUp(self):
        """Set up game environment for testing accusations."""
        # Initialize Rooms
        self.kitchen = Room("Kitchen")
        self.library = Room("Library")

        # Initialize Characters
        self.scarlett = Character("Miss Scarlett", "Kitchen")
        self.mustard = Character("Colonel Mustard", "Library")

        # Initialize Weapons
        self.candlestick = Weapon("Candlestick")
        self.rope = Weapon("Rope")

        # Solution
        self.solution = (self.scarlett, self.rope, self.kitchen)

        # Game Logic
        self.game_logic = GameLogic(
            rooms=[self.kitchen, self.library],
            characters=[self.scarlett, self.mustard],
            weapons=[self.candlestick, self.rope],
            solution=self.solution
        )

    def test_correct_accusation(self):
        """Test if a correct accusation ends the game."""
        result = self.game_logic.process_accusation("Miss Scarlett", "Miss Scarlett", "Rope", "Kitchen")
        self.assertTrue(result, "Accusation should be correct and end the game.")

    def test_incorrect_accusation(self):
        """Test if an incorrect accusation provides feedback."""
        result = self.game_logic.process_accusation("Miss Scarlett", "Colonel Mustard", "Candlestick", "Library")
        self.assertFalse(result, "Accusation should be incorrect and provide feedback.")

if __name__ == "__main__":
    unittest.main()
