import random
import copy

from vertex import DIAGONAL_LENGTH


def check_cycle(neighbours: dict, start: int, prev: int, end: int):
    """
    check if we created a loop by adding previous edge to graph
    :param neighbours: dictionary of vertices and their neighbours as values stored in an array
    :param start: starting vertex
    :param prev: previously visited vertex
    :param end: ending vertex
    :return:
    """
    stack = [(start, prev, [])]
    while stack:
        state, prev, path = stack.pop()
        if path and state == end:
            return True
        for next_state in neighbours[state]:
            if next_state not in path and next_state != prev:
                stack.append((next_state, state, path + [next_state]))
    return False


def prims(graph):
    """
    prims algorithm to create MST
    :param graph: class Graph
    :return: MST and dictionary of vertices and their neighbours
    """

    matrix = graph.get_sorted_distances()

    number_of_vertices = graph.N
    neighbours = {}
    minimal_spanning_tree = []

    matrix_index = 0
    while len(minimal_spanning_tree) < number_of_vertices - 1:
        first_vertex = matrix[matrix_index][0]
        second_vertex = matrix[matrix_index][1]
        if first_vertex in neighbours and second_vertex in neighbours:
            neighbours[first_vertex].append(second_vertex)
            neighbours[second_vertex].append(first_vertex)
            if not check_cycle(neighbours, first_vertex, first_vertex, first_vertex):
                minimal_spanning_tree.append([first_vertex, second_vertex])
            else:
                neighbours[first_vertex].remove(second_vertex)
                neighbours[second_vertex].remove(first_vertex)

        # extend on one side
        elif first_vertex in neighbours and second_vertex not in neighbours:
            neighbours[first_vertex].append(second_vertex)
            neighbours[second_vertex] = [first_vertex]
            minimal_spanning_tree.append([first_vertex, second_vertex])

        elif first_vertex not in neighbours and second_vertex in neighbours:
            neighbours[first_vertex] = [second_vertex]
            neighbours[second_vertex].append(first_vertex)
            minimal_spanning_tree.append([first_vertex, second_vertex])

        # create new partition
        else:
            neighbours[first_vertex] = [second_vertex]
            neighbours[second_vertex] = [first_vertex]
            minimal_spanning_tree.append([first_vertex, second_vertex])

        matrix_index += 1

    return minimal_spanning_tree, neighbours


def return_vertices_with_odd_degree(MST: dict):
    """
    loops through graph and returns vertices with odd degree
    :param MST: dictionary with vertices as keys and their neighbours as values
    :return: list of vertices with odd number of neighbours (degree)
    """
    odd_vertices = []
    for vertex in MST:
        if len(MST[vertex]) % 2 == 1:
            odd_vertices.append(vertex)

    return odd_vertices


def perfect_pairing(adjacency_matrix: list, vertices: list):
    """
    pair vertices with odd degree to their closest vertex with odd degree
    :param adjacency_matrix: adjacency matrix of a graph
    :param vertices: list of vertices with odd degree
    :param mst: MST of a graph
    :return:
    """
    random.shuffle(vertices)
    pairings = []
    while vertices:
        v = vertices.pop()
        length = DIAGONAL_LENGTH
        closest = vertices[0]
        for u in vertices:
            if u > v:
                if v != u and adjacency_matrix[v][u - v - 1] < length:
                    length = adjacency_matrix[v][u - v - 1]
                    closest = u
            else:
                if v != u and adjacency_matrix[u][v - u - 1] < length:
                    length = adjacency_matrix[u][v - u - 1]
                    closest = u

        pairings.append([v, closest])
        vertices.remove(closest)
    return pairings


def extend_MST(MST: dict, entensions: list):
    """

    :param MST: Minimal Spanning Tree
    :param entensions: list od pairs that contain new edges that are added to the MST
    :return: extended MST with new edges
    """
    for entention in entensions:
        MST[entention[0]].append(entention[1])
        MST[entention[1]].append(entention[0])

    return MST


def eulerian_cycle(start: int, current: int, extended_mst: dict, sequence: list):
    """
    recursively find an euler's tour through all vertices
    :param start: starting vertex
    :param current: current vertex that is being visited
    :param extended_mst: MST that is extended with edges of vertices that were odd in MST
    :param sequence: sequence of vertices that form euler's tour
    :return: param sequence (sequence of vertices that form euler's tour)
    """
    if sequence is not []:
        if all(v in sequence for v in extended_mst):
            return sequence

    for vertex in extended_mst[current]:
        sequence.append(current)
        del extended_mst[vertex][extended_mst[vertex].index(current)]
        del extended_mst[current][extended_mst[current].index(vertex)]
        s = eulerian_cycle(start, vertex, extended_mst, sequence)
        if s:
            return s
        if sequence is not []:
            extended_mst[vertex].append(current)
            extended_mst[current].append(vertex)
            sequence.pop(-1)
    return False


def remove_duplicate_vertices(sequence: list, number_of_vertices: int):
    """
    function that removes duplicated vertices in a sequence of vertices that form a path,
    and add first vertex to form an eulerian path
    :param sequence: sequence that form a path through all vertices
    :param number_of_vertices: number of vertices in a graph
    :return:
    """
    visited = [False] * number_of_vertices
    new_sequence = []
    for vertex in sequence:
        if visited[vertex] is False:
            new_sequence.append(vertex)
            visited[vertex] = True

    new_sequence.append(new_sequence[0])
    return new_sequence


def christofides(graph):
    """
    wrapper function that assembles all functions together
    :param graph: class Graph
    :return: list of vertices that form a hamiltonian circuit using christofides algorithm
    """
    seq, tree = prims(graph)
    odd_degrees = return_vertices_with_odd_degree(tree)
    pairings = perfect_pairing(graph.adjacency_matrix, odd_degrees)
    extended_mst = extend_MST(tree, pairings)
    pairs = []
    for vertex in extended_mst:
        for vertex2 in extended_mst[vertex]:
            pairs.append([vertex, vertex2])

    sequence = None
    while sequence is None:
        start = random.choice(list(extended_mst.keys()))
        MST = copy.deepcopy(extended_mst)
        sequence = eulerian_cycle(start, start, MST, [])
        sequence = remove_duplicate_vertices(sequence, graph.N)

    return sequence
