import unittest
import math

from vertex import Graph, Vertex
from nearest_neighbour import nearest_neighbour
from cheapest_link import cheapest_link
from christofides import *
from helper_functions import *


class TestNearestNeighbour(unittest.TestCase):
    def test_nearest_neighbour(self):
        graph1 = Graph(5, [Vertex(0, 1, 1), Vertex(1, 10, 1), Vertex(2, 10, 10), Vertex(3, 20, 20), Vertex(4, 100, 50)])
        total_sequence1 = [0, 1, 2, 3, 4, 0]

        nn_sequence1 = nearest_neighbour(graph1, 0)

        self.assertEqual(nn_sequence1, total_sequence1)
        self.assertIsInstance(nn_sequence1, list)

        graph2 = Graph(10,
                       [Vertex(0, 0, 0), Vertex(1, 100, 0), Vertex(2, 500, 0), Vertex(3, 1000, 0), Vertex(4, 1000, 100),
                        Vertex(5, 1000, 200), Vertex(6, 1000, 500), Vertex(7, 500, 500), Vertex(8, 0, 500),
                        Vertex(9, 0, 1000)])
        total_sequence2 = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 0]

        nn_sequence2 = nearest_neighbour(graph2, 0)

        self.assertEqual(nn_sequence2, total_sequence2)
        self.assertIsInstance(nn_sequence2, list)


class TestCheapestLink(unittest.TestCase):
    def test_cheapest_link(self):
        graph1 = Graph(6, [Vertex(0, 10, 10), Vertex(1, 110, 10), Vertex(2, 50, 500), Vertex(3, 110, 500),
                           Vertex(4, 50, 550), Vertex(5, 10, 1000)])
        total_sequence1 = [[2, 4], [2, 3], [0, 1], [4, 5], [1, 3]]

        chl_sequence1 = cheapest_link(graph1)

        self.assertEqual(chl_sequence1, total_sequence1)
        self.assertIsInstance(chl_sequence1, list)


class TestHelperFunctions(unittest.TestCase):
    def test_return_leaf(self):
        neighbours = {
            0: [1, 2],
            1: [0],
            2: [0, 3],
            3: [2],
        }
        expected_leaf = 1
        leaf = return_leaf(neighbours)

        self.assertEqual(leaf, expected_leaf)
        self.assertIsInstance(leaf, int)

    def test_return_neighbours_from_pairs(self):
        pairs = [[0, 1], [0, 2], [1, 3], [3, 2]]
        expected_neighbours = {
            0: [1, 2],
            1: [0, 3],
            2: [0, 3],
            3: [1, 2]
        }

        neighbours = return_neighbours_from_pairs(pairs)
        self.assertEqual(expected_neighbours, neighbours)
        self.assertIsInstance(neighbours, dict)

    def test_travers(self):
        neighbours = {
            0: [1, 2],
            1: [0],
            2: [0, 3],
            3: [2],
        }
        expected_path = [1, 0, 2, 3]

        path = travers(1, 1, [], neighbours)
        self.assertEqual(path, expected_path)
        self.assertIsInstance(path, list)

    def test_return_path_from_sequence_pairs(self):
        expected_path = [1, 0, 2, 3, 1]
        path = return_path_from_sequence_pairs([[0, 1], [0, 2], [2, 3]])

        self.assertEqual(path, expected_path)
        self.assertIsInstance(path, list)

    def test_calculate_distance(self):
        graph = Graph(4, [Vertex(0, 0, 0), Vertex(1, 10, 0), Vertex(2, 10, 10), Vertex(3, 20, 10)])
        adjacency_matrix = graph.adjacency_matrix
        path = [1, 0, 2, 3, 1]

        expected_distance = 20 + 2 * math.sqrt(200)

        distance = calculate_distance(adjacency_matrix, path)

        self.assertEqual(distance, expected_distance)
        self.assertIsInstance(distance, float)


