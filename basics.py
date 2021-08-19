import spacy
import os

def file_generator(dir: str):
    for filename in sorted(os.listdir(dir)):
        if "danavis" in filename:
            filepath = dir + "/" + filename

            with open(filepath, "r") as f:
                yield f.read()

def main():
    nlp = spacy.load("da_core_news_sm", exclude=["parser", "ner", "lemmatizer", "textcat"]) # Disable unused elements in the pipeline

    doc_number = 0

    token_count = 0
    adverb_count = 0
    pronoun_count = 0

    for doc in  nlp.pipe(file_generator(dir), batch_size=20, n_process=5):
        if doc_number >= 100000:
            break

        doc_number += 1

        print("Processing " + str(doc_number)) # Rough indicator of progress

        for token in doc:
            token_count += 1

            if token.tag_ == "ADV":
                adverb_count += 1
            elif token.tag_ == "PRON":
                pronoun_count += 1

    print("Adverbs: " + str(adverb_count) + ", " + str(round(adverb_count/token_count*100, 3)) + "% of all tokens")
    print("Pronouns: " + str(pronoun_count) + ", " + str(round(pronoun_count/token_count*100, 3)) + "% of all tokens")

if __name__ == "__main__":
    dir = "./danavis"
    
    main()