"""
Scrape SeatGeeks league specific 
home pages to find event ids used to query
their API
"""

import pandas as pd
from datetime import datetime
from google.cloud import storage
from google.oauth2 import service_account
import json
from helper_funcs import upload_blob_from_memory,\
    flatten,\
    get_event_ids


# iterate through active leagues

def GetEventIds():

    with open('gcp_creds.json') as file:
        creds_dict = json.load(file)

    creds = service_account.Credentials.from_service_account_info(creds_dict)

    storage_client = storage.Client('ticket-model-app', credentials=creds)

    leagues = ['nba', 'mlb', 'nhl']

    nba_link = 'https://seatgeek.com/nba-tickets'
    mlb_link = 'https://seatgeek.com/mlb-tickets'
    nhl_link = 'https://seatgeek.com/nhl-tickets'

    links = [nba_link, mlb_link, nhl_link]

    ids_list = []
    league_ids = []

    for i in range(len(links)):

        ids = get_event_ids(links[i], leagues[i])
        ids_list.append(ids)
        league_ids.append([leagues[i]]*len(ids))

    # put data into dataframe

    now = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")

    final_event_ids = flatten(ids_list)
    league_names = flatten(league_ids)

    results_df = pd.DataFrame({
        'datetime_utc': now,
        'league': league_names,
        'event_id': final_event_ids
    })

    # write to google cloud bucket

    now_date = now[:10]

    table_name = f"event_ids_{now_date}.csv"

    upload_blob_from_memory(
        storage_client,
        'ticket-data-dump',
        results_df,
        table_name
    )
