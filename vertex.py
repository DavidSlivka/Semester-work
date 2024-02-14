import random
import math

MAX_HEIGHT = 1000
MAX_WIDTH = 1000
DIAGONAL_LENGTH = math.sqrt(MAX_WIDTH ** 2 + MAX_HEIGHT ** 2)


class Vertex:
    def __init__(self, info, x, y):
        self.info = info
        self.x = x
        self.y = y

    def return_coordinates(self):
        return self.x, self.y


class Graph:
    def __init__(self, N, vertices=None):
        self.N = N
        self.vertices = self.initialize_vertices() if vertices is None else vertices
        self.adjacency_matrix = self.get_adjacency_matrix()

    def initialize_vertices(self):
        """
        :param N: Number of vertices
        :return: list of generated vertices
        """
        vertices = []

        for i in range(self.N):
            x = random.randint(0, MAX_WIDTH)
            y = random.randint(0, MAX_HEIGHT)
            vertices.append(Vertex(i, x, y))

        return vertices

    def get_adjacency_matrix(self):
        """
        calculate adjacency matrix of a graph
        :return: adjacency matrix of a graph
        """
        adjacency_matrix = []

        for vertex1 in range(len(self.vertices)):
            lengths = []
            for vertex2 in range(vertex1+1, len(self.vertices)):
                lengths.append(math.sqrt((self.vertices[vertex1].x - self.vertices[vertex2].x) ** 2 + (self.vertices[vertex1].y - self.vertices[vertex2].y) ** 2))
            adjacency_matrix.append(lengths)

        return adjacency_matrix

    def get_sorted_distances(self):
        """
        sort edges according to their lengths from smallest to largest
        :return: sorted list of triplets in a format: [first vertex, second vertex, length of the edge]
        """
        adjacency_matrix = self.adjacency_matrix
        matrix = []
        for first_index in range(len(adjacency_matrix)):
            for second_index in range(len(adjacency_matrix[first_index])):
                matrix.append(
                    [first_index, second_index + first_index + 1, adjacency_matrix[first_index][second_index]])

        return sorted(matrix, key=lambda item: item[2])
