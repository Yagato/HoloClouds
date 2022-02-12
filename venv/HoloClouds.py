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
newWords = ['thank', 'get', 'stream', 'hello', 'u', 'also', 'but']
stop.extend(newWords)

en_supa = pd.read_csv("csv/en_supas_2021-07.csv")


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
    vChat = en_supa[en_supa['originChannelId'] == 'UCL_qhgtOy0dy1Agp8vkySQg']
    vMask = np.array(Image.open("img/mori.png"))

    image_colors = ImageColorGenerator(vMask)

    text = ' '.join(chat for chat in vChat.body)

    wordcloud = WordCloud(stopwords=stop, width=800, height=800, max_words=30000, background_color="black",
                          mode="RGBA", mask=vMask, collocations=False).generate(text)

    plt.figure(figsize=(16, 9), facecolor='k')
    plt.imshow(wordcloud.recolor(color_func=image_colors), interpolation='bilinear')
    plt.axis("off")
    plt.tight_layout(pad=0)
    plt.savefig("img/wordcloud_mori_2021-07.png", dpi=700)
    plt.show()


if __name__ == '__main__':
    #global_wordcloud()
    channel_wordcloud()
