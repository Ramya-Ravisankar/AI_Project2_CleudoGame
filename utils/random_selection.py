import random
import logging

# Set up logging
logging.basicConfig(level=logging.DEBUG, filename='game_debug.log', filemode='w', format='%(message)s')

def select_solution(characters, weapons, rooms):
    character = random.choice(characters)
    weapon = random.choice(weapons)
    room = random.choice(rooms)
    # Log the solution for debugging
    print(f"Solution selected - Character: {character.name}, Weapon: {weapon.name}, Room: {room.name}")  # Added print
    return (character, weapon, room)
