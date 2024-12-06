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

current_turn Tracker:
Tracks the index of the current player in the characters list.
Ensures only the player whose turn it is can perform actions,Updates current_turn at the end of each valid action
All actions (move, suggest, accuse, quit) are restricted to the current player.
If a player makes an incorrect accusation or quits, they are removed from the characters list:
If all players are eliminated or quit, game terminates
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

# Add the `current_turn` tracker here
current_turn = 0  # Tracks the index of the current player in the `characters` list

def advance_turn():
    """Advance to the next player's turn."""
    global current_turn
    current_turn = (current_turn + 1) % len(characters)

def skip_turn_if_restricted(player):
    """Skip the player's turn if they have made an accusation."""
    if player.has_made_accusation:
        print(f"{player.name}, you cannot make any moves or accusations as you have already made an accusation.")
        return True
    return False

while True:
    game_logic.display_filtered_game_state(current_player)

    # Notify the current player
    current_player = characters[current_turn]
    print(f"\n{current_player.name}, it's your turn!")
    print("\nOptions: move, suggest, accuse, notes, add_note, remove_note, quit")
    action = input("Choose an action: ").strip().lower()

    if action in ["move", "accuse"] and skip_turn_if_restricted(current_player):
        advance_turn()
        continue

    if action == "move":
        # Handle player movement
        print(f"You are currently in {current_player.position}.")
        available_rooms = game_logic.get_room_connections(current_player.position)
        print(f"Rooms you can move to: {', '.join(room.lower() for room in available_rooms)}")
        destination = input("Enter the room you want to move to: ").strip()

        if destination.lower() in [room.lower() for room in available_rooms]:
            current_player.position = destination
            print(f"You moved to the {current_player.position}.")
        else:
            print("Invalid move. You cannot go to that room from here.")

    elif action == "suggest":
        print(f"You are currently in {current_player.position}.")
        character_name = input("Enter the name of the character you suggest: ").strip()
        weapon_name = input("Enter the name of the weapon you suggest: ").strip()
        result = game_logic.make_suggestion(current_player, character_name, weapon_name, current_player.position)
        print(result)
        # Log the suggestion into PlayerNotes
        player_notes.add_suggestion(character_name, weapon_name, current_player.position)

    elif action == "accuse":
        # Handle accusations
        if current_player.has_made_accusation:
            print(f"{current_player.name}, you have already made an accusation and cannot accuse again.")
            advance_turn()
            continue

        # Collect user inputs for the accusation
        accused_character = input("Enter the name of the character you accuse: ").strip().lower()
        accused_weapon = input("Enter the name of the weapon you accuse: ").strip().lower()
        accused_room = input("Enter the name of the room you accuse: ").strip().lower()

        # Process accusation with self-check
        result = game_logic.process_accusation(current_player.name, accused_character, accused_weapon, accused_room)

        if result is None:  # Self-accusation detected
            print(f"{current_player.name}, you accused yourself! Turn skipped.The Game continues")
            advance_turn()
            continue

        if result:  # Correct accusation
            print(f"Congratulations, {current_player.name}! You solved the mystery!")
            break

        # Mark the player as having made an accusation
        current_player.has_made_accusation = True
        print(f"Accusation incorrect. {current_player.name}, you cannot make further moves or accusations.")
        advance_turn()
        continue

    elif action == "notes":
        # Display player notes
        player_notes.view_notes()

    elif action == "add_note":
        note = input("Enter a note to add: ").strip()
        player_notes.add_manual_entry(note)
        print("Note added.")

    elif action == "remove_note":
        note = input("Enter a note to remove: ").strip()
        player_notes.remove_manual_entry(note)
        print("Note removed.")

    elif action == "quit":
        print(f"{current_player.name} has quit the game.")
        characters.pop(current_turn)
        if not characters:
            print("All players have left. The game is over!")
            break
        current_turn %= len(characters)  # Ensure valid index for remaining players
        continue

    else:
        print("Invalid action. Please choose move, suggest, accuse, notes, or quit.")
        continue

    advance_turn()
