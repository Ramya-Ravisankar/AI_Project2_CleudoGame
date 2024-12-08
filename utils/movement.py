from collections import deque

class Room:
    def __init__(self, name):
        """
        Initialize a Room object with a name and an empty list of connected rooms.
        """
        self.name = name
        self.connected_rooms = []

    def connect(self, other_room):
        """
        Connect this room to another room.
        """
        self.connected_rooms.append(other_room)
        other_room.connected_rooms.append(self)

    def list_connections(self):
        """
        List names of all connected rooms.
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
    # Create a mapping of room names to Room objects
    room_map = {room.name: room for room in rooms}

    # Validate that the start and end rooms exist
    if start_room_name not in room_map or end_room_name not in room_map:
        return None

    # Initialize the BFS queue with the starting room
    queue = deque([(start_room_name, [start_room_name])])  # (current_room, path_so_far)
    visited = set()  # To keep track of visited rooms

    while queue:
        current_room_name, path = queue.popleft()  # Dequeue the next room and path
        if current_room_name in visited:
            continue  # Skip already visited rooms

        visited.add(current_room_name)  # Mark this room as visited

        # If we reach the destination, return the path
        if current_room_name == end_room_name:
            return path

        # Enqueue all connected (unvisited) rooms
        current_room = room_map[current_room_name]
        for neighbor in current_room.connected_rooms:
            if neighbor.name not in visited:
                queue.append((neighbor.name, path + [neighbor.name]))

    return None  # If no path exists, return None

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
