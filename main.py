from scraper import windfinder as wf
from datetime import datetime, date
import numpy as np


soup = wf.get_windfinder_soup()

req_date= datetime.strptime('Sep 13 ' + str(date.today().year), '%b %d %Y')
req_date= 'last'
c, given_date = wf.get_date_div(soup, req_date)

d6 = wf.get_wind_at_time(c, 6)
d9 = c[3].find_all('span',{"class": "units-ws"})[0].get_text()
d7 = 0.333*float(d9)+0.6666*float(d6)
print('wind in 7:00: ' + str(np.round(d7,0)) + ' Kts' )



