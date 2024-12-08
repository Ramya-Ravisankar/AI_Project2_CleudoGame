"""
This module defines the Character class for the Cluedo game.

The Character class is used to represent a player or suspect in the game. It tracks:
- The character's name and current position.
- The cards held by the character, which can be used to refute suggestions.
- Whether the character has made an accusation during the game.

This module also includes helper methods for comparison, hashing, and debugging.
"""
class Character: # pylint: disable=too-few-public-methods
    """
    Represents a character in the Cluedo game.

    Attributes:
        name (str): The name of the character (e.g., "Miss Scarlett").
        position (str): The current position of the character in the game (e.g., "Kitchen").
        has_made_accusation (bool): Tracks whether the character has made an accusation.
        cards (list[str]): A list of cards held by the character, used to refute suggestions.
    """
    def __init__(self, name, position):
        """
        Initialize a Character with a name, position, and default attributes.

        Args:
            name (str): The name of the character (e.g., "Miss Scarlett").
            position (str): The starting position of the character (e.g., "Kitchen").

        Attributes:
            has_made_accusation (bool): Defaults to False. Set to True after the character
                                        makes an accusation, preventing further accusations.
            cards (list[str]): Initializes as an empty list. Stores the cards held by the character.
        """
        self.name = name
        self.position = position
        self.has_made_accusation = False  # Defaults to False when the character is initialized.
        """
        The above tracks if the player has made an accusation.Updated to True after the
        character makes a false accusation.
        """
        self.cards = []  # Cards the player holds which can be used to refute suggestions

    def __eq__(self, other):
        """
        Compare two Character objects for equality based on their names.

        Args:
            other (Character): Another Character object to compare.

        Returns:
            bool: True if the names of the characters match; False otherwise.
        """
        if isinstance(other, Character):
            return self.name == other.name
        return False

    def __hash__(self):
        """
        Generate a hash value for the Character object based on its name.

        This ensures that the Character object can be used in hashable collections like sets
        and dictionaries.

        Returns:
            int: The hash value of the character's name.
        """
        return hash(self.name)  # Ensures the object is hashable

    def __repr__(self):
        """
        Generate a string representation of the Character object for debugging.

        The string includes the character's name and current position.

        Returns:
            str: A formatted string representation of the character.
        """
        return f"Character(name='{self.name}', position='{self.position}')"
