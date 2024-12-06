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
        self.has_made_accusation = False  # Defaults to False when the character is initialized.
        # The above tracks if the player has made an accusation.Updated to True after the character makes a false accusation.
        self.cards = []  # Cards the player holds which can be used to refute suggestions

    def __eq__(self, other):
        if isinstance(other, Character):
            return self.name == other.name
        return False

    def __hash__(self):
        return hash(self.name)  # Ensures the object is hashable

    def __repr__(self):
        """
        String representation of the character for debugging purposes.
        """
        return f"Character(name='{self.name}', position='{self.position}')"
