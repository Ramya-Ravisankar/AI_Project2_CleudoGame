# weapons.py

class Weapon:
    def __init__(self, name, location):
        self.name = name
        self.location = location

weapons = [
    Weapon("Candlestick", "Library"),
    Weapon("Revolver", "Kitchen"),
    Weapon("Rope", "Conservatory"),
    Weapon("Dagger", "Dining Room"),
    Weapon("Lead Pipe", "Ballroom")
]
