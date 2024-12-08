"""
This module contains the core logic for the Cluedo game, managing suggestions, accusations,
and Bayesian reasoning to deduce the solution.

Key Classes:
- GameLogic: Handles suggestions, accusations, and game state management.
- PlayerNotes: Tracks and manages player notes, such as suggestions and refutations.
- BayesianReasoner: Implements Bayesian reasoning to determine the most likely solution.
"""

def normalize_input(input_value):
    """
    Normalize input by converting to lowercase and stripping spaces.

    Args:
        input_value (str): The input string to normalize.

    Returns:
        str: Normalized string.
    """
    return input_value.strip().lower()

class GameLogic:
    """
    Manages the core mechanics of the Cluedo game, including handling suggestions,
    accusations, and game state tracking.

    Responsibilities:
    - Validating and processing player suggestions.
    - Handling accusations and providing feedback.
    - Managing the movement and connections between rooms.
    - Maintaining the state of characters, weapons, and rooms.

    Attributes:
        rooms (list[Room]): List of all rooms in the game.
        characters (list[Character]): List of all characters in the game.
        weapons (list[Weapon]): List of all weapons in the game.
        solution (tuple): The correct solution (character, weapon, room).
    """
    def __init__(self, rooms, characters, weapons, solution):
        """
        Initialize the game logic.

        :param rooms: List of Room objects.
        :param characters: List of Character objects.
        :param weapons: List of Weapon objects.
        :param solution: Tuple containing the solution (character, weapon, room).
        """
        self.rooms = rooms
        self.characters = characters
        self.weapons = weapons
        self.solution = solution  # Tuple: (Character, Weapon, Room)

    def make_suggestion(self, suggesting_player, character_name, weapon_name, room_name):
        """
        Process a player's suggestion.

        :param suggesting_player: The player making the suggestion.
        :param character_name: Name of the character being suggested.
        :param weapon_name: Name of the weapon being suggested.
        :param room_name: Name of the room being suggested.
        :return: A message summarizing the result of the suggestion.
        """
        # Validate current room
        current_room = next((room for room in self.rooms if room.name == suggesting_player.position), None)
        if current_room is None:
            return f"Invalid suggestion: You must be in the {room_name} to suggest it."

        if current_room.name != room_name:
            return (
                f"Invalid suggestion: You are currently in the '{current_room.name}' "
                f"and must be in the '{room_name}' to suggest it."
            )

        # Find the suggested character and weapon
        suggested_character = next((char for char in self.characters if char.name == character_name), None)
        suggested_weapon = next((weap for weap in self.weapons if weap.name == weapon_name), None)

        if not suggested_character or not suggested_weapon:
            return "Invalid suggestion: Character or weapon does not exist."

        # Move character and weapon to the suggested room
        suggested_character.position = room_name
        suggested_weapon.location = room_name

        # Handle refutations
        for player in self.characters:
            if player == suggesting_player:
                continue  # Skip the suggesting player

            # Check if the player can refute the suggestion
            refutable_cards = []
            if character_name in player.cards:
                refutable_cards.append(character_name)
            if weapon_name in player.cards:
                refutable_cards.append(weapon_name)
            if room_name in player.cards:
                refutable_cards.append(room_name)

            if refutable_cards:  # If the player can refute
                refutation_card = refutable_cards[0]
                return (
                    f"Suggestion refuted by {player.name}. "
                    f"They showed the card: '{refutation_card}'."
                )

        # No refutations found
        return (
            f"Suggestion made: {character_name} with the {weapon_name} in the {room_name}. "
            "No one could refute."
        )

    def process_accusation(self, accusing_character, accused_character, accused_weapon, accused_room):
        """
        Process a player's accusation and provide feedback.

        :param accusing_character: The name of the character making the accusation.
        :param accused_character: The name of the character being accused.
        :param accused_weapon: The name of the weapon being accused.
        :param accused_room: The name of the room being accused.
        """
        print(f"Processing accusation: {accusing_character} accuses {accused_character} "
              f"with {accused_weapon} in {accused_room}"
        )
        # Normalize inputs
        accused_character = normalize_input(accused_character)
        accused_weapon = normalize_input(accused_weapon)
        accused_room = normalize_input(accused_room)

        # Normalize solution data
        solution_character, solution_weapon, solution_room = self.solution
        solution_character_name = normalize_input(solution_character.name)
        solution_weapon_name = normalize_input(solution_weapon.name)
        solution_room_name = normalize_input(solution_room.name)

        # Prevent self-accusation
        if normalize_input(accusing_character) == accused_character:
            return f"{accusing_character}, you cannot accuse yourself!"

        # Check if the accusation matches the solution
        if (
            accused_character == solution_character_name
            and accused_weapon == solution_weapon_name
            and accused_room == solution_room_name
        ):
            return "Accusation correct! You've solved the mystery!"

        # Provide feedback on incorrect accusation
        feedback = []
        if accused_character != solution_character_name:
            feedback.append(f"Character '{accused_character}' is incorrect.")
        if accused_weapon != solution_weapon_name:
            feedback.append(f"Weapon '{accused_weapon}' is incorrect.")
        if accused_room != solution_room_name:
            feedback.append(f"Room '{accused_room}' is incorrect.")

        return "Accusation incorrect. Feedback:\n" + "\n".join(feedback)

    def get_room_connections(self, room_name):
        """
        Get a list of connected rooms for the given room.

        :param room_name: The room name for which connections are to be retrieved.
        :return: A list of names of connected rooms.
        """
        room = next((r for r in self.rooms if r.name == room_name), None)
        if room:
            return [connected_room.name for connected_room in room.connected_rooms]
        return []

    def display_filtered_game_state(self, current_player):
        """
        Display the game state relevant to the current player.
        """
        current_room = current_player.position
        print(f"\nYou are currently in the {current_room}.")
        connected_rooms = self.get_room_connections(current_room)
        print(f"Connected rooms: {', '.join(connected_rooms)}")

