import imaplib
import datetime
import re
import email
import quopri
from scraper.scraper import Scraper
import numpy as np
import telebot
import sys
sys.path.extend(['C:/Users/lab7/PycharmProjects/WindScraper'])
sys.path.extend(['C:/Users/lab7/PycharmProjects/WindScraper/scraper'])


TOKEN = "1972757944:AAHSZ3MjqycJVZieWv-7MPgCAkYQuiKM_OA"
tb = telebot.TeleBot(TOKEN)  # create a new Telegram Bot object

imapServer = "imap.googlemail.com"
port = "993"
username = 'matan.benyamin'
password = 'bardugomatan2'

req_time = datetime.datetime.now()
##how often to check ? give interval in seconds! Checking too often might performance and stability.
checkInterval = 120

Mailbox = imaplib.IMAP4_SSL(imapServer, port)
rc, resp = Mailbox.login(username, password)
if rc == 'OK':
    # calling function to check for email under this label
    Mailbox.select('Inbox')
    Mailbox.list()
    status, email_ids = Mailbox.search(None, 'FROM "office@sea-time.co.il"')
    id = email_ids[0].split()[-1]
    status, data = Mailbox.fetch(id, '(RFC822)')

    raw = email.message_from_bytes(data[0][1])


def get_text(msg):
    if msg.is_multipart():
        return get_text(msg.get_payload(0))
    else:
        return msg.get_payload(None, True)

txt = get_text(raw)
utf8 = quopri.decodestring(txt)
s = utf8.decode('utf-8')

date_ind = [m.start() for m in re.finditer('מועד', s)][0]
date = datetime.datetime.strptime(s[date_ind-17:date_ind-1],'%H:%M %d/%m/%Y')

# date =  datetime.datetime.strptime('15:00 28/10/2021','%H:%M %d/%m/%Y')

# only if date is in the future
if date>datetime.datetime.now():

    ws = Scraper(site='windguru')
    df = ws.get_forecast_df(hour = date.hour)
    df = df[df.index.day==date.day]

    mess = 'Wind in your next scheduled sailing: '
    mess = mess+str(np.round(df['wind'][0],1))
    mess = mess +' Kts'
    mess = mess+ ' and '
    mess = mess+str(int(100 * np.round(df['wave'][0], 1))) + ' cm waves '

    print(mess)

    user = 630924196
    tb.send_message(user, mess)

