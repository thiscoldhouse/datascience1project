from string import punctuation
import re
import textacy
from tabulate import tabulate
import spacy
import fastcoref

nlp = spacy.load('en_core_web_sm')
coref_model = fastcoref.FCoref(device='cpu')

max_length = 25000

def resolve_pronouns(text, return_clusters=False):
    text = text[:max_length]
    doc = nlp(text)
    res = coref_model.predict(texts=[text])[0]
    clusters = res.get_clusters(as_strings=False)

    pronoun_map = {}
    for cluster in clusters:
        head = cluster[0]
        head_text = text[head[0]:head[1]]

        for span in cluster[1:]:
            mention_text = text[span[0]:span[1]]

            for token in doc:
                if (
                        token.idx == span[0] and
                        token.idx + len(token) == span[1]
                ):
                    pronoun_map[token] = head_text

    resolved = []
    for token in doc:
        if token in pronoun_map:
            resolved.append(pronoun_map[token])
        else:
            resolved.append(token.text)

    return " ".join(resolved)


def tag_tokens(text, tag_type='pos'):
    """
    tag options: lemma_, pos_, tag_, dep_,
    shape_, is_alpha, is_stop
    """
    doc = nlp(text)
    for token in doc:
        yield (token.text, getattr(token, tag_type))

               
def extract_svo(text, ):
    doc = nlp(text)
    tuples = textacy.extract.subject_verb_object_triples(doc)
    return list(tuples)


