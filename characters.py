# characters.py

class Character:
    def __init__(self, name, starting_room):
        self.name = name
        self.current_room = starting_room

    def move_to(self, room):
        self.current_room = room

characters = {
    "Miss Scarlett": Character("Miss Scarlett", "Ballroom"),
    "Colonel Mustard": Character("Colonel Mustard", "Kitchen"),
    "Mrs. Peacock": Character("Mrs. Peacock", "Library"),
    "Professor Plum": Character("Professor Plum", "Conservatory"),
    "Mr. Green": Character("Mr. Green", "Dining Room")
}
