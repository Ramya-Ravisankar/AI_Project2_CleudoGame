"""
This is the main module for the Cluedo game.
It initializes the game, processes user inputs, and manages game actions such as moving, suggesting, and accusing.

Features of the Code :
Game Initialization:
Rooms, characters, weapons, and the solution are initialized correctly, and connections between rooms are established.
This section initializes:
Rooms with connections.
Characters with starting positions.
Weapons without initial locations.
The randomly selected solution.
The game logic and player notes.

The Game State section provides useful information about:
The rooms and their connections.
The characters and their current positions.
The weapons and their locations.
This makes it easy for the player to understand the game’s current state.

Game Logic Integration:
GameLogic is used to manage gameplay, including movement, suggestions, and accusations.
PlayerNotes is initialized and used to log player suggestions.

PlayerNotes Integration:
Suggestions are logged into PlayerNotes when a suggestion is made
Players can view their notes using the notes action

Game Actions:
The while loop handles all player actions effectively:
Move: Manages movement between connected rooms and provides feedback for invalid moves.
Suggest: Logs suggestions in PlayerNotes and handles refutations through make_suggestion.
Accuse: Validates accusations against the solution and ends the game if correct.
Quit: Exits the game gracefully.
Notes: Displays logged suggestions for reference.Allows players to view logged suggestions.
"""
from classes.room import Room
from classes.character import Character
from classes.weapon import Weapon
from utils.random_selection import select_solution
from game_logic import GameLogic,PlayerNotes

# Initialize PlayerNotes
player_notes = PlayerNotes()

# Initialize Rooms
kitchen = Room("Kitchen")
ballroom = Room("Ballroom")
library = Room("Library")
study = Room("Study")

# Connect Rooms
kitchen.connect(ballroom)
ballroom.connect(library)
library.connect(study)

rooms = [kitchen, ballroom, library, study]

# Initialize Characters
characters = [
    Character("Miss Scarlett", "Kitchen"),
    Character("Colonel Mustard", "Library"),
    Character("Professor Plum", "Ballroom"),
]

# Initialize Weapons
weapons = [
    Weapon("Candlestick"),
    Weapon("Revolver"),
    Weapon("Rope"),
]

# Select Solution
solution = select_solution(characters, weapons, rooms, reveal_solution=True)

# Initialize GameLogic
game_logic = GameLogic(rooms, characters, weapons, solution)

# Game Start
print("Welcome to Cluedo!")
print("Solve the mystery of who committed the murder, with what weapon, and in which room.\n")

while True:
    # Display game state for the player's reference
    print("\nGame State:")
    print("Rooms:")
    for room in rooms:
        print(f"- {room.name}")

    print("\nCharacters:")
    for char in characters:
        print(f"- {char.name} is in {char.position}")

    print("\nWeapons:")
    for weap in weapons:
        print(f"- {weap.name} is in {weap.location if weap.location else 'None'}")

    # User options
    print("\nOptions: move, suggest, accuse, quit")
    action = input("Choose an action: ").strip().lower()

    if action == "move":
        # Handle player movement
        player = characters[0]  # Assume the first character represents the player
        print(f"You are currently in {player.position}.")
        available_rooms = game_logic.get_room_connections(player.position)
        print(f"Rooms you can move to: {', '.join(available_rooms)}")
        destination = input("Enter the room you want to move to: ").strip()

        if destination in available_rooms:
            player.position = destination
            print(f"You moved to the {player.position}.")
        else:
            print("Invalid move. You cannot go to that room from here.")

    elif action == "suggest":
        # Handle suggestions
        player = characters[0]  # Player makes the suggestion
        print(f"You are currently in {player.position}.")
        character_name = input("Enter the name of the character you suggest: ").strip()
        weapon_name = input("Enter the name of the weapon you suggest: ").strip()
        result = game_logic.make_suggestion(player, character_name, weapon_name, player.position)
        print(result)

        # Log the suggestion into PlayerNotes
        player_notes.add_suggestion(character_name, weapon_name, player.position)


    elif action == "accuse":
        # Collect user inputs for the accusation
        accused_character = input("Enter the name of the character you accuse: ").strip().lower()
        accused_weapon = input("Enter the name of the weapon you accuse: ").strip().lower()
        accused_room = input("Enter the name of the room you accuse: ").strip().lower()

        if game_logic.process_accusation(accused_character, accused_weapon, accused_room):
            print("Congratulations! You solved the mystery!")
            break

        print("Accusation incorrect. The mystery remains unsolved.")
        print("Game over. Try again next time!")
        break

    elif action == "notes":
        # Display player notes
        player_notes.view_notes()

    elif action == "quit":
        # Exit the game
        print("Thanks for playing! Goodbye!")
        break

    else:
        print("Invalid action. Please choose move, suggest, accuse, or quit.")
