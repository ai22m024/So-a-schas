from summarizer import Summarizer
import numpy as np
from textblob_de import TextBlobDE as Blob 
from germansentiment import SentimentModel
import random
import pandas as pd
from langdetect import  DetectorFactory
import langdetect
from difflib import SequenceMatcher

DetectorFactory.seed = 0
import os 
class NegativeSummarizer:
    def __init__(self, location):
        # the query location
        self.location = location

        # load the most likely csv file
        self.csv_filepath = self.__lookup_location_csv__(location)

        # load and filter all reviews that are interesting to us
        self.review_list = self.__prepare_data__(self.csv_filepath)

        # setup summarzier model (pip: bert-extractive-summarizer)
        self.summarizer_model = Summarizer(reduce_option="max")
        # setup sentiment model (pip: germansentiment)
        self.sentiment_model = SentimentModel()

        

    def __lookup_location_csv__(self, location):
        similarities = []
        # go through list of location csv files
        for loc in os.listdir("locations"):
           #calulate the word similarity with sequence matcher
           ratio = SequenceMatcher(None, loc, location).ratio()
           similarities.append(ratio)

        # get the index with the highest similarity value
        max_index = np.argmax(similarities)
        file = os.listdir("locations")[max_index]
        # join path and save
        return os.path.join("locations", file)

    def __prepare_data__(self, csv_file):
        # load csv file with pandas
        texts = pd.read_csv(csv_file, sep=";",  encoding='iso-8859-1')

        # delete all texts with no information
        texts = texts[(texts['text'] != "")]

        #only accept reviews smaller/equal 3
        texts = texts[(texts['stars'] <= 3)]

        # tidy up some NAN values
        texts = texts["text"].dropna()

        # create list of reviews out of it
        review_list = []
        for text in texts:
            review_list.append(text)

        return review_list
    
    def summarize(self, summary_count):
        # define how much many summaries should be generated (1-10 summaries available)
        self.summary_count = np.clip(summary_count, 1, 10)
        
        
        self.summaries = []
        # repeate as long, till we reach the summary count
        while len(self.summaries) < self.summary_count:
            # find a random review that fits our language
            review = self.find_random_review("de")

            negative_sentences = ""
            # create a textblob so we can iterate over the individual sentences
            review_blob = Blob(review)

            # predict the sentiment for every sentence in of the chosen review
            sentiments = self.sentiment_model.predict_sentiment(review_blob.raw_sentences)

            tags_count = {}

            for i, noun in enumerate(review_blob.raw_sentences):
                # for each sentences, check the textblob sentiment and the germansentiment.
                # by using two sentiment analyzers we have a higher chance of finding negative sentences
                if sentiments[i] == "negative"  or review_blob.sentences[i].sentiment.polarity < 0 or (sentiments[i]=="neutral" and random.random() > 0.8):
                    # append the negative sentences
                    if random.random() > 0.5:
                        negative_sentences = negative_sentences + noun
                    else:
                        negative_sentences = noun + negative_sentences

                  
            # summarize the sentences, we create a sentence between 30 and 100 characters
            summary = self.summarizer_model.run(negative_sentences, ratio=0.5, min_length=30, max_length=100, use_first=False)

            # filter our empty summaries and already created ones
            if summary == "":
                continue
            if summary in self.summaries:
                continue

            self.summaries.append(summary)

        return self.summaries                 

    def find_random_review(self, lang = "de"):
        lang_found = False
        review = ""
        while not lang_found:
            # pick random review
            np.random.seed(random.randint(0, 10000))
            rand = np.random.choice(self.review_list)

            # try if language can be detected
            # error will be thrown if the is not enough data for guessing the language
            # this filters also chars like "????!!!", which is a good thing
            try:
                if langdetect.detect(rand) == lang:
                    review = rand
                    lang_found = True
                else:
                    continue  
            except:
                continue

        return review




# sum = NegativeSummarizer("Obi")

# print(sum.summarize(3))
# sum = NegativeSummarizer("Tu wien")
# print(sum.summarize(3))

# sum = NegativeSummarizer("Höfbug")
# print(sum.summarize(3))






### IDEAS
# different language
# one long summarize of many comments comments and a few short summarize of individual comments
# max iterations, if not enough data, quit
# reinforce choosing longer reviews 

# texts = pd.read_csv("./obi-markt.csv", sep=";",  encoding='iso-8859-1')

# texts = texts[(texts['text'] != "")]
# texts = texts[(texts['stars'] <= 3)]
# texts = texts["text"].dropna()
# text_list = []
# for text in texts:
#     text_list.append(text)
# model = Summarizer(reduce_option="max")
# output_count = 0
# results = []
# while(output_count < 5):

#     review = ""
#     german_found = False
#     while not german_found:
#         rand = text_list[random.randint(0, len(text_list)-1)]
        
#         try:
#             if langdetect.detect(rand) == "de":
#                 review = rand
#                 german_found = True
#             else:
#                 continue 
                  
#         except:
#             continue
        
    
    # blob = Blob(review)

    # for sentence in blob.sentences:
    #     pass # print(sentence.sentiment)
    # sentiment_model = SentimentModel()

    # sentences = ""
    # result, result_prob = sentiment_model.predict_sentiment(blob.raw_sentences, True)
    # print(result_prob)
    # for i, noun in enumerate(blob.raw_sentences):
    #     if result[i] == "negative"  or blob.sentences[i].sentiment.polarity < 0:
    #         sentences+= noun
    #     #print(result[i], noun)

    
#     result = model.run(sentences, ratio=0.5, min_length=30, max_length=100, use_first=False)
    
#     if result == "":
#         continue

#     if result in results:
#         continue
#     results.append(result)
#     print(result + "\n\n")
#     output_count+=1

# print(results)

#     # if sentiment_model.predict_sentiment([result])[0] != "negative" or Blob(result).sentiment.polarity >= 0:
#     #     print(result, "Not negative enought")
#     #     continue
    
#     # Will return 3 sentences 


