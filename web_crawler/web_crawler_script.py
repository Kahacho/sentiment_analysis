# Loading the necessary libraries

import tweepy as tw
import pandas as pd

import nltk
from nltk.tokenize import RegexpTokenizer
from nltk.probability import FreqDist
from nltk.stem import WordNetLemmatizer
from nltk.sentiment import SentimentIntensityAnalyzer

from statistics import mean
import requests

# Importing the API keys
from web_crawler.twitter_api_keys import *


def crypto_sentiments() -> pd.DataFrame:
    """
    Get 10 most recent English tweets with the word Cryptocurrency """

    client = tw.Client(bearer_token=bearer_token,
                       consumer_key=consumer_key,
                       consumer_secret=consumer_secret,
                       access_token=access_token,
                       access_token_secret=access_token_secret,
                       return_type=requests.Response,
                       wait_on_rate_limit=True)

    # Define query - excluding retweets and the tweets should be in English
    query = '(crypto OR cryptocurrency OR cryptocurrencies) -is:retweet lang:en'

    # Get 10 most recent tweets
    tweets = client.search_recent_tweets(query=query,
                                         tweet_fields=['author_id', 'created_at'],
                                         max_results=10)

    # Save data as dictionary - This is the text stream file
    tweets_dict = tweets.json()

    # Extract "data" value from dictionary
    tweets_data = tweets_dict['data']

    # Transform to pandas Dataframe
    df = pd.json_normalize(tweets_data)

    return df


def sentiment_score(crypto_df: pd.DataFrame) -> float:
    """
    Returns the compound score of every 30-minute session

    Parameters:
    ----------
    crypto_df : Dataset of the 100 most recent tweets

    Returns:
    ----------
    compound_score : Mean compound polarity score of every 30-minute session

    """

    # Data transformation
    crypto_df['text'] = crypto_df['text'].astype(str).str.lower()

    regexp = RegexpTokenizer('\w+')

    crypto_df['text_token'] = crypto_df['text'].apply(regexp.tokenize)

    # Ensures that Stop words are up-to-date
    nltk.download('stopwords', quiet=True)

    # Make a list of english stopwords
    stopwords = nltk.corpus.stopwords.words("english")

    # Appending the list with your own custom stopwords
    stopwords.append('https')

    # Remove stopwords
    crypto_df['text_token'] = (crypto_df['text_token']
                               .apply(lambda x: [item for item in x if item not in stopwords]))

    # Remove infrequent words
    crypto_df['text_string'] = (crypto_df['text_token']
                                .apply(lambda x: ' '.join([item for item in x if len(item) > 2])))

    # Create a list of all words
    all_words = ' '.join([word for word in crypto_df['text_string']])

    # Download punkt
    nltk.download('punkt', quiet=True)

    # tokenize all words
    tokenized_words = nltk.tokenize.word_tokenize(all_words)

    # Frequency of words
    fdist = FreqDist(tokenized_words)

    # We don’t filter out any words and set the value to greater or equal to 1
    crypto_df['text_string_fdist'] = (crypto_df['text_token']
                                      .apply(lambda x: ' '.join([item for item in x if fdist[item] >= 1])))

    # Lemmatization
    nltk.download('wordnet', quiet=True)
    nltk.download('omw-1.4', quiet=True)

    wordnet_lem = WordNetLemmatizer()

    crypto_df['text_string_lem'] = crypto_df['text_string_fdist'].apply(wordnet_lem.lemmatize)

    # Sentiment Analysis

    nltk.download('vader_lexicon', quiet=True)

    analyzer = SentimentIntensityAnalyzer()

    # Polarity scores
    crypto_df['polarity'] = crypto_df['text_string_lem'].apply(lambda x: analyzer.polarity_scores(x))

    # Change data structure
    crypto_df = pd.concat(
        [crypto_df.drop(['id', 'author_id', 'polarity'], axis=1),
         crypto_df['polarity'].apply(pd.Series)], axis=1)

    # Compute the mean compound polarity score of every session
    compound_score = mean(crypto_df['compound'])

    return round(compound_score, 2)


def compute_session_sentiment_score():
    return sentiment_score(crypto_sentiments())


if __name__ == "__main__":
    compute_session_sentiment_score()
