import spacy
import os

#KCE: add output type hint
def file_generator(dir: str):
    for filename in sorted(os.listdir(dir)): # KCE: Why sort the dir?
        if "danavis" in filename:
            # KCE use os.path.join to deal with paths (to make it os independent)
            filepath = os.path.join(dir, filename)

            with open(filepath, "r") as f:
                yield f.read()

def main():
    # might as well use the large model here as it just as fast (but better)
    nlp = spacy.load("da_core_news_sm", exclude=["parser", "ner", "lemmatizer", "textcat"]) # Disable unused elements in the pipeline

    doc_number = 0

    token_count = 0
    adverb_count = 0
    pronoun_count = 0

    for doc in  nlp.pipe(file_generator(dir), batch_size=20, n_process=5):
        if doc_number >= 100000:
            break

        doc_number += 1 # KCE: Use enumerate instead of counter

        # KCE: use modulo calc i only print every n
        if doc_number % 1000:
            # KCE: use formatted string or "," in print instead of wrapping in str
            print(f"Processing {doc_number}")
            print("Processing ", doc_number)

        # KCE:alternative to token count
        # token_count += len(doc)
            
        for token in doc:
            token_count += 1

            # try to generalise this to all tags maybe look up counter
            if token.tag_ == "ADV":
                adverb_count += 1
            elif token.tag_ == "PRON":
                pronoun_count += 1

    print("Adverbs: " + str(adverb_count) + ", " + str(round(adverb_count/token_count*100, 3)) + "% of all tokens")
    print("Pronouns: " + str(pronoun_count) + ", " + str(round(pronoun_count/token_count*100, 3)) + "% of all tokens")
    # try to write it to a JSON

if __name__ == "__main__":
    dir = "./danavis"
    
    main()
