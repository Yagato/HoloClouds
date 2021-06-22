import numpy as np
import pandas as pd
import re
from matplotlib import pyplot as plt
from PIL import Image
from langdetect import detect
import nltk
from nltk.corpus import stopwords
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
import plotly.express as px

#Uncomment the line below if you don't have nltk's stopwords list downloaded already
#nltk.download('stopwords')

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
    return emoji_pattern.sub(r'',text)

if __name__ == '__main__':

    #----- DATA PREPROCESSING ----

    # Read the original csv
    #superchats = pd.read_csv(
    #    r'C:\Users\AcerMX\Documents\Escuela\S7\Big data redes sociales\Unidad 3\Hololive Insights\csv\superchats_2021-03.csv',
    #    index_col=0)

    # Store in a dataframe only the english messages
    #en_supa = superchats[superchats['body'].apply(detect_en)]

    # Save the dataframe as a csv
    #en_supa.to_csv(
    #    r'C:\Users\AcerMX\Documents\Escuela\S7\Big data redes sociales\Unidad 3\Hololive Insights\csv\en_supas.csv',
    #    index=False, header=True)

    # Clean the messages (de-emojifying/de-emoticon them)
    """en_supa['body'] = en_supa['body'].apply(deEmojify)
    en_supa['body'] = en_supa['body'].apply(only_letters)"""

    # Save it as another csv with utf-8-sig encoding to have as few broken characters as possible
    #en_supa.to_csv(
    #    r'C:\Users\AcerMX\Documents\Escuela\S7\Big data redes sociales\Unidad 3\Hololive Insights\csv\clean_en_supas.csv',
    #    index=False, header=True, encoding='utf-8-sig')


    #----- WORDCLOUDS -----

    # Global Wordcloud (including all channels from the csv)
    stop = stopwords.words('english')

    en_supa = pd.read_csv(
        r'C:\Users\AcerMX\Documents\Escuela\S7\Big data redes sociales\Unidad 3\Hololive Insights\csv\clean_en_supas.csv',
        index_col=0)

    text = ' '.join(chat for chat in en_supa.body)
    
    wordcloud = WordCloud(stopwords = stop, width=1920, height=1280, max_words=1000, 
        background_color="black").generate(text)
    
    plt.figure(figsize=(16,9), facecolor='k')
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    plt.tight_layout(pad=0)
    plt.savefig(
        r"C:\Users\AcerMX\Documents\Escuela\S7\Big data redes sociales\Unidad 3\Hololive Insights\img\wordcloud_global.png",
        dpi=700)
    plt.show()

    # Suisei Channel Wordcloud
    sui_chat = en_supa[en_supa['originChannelId'] == 'UC5CwaMl1eIgY8h02uZw7u8A']
    sui_mask = np.array(Image.open(
        r"C:\Users\AcerMX\Documents\Escuela\S7\Big data redes sociales\Unidad 3\Hololive Insights\img\sui.png"))

    image_colors = ImageColorGenerator(sui_mask)

    text = ' '.join(chat for chat in sui_chat.body)

    wordcloud = WordCloud(stopwords=stop, width=800, height=800, max_words=2000, background_color="black", 
                          mode="RGBA", mask=sui_mask).generate(text)

    plt.figure(figsize=(16,9), facecolor='k')
    plt.imshow(wordcloud.recolor(color_func=image_colors), interpolation='bilinear')
    plt.axis("off")
    plt.tight_layout(pad=0)
    plt.savefig(
        r"C:\Users\AcerMX\Documents\Escuela\S7\Big data redes sociales\Unidad 3\Hololive Insights\img\wordcloud_sui.png",
        dpi=700)
    plt.show()