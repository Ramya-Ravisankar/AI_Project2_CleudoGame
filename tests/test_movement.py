"""
This module contains unit tests for testing movement logic in the game.

The tests verify the behavior of the `GameLogic` class and `Room` connections,
ensuring that player movement is correctly handled.
"""
import unittest
from classes.room import Room
from classes.character import Character
from game_logic import GameLogic

class TestMovement(unittest.TestCase):
    """
    Unit tests for movement-related functionality in the game.

    These tests verify that the player can move between rooms as expected
    and handle invalid movements appropriately.
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

        self.rooms = [self.kitchen, self.ballroom, self.library, self.study]

        # Initialize Characters
        self.character = Character("Miss Scarlett", "Kitchen")

        # Initialize GameLogic
        self.game_logic = GameLogic(self.rooms, [self.character], [], None)

    def test_valid_movement(self):
        """Test if the player can move to a valid connected room."""
        self.character.position = "Kitchen"
        available_rooms = self.game_logic.get_room_connections(self.character.position)
        self.assertIn("Ballroom", available_rooms)
        self.character.position = "Ballroom"
        self.assertEqual(self.character.position, "Ballroom")

    def test_invalid_movement(self):
        """Test if the player cannot move to a non-connected room."""
        self.character.position = "Kitchen"
        available_rooms = self.game_logic.get_room_connections(self.character.position)
        self.assertNotIn("Library", available_rooms)
        self.character.position = "Kitchen"
        self.assertEqual(self.character.position, "Kitchen")

    def test_room_connections(self):
        """Test if room connections are correctly set up."""
        kitchen_connections = self.game_logic.get_room_connections("Kitchen")
        self.assertEqual(kitchen_connections, ["Ballroom"], "Kitchen should only connect to the Ballroom.")

        ballroom_connections = self.game_logic.get_room_connections("Ballroom")
        self.assertEqual(sorted(ballroom_connections), sorted(["Kitchen", "Library"]),
                         "Ballroom should connect to Kitchen and Library.")

    def test_invalid_room(self):
        """Test behavior when querying an invalid room."""
        invalid_connections = self.game_logic.get_room_connections("Garage")
        self.assertEqual(invalid_connections, [], "Garage is not a valid room, so connections should be empty.")

if __name__ == "__main__":
    unittest.main()
