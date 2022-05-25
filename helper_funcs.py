"""
Helper functions
"""

from google.cloud import storage
from google.oauth2 import service_account
import json
from requests import get
from bs4 import BeautifulSoup
import requests
from datetime import datetime

"""
reading and writing to GCP 
storage bucket location
"""

with open('gcp_compute_creds.json') as file:
    creds_dict = json.load(file)

creds = service_account.Credentials.from_service_account_info(creds_dict)

storage_client = storage.Client('ticket-model-app', credentials=creds)


def upload_blob_from_memory(bucket_name, df, destination_blob_name):
    """Uploads a file to the bucket."""

    # The ID of your GCS bucket
    # bucket_name = "ticket-data-dump"

    # The contents to upload to the file
    contents = df.to_csv(index=False)

    # The ID of your GCS object
    # destination_blob_name = "event_ids"

    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_string(contents)

    print(
        f"{destination_blob_name} with {df.shape[0]} event ids uploaded to {bucket_name}."
    )

"""
Functions used to get event ids on Seatgeek
"""

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

    # look for league specific links
    for i in range(len(links)):
        link = str(links[i])
        if search_str in link:
            event_ids.append(link[-7:])

    event_ids = list(set(event_ids))

    event_ids = [int(el) for el in event_ids]

    return event_ids


def flatten(list):
    flat_list = [item for sublist in list for item in sublist]

    return flat_list

"""
getting ticket data 
"""


def get_event_data(
    base_url: str,
    event_id: str,
    client_string: str
):
    now_utc = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")

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
