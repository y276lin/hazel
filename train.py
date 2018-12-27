# Import necessary modules
from rasa_nlu.training_data import load_data
from rasa_nlu.model import Trainer
from rasa_nlu import config
from constants import MODEL_PATH

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
