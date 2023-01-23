<h1 align="center">
 Sentiment Analysis using Twitter API
</h1>

<p align = "center">💡 This project is running on python version 3.10.4 </p>


# Table of Contents

- [Installing Dependencies](#installing-dependencies)
- [Running the scripts](#running-the-scripts)

---
<a name="Installing_Dependencies"></a>
## Installing Dependencies
- You need to install all the dependencies by running the code
`pip install -r requirements.txt` in the terminal.

<a name="Running_the_scripts"></a>
## Running the scripts
- Firstly, you need to set your Twitter API keys in `twitter_api_keys.py` in 
the `web_crawler` directory. 
- Secondly, run the `save_data.py` in `data` directory. The script will
fetch data from twitter, and save it in real-time in a `data.csv` file that will
be created in the `data` directory. The data is simply the sentiment score of every 
English tweet containing the words **crypto** OR **cryptocurrency** OR **cryptocurrencies**.
- Finally, run the `main.py` script, and the live data will be plotted in real time; a new
data point is created after every 30 minutes (a session)