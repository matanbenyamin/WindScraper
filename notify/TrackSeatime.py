import imaplib
import datetime
import re
import email
import quopri

imapServer = "imap.googlemail.com"
port = "993"
username = "matan.benyamin@gmail.com"
password = "bardugomatan2"

req_time = datetime.datetime.now()
##how often to check ? give interval in seconds! Checking too often might performance and stability.
checkInterval = 120

Mailbox = imaplib.IMAP4_SSL(imapServer, port)
rc, resp = Mailbox.login(username, password)
while 1:
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

df = ws.get_forecast_df(hour = date.hour)
df = df[df.index.day==date.day]

mess = 'Wind in your next scheduled sailing: '
mess = mess+str(np.round(df['wind'][0],1))
mess = mess +' Kts'
mess = mess+ ', and '
mess = mess+str(int(100 * np.round(df['wave'][ind], 1))) + ' cm waves '
mess = mess+' m'