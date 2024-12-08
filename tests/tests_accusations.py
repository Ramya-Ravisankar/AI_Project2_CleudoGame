"""
Unit tests for accusations logic in the Cluedo game.

This module verifies the behavior of the accusation mechanism in the game.
It ensures that:
- Correct accusations are identified and result in a game win.
- Incorrect accusations provide detailed feedback, highlighting discrepancies.

Features:
- Tests valid accusations against the predefined solution.
- Verifies error handling for incorrect accusations with partial or full mismatches.
"""

import unittest
from classes.room import Room
from classes.character import Character
from classes.weapon import Weapon
from game_logic import GameLogic


class TestAccusationLogic(unittest.TestCase):
    """
    Unit tests for the accusation logic in the Cluedo game.

    This test suite validates:
    - Correct processing of valid accusations.
    - Feedback generation for incorrect accusations, including mismatched character, weapon, or room.

    Attributes:
        kitchen (Room): The Kitchen room used in tests.
        library (Room): The Library room used in tests.
        scarlett (Character): The character "Miss Scarlett" in the Kitchen.
        mustard (Character): The character "Colonel Mustard" in the Library.
        candlestick (Weapon): The weapon "Candlestick."
        rope (Weapon): The weapon "Rope."
        solution (tuple): The correct solution (character, weapon, room).
        game_logic (GameLogic): An instance of GameLogic for testing accusations.
    """

    def setUp(self):
        """
        Set up the game environment for testing accusations.

        Creates:
        - Two rooms: Kitchen and Library.
        - Two characters: "Miss Scarlett" in the Kitchen and "Colonel Mustard" in the Library.
        - Two weapons: "Candlestick" and "Rope."

        Initializes the GameLogic with the above entities and sets the solution
        to "Miss Scarlett with the Rope in the Kitchen."
        """
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
        """
        Test if a correct accusation ends the game.

        Simulates an accusation where:
        - The accused character matches the solution's character.
        - The accused weapon matches the solution's weapon.
        - The accused room matches the solution's room.

        Ensures that the GameLogic identifies the accusation as correct and
        returns the appropriate success message.
        """
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
        """
        Test if an incorrect accusation provides detailed feedback.

        Simulates an accusation where:
        - The accused character, weapon, and room do not match the solution.

        Ensures that the GameLogic identifies the mismatches and returns a feedback
        message highlighting which parts of the accusation were incorrect.
        """
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
