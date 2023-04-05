import snscrape.modules.twitter as sntwitter
import pandas as pd
# For sending GET requests from the API
import requests
# For saving access tokens and for file management when creating and adding to the dataset
import os
# For dealing with json responses we receive from the API
import json
# For saving the response data in CSV format
import csv
# For parsing the dates received from twitter in readable formats
import datetime
import dateutil.parser
import unicodedata
#To add wait time between requests
import time
from datetime import datetime
from datetime import timedelta

def timedeltas(start='2022-06-24 06:00:00',last="2022-07-01 06:00:00",hour_delta=8,min_gap=10):

    end = pd.Timestamp(start)+timedelta(minutes=min_gap)
#     end = end.tz_localize(None)
    end = end.isoformat("_", "seconds")

    if last == None:
        current = datetime.now()
        current.isoformat()
    else:
        current = pd.Timestamp(last)

    ts = pd.Timestamp(start)

#     ts = ts.tz_localize(None)

    start_list = []
    end_list = []
    start_list.append(ts.isoformat("_", "seconds")+"_UTC")
    end_list.append(end+"_UTC")


    while (ts+timedelta(hours=hour_delta))<(current-timedelta(minutes=min_gap)):
        ts = ts + timedelta(hours=hour_delta)
        es = ts + timedelta(minutes=min_gap)
        start_list.append(ts.isoformat("_", "seconds")+"_UTC")
        end_list.append(es.isoformat("_", "seconds")+"_UTC")

    return start_list, end_list


def append_to_csv(tweet, fileName):

    #A counter variable
    counter = 0

    #Open OR create the target CSV file
    csvFile = open(fileName, "a", newline="", encoding='utf-8')
    csvWriter = csv.writer(csvFile)

    #Loop through each tweet


    # We will create a variable for each since some of the keys might not exist for some tweets
    # So we will account for that
#         tweet.date, tweet.id, tweet.content, tweet.user.username

    # 1. Tweet Date
    datetime = tweet.date

    # 2. username
    username = tweet.user.username

    # 8. Tweet text
    text = tweet.rawContent

    # Assemble all data in a list
    res = [datetime, username, text]

    # Append the result to the CSV file
    csvWriter.writerow(res)
    counter += 1

    # When done, close the CSV file
    csvFile.close()


    return

def snscrape(num_tweets=100,start_date='2023-03-05T06:00:00.000Z',end_date='2023-03-06T06:00:00.000Z', hour_delta=8,min_gap=10,filename='run1.csv',make_csv=True):

    # Creating list to append tweet data to
#     start_list, end_list = timedeltas2(start=start_date,end=end_date,hour_delta=hour_delta,min_gap=min_gap)
    start_list, end_list = timedeltas(start=start_date,last=end_date,hour_delta=hour_delta,min_gap=min_gap)

#     print(start_list)

    # Create file
    csvFile = open(filename, "a", newline="", encoding='utf-8')
    csvWriter = csv.writer(csvFile)

    #Create headers for the data you want to save, in this example, we only want save these columns in our dataset
    csvWriter.writerow(['datetime', 'username', 'text'])
    csvFile.close()

    # Using TwitterSearchScraper to scrape data and append tweets to list
    for i in range(len(start_list)):
        for i,tweet in enumerate(sntwitter.TwitterSearchScraper(f'#bitcoin since:{start_list[i]} until:{end_list[i]} lang:en').get_items()):
            if i>num_tweets:
                break
            append_to_csv(tweet, filename)

    # Creating a dataframe from the tweets list above
#     tweets_df2 = pd.DataFrame(tweets_list2, columns=['Datetime', 'Tweet Id', 'Text', 'Username'])

    if make_csv:
        return pd.read_csv(filename)
    else:
        return

if __name__ == "__main__":
    snscrape(num_tweets=149,start_date='2020-09-01T00:00:00',end_date='2020-12-31T23:00:00', hour_delta=8,min_gap=10,filename='09-03-23_to_15-03-23.csv',make_csv=False)
