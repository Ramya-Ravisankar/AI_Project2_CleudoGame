"""
This module provides a utility function for randomly selecting the solution
in the Cluedo game.

The solution consists of a randomly chosen character, weapon, and room.
"""

import random
import logging

# Set up logging
logging.basicConfig(level=logging.DEBUG, filename='game_debug.log', filemode='w', format='%(message)s')

def select_solution(characters, weapons, rooms, seed=None):
    """
    Randomly select a solution for the Cluedo game.

    Args:
        characters (list[Character]): List of all characters in the game.
        weapons (list[Weapon]): List of all weapons in the game.
        rooms (list[Room]): List of all rooms in the game.
        seed (int, optional): Seed for random number generator, useful for testing.

    Returns:
        tuple: A tuple containing a randomly selected character, weapon, and room.
    """
    if not characters or not weapons or not rooms:
        raise ValueError("Characters, weapons, and rooms lists must not be empty.")

    if seed is not None:
        random.seed(seed)

    character = random.choice(characters)
    weapon = random.choice(weapons)
    room = random.choice(rooms)
    logging.debug("Solution selected (hidden): %s, %s, %s", character.name, weapon.name, room.name)
    return (character, weapon, room)
