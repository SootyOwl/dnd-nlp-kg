from nlp import logic as make_triples_from_string
from vis import logic as make_graph_from_triples
from vis import save_graph

def read_file(filename) -> str:
    return open(filename, 'r').read()

def read_input() -> str:
    return input("\n\nCreate knowledge graph from input text:\n")

def main(input_text: str):
    triples = make_triples_from_string(input_text)
    graph = make_graph_from_triples(triples)
    save_graph(graph, f_name=input("graph filename:"))


if __name__ == '__main__':
    main(input_text=read_file("dnd_nlp_kg/data/lotr.txt"))
    # main(input_text=read_input())