from multiprocessing import Process

import networkx as nx
import matplotlib.pyplot as plt
from matplotlib import colors
from itertools import cycle

from handlers.solutions import load_solution
from handlers.instances import get_all_instances_ids


def draw_instance(instance_id):
    solution = load_solution(instance_id)
    if solution:
        G = nx.Graph()
        G.add_nodes_from(range(len(solution["points"])))

        col = cycle(colors.TABLEAU_COLORS)  # type: ignore
        pos = {point['customer_id']: (point['x'], point['y'])
               for point in solution["points"]}

        fig, ax = plt.subplots(figsize=(15, 15), dpi=300)

        print("Drawing instance " + instance_id)
        for route in solution["solution"]:
            nx.add_path(G, route)

            path = []
            for i in range(len(route) - 1):
                path.append((route[i], route[i+1]))

            path_color = next(col)
            nodes_in_path = {x for p in path for x in p}
            node_sizes = [point['demand'] for point in solution["points"]
                          if point['customer_id'] in nodes_in_path]

            nx.draw_networkx_edges(
                G, pos=pos, edgelist=path, ax=ax, edge_color=path_color)
            nx.draw_networkx_nodes(G, pos=pos, nodelist=nodes_in_path, node_size=len(
                node_sizes), node_color=path_color, ax=ax)

        plt.savefig("solutions/{}.png".format(instance_id), dpi=300)
        plt.close()


def draw_solutions():
    instances_ids = get_all_instances_ids()

    for instance_id in instances_ids:
        draw_instance(instance_id)
    # ? For some reason, this doesn't work
    # all_processes = []
    # for instance_id in instances_ids:
    #     p = Process(target=draw_instance, args=(instance_id))
    #     p.start()
    #     all_processes.append(p)
    # for p in all_processes:
    #     p.join()
