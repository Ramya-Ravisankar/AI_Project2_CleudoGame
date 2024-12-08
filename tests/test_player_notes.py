"""
This module contains unit tests for the `PlayerNotes` class in the Cluedo game.

It verifies the functionality of adding, viewing, and removing notes in the player's notebook.
The tests ensure that the notes are correctly recorded, retrieved, and manipulated.
"""
import unittest
from game_logic import PlayerNotes

class TestPlayerNotes(unittest.TestCase):
    """
    Unit tests for the `PlayerNotes` class.

    The `PlayerNotes` class allows players to:
    - Add suggestions made during the game.
    - View notes for tracking suggestions and refutations.
    - Remove notes if needed (manipulated directly via the `suggestions` list).
    """

    def setUp(self):
        """
        Set up a PlayerNotes object for testing.

        This method initializes a `PlayerNotes` instance that will be used in all tests.
        """
        self.notes = PlayerNotes()

    def test_add_custom_note(self):
        """
        Test adding a custom note to the player's notes.

        This verifies that custom fields can be manually added to a note entry and retrieved correctly.
        """
        self.notes.add_suggestion(None, None, None, refuted_by=None)
        self.notes.suggestions[-1]["custom"] = "This is a custom note"
        self.assertIn(
            {"character": None, "weapon": None, "room": None, "refuted_by": None, "custom": "This is a custom note"},
            self.notes.suggestions
        )

    def test_add_game_suggestion(self):
        """
        Test adding a game suggestion to the notes.

        This verifies that a game suggestion is correctly recorded in the `suggestions` list.
        """
        self.notes.add_suggestion("Scarlett", "Rope", "Library", refuted_by="Mustard")
        self.assertEqual(len(self.notes.suggestions), 1)
        self.assertEqual(
            self.notes.suggestions[0],
            {"character": "Scarlett", "weapon": "Rope", "room": "Library", "refuted_by": "Mustard"}
        )

    def test_remove_note_valid_index(self):
        """
        Test removing a note by a valid index.

        This verifies that notes can be removed correctly using the `pop` method on the `suggestions` list.
        """
        self.notes.add_suggestion("Scarlett", "Rope", "Library")
        self.notes.add_suggestion("Mustard", "Candlestick", "Ballroom")
        removed_note = self.notes.suggestions.pop(0)  # Remove the first note
        self.assertEqual(
            removed_note, {"character": "Scarlett", "weapon": "Rope", "room": "Library", "refuted_by": None})
        self.assertEqual(len(self.notes.suggestions), 1)

    def test_remove_note_invalid_index(self):
        """
        Test trying to remove a note with an invalid index.

        This verifies that attempting to remove a non-existent note raises an `IndexError`.
        """
        self.notes.add_suggestion("Scarlett", "Rope", "Library")
        with self.assertRaises(IndexError):
            self.notes.suggestions.pop(5)  # Attempt to remove a non-existent note

    def test_view_notes(self):
        """
        Test viewing notes and ensuring correct formatting.

        This verifies that the notes are retrieved and formatted as expected for display.
        """
        self.notes.add_suggestion("Scarlett", "Rope", "Library", refuted_by="Mustard")
        self.notes.add_suggestion("Mustard", "Candlestick", "Ballroom")
        # Simulating note formatting
        formatted_notes = [
            f"Suggested: {note['character']} with {note['weapon']} in {note['room']}" +
            (f" - Refuted by {note['refuted_by']}" if note["refuted_by"] else "")
            for note in self.notes.suggestions
        ]
        expected_notes = [
            "Suggested: Scarlett with Rope in Library - Refuted by Mustard",
            "Suggested: Mustard with Candlestick in Ballroom"
        ]
        self.assertEqual(formatted_notes, expected_notes)


if __name__ == "__main__":
    unittest.main()
