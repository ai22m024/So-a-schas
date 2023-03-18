from summarizer import Summarizer
import numpy as np
from textblob_de import TextBlobDE as Blob 
from germansentiment import SentimentModel




import random
import pandas as pd
from langdetect import  DetectorFactory
import langdetect
DetectorFactory.seed = 0


texts = pd.read_csv("./obi-markt.csv", sep=";",  encoding='iso-8859-1')

texts = texts[(texts['text'] != "")]
texts = texts[(texts['stars'] <= 3)]
texts = texts["text"].dropna()
text_list = []
for text in texts:
    text_list.append(text)
model = Summarizer(reduce_option="max")
output_count = 0
results = []
while(output_count < 5):

    review = ""
    german_found = False
    while not german_found:
        rand = text_list[random.randint(0, len(text_list)-1)]
        
        try:
            if langdetect.detect(rand) == "de":
                review = rand
                german_found = True
            else:
                continue 
                  
        except:
            continue
        
    
    blob = Blob(review)

    for sentence in blob.sentences:
        pass # print(sentence.sentiment)
    sentiment_model = SentimentModel()

    sentences = ""
    result, result_prob = sentiment_model.predict_sentiment(blob.raw_sentences, True)
    print(result_prob)
    for i, noun in enumerate(blob.raw_sentences):
        if result[i] == "negative"  or blob.sentences[i].sentiment.polarity < 0:
            sentences+= noun
        #print(result[i], noun)

    
    result = model.run(sentences, ratio=0.5, min_length=30, max_length=100, use_first=False)
    
    if result == "":
        continue

    if result in results:
        continue
    results.append(result)
    print(result + "\n\n")
    output_count+=1

print(results)

    # if sentiment_model.predict_sentiment([result])[0] != "negative" or Blob(result).sentiment.polarity >= 0:
    #     print(result, "Not negative enought")
    #     continue
    
    # Will return 3 sentences 


