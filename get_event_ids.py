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

conn = sqlite3.connect('tickets.db')


def get_page(url):
    # grabbing the HTML and getting text
    my_header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
        + ' AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36'}
    fantasy_page = get(url, headers=my_header)

    return(fantasy_page)


def get_ticket_data(link, league):

    page = get_page(link)

    html = BeautifulSoup(page.text, "lxml")

    links = []
    event_ids = []

    for link in html.findAll('a'):
        links.append(link.get('href'))

    search_str = "/" + league + "/"

    # get nba links
    for i in range(1, len(links)):
        link = str(links[i])
        if search_str in link:
            event_ids.append(link[-7:])

    event_ids = list(set(event_ids))

    event_ids = [int(el) for el in event_ids]

    return event_ids


def flatten(list):
    flat_list = [item for sublist in list for item in sublist]

    return flat_list

# iterate through active leagues

leagues = ['nba', 'mlb', 'nhl']

nba_link = 'https://seatgeek.com/nba-tickets'
mlb_link = 'https://seatgeek.com/mlb-tickets'
nhl_link = 'https://seatgeek.com/nhl-tickets'

links = [nba_link, mlb_link, nhl_link]

ids_list = []
league_ids = []

for i in range(0, len(links)):

    ids = get_ticket_data(links[i], leagues[i])
    ids_list.append(ids)
    league_ids.append([leagues[i]]*len(ids))

# write event ids to DB

now = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")

final_event_ids = flatten(ids_list)
league_names = flatten(league_ids)

results_df = pd.DataFrame({
    'datetime_utc': now,
    'league': league_names,
    'event_id': final_event_ids
})

results_df.to_sql(
    name='event_id_dump',
    con=conn,
    if_exists='append',
    index=False
)