class TestChristofides(unittest.TestCase):
    def test_prims(self):
        graph = Graph(4, [Vertex(0, 0, 0), Vertex(1, 10, 0), Vertex(2, 10, 10), Vertex(3, 20, 10)])
        expected_mst = [[0, 1], [1, 2], [2, 3]]
        expected_neighbours = {
            0: [1],
            1: [0, 2],
            2: [1, 3],
            3: [2]
        }

        mst, neighbours = prims(graph)

        self.assertEqual(mst, expected_mst)
        self.assertIsInstance(mst, list)

        self.assertEqual(neighbours, expected_neighbours)
        self.assertIsInstance(neighbours, dict)

    def test_return_vertices_with_odd_degree(self):
        MST = {
            0: [1, 2],
            1: [0],
            2: [0, 3],
            3: [2],
        }

        expected_vertices = [1, 3]
        vertices = return_vertices_with_odd_degree(MST)

        self.assertEqual(vertices, expected_vertices)
        self.assertIsInstance(vertices, list)

        MST = {
            0: [1, 2, 4, 5],
            1: [0],
            2: [0, 3],
            3: [2],
            4: [0],
            5: [0]
        }

        expected_vertices = [1, 3, 4, 5]
        vertices = return_vertices_with_odd_degree(MST)

        self.assertEqual(vertices, expected_vertices)
        self.assertIsInstance(vertices, list)

    def test_remove_duplicate_vertices(self):
        sequence = [0, 1, 2, 1, 3, 2, 4]
        expected_sequence = [0, 1, 2, 3, 4, 0]
        s = remove_duplicate_vertices(sequence, 5)

        self.assertEqual(s, expected_sequence)
        self.assertIsInstance(s, list)

    def test_extend_mst(self):
        MST = {
            0: [1, 2, 4, 5],
            1: [0],
            2: [0, 3],
            3: [2],
            4: [0],
            5: [0]
        }
        pairs = [[3, 5], [1, 4]]

        expected_extended_mst = {
            0: [1, 2, 4, 5],
            1: [0, 4],
            2: [0, 3],
            3: [2, 5],
            4: [0, 1],
            5: [0, 3]
        }

        extended_mst = extend_MST(MST, pairs)

        self.assertEqual(extended_mst, expected_extended_mst)
        self.assertIsInstance(extended_mst, dict)

    def test_eulerian_cycle(self):
        extended_mst = {
            0: [1, 2, 4, 5],
            1: [0, 4],
            2: [0, 3],
            3: [2, 5],
            4: [0, 1],
            5: [0, 3]
        }
        expected_sequence = [0, 1, 4, 0, 2, 3, 5]

        sequence = eulerian_cycle(0, 0, extended_mst, [])

        self.assertEqual(sequence, expected_sequence)
        self.assertIsInstance(sequence, list)

    def test_check_cycle(self):
        neighbours = {
            0: [1, 2, 4, 5],
            1: [0],
            2: [0, 3],
            3: [2],
            4: [0],
            5: [0]
        }
        expected_outcome1 = False

        outcome1 = check_cycle(neighbours, 0, 0, 0)

        self.assertEqual(outcome1, expected_outcome1)
        self.assertIsInstance(outcome1, bool)

        neighbours = {
            0: [1, 2, 4, 5],
            1: [0, 4],
            2: [0, 3],
            3: [2, 5],
            4: [0, 1],
            5: [0, 3]
        }
        expected_outcome2 = True

        outcome2 = check_cycle(neighbours, 0, 0, 0)

        self.assertEqual(outcome2, expected_outcome2)
        self.assertIsInstance(outcome1, bool)

    def test_christofides(self):
        graph = Graph(5, [Vertex(0, 10, 10), Vertex(1, 20, 10), Vertex(2, 30, 30), Vertex(3, 15, 50), Vertex(4, 35, 35)])

        sequence = christofides(graph)

        # whole sequence cannot be tested due to random choice of starting vertex

        self.assertIsInstance(sequence, list)