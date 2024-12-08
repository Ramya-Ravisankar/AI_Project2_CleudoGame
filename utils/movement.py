"""
movement.py

This module provides functionality for finding paths between rooms in the game using BFS.
"""

from collections import deque


class Room:
    def __init__(self, name):
        """
        Initialize a Room object with a name and an empty list of connected rooms.

        :param name: The name of the room.
        """
        self.name = name
        self.connected_rooms = []

    def connect(self, other_room):
        """
        Connect this room to another room.

        :param other_room: Another Room object to connect to.
        """
        self.connected_rooms.append(other_room)
        other_room.connected_rooms.append(self)

    def list_connections(self):
        """
        List names of all connected rooms.

        :return: A list of names of connected rooms.
        """
        return [room.name for room in self.connected_rooms]

from collections import deque

def find_path(start_room_name, end_room_name, rooms):
    """
    Find the shortest path between two rooms using BFS.

    Args:
        start_room_name (str): The name of the starting room.
        end_room_name (str): The name of the destination room.
        rooms (list[Room]): List of Room objects.

    Returns:
        list: The shortest path from start_room_name to end_room_name, or None if no path exists.
    """
    # Map room names to Room objects for quick lookup
    room_map = {room.name: room for room in rooms}

    if start_room_name not in room_map or end_room_name not in room_map:
        return None  # Invalid room names

    # BFS initialization
    queue = deque([(start_room_name, [start_room_name])])  # Each element is (current room, path so far)
    visited = set()  # To track visited rooms

    while queue:
        current_room_name, path = queue.popleft()

        if current_room_name == end_room_name:
            return path  # Return the path when the destination is reached

        visited.add(current_room_name)  # Mark the room as visited

        # Add unvisited neighbors to the queue
        for neighbor in room_map[current_room_name].connected_rooms:
            if neighbor.name not in visited:
                queue.append((neighbor.name, path + [neighbor.name]))
                visited.add(neighbor.name)  # Mark neighbor as visited to avoid re-queuing

    return None  # No path found


# Example Usage
if __name__ == "__main__":
        # Create rooms
            kitchen = Room("Kitchen")
            ballroom = Room("Ballroom")
            library = Room("Library")
            study = Room("Study")

            # Connect rooms
            kitchen.connect(ballroom)
            ballroom.connect(library)
            library.connect(study)
            study.connect(kitchen)  # Cyclic connection

            # List of all rooms
            rooms = [kitchen, ballroom, library, study]

            # Find path
            path = find_path("Kitchen", "Study", rooms)
            print("Path from Kitchen to Study:", path)
