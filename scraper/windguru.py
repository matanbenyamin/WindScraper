import requests, re
from bs4 import BeautifulSoup
import numpy as np
from datetime import datetime, date, timedelta
import pandas as pd
from scraper.scraper import Scraper
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options



class Windguru(Scraper):

    def get_wind_at_time(self, date_div, time):
        pass

    def get_wind_at_time(self, date_div, time):
        pass

    def get_forecast_df(self,  hour):


        df = pd.DataFrame()
        week_dict = {0: 'Monday', 1: 'Tuesday', 2: 'Wednesday', 3: 'Thursday', 4: 'Friday', 5: 'Saturday', 6: 'Sunday'}
        hours = np.array([6, 9, 12, 15, 18, 21,24])

        CHROMEDRIVER_PATH = 'C:\\Users\lab7\Downloads\chromedriver_win32_2\chromedriver.exe'
        WINDOW_SIZE = "1920,1080"
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--window-size=%s" % WINDOW_SIZE)
        d = webdriver.Chrome(executable_path=CHROMEDRIVER_PATH,
                             chrome_options=chrome_options)
        spot = '308'
        urlPrefix = 'https://www.windguru.cz/'
        url = urlPrefix + spot

        d.get(url)
        time.sleep(0.5)
        a = d.find_elements_by_id('tabid_0_0_WINDSPD')[0]
        winds = [int(x) for x in a.text.split()]
        a = d.find_elements_by_id('tabid_0_0_HTSGW')[0]
        waves = [float(x) for x in a.text.split()]
        a = d.find_elements_by_id('tabid_0_0_dates')[0]
        a = a.text.split()[2::3]
        dates = [x[0:2] for x in a]

        for day in range(0,len(winds),9):
            curr_day_winds = winds[day:day+8]


        forecast_flag = True
        i = -1
        while forecast_flag:
            i = i + 1
            curr_day = datetime.today() + timedelta(days=i)
            curr_day = curr_day.replace(hour=hour, minute=0, second=0, microsecond=0)
            c, given_date = self.get_date_div(soup, curr_day)
            if len(c) < 1:
                forecast_flag = False
                continue
            d7 = self.get_wind_at_time(c, hour)
            w6 = float(self.get_wave_at_time(c, hour))
            df = df.append(
                pd.DataFrame(data=[[week_dict[curr_day.weekday()], d7, w6]], index=[curr_day],
                             columns=['weekday', 'wind', 'wave']))

        return df
