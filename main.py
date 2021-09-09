from scraper.windfinder import Windfinder
from datetime import datetime, date
import numpy as np



wf = Windfinder()
soup = wf.get_soup()
df = wf.get_forecast_df(soup = soup, hour =8)

print(df[(df['wind']>5) & (df['wave']<1)])

req_date= 'last'
req_date = datetime.today()
c, given_date = wf.get_date_div(soup, req_date)

d6 = wf.get_wind_at_time(c, 6)
d9 = wf.get_wind_at_time(c, 9)
d7 = 0.333*float(d9)+0.6666*float(d6)
print('wind in 7:00: ' + str(np.round(d7,0)) + ' Kts' )
w6 = wf.get_wave_at_time(c, 6)
