# pip freeze > requirements.txt
# pip install - r requirements.txt
## how to create the telegram bot
# https://medium.com/@robertbracco1/how-to-write-a-telegram-bot-to-send-messages-with-python-bcdf45d0a580


import sys
import copy
from scraper.windfinder import Windfinder
import numpy as np
import yaml
import telebot

TOKEN = "1972757944:AAHSZ3MjqycJVZieWv-7MPgCAkYQuiKM_OA"
tb = telebot.TeleBot(TOKEN)  # create a new Telegram Bot object
#tb.polling(none_stop=False, interval=0, timeout=20)


fname = "config.yaml"
fname = "C:\\Users\lab7\PycharmProjects\WindScraper\config.yaml"
stream = open(fname, 'r')
data = yaml.load(stream)
ref_data = data[123]


def update_config(mess, data_dict):
    if 'wind_th' in mess:
        val = [int(s) for s in mess.split() if s.isdigit()]
        data_dict['thresholds']['wind'] = val[0]

    if 'wave_th' in mess:
        val = [int(s) for s in mess.split() if s.isdigit()]
        data_dict['thresholds']['wave'] = val[0]

    if 'hour' in mess:
        val = [int(s) for s in mess.split() if s.isdigit()]
        data_dict['notifications']['hour'] = val[0]
    return data_dict

# new flow
# 3
# 1. get updates and see if config.yaml needs to be changed
updates = tb.get_updates()
if len(updates) > 0:
    for up in updates:
        #try:
            user_id = up.message.chat.id
            if user_id==123:
                continue
            mess = up.message.text
            # check validity

            # update yaml
            if user_id not in data.keys():  # new id
                data[user_id] = copy.deepcopy(ref_data)

            user_data = data[user_id]
            user_data = update_config(mess, user_data)

            with open(fname, 'w') as yaml_file:
                yaml_file.write(yaml.dump(data, default_flow_style=False))
        #except:
         #   print('failed')

# syntax:
# wind_th = 7
# wave_th = 1
# hour =

#def update_config_file(updates, data):


# get all caht ids
for user in data:

    # get df and user data
    user_data = data[user]
    wf = Windfinder()
    soup = wf.get_soup()
    df = wf.get_forecast_df(soup=soup, hour=user_data['notifications']['sailing_hour'])
    df = df[(df['wind'] > user_data['thresholds']['wind']) & (df['wave'] < user_data['thresholds']['wave'])]

    # generate messag and send
    if len(df) > 0:
        for ind in df.index:
            mess = 'Next ' + df['weekday'][ind] + ',' + str(ind.day) + '.' + str(ind.month) + ' has ' + \
                   str(int(df['wind'][ind])) + ' Kts '
            if df['wave'][ind] > -1:
                mess = mess + 'and ' + str(int(100 * np.round(df['wave'][ind], 1))) + ' cm waves '
            mess = mess + 'at ' + str(ind.hour) + ' o''clock'
            tb.send_message(user, mess)

    print(user_data)

