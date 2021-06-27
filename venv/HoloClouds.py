import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from PIL import Image
import nltk
from nltk.corpus import stopwords
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator

#Uncomment the line below if you don't have nltk's stopwords list downloaded already
#nltk.download('stopwords')

stop = stopwords.words('english')
newWords = ['thanks', 'thank', 'get', 'stream', 'hello']
stop.extend(newWords)

en_supa = pd.read_csv("csv/en_supas.csv", index_col=0)


# Wordcloud that includes all super chats from the csv
def global_wordcloud():
    text = ' '.join(chat for chat in en_supa.body)
    wordcloud = WordCloud(stopwords=stop, width=1920, height=1280, max_words=1000,
                          background_color="black").generate(text)

    plt.figure(figsize=(16, 9), facecolor='k')
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    plt.tight_layout(pad=0)
    plt.savefig("img/wordcloud_global3.png", dpi=700)
    plt.show()


#Wordcloud that includes the super chats from a specific channel
def channel_wordcloud():
    # Suisei Channel Wordcloud
    sui_chat = en_supa[en_supa['originChannelId'] == 'UC5CwaMl1eIgY8h02uZw7u8A']
    sui_mask = np.array(Image.open("img/sui.png"))

    image_colors = ImageColorGenerator(sui_mask)

    text = ' '.join(chat for chat in sui_chat.body)

    wordcloud = WordCloud(stopwords=stop, width=800, height=800, max_words=20000, background_color="black",
                          mode="RGBA", mask=sui_mask).generate(text)

    plt.figure(figsize=(16, 9), facecolor='k')
    plt.imshow(wordcloud.recolor(color_func=image_colors), interpolation='bilinear')
    plt.axis("off")
    plt.tight_layout(pad=0)
    plt.savefig("img/wordcloud_sui3.png", dpi=700)
    plt.show()


if __name__ == '__main__':
    global_wordcloud()
    channel_wordcloud()
