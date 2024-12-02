class Room:
    def __init__(self, name):
        self.name = name
        self.connected_rooms = []

    def connect(self, room):
        if room not in self.connected_rooms:
            self.connected_rooms.append(room)
            room.connected_rooms.append(self)