class PlayerNotes:
    """
    Tracks player notes, including suggestions and refutations, during the Cluedo game.

    Responsibilities:
    - Storing suggestions made by players.
    - Recording which player refuted a suggestion, if any.
    - Displaying a summary of all suggestions for review.

    Attributes:
        suggestions (list[dict]): A list of suggestions with details about refutations.
    """
    def __init__(self):
        """
        Initialize the PlayerNotes object.

        Attributes:
            suggestions (list[dict]): Stores a list of dictionaries, where each dictionary
                                      represents a suggestion with details like character, weapon,
                                      room, and who refuted the suggestion (if any).
        """
        self.suggestions = []

    def add_suggestion(self, character, weapon, room, refuted_by=None):
        """
        Add a suggestion to the player's notes.

        Args:
            character (str): The name of the suggested character.
            weapon (str): The name of the suggested weapon.
            room (str): The name of the suggested room.
            refuted_by (str, optional): The name of the player who refuted the suggestion, if any.

        Example:
            player_notes.add_suggestion("Scarlett", "Rope", "Library", refuted_by="Mustard")
        """
        self.suggestions.append({
            "character": character,
            "weapon": weapon,
            "room": room,
            "refuted_by": refuted_by
        })

    def view_notes(self):
        """
        Display all stored suggestions and their refutations, if any.

        Prints a list of suggestions in the format:
            - Suggested: <character> with <weapon> in <room>
            - Refuted by: <refuted_by> (if applicable)
        """
        print("\nPlayer Notes:")
        for note in self.suggestions:
            print(f"Suggested: {note['character']} with {note['weapon']} in {note['room']}")
            if note["refuted_by"]:
                print(f" - Refuted by {note['refuted_by']}")
        print("\n")

class BayesianReasoner:
    """
    Implements Bayesian reasoning to deduce the most likely solution to the Cluedo game.

    Responsibilities:
    - Maintains probabilities for all possible combinations of character, weapon, and room.
    - Updates probabilities based on refutations or confirmations of suggestions.
    - Provides the most likely combination based on current probabilities.

    Attributes:
        probabilities (dict): A dictionary mapping (character, weapon, room) combinations
                              to their respective probabilities.
    """
    def __init__(self, characters, weapons, rooms):
        """
        Initialize the Bayesian reasoner with uniform probabilities for all combinations.

        Args:
            characters (list): List of characters.
            weapons (list): List of weapons.
            rooms (list): List of rooms.
        """
        self.probabilities = {
            (c, w, r): 1 / (len(characters) * len(weapons) * len(rooms))
            for c in characters
            for w in weapons
            for r in rooms
        }

    def update_probabilities(self, character, weapon, room, refuted):
        """
        Update the probabilities for a given suggestion based on whether it was refuted.

        Args:
            character (str): The suggested character.
            weapon (str): The suggested weapon.
            room (str): The suggested room.
            refuted (bool): Whether the suggestion was refuted.
        """
        key = (character, weapon, room)
        if key not in self.probabilities:
            raise ValueError(f"Invalid combination: {key}")

        # Adjust probabilities based on refutation
        if refuted:
            self.probabilities[key] *= 0.5  # Decrease likelihood
        else:
            self.probabilities[key] *= 2  # Increase likelihood

        # Normalize probabilities to maintain a valid distribution
        total = sum(self.probabilities.values())
        for k in self.probabilities:
            self.probabilities[k] /= total

    def get_most_likely(self):
        """
        Get the combination with the highest likelihood.

        Returns:
            tuple: The most likely (character, weapon, room).
        """
        return max(self.probabilities, key=self.probabilities.get)
