"""
Unit tests for testing suggestion logic in the Cluedo game.

This module verifies the behavior of the suggestion mechanism in the game.
It ensures that:
- Valid suggestions are processed correctly.
- Invalid suggestions (e.g., incorrect room) are handled appropriately.
- Scenarios where suggestions are refuted or not refuted are accurately processed.

Features:
- Tests valid suggestions with correct characters, weapons, and rooms.
- Verifies error handling for suggestions in the wrong room.
- Checks if players can refute or fail to refute suggestions based on their cards.
"""
import unittest
from classes.room import Room
from classes.character import Character
from classes.weapon import Weapon
from game_logic import GameLogic


class TestSuggestions(unittest.TestCase):
    """
    Unit tests for the suggestion logic in the Cluedo game.

    This test suite validates:
    - Handling of valid suggestions made by players.
    - Error handling for invalid room suggestions.
    - Refutation scenarios where players can or cannot refute a suggestion.

    Attributes:
        kitchen (Room): The Kitchen room used in tests.
        library (Room): The Library room used in tests.
        ballroom (Room): The Ballroom room used in tests.
        rooms (list[Room]): A list of all rooms involved in the tests.
        scarlett (Character): The character "Miss Scarlett" in the Kitchen.
        mustard (Character): The character "Colonel Mustard" in the Library.
        weapons (list[Weapon]): A list of weapons involved in the tests.
        game_logic (GameLogic): An instance of GameLogic for testing suggestions.
    """

    def setUp(self):
        """
        Set up the test environment.

        Creates:
        - Three rooms: Kitchen, Library, and Ballroom.
        - Two characters: "Miss Scarlett" in the Kitchen and "Colonel Mustard" in the Library.
        - Two weapons: "Candlestick" and "Revolver."

        Initializes the GameLogic with the above entities for testing suggestions.
        """
        self.kitchen = Room("Kitchen")
        self.library = Room("Library")
        self.ballroom = Room("Ballroom")
        self.rooms = [self.kitchen, self.library, self.ballroom]

        self.scarlett = Character("Miss Scarlett", "Kitchen")
        self.mustard = Character("Colonel Mustard", "Library")
        self.weapons = [Weapon("Candlestick"), Weapon("Revolver")]

        self.game_logic = GameLogic(self.rooms, [self.scarlett, self.mustard], self.weapons, None)

    def test_valid_suggestion(self):
        """
        Test if a valid suggestion is processed correctly.

        A valid suggestion includes:
        - An existing character.
        - An existing weapon.
        - The room the player is currently in.

        Ensures that the GameLogic correctly identifies and processes the suggestion.
        """
        result = self.game_logic.make_suggestion(self.scarlett, "Colonel Mustard", "Candlestick", "Kitchen")
        self.assertIn("Suggestion made", result)

    def test_invalid_room_suggestion(self):
        """
        Test handling of invalid room suggestions.

        Verifies that suggestions made for a room other than the one the player
        is currently in are identified as invalid and return an appropriate error message.
        """
        result = self.game_logic.make_suggestion(self.scarlett, "Colonel Mustard", "Candlestick", "Library")
        self.assertIn("Invalid suggestion", result)

    def test_suggestion_no_refute(self):
        """
        Test suggestion scenarios where no players can refute.

        Ensures that when a suggestion is made and no player has a matching
        card to refute it, the game correctly identifies this scenario and
        returns the appropriate message.
        """
        result = self.game_logic.make_suggestion(self.scarlett, "Miss Scarlett", "Revolver", "Kitchen")
        self.assertIn("No one could refute", result)

    def test_suggestion_with_refute(self):
        """
        Test suggestion scenarios where a player can refute.

        Simulates a scenario where a player has a matching card for the suggestion
        and can refute it. Verifies that the GameLogic correctly identifies the
        refuting player and their card.
        """
        self.mustard.cards = ["Candlestick"]
        result = self.game_logic.make_suggestion(self.scarlett, "Colonel Mustard", "Candlestick", "Kitchen")
        self.assertIn("Suggestion refuted", result)

if __name__ == "__main__":
    unittest.main()
