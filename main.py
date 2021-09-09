#  pip freeze > requirements.txt
# pip install - r requirements.txt



## how to create the telegram bot
# https://medium.com/@robertbracco1/how-to-write-a-telegram-bot-to-send-messages-with-python-bcdf45d0a580



from scraper.windfinder import Windfinder
import telegram_send
import numpy as np

wf = Windfinder()
soup = wf.get_soup()
df = wf.get_forecast_df(soup=soup, hour=6)
df = df[(df['wind'] > 5) & (df['wave'] < 1)]
print(df)


if len(df)>0:
    for ind in df.index:
        mess = 'Next '+df['weekday'][ind]+ ',' + str(ind.day) + '.' +str(ind.month) +  ' has ' + \
               str(int(df['wind'][ind]))  +' Kts at ' + str(ind.hour) + ' o''clock'
        telegram_send.send(messages=[mess])
