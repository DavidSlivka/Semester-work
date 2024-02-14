#!/usr/bin/env python3

import matplotlib.pyplot as plt
import time

from nearest_neighbour import nearest_neighbour
from cheapest_link import cheapest_link
from christofides import christofides
from vertex import Graph, Vertex
from helper_functions import return_path_from_sequence_pairs, calculate_distance, plot_graph


if __name__ == "__main__":
    file = ''
    number_of_vertices = 25

    # open file or generate vertices
    if file != '':
        vertices = []
        with open(file, 'r') as f:
            for index, line in enumerate(f):
                x, y = line.split(', ')
                vertices.append(Vertex(index, int(x), int(y)))

        graph = Graph(len(vertices), vertices)
    elif number_of_vertices is not None:
        graph = Graph(number_of_vertices)
    else:
        quit()

    times = []
    distances = []

    # Nearest neighbour
    start_time1 = time.perf_counter()

    seq_nn = nearest_neighbour(graph)
    distances.append(calculate_distance(graph.adjacency_matrix, seq_nn))
    time_nn = (time.perf_counter() - start_time1) * 1000
    times.append(time_nn)

    plot_graph(graph, seq_nn, 'Nearest neighbour')

    # Cheapest-link
    start_time2 = time.perf_counter()
    seq_chl = cheapest_link(graph)
    seq_chl = return_path_from_sequence_pairs(seq_chl)
    distances.append(calculate_distance(graph.adjacency_matrix, seq_chl))
    time_chl = (time.perf_counter() - start_time2) * 1000
    times.append(time_chl)

    plot_graph(graph, seq_chl, 'Cheapest-link')

    # Christofides
    start_time3 = time.perf_counter()
    seq_chr = christofides(graph)
    distances.append(calculate_distance(graph.adjacency_matrix, seq_chr))
    time_chr = (time.perf_counter() - start_time3) * 1000
    times.append(time_chr)

    plot_graph(graph, seq_chr, 'Christofides')

    print(distances)
    print(times)

    # plot distance a time graph as a bar graph
    algorithms = ['Nearest Neighbour', 'Cheapest-link', 'Christofides']

    plt.bar(algorithms, distances, color='maroon',
            width=0.4)
    plt.xlabel("Algorithms")
    plt.ylabel("Distances")
    plt.title("Distances")
    plt.show()

    plt.bar(algorithms, times, color='maroon',
            width=0.4)
    plt.xlabel("Algorithms")
    plt.ylabel("Time in ms")
    plt.title("Times")
    plt.show()
