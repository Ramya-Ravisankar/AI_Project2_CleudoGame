"""
Unit tests for testing room movement logic in the Cluedo game.

This module verifies the functionality of the `Room` class, specifically
the ability to establish connections between rooms and validate player
movement in the game. It includes tests for valid and invalid movements,
as well as scenarios involving disconnected rooms.

Features:
- Test valid and invalid room connections.
- Ensure bidirectional connections are correctly established.
- Verify behavior of disconnected rooms.
"""

import unittest
from utils.movement import Room


class TestMovement(unittest.TestCase):
    """
    Unit tests for movement-related functionality in the Cluedo game.

    This test suite ensures that:
    - Players can navigate between connected rooms.
    - The `Room` class properly manages connections between rooms.
    - Disconnected rooms are handled correctly.

    Attributes:
        kitchen (Room): The kitchen room for testing.
        ballroom (Room): The ballroom room for testing.
        library (Room): The library room for testing.
        study (Room): The study room for testing.
        rooms (list[Room]): A list of all rooms used in the tests.
    """

    def setUp(self):
        """
        Set up the game environment for testing.

        Creates four connected rooms: Kitchen, Ballroom, Library, and Study.
        Connections are established as follows:
        - Kitchen <-> Ballroom
        - Ballroom <-> Library
        - Library <-> Study

        These connections are stored in the `rooms` attribute for use in tests.
        """
        self.kitchen = Room("Kitchen")
        self.ballroom = Room("Ballroom")
        self.library = Room("Library")
        self.study = Room("Study")

        # Create connections
        self.kitchen.connect(self.ballroom)
        self.ballroom.connect(self.library)
        self.library.connect(self.study)

        # Store rooms in a list for testing
        self.rooms = [self.kitchen, self.ballroom, self.library, self.study]

    def test_valid_movement(self):
        """
        Test if the player can move to a valid connected room.

        Verifies that the `list_connections` method correctly identifies
        rooms directly connected to the current room. Specifically, ensures
        that the Kitchen is connected to the Ballroom.
        """
        available_rooms = self.kitchen.list_connections()
        self.assertIn("Ballroom", available_rooms, "Kitchen should connect to Ballroom.")

    def test_invalid_movement(self):
        """
        Test if the player cannot move to a non-connected room.

        Ensures that attempting to move to a room with no established connection
        (e.g., Garage) is not allowed. Verifies that the `list_connections` method
        does not include disconnected rooms.
        """
        disconnected_room = Room("Garage")
        self.assertNotIn(
            disconnected_room.name, self.kitchen.list_connections(), "Kitchen should not connect to Garage."
        )

    def test_room_connections(self):
        """
        Test if room connections are correctly established.

        Verifies that:
        - Kitchen connects only to Ballroom.
        - Ballroom connects to both Kitchen and Library.
        - The connections are bidirectional and accurate.
        """
        self.assertEqual(
            sorted(self.kitchen.list_connections()),
            ["Ballroom"],
            "Kitchen should connect to Ballroom."
        )
        self.assertEqual(
            sorted(self.ballroom.list_connections()),
            ["Kitchen", "Library"],
            "Ballroom should connect to Kitchen and Library."
        )

    def test_disconnected_room(self):
        """
        Test behavior when a room is disconnected.

        Ensures that a room with no connections (e.g., Garage) returns an
        empty list when `list_connections` is called.
        """
        disconnected_room = Room("Garage")
        self.assertEqual(disconnected_room.list_connections(), [], "Garage should not have any connections.")


if __name__ == "__main__":
    unittest.main()
