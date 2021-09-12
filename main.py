# pip freeze > requirements.txt
# pip install - r requirements.txt
## how to create the telegram bot
# https://medium.com/@robertbracco1/how-to-write-a-telegram-bot-to-send-messages-with-python-bcdf45d0a580
import sys; print('Python %s on %s' % (sys.version, sys.platform))
sys.path.extend(['C:\\Users\\lab7\\PycharmProjects\\WindScraper',
                 'C:\\Users\\lab7\\PycharmProjects\\WindScraper\\scraper',
                 'C:/Users/lab7/PycharmProjects/WindScraper'])

import yaml
from scraper.windfinder import Windfinder
import telegram_send
import numpy as np

#       stream = open("config.yaml")
stream = open("C:\\Users\lab7\PycharmProjects\WindScraper\config.yaml")
dict = yaml.load(stream)


wf = Windfinder()
soup = wf.get_soup()
df = wf.get_forecast_df(soup=soup, hour=dict['notifications']['sailing_hour'])
df = df[(df['wind'] > dict['thresholds']['wind']) & (df['wave'] < dict['thresholds']['wave'])]

#df = wf.get_forecast_df(soup=soup, hour=7)
#df = df[(df['wind'] > 6) & (df['wave'] < 2)]

print(df)


if len(df)>0:
    for ind in df.index:
        mess = 'Next '+df['weekday'][ind]+ ',' + str(ind.day) + '.' +str(ind.month) +  ' has ' + \
               str(int(df['wind'][ind]))  +' Kts at ' + str(ind.hour) + ' o''clock'
        telegram_send.send(messages=[mess])
