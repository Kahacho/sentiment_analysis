# Import the necessary libraries
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


def plot_session_sentiment_score():
    """ Plots real-time sentiment score of the tweets after every 30 minutes"""

    def animate(i):
        data = pd.read_csv('data/data.csv')

        x = data['session']
        y = data['scores']

        plt.cla()
        plt.plot(x, y, label='Crypto Sentiment Scores every 30 minutes', marker='o')
        plt.xlabel('Session time')
        plt.ylabel('Sentiment Score')

        plt.legend(loc='upper left')
        plt.tight_layout()

    ani = FuncAnimation(plt.gcf(), animate, interval=1000)

    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    plot_session_sentiment_score()
