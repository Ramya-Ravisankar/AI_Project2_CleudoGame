"""
Unit tests for accusations logic in the Cluedo game.
"""

import unittest
from classes.room import Room
from classes.character import Character
from classes.weapon import Weapon
from game_logic import GameLogic


class TestAccusationLogic(unittest.TestCase):
    """
    Unit tests for the accusation logic in the Cluedo game.
    """

    def setUp(self):
        """Set up the game environment for testing accusations."""
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
            solution=self.solution,
        )

    def test_correct_accusation(self):
        """Test if a correct accusation ends the game."""
        result = self.game_logic.process_accusation(
            accusing_character="Miss Scarlett",
            accused_character="Miss Scarlett",
            accused_weapon="Rope",
            accused_room="Kitchen",
        )
        self.assertEqual(
            result, "Accusation correct! You've solved the mystery!", "Correct accusation failed."
        )

    def test_incorrect_accusation(self):
        """Test if an incorrect accusation provides feedback."""
        result = self.game_logic.process_accusation(
            accusing_character="Miss Scarlett",
            accused_character="Colonel Mustard",
            accused_weapon="Candlestick",
            accused_room="Library",
        )
        self.assertIn(
            "Accusation incorrect. Feedback:", result, "Incorrect accusation feedback is missing."
        )
        self.assertIn("Character 'colonel mustard' is incorrect.", result)
        self.assertIn("Weapon 'candlestick' is incorrect.", result)
        self.assertIn("Room 'library' is incorrect.", result)


if __name__ == "__main__":
    unittest.main()
