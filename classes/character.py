"""
This module defines the Character class for the game.

The Character class is used to represent a character in the game, including their name and position.
"""
class Character: # pylint: disable=too-few-public-methods
    """
    Represents a character in the game.

    Attributes:
        name (str): The name of the character.
        position (str): The current position of the character in the game.
    """
    def __init__(self, name, position):
        """
        Initialize a Character with a name and position.

        Args:
            name (str): The name of the character.
            position (str): The starting position of the character.
        """
        self.name = name
        self.position = position

    def __eq__(self, other):
        if isinstance(other, Character):
            return self.name == other.name
        return False

    def __hash__(self):
        return hash(self.name)  # Ensures the object is hashable
