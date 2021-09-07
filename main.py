from scraper import windfinder as wf
from datetime import datetime, date
import numpy as np


soup = wf.get_windfinder_soup()

req_date= 'last'
c, given_date = wf.get_date_div(soup, req_date)

d6 = wf.get_wind_at_time(c, 6)
d9 = wf.get_wind_at_time(c, 9)
d7 = 0.333*float(d9)+0.6666*float(d6)
print('wind in 7:00: ' + str(np.round(d7,0)) + ' Kts' )
w6 = wf.get_wave_at_time(c, 9)

for i in range(7,15):
    req_date= datetime.strptime('Sep ' + str(i) + ' ' + str(date.today().year), '%b %d %Y')
    c, given_date = wf.get_date_div(soup, req_date)
    d6 = wf.get_wind_at_time(c, 6)
    d9 = wf.get_wind_at_time(c, 9)
    d7 = 0.333*float(d9)+0.6666*float(d6)
    print('wind in 7:00: ' + str(np.round(d7,0)) + ' Kts' )
    w6 = wf.get_wave_at_time(c, 9)
