import random

from vertex import DIAGONAL_LENGTH


def nearest_neighbour(graph, start=None):
    """
    algorithm that creates path using nearest neighbour algorithm
    :param graph: graph class
    :param start: starting vertex to form a path through all vertices
    :return: sequence of vertices to create hamiltonian circuit
    """
    adjacency_matrix = graph.adjacency_matrix
    number_of_vertices = graph.N
    if start is None:
        start = random.randint(0, number_of_vertices-1)
    sequence = [start]
    visited = [False] * number_of_vertices
    visited[start] = True

    for j in range(number_of_vertices):
        last_visited_vertex = sequence[-1]
        distance = DIAGONAL_LENGTH
        closest_vertex = None
        for i in range(len(adjacency_matrix[last_visited_vertex])):
            if adjacency_matrix[last_visited_vertex][i] < distance and visited[last_visited_vertex + i + 1] is False:
                distance = adjacency_matrix[last_visited_vertex][i]
                closest_vertex = last_visited_vertex + i + 1

        for i in range(last_visited_vertex):
            if adjacency_matrix[i][last_visited_vertex - number_of_vertices] < distance and visited[i] is False:
                distance = adjacency_matrix[i][last_visited_vertex - number_of_vertices]
                closest_vertex = i

        if closest_vertex is not None:
            sequence.append(closest_vertex)
            visited[closest_vertex] = True

    sequence.append(sequence[0])
    return sequence
