class Room:  # pylint: disable=too-few-public-methods
    def __init__(self, name):
        self.name = name
        self.connected_rooms = []

    def connect(self, room):
        """
        Connect this room to another room.
        Args:
            room (Room): The room to connect to this room.
        """
        if room not in self.connected_rooms:
            self.connected_rooms.append(room)
            room.connected_rooms.append(self)
