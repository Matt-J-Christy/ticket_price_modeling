"""
Scrape SeatGeeks league specific 
home pages to find event ids used to query
their API
"""

import pandas as pd
import sqlite3
from requests import get
from bs4 import BeautifulSoup
from datetime import datetime


nba_link = 'https://seatgeek.com/nba-tickets'
mlb_link = 'https://seatgeek.com/mlb-tickets'

conn = sqlite3.connect('tickets.db')


def get_page(url):
    # grabbing the HTML and getting text
    my_header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
        + ' AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36'}
    fantasy_page = get(url, headers=my_header)

    return(fantasy_page)


"""
Get NBA Data
"""
nba_page = get_page(nba_link)

nba_html = BeautifulSoup(nba_page.text, "lxml")

links = []
nba_games = []
nba_event_ids = []

for link in nba_html.findAll('a'):
    links.append(link.get('href'))

# get nba links
for i in range(1, len(links)):
    link = str(links[i])
    if "/nba/" in link:
        nba_games.append(link)
        nba_event_ids.append(link[-7:])


nba_event_ids = list(set(nba_event_ids))

nba_event_ids = [int(el) for el in nba_event_ids]


"""
Get MLB Data
"""

mlb_link = get_page(mlb_link)

mlb_html = BeautifulSoup(nba_page.text, "lxml")

links = []
mlb_games = []
mlb_event_ids = []

for link in mlb_html.findAll('a'):
    links.append(link.get('href'))

# get nba links
for i in range(1, len(links)):
    link = str(links[i])
    if "/nba/" in link:
        mlb_games.append(link)
        mlb_event_ids.append(link[-7:])


mlb_event_ids = list(set(mlb_event_ids))

mlb_event_ids = [int(el) for el in mlb_event_ids]

# write event ids to DB

now = datetime.utcnow()
nba = ['nba'] * len(nba_event_ids)
mlb = ['mlb'] * len(mlb_event_ids)

results_df = pd.DataFrame({
    'datetime_utc': now,
    'league': nba + mlb,
    'event_ids': nba_event_ids + mlb_event_ids
})

results_df.to_sql(
    name='event_id_dump',
    con=conn,
    if_exists='append',
    index=False
)
