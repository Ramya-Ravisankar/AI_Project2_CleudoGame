"""
Unit tests for Bayesian reasoning logic.
"""

import unittest
from game_logic import BayesianReasoner  # Ensure this matches the location of your BayesianReasoner class

class TestBayesianReasoner(unittest.TestCase):
    def setUp(self):
        """Set up the test environment."""
        self.characters = ["Scarlett", "Mustard"]
        self.weapons = ["Rope", "Revolver"]
        self.rooms = ["Kitchen", "Library"]
        self.reasoner = BayesianReasoner(self.characters, self.weapons, self.rooms)

    def test_update_probabilities(self):
        """Test probability updates."""
        # Update probabilities and check the most likely suggestion
        self.reasoner.update_probabilities("Scarlett", "Rope", "Kitchen", refuted=False)
        most_likely = self.reasoner.get_most_likely()
        self.assertEqual(most_likely, ("Scarlett", "Rope", "Kitchen"))

        # Refute another suggestion and check probabilities
        self.reasoner.update_probabilities("Mustard", "Revolver", "Library", refuted=True)
        updated_prob = self.reasoner.probabilities[("Mustard", "Revolver", "Library")]
        self.assertLess(updated_prob, 1, "Probability should decrease when refuted.")

        # Check normalization
        total_prob = sum(self.reasoner.probabilities.values())
        self.assertAlmostEqual(total_prob, 1, msg="Probabilities should sum to 1.")

if __name__ == "__main__":
    unittest.main()

