import unittest
import networkx as nx
from utils import condense_graph

class TestCondenseGraph(unittest.TestCase):
    def test_condense_graph_no_condensation(self):
        # Create a small graph with no node exceeding threshold
        G_raw = nx.DiGraph()
        G_raw.add_edge("A", "B", label="job1")
        G_raw.add_edge("B", "C", label="job2")
        
        condensed_G = condense_graph(G_raw, 5)
        
        self.assertEqual(len(condensed_G.nodes()), 3)
        self.assertEqual(len(condensed_G.edges()), 2)
        self.assertIn("A", condensed_G)
        self.assertIn("B", condensed_G)
        self.assertIn("C", condensed_G)
        self.assertEqual(condensed_G["A"]["B"]["label"], "job1")

    def test_condense_graph_with_chokepoint(self):
        # Create a graph where A is a chokepoint (threshold = 2, successors = 3)
        G_raw = nx.DiGraph()
        G_raw.add_edge("A", "B", label="jobB")
        G_raw.add_edge("A", "C", label="jobC")
        G_raw.add_edge("A", "D", label="jobD")
        G_raw.add_edge("D", "E", label="jobE") # E is successor of D, which is condensed
        
        condensed_G = condense_graph(G_raw, 2)
        
        # Expected: A -> Condensed_from_A. B, C, D are hidden.
        # D -> E exists, so Condensed_from_A -> E should be created.
        
        self.assertIn("A", condensed_G)
        self.assertIn("Condensed_from_A", condensed_G)
        self.assertIn("E", condensed_G)
        self.assertNotIn("B", condensed_G)
        self.assertNotIn("C", condensed_G)
        self.assertNotIn("D", condensed_G)
        
        self.assertTrue(condensed_G.has_edge("A", "Condensed_from_A"))
        self.assertTrue(condensed_G.has_edge("Condensed_from_A", "E"))
        
        # Check labels
        self.assertEqual(condensed_G.nodes["Condensed_from_A"]["label"], "[3 nodes]")
        # Edge label from D to E should be preserved
        self.assertEqual(condensed_G["Condensed_from_A"]["E"]["label"], "jobE")

    def test_condense_graph_multiple_parents(self):
        # Graph: A -> B, A -> C, A -> D (A is chokepoint)
        # X -> B (B has another parent X)
        G_raw = nx.DiGraph()
        for node in ["B", "C", "D"]:
            G_raw.add_edge("A", node, label=f"job_{node}")
        G_raw.add_edge("X", "B", label="job_X_B")
        
        condensed_G = condense_graph(G_raw, 2)
        
        # Expected: A -> Condensed_from_A, X -> Condensed_from_A
        self.assertIn("A", condensed_G)
        self.assertIn("X", condensed_G)
        self.assertIn("Condensed_from_A", condensed_G)
        self.assertTrue(condensed_G.has_edge("A", "Condensed_from_A"))
        self.assertTrue(condensed_G.has_edge("X", "Condensed_from_A"))

    def test_condense_graph_nested_condensation(self):
        # A -> B, A -> C, A -> D (A chokepoint)
        # B -> E, B -> F, B -> G (B chokepoint)
        G_raw = nx.DiGraph()
        for node in ["B", "C", "D"]:
            G_raw.add_edge("A", node, label=f"job_A_{node}")
        for node in ["E", "F", "G"]:
            G_raw.add_edge("B", node, label=f"job_B_{node}")
            
        condensed_G = condense_graph(G_raw, 2)
        
        # Expected: A -> Condensed_from_A -> Condensed_from_B
        self.assertIn("A", condensed_G)
        self.assertIn("Condensed_from_A", condensed_G)
        self.assertIn("Condensed_from_B", condensed_G)
        self.assertTrue(condensed_G.has_edge("A", "Condensed_from_A"))
        self.assertTrue(condensed_G.has_edge("Condensed_from_A", "Condensed_from_B"))

if __name__ == '__main__':
    unittest.main()
