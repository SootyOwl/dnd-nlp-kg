from nlp import logic as make_triples_from_string
from vis import logic as make_graph_from_triples
from vis import save_graph
from smart_open import open
import json


def read_file(filename) -> str:
    return open(filename, 'r').read()


def read_nyt10() -> str:
    with open('dnd_nlp_kg/data/nyt10/nyt10_test.txt') as f:
        raw_data = f.readlines()

    return_string = '\n'.join([json.loads(j)['text'] for j in raw_data[:100]])
    return return_string


def read_input() -> str:
    return input("\n\nCreate knowledge graph from input text:\n")


def main(input_text: str):
    triples = make_triples_from_string(input_text)
    graph = make_graph_from_triples(triples)
    save_graph(graph, f_name=input("graph filename:"))


if __name__ == '__main__':
    main(input_text=read_nyt10())
    # main(input_text=read_input())