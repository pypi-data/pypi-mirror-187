"""
Downloads, installs and loads up the specified Spacy language model
"""

import spacy
import sys, os


# Spacy model name
MODEL = "en_core_web_lg"

# Getting local environment download path
env_loc = os.path.dirname(sys.executable)
env_loc = env_loc.replace("Scripts", f"Lib\\site-packages\\{MODEL}")

# Downloading SpaCy model
if not os.path.exists(env_loc):
    spacy.cli.download(MODEL)
    
# Spacy nlp object for NER tasks
nlp = spacy.load(MODEL)
