"""
This module defines the Weapon class for the Cluedo game.

The Weapon class represents weapons that are part of the game's mystery. Each weapon
has a name and can be associated with a specific location on the game board. This module
enables the creation and management of weapons during gameplay.
"""
class Weapon: # pylint: disable=too-few-public-methods
    """
    Represents a weapon in the Cluedo game.

    Weapons are one of the key elements in the game's mystery and can be placed
    in different rooms during gameplay.

    Attributes:
        name (str): The name of the weapon (e.g., "Candlestick", "Revolver").
        location (str): The current location of the weapon on the game board.
    """
    def __init__(self, name):
        """
        Initialize a Weapon with a name.

        The weapon's location is initially set to None, indicating it has not been
        placed on the game board.

        Args:
            name (str): The name of the weapon (e.g., "Candlestick").
        """
        self.name = name
        self.location = None

    def __eq__(self, other):
        """
        Compare two Weapon objects for equality based on their names.

        Args:
            other (Weapon): Another Weapon object to compare.

        Returns:
            bool: True if the names of the weapons match; False otherwise.
        """
        if isinstance(other, Weapon):
            return self.name == other.name
        return False

    def __hash__(self):
        """
        Generate a hash value for the Weapon object based on its name.

        This ensures that the Weapon object can be used in hashable collections
        like sets and dictionaries.

        Returns:
            int: The hash value of the weapon's name.
        """
        return hash(self.name)
