import pandas as pd
import re
from langdetect import detect

emoji_pattern = re.compile(pattern = "["
            u"\U0001F600-\U0001F64F"  # emoticons
            u"\U0001F300-\U0001F5FF"  # symbols & pictographs
            u"\U0001F680-\U0001F6FF"  # transport & map symbols
            u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
            u"\U00002500-\U00002BEF"  # chinese char
            u"\U00002702-\U000027B0"
            u"\U00002702-\U000027B0"
            u"\U000024C2-\U0001F251"
            u"\U0001f926-\U0001f937"
            u"\U00010000-\U0010ffff"
            u"\u2640-\u2642"
            u"\u2600-\u2B55"
            u"\u200d"
            u"\u23cf"
            u"\u23e9"
            u"\u231a"
            u"\ufe0f"  # dingbats
            u"\u3030"
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

    #Dataframe with the columns to read
    col_list = ["body", "originChannelId"]

    # Reads the original csv and chooses the specified columns
    superchats = pd.read_csv(r'csv/superchats_2021-06.csv', usecols=col_list)

    # Store in a dataframe only the english messages
    en_supa = superchats[superchats['body'].apply(detect_en)]

    # Clean the messages (de-emojify/de-emoticon them)
    en_supa['body'] = en_supa['body'].apply(deEmojify)
    en_supa['body'] = en_supa['body'].apply(only_letters)

    # Save it as another csv encoded with utf-8-sig to have as few broken characters as possible
    en_supa.to_csv(r'csv/en_supas_2021-06.csv', index=False, header=True, encoding='utf-8-sig')