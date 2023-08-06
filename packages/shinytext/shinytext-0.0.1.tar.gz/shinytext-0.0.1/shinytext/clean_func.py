from shinytext.utils.emoticons import UNICODE_EMOJI, EMOTICONS_EMO
from shinytext.utils.chats import CHATWORDS
import re
import string
from nltk.corpus import stopwords
from collections import Counter
import nltk
from nltk.corpus import wordnet
from nltk.stem.snowball import SnowballStemmer
from nltk.stem import WordNetLemmatizer
from spellchecker import SpellChecker



def lowercase(text:str):
    return text.lower()
    
def remove_punctuation(text:str):
    PUNCT_TO_REMOVE = string.punctuation
    return text.translate(str.maketrans('', '', PUNCT_TO_REMOVE))

def remove_stopwords(text:str):
    STOPWORDS = set(stopwords.words('english'))
    return " ".join([word for word in text.split() if word not in STOPWORDS])

def remove_frequent_words(text:str, threshold:int=10):
    counter = Counter()
    FREQWORDS = set([w for (w, wc) in counter.most_common(threshold)])
    return " ".join([word for word in text.split() if word not in FREQWORDS])

def remove_rare_words(text:str, threshold:int=10):
    counter = Counter()
    RAREWORDS = set([w for (w, wc) in counter.most_common()[:-threshold-1:-1]])
    return " ".join([word for word in text.split() if word not in RAREWORDS])

def stemmer(text:str):
    stemmer = SnowballStemmer("english")
    return " ".join([stemmer.stem(word) for word in text.split()])

def lemmatizer(text:str, pos:bool=False):
    if pos:
        lemmatizer = WordNetLemmatizer()
        wordnet_map = {"N":wordnet.NOUN, "V":wordnet.VERB, "J":wordnet.ADJ, "R":wordnet.ADV}
        pos_tagged_text = nltk.pos_tag(text.split())
        return " ".join([lemmatizer.lemmatize(word, wordnet_map.get(pos[0], wordnet.NOUN)) for word, pos in pos_tagged_text])
    else:
        lemmatizer = WordNetLemmatizer()
        return " ".join([lemmatizer.lemmatize(word) for word in text.split()])

def remove_emojis(text:str):
    emoji_pattern = re.compile("["
                           u"\U0001F600-\U0001F64F"  # emoticons
                           u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                           u"\U0001F680-\U0001F6FF"  # transport & map symbols
                           u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                           u"\U00002702-\U000027B0"
                           u"\U000024C2-\U0001F251"
                           "]+", flags=re.UNICODE)
    return emoji_pattern.sub(r'', text)

def convert_emojis(text:str):
    for emot in UNICODE_EMOJI:
        text = re.sub(r'('+emot+')', "_".join(UNICODE_EMOJI[emot].replace(",","").replace(":","").split()), text)
    return text


def remove_emoticons(text:str):
    emoticon_pattern = re.compile(u'(' + u'|'.join(k for k in EMOTICONS_EMO) + u')')
    return emoticon_pattern.sub(r'', text)

def convert_emoticons(text:str):
    for emot in EMOTICONS_EMO:
        text = re.sub(u'('+emot+')', "_".join(EMOTICONS_EMO[emot].replace(",","").split()), text)
    return text

def remove_urls(text:str):
    url_pattern = re.compile(r'https?://\S+|www\.\S+')
    return url_pattern.sub(r'', text)

def remove_html(text:str):
    html_pattern = re.compile('<.*?>')
    return html_pattern.sub(r'', text)

def convert_chatwords(text:str):
    chat_words_map_dict = {}
    chat_words_list = []

    for line in CHATWORDS.split("\n"):
        if line != "":
            cw = line.split("=")[0]
            cw_expanded = line.split("=")[1]
            chat_words_list.append(cw)
            chat_words_map_dict[cw] = cw_expanded
    chat_words_list = set(chat_words_list)

    new_text = []

    for w in text.split():
        if w.upper() in chat_words_list:
            new_text.append(chat_words_map_dict[w.upper()])
        else:
            new_text.append(w)
    return " ".join(new_text)

def check_spellings(text:str):
    spell = SpellChecker()
    corrected_text = []
    misspelled_words = spell.unknown(text.split())
    for word in text.split():
        if word in misspelled_words:
            corrected_text.append(spell.correction(word))
        else:
            corrected_text.append(word)
    return " ".join(corrected_text)

