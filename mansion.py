# mansion.py

class Room:
    def __init__(self, name):
        self.name = name
        self.connections = []

    def connect(self, other_room):
        self.connections.append(other_room)
        other_room.connections.append(self)

    def __repr__(self):
        connections = ', '.join(room.name for room in self.connections)
        return f"{self.name} (Connected to: {connections})"

def create_mansion():
    # Define rooms
    kitchen = Room("Kitchen")
    library = Room("Library")
    ballroom = Room("Ballroom")
    study = Room("Study")
    lounge = Room("Lounge")

    # Connect rooms
    kitchen.connect(library)
    kitchen.connect(ballroom)
    library.connect(study)
    ballroom.connect(lounge)

    # Return all rooms as a list
    return [kitchen, library, ballroom, study, lounge]