import matplotlib.pyplot as plt

from vertex import MAX_WIDTH, MAX_HEIGHT


def return_leaf(neighbours: dict):
    """
    return first vertex with degree 1 (has only 1 neighbour)
    :param neighbours: dictionary of vertices and their neighbours
    :return:
    """
    current = None
    for vertex in neighbours:
        if len(neighbours[vertex]) == 1:
            current = vertex
            break

    return current


def return_neighbours_from_pairs(sequence: list):
    """
    :param sequence: array of pairs that form a path
    :return: dictionary of all vertices and their neighbours
    """
    neighbours = {}
    for pair in sequence:
        if pair[0] in neighbours:
            neighbours[pair[0]].append(pair[1])
        else:
            neighbours[pair[0]] = [pair[1]]

        if pair[1] in neighbours:
            neighbours[pair[1]].append(pair[0])
        else:
            neighbours[pair[1]] = [pair[0]]

    return neighbours


def travers(current: int, prev: int, path: list, neighbours: dict):
    """
    create a path from dict of neighbours
    :param current: current vertex
    :param prev: previous vertex
    :param path: path from neighbours that is recursively created from one leaf to another
    :param neighbours: dict of all vertices and their neighbours
    :return: path from one leaf to another
    """
    path.append(current)

    if len(path) == len(neighbours):
        return path
    for vertex in neighbours[current]:
        if vertex != prev:
            return travers(vertex, current, path, neighbours)


def return_path_from_sequence_pairs(sequence: list):
    """
    wrapper function
    :param sequence: array of pairs of vertices
    :return: array of vertices in order that form hamiltonian circuit
    """
    path = None
    if all(len(pair) == 2 for pair in sequence):
        neighbours = return_neighbours_from_pairs(sequence)
        current = return_leaf(neighbours)
        path = travers(current, current, [], neighbours)
        path.append(current)
    return path


def calculate_distance(adjacency_matrix: list, sequence: list):
    """
    calculates distance of hamiltonian circuit
    :param adjacency_matrix: adjacency matrix of a graph
    :param sequence: array of vertices in order that form hamiltonian circuit
    :return:
    """
    total_distance = 0
    for vertex_index in range(len(sequence)-1):
        first_vertex = sequence[vertex_index]
        second_vertex = sequence[vertex_index+1]
        if first_vertex < second_vertex:
            total_distance += adjacency_matrix[first_vertex][second_vertex-first_vertex-1]
        else:
            total_distance += adjacency_matrix[second_vertex][first_vertex-second_vertex-1]

    return total_distance


def plot_graph(graph, sequence: list, title: str):
    """
    plot hamiltonian circuit
    :param graph: class graph
    :param sequence: sequence of vertices that form a hamiltonian circuit
    :param title: title of the graph
    :return:
    """
    x_coords = [graph.vertices[i].x for i in range(graph.N)]
    y_coords = [graph.vertices[i].y for i in range(graph.N)]
    for i in range(graph.N):
        plt.text(x_coords[i], y_coords[i], i)
    for index in range(len(sequence) - 1):
        plt.plot([graph.vertices[sequence[index]].x, graph.vertices[sequence[index + 1]].x],
                 [graph.vertices[sequence[index]].y, graph.vertices[sequence[index + 1]].y], 'bo-')
    step = MAX_WIDTH // 10
    plt.xticks([i for i in range(0, MAX_WIDTH + 1, step)])
    plt.yticks([i for i in range(0, MAX_HEIGHT + 1, step)])
    plt.title(title)
    plt.show()