# Import necessary modules
from rasa_nlu.training_data import load_data
from rasa_nlu.model import Trainer
from rasa_nlu import config
from constants import MODEL_PATH
import spacy

# Create a trainer that uses this config
trainer = Trainer(config.load("./config/config_spacy.yml"))

# Load the training data
training_data = load_data('./config/rasa.json')

# Train Model
interpreter = trainer.train(training_data)
folder_name, project_name, fixed_model_name = MODEL_PATH.split('/')[1:]
trainer.persist(folder_name, project_name=project_name, fixed_model_name=fixed_model_name)

print('=-=-=-=-=-=-=-=-=-=')
print('Model Training Done')
print('=-=-=-=-=-=-=-=-=-=')

nlp = spacy.load("en_core_web_md")

# Define included entities
include_entities = ['DATE', 'TIME', 'GPE', 'PERSON', 'ORG', 'FAC']


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
