"""
This module contains unit tests for testing the suggestion logic in the game.

The tests validate the behavior of the `GameLogic` class when players make suggestions,
including moving characters and weapons to the suggested room and handling invalid inputs.
"""

import unittest
from classes.room import Room
from classes.character import Character
from classes.weapon import Weapon
from game_logic import GameLogic

class TestSuggestions(unittest.TestCase):
    """
    Unit tests for suggestion-related functionality in the game.

    These tests verify the behavior of the `GameLogic` class when handling suggestions,
    including valid suggestions, invalid suggestions, and their impact on the game state.
    """

    def setUp(self):
        """Set up the game environment for testing."""
        # Initialize Rooms
        self.kitchen = Room("Kitchen")
        self.ballroom = Room("Ballroom")
        self.library = Room("Library")
        self.study = Room("Study")

        # Connect Rooms
        self.kitchen.connect(self.ballroom)
        self.ballroom.connect(self.library)
        self.library.connect(self.study)

        # Initialize Characters
        self.miss_scarlett = Character("Miss Scarlett", "Kitchen")
        self.colonel_mustard = Character("Colonel Mustard", "Library")
        self.professor_plum = Character("Professor Plum", "Ballroom")

        # Initialize Weapons
        self.candlestick = Weapon("Candlestick")
        self.revolver = Weapon("Revolver")
        self.rope = Weapon("Rope")

        # Aggregate
        self.rooms = [self.kitchen, self.ballroom, self.library, self.study]
        self.characters = [self.miss_scarlett, self.colonel_mustard, self.professor_plum]
        self.weapons = [self.candlestick, self.revolver, self.rope]

        # Set the solution to existing instances
        self.solution = (self.miss_scarlett, self.candlestick, self.kitchen)

        # Initialize Game Logic
        self.game_logic = GameLogic(self.rooms, self.characters, self.weapons, self.solution)


    def test_valid_suggestion(self):
        """Test if a valid suggestion moves the suggested character and weapon to the current room."""
        player = self.miss_scarlett
        player.position = "Kitchen"
        result = self.game_logic.make_suggestion(player, "Colonel Mustard", "Revolver", "Kitchen")
        self.assertEqual(
            result, "Suggestion made: Colonel Mustard with the Revolver in the Kitchen."
        )

    def test_invalid_suggestion_room(self):
        """Test behavior when suggesting a room the player is not in."""
        player = self.miss_scarlett
        player.position = "Ballroom"
        result = self.game_logic.make_suggestion(player, "Colonel Mustard", "Revolver", "Kitchen")
        self.assertEqual(
            result, "Invalid suggestion: You must be in the Kitchen to suggest it."
        )

    def test_invalid_character_or_weapon(self):
        """Test behavior when suggesting a non-existent character or weapon."""
        suggesting_player = self.miss_scarlett
        suggesting_player.position = "Kitchen"  # Player is in the Kitchen

        # Invalid character
        result = self.game_logic.make_suggestion(suggesting_player, "Invalid Character", "Revolver", "Kitchen")
        self.assertEqual(
            result, "Invalid suggestion: Character or weapon does not exist."
            )

        # Invalid weapon
        result = self.game_logic.make_suggestion(suggesting_player, "Colonel Mustard", "Invalid Weapon", "Kitchen")
        self.assertEqual(
            result, "Invalid suggestion: Character or weapon does not exist."
            )

    def test_suggestion_does_not_affect_solution(self):
        """Test that making a suggestion does not alter the game's solution."""
        suggesting_player = self.miss_scarlett
        suggesting_player.position = "Kitchen"  # Player is in the Kitchen
        character_name = "Professor Plum"
        weapon_name = "Rope"
        room_name = "Kitchen"

        # Make a suggestion
        self.game_logic.make_suggestion(suggesting_player, character_name, weapon_name, room_name)

        # Assert that the solution remains unchanged
        solution_character, solution_weapon, solution_room = self.solution
        self.assertEqual(solution_character, self.miss_scarlett, "Solution character should not change.")
        self.assertEqual(solution_weapon, self.candlestick, "Solution weapon should not change.")
        self.assertEqual(solution_room, self.kitchen, "Solution room should not change.")

    def test_valid_suggestion_no_refute(): # Test Valid Suggestion (No Refutation):
        """
        Purpose:
        This test case verifies that the make_suggestion method behaves correctly when a
        suggestion is made, and no other player has a card to refute it.
        This test sets up a game state where:

        A player (the suggesting player) is in a valid room for making a suggestion.
        Other players do not hold any cards that match the suggested character, weapon, or room.
        The test ensures that:

        The suggestion is valid.
        No refutation occurs because no player can match the suggested cards.
        The output message correctly states that no one could refute the suggestion.
        """
        suggesting_player = Character("Miss Scarlett", "Kitchen")
        suggesting_player.cards = []
        player2 = Character("Colonel Mustard", "Library")
        player2.cards = ["Ballroom"]

        game_logic = GameLogic(
            rooms=[Room("Kitchen"), Room("Ballroom")],
            characters=[suggesting_player, player2],
            weapons=[Weapon("Rope")],
            solution=None
        )

        result = game_logic.make_suggestion(suggesting_player, "Colonel Mustard", "Rope", "Kitchen")
        assert result == "Suggestion made: Colonel Mustard with the Rope in the Kitchen. No one could refute."

    def test_valid_suggestion_with_refute(): # Test Valid Suggestion (Refutation):
        """
        Purpose:
        This test case verifies that the make_suggestion method correctly handles scenarios w
        here a suggestion is made, and another player has a card to refute it.
        Description:
        This test sets up a game state where:
        A player (the suggesting player) is in a valid room for making a suggestion.
        Another player holds a card that matches one of the suggested components (character, weapon, or room).
        The test ensures that:

        The suggestion is valid.
        The first player who can refute the suggestion does so.
        The output message correctly identifies the player who refuted the suggestion and the card they used.
        """
        suggesting_player = Character("Miss Scarlett", "Kitchen")
        suggesting_player.cards = []
        player2 = Character("Colonel Mustard", "Library")
        player2.cards = ["Rope"]

        game_logic = GameLogic(
            rooms=[Room("Kitchen"), Room("Ballroom")],
            characters=[suggesting_player, player2],
            weapons=[Weapon("Rope")],
            solution=None
        )

        result = game_logic.make_suggestion(suggesting_player, "Colonel Mustard", "Rope", "Kitchen")
        assert result == "Suggestion refuted by Colonel Mustard with Rope."

if __name__ == "__main__":
    unittest.main()
