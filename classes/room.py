"""
This module defines the Room class for the Cluedo game.

The Room class represents rooms in the game. Each room has a name and can be connected
to other rooms, forming a map that players can navigate. This module provides methods
to establish connections between rooms and retrieve a list of connected rooms.
"""
class Room:  # pylint: disable=too-few-public-methods
    """
    Represents a room in the Cluedo game.

    Rooms are nodes in the game map that can connect to other rooms. These connections
    allow players to move between rooms during gameplay.

    Attributes:
        name (str): The name of the room (e.g., "Kitchen", "Library").
        connected_rooms (list[Room]): A list of Room objects directly connected to this room.
    """
    def __init__(self, name):
        """
        Initialize a Room with a name and an empty list of connected rooms.

        Args:
            name (str): The name of the room (e.g., "Kitchen").
        """
        self.name = name
        self.connected_rooms = []

    def __eq__(self, other):
        """
        Compare two Room objects for equality based on their names.

        Args:
            other (Room): Another Room object to compare.

        Returns:
            bool: True if the names of the rooms match; False otherwise.
        """
        if isinstance(other, Room):
            return self.name == other.name
        return False

    def __hash__(self):
        """
        Generate a hash value for the Room object based on its name.

        This ensures that the Room object can be used in hashable collections like sets
        and dictionaries.

        Returns:
            int: The hash value of the room's name.
        """
        return hash(self.name)

    def connect(self, room):
        """
        Establish a two-way connection between this room and another room.

        This method adds the other room to this room's connected_rooms list
        and vice versa, creating a bidirectional link.

        Args:
            room (Room): The Room object to connect to.
        """
        if room not in self.connected_rooms:
            self.connected_rooms.append(room)
            room.connected_rooms.append(self)

    def list_connections(self):
        """
        Retrieve a list of names of rooms connected to this room.

        Returns:
            list[str]: A list of names of rooms directly connected to this room.
        """
        return [room.name for room in self.connected_rooms]
