from scraper import windfinder as wf
from datetime import datetime, date
import numpy as np
from notify.notifications import get_best_day

soup = wf.get_windfinder_soup()

df = get_best_day(soup = soup,wind_threshold = 5,wave_threshold = 1, hour = 0)

req_date= 'last'
c, given_date = wf.get_date_div(soup, req_date)

d6 = wf.get_wind_at_time(c, 6)
d9 = wf.get_wind_at_time(c, 9)
d7 = 0.333*float(d9)+0.6666*float(d6)
print('wind in 7:00: ' + str(np.round(d7,0)) + ' Kts' )
w6 = wf.get_wave_at_time(c, 9)
