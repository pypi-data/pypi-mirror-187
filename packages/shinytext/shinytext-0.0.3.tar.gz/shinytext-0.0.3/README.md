# ✨ Shiny Text
This package aims to be a one stop all package for all text processing tasks.
The package was developed using Python3.10.

### 💻 Installation
```python
pip install -U shinytext
```

### 🚀 Usage
```python

# To clean text
from shinytext.cleantext import <method>

# To clean dataframe
from shinytext.cleandata import <method>

# To download/fetch a spacy language model
from shinytext.utils.spacy_loader import get_spacy_object
```
#### List of text cleaning methods

* **remove_punctuation**: To remove punctuations
* **remove_stopwords**: To remove stopwords
* **remove_frequent_words**: To remove frequently occuring words
* **remove_rare_words**: To remove rarely occuring words
* **stemmer**: To perform stemming
* **lemmatizer**: To perform lemmatizing
* **remove_emojis**: To remove emoji's
* **convert_emojis**: To convert emoji's to text
* **remove_emoticons**: To remove emoticons
* **convert_emoticons**: To convert emoticons to text
* **remove_urls**: To remove URLs
* **remove_html**: To remove html
* **convert_chatwords**: To convert chat words to text

#### List of dataframe cleaning methods

* **filter_english_records**: To extract data with only english text


### ✍ Contribution Guidelines
Please ensure that you adhere to the following guidelines while making a pull request.

1. Fork the project on to your repo. Create a branch under your name and create PR from your branch.

2. USE proper commit messages and give detailed descriptions for your commit including the file name, function name and the changes made.

Customize your commit titles according to below given instructions  

    * "ADD: <your task title>" for new additions  
    * "MOD: <your task title>" for modifications 
    * "DEL: <your task title>" for deletions
    * "FIX: <your task title>" for fixing bugs

3. Ensure that your code adheres to PEP-8 guidelines. [Click here](https://peps.python.org/pep-0008/) to know more about it.

### 💼 Current Requirements
1. More text processing techniques

2. Test cases for existing functions

### 🙌 Contributors
1. [Retin P Kumar](https://github.com/Retinpkumar)

### ❤ Credits
1. [Emot library](https://github.com/NeelShah18/emot) by [Neel Shah](https://github.com/NeelShah18)
2. [Getting started with Text Preprocessing](https://www.kaggle.com/code/sudalairajkumar/getting-started-with-text-preprocessing/notebook) by [Sudalai Rajkumar](https://www.kaggle.com/sudalairajkumar)

### ⚙ Dependancies
* [NLTK](https://www.nltk.org/)
* [Pandas](https://pandas.pydata.org/)
* [PySpellchecker](https://pypi.org/project/pyspellchecker/)
* [SpaCy](https://spacy.io/)
