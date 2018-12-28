import spacy

nlp = spacy.load("en_core_web_md")

# Define included entities
include_entities = ['DATE','TIME', 'GPE', 'PERSON']


# Define extract_entities()
def extract_entities(message):
    ents = dict.fromkeys(include_entities)
    # Create a spacy document
    doc = nlp(message)
    for ent in doc.ents:
        if ent.label_ in ents:
            # Save interesting entities
            ents[ent.label_] = ent
    return ents


print(extract_entities('David needs to finish the final project before 6:00 pm on Sunday in Waterloo'))
print(extract_entities('Yuxin who graduated from MIT in 1999'))
