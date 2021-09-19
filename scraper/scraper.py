import requests
from bs4 import BeautifulSoup
import numpy as np
from datetime import datetime, date, timedelta
import pandas as pd
from scraper.windfinder import Windfinder
from scraper.windguru import Windguru

class Scraper:

    def __init__(self, site = 'windguru'):
        self.site = site
        pass

    def get_forecast_df(self, hour):
        if self.site == 'windguru':
            wg = Windguru()
            df = wg.get_forecast_df(hour = hour)
        if self.site ==  'windfinder':
            wf = Windfinder()
            df = wf.get_forecast_df(hour = hour)
        return df

