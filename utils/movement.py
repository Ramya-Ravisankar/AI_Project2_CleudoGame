"""
This module defines the `Room` class, which is used to represent rooms in the Cluedo game.

Each room can be connected to other rooms, forming a graph-like structure that models
the game map. The `Room` class provides methods for:
- Establishing bidirectional connections between rooms.
- Listing all rooms directly connected to a given room.

This is a core utility for managing room navigation and gameplay mechanics.
"""
class Room:
    """
    Represents a room in the Cluedo game.

    A `Room` object models a single room in the game map. Rooms can be connected
    to other rooms, allowing players to navigate between them during gameplay.

    Attributes:
        name (str): The name of the room.
        connected_rooms (list[Room]): A list of `Room` objects that are directly connected
                                      to this room, forming a graph-like structure.
    """
    def __init__(self, name):
        """
            Initialize a Room object with a name and an empty list of connected rooms.

            Args:
                name (str): The name of the room (e.g., "Kitchen", "Library").
        """
        self.name = name
        self.connected_rooms = []  # List of connected Room objects

    def connect(self, other_room):
        """
            Connect this room to another room, creating a bidirectional connection.

            This method establishes a connection between the current room and another
            room, allowing players to navigate between them.

            Args:
                other_room (Room): The room to connect to.
        """
        self.connected_rooms.append(other_room)
        other_room.connected_rooms.append(self)

    def list_connections(self):
        """
            List the names of all rooms directly connected to this room.

            Returns:
                list[str]: A list of names of rooms that are connected to this room.
        """
        return [room.name for room in self.connected_rooms]
