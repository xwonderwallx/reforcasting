from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from modules.MoodState import MoodState


class NewsAnalyzer:
    def __init__(self, news):
        self.news = news


    def analyze(self):
        analyzer = SentimentIntensityAnalyzer()

        for text in news:
            sentiment = analyzer.polarity_scores(text)
            mood_state = self.sentiment_analysis(sentiment)


    def sentiment_analysis(self, sentiment):
        if sentiment['compound'] >= 0.05:
            return MoodState.POSITIVE
        elif sentiment['compound'] <= -0.05:
            return MoodState.NEGATIVE
        else:
            return MoodState.NEUTRAL