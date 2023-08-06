"""
Downloads, installs and loads up the specified Spacy language model
"""

import spacy
import sys, os


def get_spacy_object(model: str='en_core_web_sm'):
    """
    Fetch spacy model object for nlp tasks.

    Keyword Arguments:
        model -- Name of the spacy language model (default: {'en_core_web_sm'})

    Returns:
        Returns the loaded model object
    """
    # Getting local environment download path
    env_loc = os.path.dirname(sys.executable)
    env_loc = env_loc.replace("Scripts", f"Lib\\site-packages\\{model}")

    if not os.path.exists(env_loc):
        spacy.cli.download(model)
        
    try:
        nlp = spacy.load(model)
    except:
        nlp = model.load()
    return nlp

