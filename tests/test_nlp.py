from re import sub
from dnd_nlp_kg.nlp import logic, Triple

def test_triple_generation():
    triple = logic("Bart hates school.")
    assert Triple(subject="Bart", predicate="hates", object="school") in triple

def test_triples_generation():
    triples = logic("Bart is the brother of Lisa. Homer is married to Marge. Maggie is the daughter of Homer.")
    assert Triple(subject="Bart", predicate="is the brother of", object="Lisa") in triples
    assert Triple(subject="Homer", predicate="is married", object="Marge") in triples
    assert Triple(subject="Maggie", predicate="is the daughter of", object="Homer") in triples