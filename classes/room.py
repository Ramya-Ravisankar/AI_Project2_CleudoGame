"""
This module defines the Room class for the game.

The Room class represents rooms in the game and allows for connecting rooms to create a map.
"""
class Room:  # pylint: disable=too-few-public-methods
    """
    Represents a room in the game.

    Attributes:
        name (str): The name of the room.
        connected_rooms (list[Room]): A list of rooms connected to this room.
    """
    def __init__(self, name):
        """
        Initialize a Room with a name.

        Args:
            name (str): The name of the room.
        """
        self.name = name
        self.connected_rooms = []

    def __eq__(self, other):
        if isinstance(other, Room):
            return self.name == other.name
        return False

    def __hash__(self):
        return hash(self.name)

    def connect(self, room):
        """Establish a two-way connection between rooms."""
        if room not in self.connected_rooms:
            self.connected_rooms.append(room)
            room.connected_rooms.append(self)

    def list_connections(self):
        """Return a list of connected room names."""
        return [room.name for room in self.connected_rooms]
