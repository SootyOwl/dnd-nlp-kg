"""Use SpaCy to extract relationship triples from input text."""

from collections import namedtuple
from dataclasses import dataclass
from typing import List
import spacy
from spacy.matcher import Matcher
import coreferee

nlp = spacy.load('en_core_web_sm')
nlp.add_pipe('merge_entities')
nlp.add_pipe('sentencizer')
nlp.add_pipe('coreferee')

@dataclass
class Triple:
    subject: str
    predicate: str
    object: str

    def __str__(self) -> str:
        return f"({self.subject}, {self.predicate}, {self.object})"


def read(filename) -> str:
    """Read example data from a given filename."""
    import os
    dirname = os.path.dirname(__file__)
    filename = os.path.join(dirname, filename)
    with open(filename, 'r') as fin:
        return '. '.join([line.strip() for line in fin.readlines()])

def subtree_matcher(doc):
    subjpass = 0

    for tok in doc:
        # find dependency tag that contains the text "subjpass"    
        if not tok.dep_.find("subjpass") == -1:
            subjpass = 1
            break

    x = ''
    y = ''
    # TODO: use a matcher, define some patterns
    # if subjpass == 1 then sentence is passive
    if subjpass == 1:
        for i,tok in enumerate(doc):
            if tok.dep_.find("subjpass") == True:
                y = tok

            if tok.dep_.endswith("obj") == True:
                x = tok

            if x and y:
                break
    
    # if subjpass == 0 then sentence is not passive
    else:
        for i,tok in enumerate(doc):
            if tok.dep_.endswith("subj") == True:
                x = tok

            if tok.dep_.endswith("obj") == True:
                y = tok

            if x and y:
                break

    return x,y

def get_relation(doc):
    """
    Get relation between sentence entities."""

    # Matcher class object
    matcher = Matcher(nlp.vocab)

    #define the pattern
    pattern = [{'DEP':'ROOT'},
               {'DEP': 'det', 'OP': "?"},
               {'DEP': 'attr', 'OP': "?"},
               {'DEP':'prep','OP':"?"},
            #    {'DEP':'agent','OP':"?"},
               {'POS':'ADJ','OP':"?"}
               ]

    matcher.add("relation", [pattern])

    matches = matcher(doc)
    k = len(matches) - 1

    span = doc[matches[k][1] : matches[k][2]]

    return(span)

def logic(input: str) -> List[Triple]:
    """Process natural language text to extract relationship triples from every sentence."""
    triples = []
    doc = nlp(input)
    for sent in doc.sents:
        subj, obj = subtree_matcher(sent)
        pred = get_relation(sent)
        # get subject and conjuncts
        for sub in (subj, *subj.conjuncts):
            triples.append(Triple(sub.text, pred.text, obj.text))
    return triples
    

def write(triples: List[Triple]) -> None:
    """Output the triples"""
    # just print them
    triple_output: str = '\n'.join([str(t) for t in triples])
    print(triple_output)

def main():
    """Run the RLW."""
    input = read('./data/tarakona.txt')
    triple_list = logic(input)
    write(triple_list)

if __name__ == "__main__":
    main()