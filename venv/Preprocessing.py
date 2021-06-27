import pandas as pd
import re
from langdetect import detect

emoji_pattern = re.compile(pattern = "["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
        u"\U00002702-\U000027B0"
        u"\U000024C2-\U0001F251"
                           "]+", flags = re.UNICODE)

def detect_en(text):
    try:
        return detect(text) == 'en'
    except:
        return False

def only_letters(text):
    return re.sub(r"[^A-Za-z0-9]+", ' ', text)

def deEmojify(text):
    return emoji_pattern.sub(r'', text)

if __name__ == '__main__':

    #----- DATA PREPROCESSING ----

    # Read the original csv
    superchats = pd.read_csv(r'csv/superchats_2021-04.csv', index_col=0)

    # Store in a dataframe only the english messages
    en_supa = superchats[superchats['body'].apply(detect_en)]

    # Clean the messages (de-emojifying/de-emoticon them)
    en_supa['body'] = en_supa['body'].apply(deEmojify)
    en_supa['body'] = en_supa['body'].apply(only_letters)

    # Save it as another csv with utf-8-sig encoding to have as few broken characters as possible
    en_supa.to_csv(r'csv/en_supas.csv', index=False, header=True, encoding='utf-8-sig')