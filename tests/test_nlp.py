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

def test_noun_expansion():
    input = "Bart attends Springfield Elementary School. Homer works at Springfield Nuclear Power Plant"
    expected = [
        Triple("Bart", "attends", "Springfield Elementary School"),
        Triple("Homer", "works at", "Springfield Nuclear Power Plant"),
    ]
    triples = logic(input)
    for test in expected:
        assert test in triples

def test_conjuctions():
    input = "Bart and Lisa attend school. Lenny and Carl both drink at the bar."
    expected = [
        Triple("Bart", "attend", "school"),
        Triple("Lisa", "attend", "school"),
        Triple("Lenny", "drink at", "bar"),
        Triple("Carl", "drink at", "bar"),
    ]
    triples = logic(input)
    for test in expected:
        assert test in triples

def test_passive_sentences():
    input = "The saxophone was played by Lisa. Bart was strangled by Homer."
    expected = [Triple("Lisa", "played", "saxophone"), Triple("Homer", "strangled", "Bart")]
    triples = logic(input)
    for test in expected:
        assert test in triples