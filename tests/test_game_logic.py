"""
Unit tests for the GameLogic class in the Cluedo game.

This module tests the core functionality of the GameLogic class, including:
- Validating and processing player suggestions.
- Handling accusations and providing feedback.
- Managing room connections.

The tests ensure the game's logic behaves as expected under various scenarios.
"""
import unittest
from classes.room import Room
from classes.character import Character
from classes.weapon import Weapon
from game_logic import GameLogic

class TestGameLogic(unittest.TestCase):
    """
    Unit tests for the GameLogic class.

    The tests cover various functionalities such as:
    - Making suggestions and validating inputs.
    - Processing accusations and providing appropriate feedback.
    - Handling room connections and navigation.
    """
    def setUp(self):
        """
        Set up the test environment with rooms, characters, weapons, and a solution.
        """
        self.kitchen = Room("Kitchen")
        self.library = Room("Library")
        self.ballroom = Room("Ballroom")
        self.rooms = [self.kitchen, self.library, self.ballroom]

        self.scarlett = Character("Miss Scarlett", "Kitchen")
        self.mustard = Character("Colonel Mustard", "Library")
        self.weapons = [Weapon("Candlestick"), Weapon("Revolver")]
        self.solution = (self.scarlett, self.weapons[0], self.kitchen)

        self.game_logic = GameLogic(self.rooms, [self.scarlett, self.mustard], self.weapons, self.solution)

    def test_make_suggestion_not_in_room(self):
        """
        Test that a player cannot make a suggestion if they are not in the suggested room.
        """
        result = self.game_logic.make_suggestion(self.mustard, "Miss Scarlett", "Candlestick", "Kitchen")
        self.assertIn(
            "Invalid suggestion: You are currently in the 'Library' "
                      "and must be in the 'Kitchen' to suggest it.", result)

    def test_make_suggestion_invalid_character(self):
        """
        Test that an invalid character name in a suggestion is properly handled.
        """
        result = self.game_logic.make_suggestion(self.scarlett, "Invalid Character", "Candlestick", "Kitchen")
        self.assertIn("Invalid suggestion: Character or weapon does not exist.", result)

    def test_make_suggestion_with_refutation(self):
        """
        Test that a suggestion is refuted when another player has the refuting card.
        """
        self.mustard.cards = ["Candlestick"]
        result = self.game_logic.make_suggestion(self.scarlett, "Miss Scarlett", "Candlestick", "Kitchen")
        self.assertIn("Suggestion refuted by Colonel Mustard", result)

    def test_process_accusation_self_accusation(self):
        """
        Test that self-accusations are prevented and an appropriate message is returned.
        """
        # Simulating self-accusation
        result = self.game_logic.process_accusation(
            "Miss Scarlett",  # Accusing character
            "Miss Scarlett",  # Accused character
            "Candlestick",    # Accused weapon
            "Kitchen"         # Accused room
        )
        # Verify the result contains the expected message
        self.assertIn("you cannot accuse yourself", result)

    def test_process_accusation_partial_incorrect(self):
        """
        Test that a partially incorrect accusation returns appropriate feedback.
        """
        result = self.game_logic.process_accusation("Miss Scarlett", "Colonel Mustard", "Candlestick", "Kitchen")
        self.assertIn("Character 'colonel mustard' is incorrect.", result)

    def test_process_accusation_correct(self):
        """
        Test that a correct accusation ends the game with the correct message.
        """
        result = self.game_logic.process_accusation("Colonel Mustard", "Miss Scarlett", "Candlestick", "Kitchen")
        self.assertEqual(result, "Accusation correct! You've solved the mystery!")

    def test_get_room_connections(self):
        """
        Test that the room connections are retrieved correctly.
        """
        self.kitchen.connect(self.library)
        connections = self.game_logic.get_room_connections("Kitchen")
        self.assertEqual(connections, ["Library"])

    def test_get_room_connections_no_connections(self):
        """
        Test that a room with no connections returns an empty list.
        """
        connections = self.game_logic.get_room_connections("Ballroom")
        self.assertEqual(connections, [])

if __name__ == "__main__":
    unittest.main()
