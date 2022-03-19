from dnd_nlp_kg.vis import save_graph, logic
import networkx as nx
import pytest
from dnd_nlp_kg.nlp import Triple as TestTriple


@pytest.fixture
def triples():
    return [
        TestTriple("Jamie Lannister", "pushed", "Bran Stark"),
        TestTriple("Jamie Lannister", "father of", "Joffrey Lannister"),
        TestTriple("Joffrey Lannister", "beheaded", "Ned Stark"),
        TestTriple("Ned Stark", "father of", "Bran Stark"),
        TestTriple("Ned Stark", "father of", "Jon Snow"),
        TestTriple("Ned Stark", "father of", "Arya Stark"),
        TestTriple("Ned Stark", "fought beside", "Jamie Lannister"),
        TestTriple("Jamie Lannister", "brother", "Tyrion Lannister"),
        TestTriple("Jamie Lannister", "brother", "Cersei Lannister"),
        TestTriple("Cersei Lannister", "mother of", "Joffrey Lannister"),
        TestTriple("Tyrion Lannister", "killed", "Tywin Lannister"),
        TestTriple("Tywin Lannister", "father of", "Jamie Lannister"),
        TestTriple("Tywin Lannister", "father of", "Cersei Lannister"),
        TestTriple("Tywin Lannister", "father of", "Tyrion Lannister")
    ]

@pytest.fixture
def graph(triples):
    return logic(triples)


def test_create_graph_from_triples(graph):
    assert isinstance(graph, nx.Graph)


def test_graph_contains_correct_nodes(triples, graph):
    nodes = graph.nodes
    for triple in triples:
        assert triple.subject in nodes
        assert triple.object in nodes


def test_graph_edges_connected(triples, graph):
    edges = graph.edges
    for triple in triples:
        assert (triple.subject, triple.object) in edges

def test_graph_edges_correct_label(triples, graph):
    edge_data = [graph.get_edge_data(*edge)['label'] for edge in graph.edges]
    for triple in triples:
        assert triple.predicate in edge_data