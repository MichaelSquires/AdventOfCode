import math
import logging

import networkx as nx

def parse(data):
    graph = nx.Graph()

    for line in data.splitlines():
        local, remotes = line.split(' <-> ')
        local = int(local)
        remotes = [int(k) for k in remotes.split(',')]

        graph.add_node(local)

        for remote in remotes:
            graph.add_node(remote)
            graph.add_edge(local, remote)

    return graph

def part1(graph):
    seen = set()
    for l,r in nx.bfs_edges(graph, 0):
        seen.add(l)
        seen.add(r)

    return len(seen)

def part2(graph):
    subgraphs = list(nx.k_edge_subgraphs(graph, 1))
    return len(subgraphs)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog=sys.argv[0])

    # Optional arguments
    parser.add_argument('-p', '--part', help='Specify which part to run', type=int, choices=[1,2])
    parser.add_argument('-v', '--verbose', help='Show verbose messages', action='count', default=0)

    # Positional arguments
    parser.add_argument('file', help='Input file', type=open)

    args = parser.parse_args()
    if args.verbose == 1:
        logging.getLogger().setLevel(logging.INFO)
    elif args.verbose == 2:
        logging.getLogger().setLevel(logging.DEBUG)

    try:
        sys.exit(main(args))
    except Exception as exc:
        logging.exception('ERROR in main: %s', exc)
        sys.exit(-1)
