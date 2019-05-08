### first import all neccessary libraries ###
import numpy as np
import pandas as pd
from os import path
from PIL import Image
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
import matplotlib.pyplot as plt

## Then open the textfile downloaded from the 'hashtag' library ###

text = open('alle_hashtags.txt', 'r')

## Read the text ##

data = text.read()
data

##Plot figure ##

plt.figure(figsize=(20,10))
wordcloud = WordCloud(background_color='white',
                      mode = "RGB",
                      width = 1200, height=1000,
                      collocations = False, stopwords = STOPWORDS  ##Makes sure that the same word is not counted twice
                      ).generate(data)
plt.title("Sptzenkandidaten Hashtags")
plt.imshow(wordcloud)
plt.axis("off")
plt.show()
