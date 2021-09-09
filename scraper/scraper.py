import requests
from bs4 import BeautifulSoup
import numpy as np
from datetime import datetime, date, timedelta
import pandas as pd


class Scraper:

    def __init__(self):
        pass

    def get_forecast_df(self, soup, hour):
        pass

    def get_wave_at_time(self, date_div, time):
        pass

    def get_soup(self, spot='marina_tel_aviv'):
       pass

    def get_date_div(self, soup, req_date):
        pass

    def get_wind_at_time(self, date_div, time):
        pass