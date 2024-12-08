import unittest
from utils.movement import Room, find_path


class TestMovement(unittest.TestCase):
    """
    Unit tests for movement-related functionality in the game.

    These tests verify that the player can move between rooms as expected
    and handle invalid movements appropriately.
    """

    def setUp(self):
        """Set up the game environment for testing."""
        self.kitchen = Room("Kitchen")
        self.ballroom = Room("Ballroom")
        self.library = Room("Library")
        self.study = Room("Study")

        # Create cyclic connections
        self.kitchen.connect(self.ballroom)
        self.ballroom.connect(self.library)
        self.library.connect(self.study)
        self.study.connect(self.kitchen)  # Cyclic connection

        # Store rooms in a list for testing
        self.rooms = [self.kitchen, self.ballroom, self.library, self.study]

    def test_valid_movement(self):
        """Test if the player can move to a valid connected room."""
        available_rooms = self.kitchen.list_connections()
        self.assertIn("Ballroom", available_rooms, "Kitchen should connect to Ballroom.")

    def test_invalid_movement(self):
        """Test if the player cannot move to a non-connected room."""
        disconnected_room = Room("Garage")
        self.assertNotIn(
            disconnected_room.name, self.kitchen.list_connections(), "Kitchen should not connect to Garage."
        )

    def test_room_connections(self):
        """Test if room connections are correctly established."""
        self.assertEqual(
            sorted(self.kitchen.list_connections()),
            ["Ballroom", "Study"],
            "Kitchen should connect to Ballroom and Study."
        )
        self.assertEqual(
            sorted(self.ballroom.list_connections()),
            ["Kitchen", "Library"],
            "Ballroom should connect to Kitchen and Library."
        )
        self.assertEqual(
            sorted(self.library.list_connections()),
            ["Ballroom", "Study"],
            "Library should connect to Ballroom and Study."
        )
        self.assertEqual(
            sorted(self.study.list_connections()),
            ["Kitchen", "Library"],
            "Study should connect to Kitchen and Library."
        )

    def test_pathfinding(self):
        """Test if the pathfinding algorithm returns a valid path."""
        path = find_path("Kitchen", "Study", self.rooms)
        expected_path = ["Kitchen", "Ballroom", "Library", "Study"]
        self.assertEqual(
            path,
            expected_path,
            "Pathfinding failed. Ensure BFS is working correctly."
        )

    def test_pathfinding_same_start_end(self):
        """Test pathfinding when start and end rooms are the same."""
        path = find_path("Kitchen", "Kitchen", self.rooms)
        self.assertEqual(path, ["Kitchen"], "Pathfinding should return the same room when start and end are the same.")

    def test_pathfinding_single_room(self):
        """Test pathfinding when only one room exists."""
        single_room = Room("Kitchen")
        path = find_path("Kitchen", "Kitchen", [single_room])
        self.assertEqual(path, ["Kitchen"], "Pathfinding should return the single room.")

    def test_invalid_path(self):
        """Test if pathfinding returns None for invalid paths."""
        path = find_path("Kitchen", "Garage", self.rooms)
        self.assertIsNone(path, "Pathfinding should return None for invalid destinations.")

    def test_cyclic_room_connections(self):
        """Test pathfinding in a cyclic graph."""
        path = find_path("Kitchen", "Study", self.rooms)
        expected_path = ["Kitchen", "Ballroom", "Library", "Study"]
        self.assertEqual(path, expected_path, "Pathfinding failed in cyclic graph.")

    def test_pathfinding_disconnected_graph(self):
        """Test pathfinding in a disconnected graph."""
        disconnected_room = Room("Garage")
        self.rooms.append(disconnected_room)  # Add disconnected room
        path = find_path("Kitchen", "Garage", self.rooms)
        self.assertIsNone(path, "Pathfinding should return None for disconnected rooms.")

    def test_direct_connection(self):
        """Test direct path between two directly connected rooms."""
        path = find_path("Kitchen", "Ballroom", self.rooms)
        expected_path = ["Kitchen", "Ballroom"]
        self.assertEqual(path, expected_path, "Pathfinding failed for direct connection.")

    def test_disconnected_graph(self):
        """Test pathfinding in a graph where the rooms are not connected."""
        path = find_path("Kitchen", "NonExistentRoom", self.rooms)
        self.assertIsNone(path, "Pathfinding did not return None for disconnected graph.")

if __name__ == "__main__":
    unittest.main()
