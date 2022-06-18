import requests
from datetime import date, timedelta
from twilio.rest import Client

STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"

STOCK_API_KEY = "5DR0TO2OEWX38C0J"
NEWS_API_KEY = "178b7d01f47546438caf3fed12be3389"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

TWILIO_SID = "AC1dd04f9d07d9eb15998db42ab63c98f7"
AUTH_TOKEN = "30af9f8120651b89bf77e34f4e2ff73f"

d = date.today()
yesterday = d - timedelta(days=1)
yesterday_str = str(yesterday)

before_yesterday = yesterday - timedelta(days=1)
before_yesterday_str = str(before_yesterday)


## STEP 1: Use https://newsapi.org/docs/endpoints/everything
# When STOCK price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").
#HINT 1: Get the closing price for yesterday and the day before yesterday. Find the positive difference between the two prices. e.g. 40 - 20 = -20, but the positive difference is 20.
#HINT 2: Work out the value of 5% of yerstday's closing stock price.

stock_parameters = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK,
    "apikey": STOCK_API_KEY
}

response_stock = requests.get(STOCK_ENDPOINT, params=stock_parameters)
response_stock.raise_for_status()

data = response_stock.json()["Time Series (Daily)"]
data_list = [value for (key, value) in data.items()]
yesterday_close = data_list[0]["4. close"]
before_yesterday_close = data_list[1]["4. close"]

difference = float(yesterday_close) - float(before_yesterday_close)
up_down = None
if difference > 0:
    up_down = "🔺"
else:
    up_down = "🔻"

diff_percent = round((difference / float(yesterday_close))*100)
print(diff_percent)

if abs(diff_percent) > 1:
    news_parameters = {
        "apiKey": NEWS_API_KEY,
        "qInTitle": COMPANY_NAME,

        # "from": before_yesterday,
        # "to": yesterday
    }

    response_news = requests.get(NEWS_ENDPOINT, params=news_parameters)
    response_news.raise_for_status()
    articles = response_news.json()["articles"]
    three_articles = articles[:3]
    print(three_articles)


## STEP 3: Use twilio.com/docs/sms/quickstart/python
# Send a separate message with each article's title and description to your phone number. 
#HINT 1: Consider using a List Comprehension.

    art = [f"{STOCK}: {up_down}{diff_percent}% \nHeadline: {article['title']}.\nBrief: {article['description']}" for article in three_articles]

    client = Client(TWILIO_SID, AUTH_TOKEN)
    for article in art:
        message = client.messages \
            .create(
            body=article,
            from_='+19378822298',
            to=''
        )


#Optional: Format the SMS message like this: 
"""
TSLA: 🔺2%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
or
"TSLA: 🔻5%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
"""

