# Import necessary modules
from rasa_nlu.training_data import load_data
from rasa_nlu.model import Trainer
from rasa_nlu import config
from constants import MODEL_PATH
import spacy

# Create a trainer that uses this config
trainer = Trainer(config.load("./config/config_spacy.yml"))

# Load the training data
training_data = load_data('./config/rasa.md')
# training_data = load_data('./config/rasa.json')

# Train Model
interpreter = trainer.train(training_data)
folder_name, project_name, fixed_model_name = MODEL_PATH.split('/')[1:]
trainer.persist(folder_name, project_name=project_name, fixed_model_name=fixed_model_name)

print('=-=-=-=-=-=-=-=-=-=')
print('Model Training Done')
print('=-=-=-=-=-=-=-=-=-=')

nlp = spacy.load("en")
# nlp = spacy.load("en_core_web_md")

# Define included entities
include_entities = ['DATE', 'TIME', 'GPE', 'PERSON', 'ORG', 'FAC']


# Define extract_entities()
def extract_entities(message, given_ents = None):
    ents = dict.fromkeys(include_entities) if given_ents is None else given_ents
    # Create a spacy document
    doc = nlp(message)
    print(doc.ents)
    for ent in doc.ents:
        if ent.label_ in ents:
            # Save interesting entities
            if ent.label_ == 'PERSON':
                if ent.label_ in ents and ents[ent.label_] is not None:
                    # append to array
                    ents[ent.label_].append(ent)
                else:
                    # create new array
                    ents[ent.label_] = [ent]
            else:
                ents[ent.label_] = ent

    print(ents)
    return ents
