# mansion.py

class Mansion:
    def __init__(self):
        self.rooms = {
            "Kitchen": ["Dining Room", "Ballroom"],
            "Dining Room": ["Kitchen", "Library"],
            "Ballroom": ["Kitchen", "Conservatory"],
            "Library": ["Dining Room", "Conservatory"],
            "Conservatory": ["Ballroom", "Library"]
        }

    def get_neighbors(self, room):
        return self.rooms.get(room, [])
