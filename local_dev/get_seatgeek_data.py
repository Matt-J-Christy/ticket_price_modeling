"""
Querying SeatGeek API to 
get event price data 
"""

import requests
import pandas as pd
import sqlite3
import config  # pull api credential from file (not shared on github)
from datetime import datetime

# set up base parameters for queries

base_url = 'https://api.seatgeek.com/2/events/'

client_string = '?client_id=' + config.my_client_id

conn = sqlite3.connect('../tickets.db')

event_query = f"""
select distinct event_id, league
from event_id_dump
where date(datetime_utc) = date()
"""

id_table = pd.read_sql(
    event_query,
    con=conn
)

print(f"Events today: {id_table.shape[0]}")

now_utc = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")


def get_event_data(
    base_url: str,
    event_id: str,
    client_string: str
):

    results_dict = {}

    query_url = base_url + str(event_id) + client_string

    json_result = requests.get(query_url).json()

    if 'status' in json_result.keys() and \
            json_result['status'] == 'error':
        print(f"[!] {json_result['code']} error: event_id {event_id}")

    else:

        # keys I care about:
        # stats, datetime_local, datetime_utc,
        # there keys are nested in 'performers':
        # id, name, popularity, slug, type, location

        price_info = json_result['stats']
        price_info.pop('dq_bucket_counts')

        home = json_result['performers'][0]
        away = json_result['performers'][1]

        for i in ['name', 'id', 'popularity', 'slug', 'type']:
            key = 'home_' + i
            results_dict[i] = home[i]

        for i in ['name', 'id', 'popularity', 'slug']:
            key = 'away_' + i
            results_dict[key] = away[i]

        for key in price_info.keys():
            results_dict[key] = price_info[key]

        results_dict['event_datetime_local'] = json_result['datetime_local']
        results_dict['event_datetime_utc'] = json_result['datetime_utc']
        results_dict['query_datetime_utc'] = now_utc
        results_dict['event_id'] = str(event_id)

        return results_dict


# iterate through events list
id_list = id_table['event_id']
ticket_data = []  # create empty list to drop dictionaries

for id in id_list:
    res = get_event_data(
        base_url=base_url,
        event_id=id,
        client_string=client_string
    )

    if res != None:
        ticket_data.append(res)

print(f"Events scraped: {len(ticket_data)}")

# write results to db

results_df = pd.DataFrame(ticket_data)

results_df.to_sql(
    name='ticket_price_dump',
    con=conn,
    if_exists='append',
    index=False
)
