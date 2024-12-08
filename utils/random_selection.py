"""
This module provides a utility function for randomly selecting the solution
in the Cluedo game.

The solution consists of a randomly chosen character, weapon, and room.
"""

import random
import logging

# Set up logging
logging.basicConfig(level=logging.DEBUG, filename='game_debug.log', filemode='w', format='%(message)s')

def select_solution(characters, weapons, rooms, seed=None, reveal_solution=False):
    """
    Randomly select a solution for the Cluedo game.

    Args:
        characters (list[Character]): List of all characters in the game.
        weapons (list[Weapon]): List of all weapons in the game.
        rooms (list[Room]): List of all rooms in the game.
        seed (int, optional): Seed for random number generator, useful for testing.
        reveal_solution (bool, optional): If True, print the selected solution for debugging.

    Returns:
        tuple: A tuple containing a randomly selected character, weapon, and room.
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
