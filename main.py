import requests
import datetime as dt
from datetime import timedelta
import data
import os


# メッセージ送信
def telegram_bot_send_text(bot_message):
    bot_token = os.environ.get("BOT_TOKEN")
    bot_chatID = os.environ.get("BOT_CHATID")
    send_text = ('https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID
                 + '&parse_mode=Markdown&text=' + bot_message)
    res = requests.get(send_text)
    return res.json()


STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"

parameters = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK,
    "apikey": os.environ.get("STOCK_API_KEY"),
}

response = requests.get(url="https://www.alphavantage.co/query", params=parameters)
response.raise_for_status()
# data = response.json()
data = data.stock

# data_list = [value for (key, value) in data["Time Series (Daily)"].items()]
# yesterday_end = float(data_list[0]['4. close'])
# yesterday_before_end = float(data_list[1]['4. close'])
yesterday_end = 133.3333
yesterday_before_end = 100.0000

rate_of_change = (yesterday_end - yesterday_before_end) / yesterday_before_end

if rate_of_change >= 0.05 or rate_of_change <= -0.05:

    # 株価変動のお知らせ
    if rate_of_change > 0:
        mark = "🔺"
    else:
        mark = "🔻"
    percent = round(abs(rate_of_change) * 100, 2)
    msg = f"{STOCK}: {mark}{percent}%"
    # print(msg)
    test = telegram_bot_send_text(msg)

    # ニュース記事の取得
    parameters = {
        "q": "Tesla",
        "sortBy": "popularity",
        "apiKey": os.environ.get("NEWS_API_KEY"),
    }
    response = requests.get(url="https://newsapi.org/v2/everything", params=parameters)
    response.raise_for_status()
    data = response.json()
    articles = data["articles"]

    # 上位3記事をメッセージ送信
    for article in articles[:3]:
        title = article['title']
        description = article['description']
        test = telegram_bot_send_text(f"Headline:{title}\n\nBrief:{description}")
