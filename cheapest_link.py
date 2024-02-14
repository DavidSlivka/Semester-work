def check_cycle(start, current, previous, visited):
    """

    :param start: starting vertex
    :param current: current vertex that is being checked
    :param previous: previous vertex to prevent loops
    :param visited: already visited vertices with edges format: {vertex: [connected vertices]}
    :return:
    """
    for vertex in visited[current]:
        if vertex != previous and vertex != start:
            return check_cycle(start, vertex, current, visited)
        elif vertex == previous:
            pass
        else:
            return True
    return False


def cheapest_link(graph) -> [list, float]:
    """
    algorithm that creates path through all vertices using cheapest-link algorithm
    :param graph: class graph
    :return: list containing path through all vertices and total distance
    """
    matrix = graph.get_sorted_distances()

    number_of_vertices = graph.N
    visited = {}
    sequence = []

    matrix_index = 0
    while len(sequence) < number_of_vertices - 1:
        first_vertex = matrix[matrix_index][0]
        second_vertex = matrix[matrix_index][1]
        if first_vertex in visited and second_vertex in visited:
            if len(visited[first_vertex]) < 2 and len(visited[second_vertex]) < 2:
                visited[first_vertex].append(second_vertex)
                visited[second_vertex].append(first_vertex)
                if not check_cycle(first_vertex, first_vertex, first_vertex, visited):
                    sequence.append([first_vertex, second_vertex])
                else:
                    visited[first_vertex].remove(second_vertex)
                    visited[second_vertex].remove(first_vertex)

        # extend on one side
        elif first_vertex in visited and second_vertex not in visited:
            if len(visited[first_vertex]) < 2:
                visited[first_vertex].append(second_vertex)
                visited[second_vertex] = [first_vertex]
                sequence.append([first_vertex, second_vertex])

        elif first_vertex not in visited and second_vertex in visited:
            if len(visited[second_vertex]) < 2:
                visited[first_vertex] = [second_vertex]
                visited[second_vertex].append(first_vertex)
                sequence.append([first_vertex, second_vertex])

        # create new partition
        else:
            visited[first_vertex] = [second_vertex]
            visited[second_vertex] = [first_vertex]
            sequence.append([first_vertex, second_vertex])

        matrix_index += 1

    return sequence
