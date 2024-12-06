"""
This module defines the Weapon class for the game.

The Weapon class is used to represent weapons in the game.
"""
class Weapon: # pylint: disable=too-few-public-methods
    """
    Represents a weapon in the game.

    Attributes:
        name (str): The name of the weapon.
        location (str): The current location of the weapon.
    """
    def __init__(self, name):
        self.name = name
        self.location = None

    def __eq__(self, other):
        if isinstance(other, Weapon):
            return self.name == other.name
        return False

    def __hash__(self):
        return hash(self.name)
