
import requests
import pandas as pd
import sqlite3
import config
from datetime import datetime

base_url = 'https://api.seatgeek.com/2/events/'

client_string = '?client_id=' + config.my_client_id

event_id = '5653471'

query_url = base_url + event_id + client_string

json_result = requests.get(query_url).json()

now_utc = datetime.utcnow()

# keys I care about:
# stats, datetime_local, datetime_utc,
# there keys are nested in 'performers':
# id, name, popularity, slug, type, location

price_info = json_result['stats']
price_info.pop('dq_bucket_counts')

results_dict = {}

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

results_df = pd.DataFrame([results_dict])

db_name = 'tickets.db'

conn = sqlite3.connect(db_name)



results_df.to_sql(
    name='ticket_price_dump',
    con=conn,
    if_exists='append',
    index=False
)
