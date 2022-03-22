from collections import namedtuple
from typing import List
import networkx as nx
from random import randint


Triple = namedtuple("Triple", ["subject", "predicate", "object"])


def load_triples():
    return


def logic(triples: List[Triple]) -> nx.MultiDiGraph:
    # create pandas dataframe from Triples
    edges = [
        (
            triple.subject,
            triple.object,
            {"label": triple.predicate, "test": randint(0, 100)},
        )
        for triple in triples
    ]
    G = nx.MultiDiGraph()
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
        },
    )
    pydotgraph = nx.drawing.nx_pydot.to_pydot(G)
    pydotgraph.write_png(
        f"output/{f_name}.pydot.png",
    )
    nx.drawing.nx_pydot.write_dot(G, f"output/{f_name}.dot")


def main():
    triples = load_triples()
    graph = logic(triples)
    save_graph(graph)


if __name__ == "__main__":
    main()
