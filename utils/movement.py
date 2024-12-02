"""
This module contains utility functions for handling movement logic in the game.

The functions here are used to validate and process player movements between rooms.
"""

def move_to_room(player, destination, rooms):
    """
    Move a player to a specified destination if it is a valid connection.

    Args:
        player (Character): The player attempting to move.
        destination (str): The target room the player wants to move to.
        rooms (list[Room]): List of all rooms in the game.

    Returns:
        bool: True if the move is successful, False otherwise.
    """
    # Find the current room based on the player's position
    current_room = next((room for room in rooms if room.name == player.position), None)

    # Check if the destination is connected to the current room
    if current_room and destination in [room.name for room in current_room.connected_rooms]:
        player.position = destination
        return True

    # If the destination is invalid, return False
    return False
