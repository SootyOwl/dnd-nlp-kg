from collections import namedtuple
from typing import List, Protocol
import networkx as nx
import pandas as pd
import matplotlib.pyplot as plt
from random import randint


Triple = namedtuple("Triple", ["subject", "predicate", "object"])


def load_triples():
    return


def logic(triples: List[Triple]) -> nx.DiGraph:
    # create pandas dataframe from Triples
    edges = [
        (triple.subject, triple.object, {"label": triple.predicate, "test": randint(0, 100)})
        for triple in triples
    ]
    G = nx.DiGraph()
    G.add_edges_from(edges)
    return G


def save_graph(G: nx.Graph, f_name: str = "graph"):
    pos = nx.nx_pydot.graphviz_layout(G, prog="neato")
    nx.draw_networkx_edge_labels(
        G,
        pos,
        edge_labels={
            (u, v): G.get_edge_data(u, v)["label"]
            for u, v in [edge for edge in G.edges]
        }
    )
    pydotgraph = nx.drawing.nx_pydot.to_pydot(G)
    pydotgraph.write_png(f'{f_name}.pydot.png', )
    nx.drawing.nx_pydot.write_dot(G, f"{f_name}.dot")


def main():
    triples = load_triples()
    graph = logic(triples)
    save_graph(graph)


if __name__ == "__main__":
    main()
