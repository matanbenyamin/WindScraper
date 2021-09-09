
import requests
from bs4 import BeautifulSoup
import datetime
from datetime import datetime,date
import numpy as np


def get_windfinder_soup(spot= 'marina_tel_aviv'):
    urlPrefix = 'http://www.windfinder.com/forecast/'
    url = urlPrefix + spot
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    text = soup.find_all('div')
    return soup

def get_date_div(soup, req_date):

    # req_date: dateitme object of requested date
    # go to table with relevant date
    all_divs = soup.find_all("div", {"class": "weathertable__header"})
    if req_date=='last':
        date_ind = -1
    else:
        req_date = req_date.strftime('%b %d')
        date_ind = -1
        for ind, div in  enumerate(all_divs):
            div_date = div.get_text()
            loc = div_date.find(req_date)
            if loc > -1:
                date_ind = ind

    if date_ind==-1:
        return [],-1


    given_date = all_divs[date_ind].get_text()
    given_date = given_date[given_date.find('\n',1)+10:given_date.find('\n',2)].strip()
    b = all_divs[date_ind].find_parent()
    return  b, given_date

def get_wind_at_time(date_div, time):

    date_div_wind = date_div.find_all("div", {"class": "speed"})
    if len(date_div_wind) < 8:
        return -1
    hours = np.array([0, 3, 6, 9, 12, 15, 18, 21])
    ind = np.where((hours >= time - 1) & (hours <= time + 1))
    ind2 = np.where(hours >= time)[0][0]
    ind1 = np.where(hours <= time)[-1][-1]

    w1 = float(date_div_wind[ind1].find_all('span', {"class": "units-ws"})[0].get_text())
    w2 = float(date_div_wind[ind2].find_all('span', {"class": "units-ws"})[0].get_text())

    return np.interp(time, [hours[ind1], hours[ind2]], [w1, w2])

def get_wave_at_time(date_div, time):

    date_div_wave = date_div.find_all("div", {"class": "data-waveheight"})
    if len(date_div_wave)<8:
        return -1
    hours = np.array([0, 3, 6, 9 ,12, 15, 18, 21])
    ind = np.where((hours>=time-1) & (hours<=time+1))
    ind2 = np.where(hours >= time)[0][0]
    ind1 = np.where(hours<=time)[-1][-1]

    w1 = float(date_div_wave[ind1].find_all('span', {"class": "units-wh"})[0].get_text())
    w2 = float(date_div_wave[ind2].find_all('span', {"class": "units-wh"})[0].get_text())


    return np.interp(time, [hours[ind1], hours[ind2]], [w1, w2])

