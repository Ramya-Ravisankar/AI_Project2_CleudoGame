"""
Unit tests for testing suggestion logic in the game.
"""

import unittest
from classes.room import Room
from classes.character import Character
from classes.weapon import Weapon
from game_logic import GameLogic


class TestSuggestions(unittest.TestCase):
    """Tests for suggestion logic."""

    def setUp(self):
        """Set up the test environment."""
        self.kitchen = Room("Kitchen")
        self.library = Room("Library")
        self.ballroom = Room("Ballroom")
        self.rooms = [self.kitchen, self.library, self.ballroom]

        self.scarlett = Character("Miss Scarlett", "Kitchen")
        self.mustard = Character("Colonel Mustard", "Library")
        self.weapons = [Weapon("Candlestick"), Weapon("Revolver")]

        self.game_logic = GameLogic(self.rooms, [self.scarlett, self.mustard], self.weapons, None)

    def test_valid_suggestion(self):
        """Test valid suggestion."""
        result = self.game_logic.make_suggestion(self.scarlett, "Colonel Mustard", "Candlestick", "Kitchen")
        self.assertIn("Suggestion made", result)

    def test_invalid_room_suggestion(self):
        """Test invalid room suggestion."""
        result = self.game_logic.make_suggestion(self.scarlett, "Colonel Mustard", "Candlestick", "Library")
        self.assertIn("Invalid suggestion", result)

    def test_suggestion_no_refute(self):
        """Test suggestion when no one can refute."""
        result = self.game_logic.make_suggestion(self.scarlett, "Miss Scarlett", "Revolver", "Kitchen")
        self.assertIn("No one could refute", result)

    def test_suggestion_with_refute(self):
        """Test suggestion when a player can refute."""
        self.mustard.cards = ["Candlestick"]
        result = self.game_logic.make_suggestion(self.scarlett, "Colonel Mustard", "Candlestick", "Kitchen")
        self.assertIn("Suggestion refuted", result)


if __name__ == "__main__":
    unittest.main()
