"""
Querying SeatGeek API to 
get event price data 
"""

import json
from io import StringIO
import pandas as pd
from datetime import datetime
from google.oauth2 import service_account
from google.cloud import storage, bigquery
from helper_funcs import get_event_data
import config  # pull api credential from file (not shared on github)


with open('gcp_creds.json') as file:
    creds_dict = json.load(file)

creds = service_account.Credentials.from_service_account_info(creds_dict)

storage_client = storage.Client(credentials=creds)
bucket = storage_client.bucket('ticket-data-dump')

today = datetime.utcnow().strftime("%Y-%m-%d")
event_id_table = f"event_ids_{today}.csv"

blob = bucket.blob(event_id_table)

id_table = pd.read_csv(StringIO(blob.open('r').read()), sep=',')

print(f"Events today: {id_table.shape[0]}")

# set up base parameters for queries

base_url = 'https://api.seatgeek.com/2/events/'

client_string = '?client_id=' + config.my_client_id

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

# write to google cloud bucket

results_df = pd.DataFrame(ticket_data)

# fix data types

strings = ['name', 'id', 'slug', 'type', 'away_id', 'away_name', 'away_slug', 'event_id',
           'event_datetime_utc', 'event_datetime_local', 'query_datetime_utc']

floats = ['average_price', 'lowest_price_good_deals', 'lowest_price',
          'highest_price', 'listing_count', 'visible_listing_count', 'median_price',
          'lowest_sg_base_price', 'lowest_sg_base_price_good_deals',
          'popularity', 'away_popularity']

results_df[strings] = results_df[strings].astype(str)
results_df[floats] = results_df[floats].astype(float)


bq = bigquery.Client(credentials=creds)

table_id = 'ticket-model-app.ticket_data.ticket_data_dump'

schema = [
    bigquery.SchemaField("name", "STRING"),
    bigquery.SchemaField("id", "STRING"),
    bigquery.SchemaField("popularity", "FLOAT64"),
    bigquery.SchemaField("slug", "STRING"),
    bigquery.SchemaField("type", "STRING"),
    bigquery.SchemaField("away_name", "STRING"),
    bigquery.SchemaField("away_id", "STRING"),
    bigquery.SchemaField("away_popularity", "FLOAT64"),
    bigquery.SchemaField("away_slug", "STRING"),
    bigquery.SchemaField("listing_count", "FLOAT64"),
    bigquery.SchemaField("average_price", "FLOAT64"),
    bigquery.SchemaField("lowest_price_good_deals", "FLOAT64"),
    bigquery.SchemaField("lowest_price", "FLOAT64"),
    bigquery.SchemaField("highest_price", "FLOAT64"),
    bigquery.SchemaField("visible_listing_count", "FLOAT64"),
    bigquery.SchemaField("median_price", "FLOAT64"),
    bigquery.SchemaField("lowest_sg_base_price", "FLOAT64"),
    bigquery.SchemaField("lowest_sg_base_price_good_deals", "FLOAT64"),
    bigquery.SchemaField("event_datetime_local", "STRING"),
    bigquery.SchemaField("event_datetime_utc", "STRING"),
    bigquery.SchemaField("query_datetime_utc", "STRING"),
    bigquery.SchemaField("event_id", "STRING")
]

job_config = bigquery.LoadJobConfig(
    schema=schema
)

job = bq.load_table_from_dataframe(
    results_df, table_id, job_config=job_config
)

print(job.result())
