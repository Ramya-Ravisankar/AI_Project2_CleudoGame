"""
This module provides utilities for randomly selecting the solution
in the Cluedo game.

The solution is composed of a character, weapon, and room randomly chosen
from the game's available options. The module also supports debugging by
allowing the solution to be logged or revealed based on user preference.

Features:
- Random selection of character, weapon, and room for the solution.
- Option to set a random seed for reproducibility during testing.
- Logging of the solution for debugging purposes.
"""

import random
import logging

# Set up logging
logging.basicConfig(level=logging.DEBUG, filename='game_debug.log', filemode='w', format='%(message)s')

def select_solution(characters, weapons, rooms, seed=None, reveal_solution=False):
    """
    Randomly select a solution for the Cluedo game.

    The solution consists of a randomly chosen character, weapon, and room.
    Optionally logs or reveals the solution for debugging purposes.

    Args:
        characters (list[Character]): List of all characters in the game.
        weapons (list[Weapon]): List of all weapons in the game.
        rooms (list[Room]): List of all rooms in the game.
        seed (int, optional): Seed for the random number generator, useful for testing reproducibility.
        reveal_solution (bool, optional): If True, logs and reveals the selected solution for debugging.

    Returns:
        tuple: A tuple containing a randomly selected character, weapon, and room.

    Example:
        characters = [Character("Miss Scarlett"), Character("Colonel Mustard")]
        weapons = [Weapon("Candlestick"), Weapon("Revolver")]
        rooms = [Room("Kitchen"), Room("Library")]

        solution = select_solution(characters, weapons, rooms, seed=42, reveal_solution=True)
        print(solution)
    """
    # Optional: Set the seed for reproducibility (useful for tests)
    if seed is not None:
        random.seed(seed)

    # Randomly select one of each type
    character = random.choice(characters)
    weapon = random.choice(weapons)
    room = random.choice(rooms)

    if reveal_solution:
        logging.debug("Solution selected (revealed): %s, %s, %s", character.name, weapon.name, room.name)
    else:
        logging.debug("Solution selected (hidden).")

    return character, weapon, room
