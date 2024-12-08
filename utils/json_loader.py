"""
This module provides a utility function for loading rooms and their connections from a JSON file.

The JSON file should define the names of rooms and their connections, which are used to create
a graph-like structure for the Cluedo game. The resulting `Room` objects can then be used to
model navigation and gameplay.

Features:
- Parses a JSON file to initialize `Room` objects.
- Establishes bidirectional connections between rooms based on the JSON data.
"""
import json
from utils.movement import Room

def load_rooms_from_json(json_file):
    """
    Load rooms and their connections from a JSON file.

    The JSON file should have the following structure:
    {
        "rooms": [
            {
                "name": "Room Name",
                "connections": [
                    {"to": "Connected Room Name"},
                    {"to": "Another Connected Room Name"}
                ]
            },
            ...
        ]
    }

    This function reads the JSON file, creates `Room` objects for each room, and
    establishes bidirectional connections between rooms based on the `connections`
    field in the JSON data.

    Args:
        json_file (str): The path to the JSON file containing room definitions.

    Returns:
        list[Room]: A list of `Room` objects with connections established.

    Example:
        Assuming the JSON file contains:
        {
            "rooms": [
                {"name": "Kitchen", "connections": [{"to": "Library"}]},
                {"name": "Library", "connections": [{"to": "Kitchen"}]}
            ]
        }

        Usage:
        rooms = load_rooms_from_json("rooms.json")
        for room in rooms:
            print(f"Room: {room.name}, Connections: {room.list_connections()}")

    Raises:
        FileNotFoundError: If the JSON file is not found.
        json.JSONDecodeError: If the JSON file is improperly formatted.
    """
    with open(json_file, "r", encoding="utf-8") as file:
        data = json.load(file)

    # Create a mapping of room names to Room objects
    rooms = {room["name"]: Room(room["name"]) for room in data["rooms"]}

    # Add connections (unweighted)
    for room in data["rooms"]:
        current_room = rooms[room["name"]]
        for connection in room["connections"]:
            neighbor_room = rooms[connection["to"]]
            current_room.connect(neighbor_room)

    return list(rooms.values())
