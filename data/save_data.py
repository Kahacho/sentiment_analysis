import csv
from datetime import datetime, timedelta
import time

from web_crawler.web_crawler_script import compute_session_sentiment_score


# Initialising the start of the session and compound score
session = datetime.now().replace(second=0, microsecond=0)
scores = compute_session_sentiment_score()

# Naming the columns of the dataset containing session and compound scores
fieldnames = ["session", "scores"]

with open('data.csv', 'w') as csv_file:
    # Create a .csv file that stores the session and the computed polarity score
    csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    csv_writer.writeheader()

while True:
    # Run the script forever and save the data in real time

    with open('data.csv', 'a') as csv_file:
        # Append sentiment scores of every new session
        csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

        info = {
            "session": session,
            "scores": scores
        }

        csv_writer.writerow(info)
        print(str(session), scores)

        # Updating the session after every 30 minutes
        session = session + timedelta(minutes=30)

        # Update the next session sentiment score
        scores = compute_session_sentiment_score()

    # Executing and updating the data after every 30 minutes = 1800 seconds
    time.sleep(1800)
