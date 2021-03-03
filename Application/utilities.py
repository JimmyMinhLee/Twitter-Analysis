import json, sys
from os import system
import numpy as np
import datetime as dt
# from textblob import TextBlob
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import matplotlib.pyplot as plt

class TextProcessor():
    def __init__(self, hashtag):
        self.name = hashtag
        self.hashtag = {hashtag:0}
        self.analyzer = SentimentIntensityAnalyzer()

        # Averaging variables
        self.current_average = 0
        self.average_count = 0

        # Plotting variables
        self.total_step_count = 0
        self.x_data = [0]

        # Trend of sentiment vs. time
        self.trend_y_data = [0]
        # Individual y scores vs. time
        self.average_y_data = [0]

    def process(self, raw_data, average_step):
        # csv = open('data.csv', "a")
        text = self.get_text(raw_data)
        # if "RT" in text: return
        weights = {1:1, 0:1.3}
        response = self.analyzer.polarity_scores(text)['compound']
        print(text)

        # if response < 0: response = response * 1.3

        # Instantiate plot
        plt.ion()
        plt.ylabel('Average sentiment per 10 tweets')
        plt.xlabel('Tweet count processed')
        plt.title("{} composite sentiment based on tweets".format(self.name))
        plt.plot(self.x_data, self.trend_y_data, label = "Total score of tweets processed")
        plt.plot(self.x_data, self.average_y_data, label = "Individual average of tweets per 10")
        plt.draw()

        # Perform averaging and plot and store data into csv file
        self.normalize(text, response, average_step)

    def get_text(self, raw_data):
        try: return json.loads(raw_data)['text']
        except KeyError: return "KeyError encountered while streaming tweets."

    def plot(self):
        # Update plot
        plt.clf()
        plt.title("{} composite sentiment based on tweets".format(self.name))
        plt.plot(self.x_data, self.trend_y_data, label = "Total score of tweets processed")
        plt.plot(self.x_data, self.average_y_data, label = "Individual average of tweets per 10")
        plt.legend(loc=2)
        plt.pause(0.1)


    def normalize(self, text, response, average_step):
        if self.average_count != average_step:
            self.current_average += response
            self.average_count += 1
        else:
            self.hashtag[self.name] += self.current_average / self.average_count

            # Append data
            self.total_step_count += 1
            self.x_data.append(self.total_step_count * 10)
            self.average_y_data.append(self.current_average / self.average_count)
            self.trend_y_data.append(self.hashtag[self.name])
            # csv.write("{} ..., {}, {} \n".format(text[0:20], response, str(dt.datetime.now())))

            # Reset
            self.current_average = 0
            self.average_count = 0
            self.plot()


    def clean(self, text):
        ## TODO: may be useful to ignore certain tweets and use others, i.e rt
        pass
