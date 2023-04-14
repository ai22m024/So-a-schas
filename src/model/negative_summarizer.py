from summarizer import Summarizer
import numpy as np
from textblob_de import TextBlobDE as Blob 
from germansentiment import SentimentModel
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

import random
import pandas as pd
from langdetect import  DetectorFactory
import langdetect
from difflib import SequenceMatcher
from enum import Enum

from src.experiment.review_logger import ReviewLogger

DetectorFactory.seed = 0
import os 

class SummarizerType(Enum):
    EXTRACTIVE = 0,
    ABSTRACTIVE = 1,
    BOTH = 2

class NegativeSummarizer:
    def __init__(self, location, sum_type = SummarizerType.EXTRACTIVE):
        self.sum_type = sum_type
        
        # the query location
        self.location = location

        # load the most likely csv file
        self.csv_filepath = self.__lookup_location_csv__(location)

        # load and filter all reviews that are interesting to us
        self.review_list = self.__prepare_data__(self.csv_filepath)

        # setup summarzier model (pip: bert-extractive-summarizer)
        if sum_type == SummarizerType.EXTRACTIVE or sum_type == SummarizerType.BOTH:
            self.summarizer_model_ext = Summarizer(reduce_option="max")

            self.review_logger = ReviewLogger("Extractive", self.location)
        if sum_type == SummarizerType.ABSTRACTIVE or sum_type == SummarizerType.BOTH:
            self.tokenizer = AutoTokenizer.from_pretrained("Einmalumdiewelt/T5-Base_GNAD")
            self.summarizer_model_abst = AutoModelForSeq2SeqLM.from_pretrained("Einmalumdiewelt/T5-Base_GNAD")

            self.review_logger= ReviewLogger("Abstractive", self.location)

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
    
    def sample_summary_data(self, summary_count):

        sentences = []
        # define how much many summaries should be generated (1-10 summaries available)
        self.summary_count = np.clip(summary_count, 1, 50)
        
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

            for i, noun in enumerate(review_blob.raw_sentences):
                # for each sentences, check the textblob sentiment and the germansentiment.
                # by using two sentiment analyzers we have a higher chance of finding negative sentences
                if sentiments[i] == "negative" or sentiments[i] == "neutral"  or review_blob.sentences[i].sentiment.polarity <= 0:
                    # append the negative sentences
                    if random.random() > 0.5:
                        negative_sentences = negative_sentences + noun
                    else:
                        negative_sentences = noun + negative_sentences
            
            sentences.append(negative_sentences)

        return sentences
    
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
                if sentiments[i] == "negative" or sentiments[i] == "neutral"  or review_blob.sentences[i].sentiment.polarity <= 0:
                    # append the negative sentences
                    if random.random() > 0.5:
                        negative_sentences = negative_sentences + noun
                    else:
                        negative_sentences = noun + negative_sentences

            if self.sum_type == SummarizerType.EXTRACTIVE:
                # summarize the sentences, we create a sentence between 30 and 100 characters
                summary = self.summarizer_model_ext.run(negative_sentences, num_sentences=2, min_length=30, max_length=90, use_first=False)
                
            else:
                input_ids = self.tokenizer.encode(negative_sentences, return_tensors="pt")
                outputs = self.summarizer_model_abst.generate(input_ids, min_new_tokens = 10,max_new_tokens = 35)
                summary = self.tokenizer.decode(outputs[0], skip_special_tokens=True)

                #self.review_logger_abst.log_review(review, summary)

            # filter our empty summaries and already created ones
            if summary == "":
                continue
            if summary in self.summaries:
                continue
        
            self.review_logger.log_review(review, summary)
            
            # summary_sentiment = self.sentiment_model.predict_sentiment([summary])[0] 
            # if Blob(summary).sentiment.polarity >= 0 or summary_sentiment == "positive":
            #     continue

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



