"""Use SpaCy to extract relationship triples from input text."""

from collections import namedtuple
from typing import List
import spacy
from spacy.matcher import Matcher
import claucy  # noqa

nlp = spacy.load("en_core_web_trf")
# nlp.add_pipe("merge_noun_chunks")
# nlp.add_pipe("merge_entities")
nlp.add_pipe("claucy")

Triple = namedtuple("Triple", ["subject", "predicate", "object"])


def read(filename) -> str:
    """Read example data from a given filename."""
    import os

    dirname = os.path.dirname(__file__)
    filename = os.path.join(dirname, filename)
    with open(filename, "r") as fin:
        return fin.read()


def subtree_matcher(sent):
    subjpass = 0

    for tok in sent:
        # find dependency tag that contains the text "subjpass"
        if not tok.dep_.find("subjpass") == -1:
            subjpass = 1
            break

    x = None
    y = None
    # TODO: use a matcher, define some patterns
    # if subjpass == 1 then sentence is passive
    if subjpass == 1:
        for i, tok in enumerate(sent):
            if not tok.dep_.find("subjpass") == -1:
                y = tok

            if tok.dep_.endswith("obj") is True:
                x = tok

            if x and y:
                break

    # if subjpass == 0 then sentence is not passive
    else:
        for i, tok in enumerate(sent):
            if tok.dep_.endswith("subj") is True:
                x = tok

            if tok.dep_.endswith("obj") is True:
                y = tok

            if x and y:
                break
    return x, y


def get_relation(sent):
    """
    Get relation between sentence entities."""

    # Matcher class object
    matcher = Matcher(nlp.vocab)

    # define the pattern
    pattern = [
        {"DEP": "ROOT"},
        {"DEP": "det", "OP": "?"},
        {"DEP": "attr", "OP": "?"},
        {"DEP": "prep", "OP": "?"},
        #    {'DEP':'agent','OP':"?"},
        {"POS": "ADJ", "OP": "?"},
    ]

    matcher.add("relation", [pattern])

    matches = matcher(sent, as_spans=True, with_alignments=True)
    return matches[-1]


def logic(input: str) -> List[Triple]:
    """Process natural language text to extract relationship triples from every sentence."""
    triples = []
    doc = nlp(input)
    for clause in doc._.clauses:
        props = clause.to_propositions(as_text=False, inflect=None)
        for prop in filter(lambda x: len(x) == 3, props):
            if clause.type == 'SVO':
                subj, pred, obj = prop
            elif clause.type == 'SV' and prop[-1].ents:
                subj, pred, adjunct = prop
                obj = adjunct.ents[0]
                # fix predicate
                pred = pred.text + ' ' + (adjunct.text.replace(obj.text, ''))
            elif clause.type == 'SVC':
                subj, pred, comp = clause.subject, clause.verb, clause.complement
                # fix obj
                if comp.ents:
                    obj = comp.ents[0]
                else:
                    for tok in comp:
                        if tok.dep_.endswith("obj"):
                            obj = tok
                            break
                    else:
                        break
                pred = ' '.join((pred.text, comp.root.text))
            else:
                break
            # turn spans to strings
            ssubj, spred, sobj = map(lambda x: str(x).strip(), [subj, pred, obj])
            triples.append(Triple(ssubj, spred, sobj))
    return triples


def write(triples: List[Triple]) -> None:
    """Output the triples"""
    # just print them
    triple_output: str = "\n".join([str(t) for t in triples])
    print(triple_output)


def main():
    """Run the RLW."""
    input = read("./data/humblewood.txt")
    triple_list = logic(input)
    write(triple_list)


if __name__ == "__main__":
    main()
