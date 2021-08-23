from typing import Counter, Generator
from spacy.tokens import Doc
import spacy
import os
from utils import file_generator

def get_pos_counts(doc: Doc) -> Counter:
    token_count = 0
    pos_counts = Counter()

    token_count += len(doc)
            
    for token in doc:
        pos_counts[token.tag_] += 1

    return pos_counts

def main():
    nlp = spacy.load("da_core_news_sm", exclude=["parser", "ner", "lemmatizer", "textcat"]) # Disable unused elements in the pipeline

    pos_total = Counter()

    for count, doc in  enumerate(nlp.pipe(file_generator(dir), batch_size=2, n_process=4)):
        if count >= 10: # Arbitrary breakpoint for faster iteration in development
            break
    
        pos_total += doc._.pos_counts
    
    print(pos_total)


if __name__ == "__main__":
    dir = "./danavis"

    Doc.set_extension("pos_counts", getter=get_pos_counts)

    main()