from typing import Counter, Generator
import spacy
import os
import json
from utils import file_generator

def main():
    nlp = spacy.load("da_core_news_sm", exclude=["parser", "ner", "lemmatizer", "textcat"]) # Disable unused elements in the pipeline

    token_count = 0
    pos_counts = Counter()

    for count, doc in  enumerate(nlp.pipe(file_generator(dir), batch_size=2, n_process=4)):
        if count >= 10: # Arbitrary breakpoint for faster iteration in development
            break

        if count % 5 == 0:
            print(f"Processing {count}")

        token_count += len(doc)
            
        for token in doc:
            pos_counts[token.tag_] += 1 #Loving counters right here

    print(f"Adverbs: {pos_counts['ADV']}, {round(pos_counts['ADV']/token_count*100, 3)}% of all tokens")
    print(f"Pronouns: {pos_counts['PRON']}, {round(pos_counts['PRON']/token_count*100, 3)}% of all tokens")

    with open("tag_counts.json", "w") as f:
        json.dump(pos_counts, f)

if __name__ == "__main__":
    dir = "./danavis"
    
    main()
