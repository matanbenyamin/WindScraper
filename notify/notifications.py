from scraper import windfinder as wf
from datetime import datetime, date, timedelta
import numpy as np
import pandas as pd


def get_best_day(soup, wind_threshold, wave_threshold, hour):
    df = pd.DataFrame()
    week_dict = {0:'Monday', 1:'Tuesday', 2:'Wednesday', 3:'Thursday', 4:'Friday', 5:'Saturday',6:'Sunday'}
    forecast_flag = True
    i=-1
    while forecast_flag:
        i=i+1
        today = datetime.strftime(datetime.today(), '%b %d')
        curr_day = datetime.today() + timedelta(days=i)
        c, given_date = wf.get_date_div(soup, curr_day)
        if len(c)<1:
            forecast_flag = False
            continue
        d6 = wf.get_wind_at_time(c, 6)
        d9 = wf.get_wind_at_time(c, 9)
        d7 = 0.333 * float(d9) + 0.6666 * float(d6)
        print('wind in 7:00: ' + str(np.round(d7, 0)) + ' Kts')
        w6 = float(wf.get_wave_at_time(c, 9))
        if d7 > wind_threshold and w6 < wave_threshold:
            df = df.append(
                pd.DataFrame(data=[[week_dict[curr_day.weekday()],d7, w6]], index=[datetime.today() + timedelta(days=i)], columns=['weekday','wind', 'wave']))

    return df
