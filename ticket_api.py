import requests
import base64
import json
import pprint
import pandas as pd
import datetime
import logging

logger = logging.getLogger("root")
logging.basicConfig(
    format = "\033[1;36m%(levelname)s: %(filename)s (def %(funcName)s %(lineno)s): \033[1;37m %(message)s",
    level=logging.DEBUG
)

APP_TOKEN = ''

CONSUMER_KEY = 'Y502ntnW1YITojs6uEgRwFC0ilEAUOXN'

CONSUMER_SECRET = 'zEbDxgheno4mnnku'

STUBHUB_USERNAME = 'matthewjchristy66@gmail.com'

STUBHUB_PASSWORD = 'B@xtermyfluffy00'

# generating basic authorization token
COMBO = CONSUMER_KEY + ':' + CONSUMER_SECRET

BASIC_AUTHORIZATION_TOKEN = base64.b64encode(COMBO.encode('utf-8'))

HEADERS = {
    'Content-Type':'application/x-www-form-urlencoded',
    'Authorization':'Basic '+BASIC_AUTHORIZATION_TOKEN.decode('utf-8'),
}

BODY = {
    'grant_type': 'password',
    'username': STUBHUB_USERNAME,
    'password': STUBHUB_PASSWORD,
    'scope': 'PRODUCTION'
}

DATA = {
    'eventid': '105053252',
    'sort': 'quantity desc',
    'start': 0,
    'rows': 100
}


class StuHubEventSearch(object):

    ## making the call
    url = 'https://api.stubhub.com/login'

    inventory_url = 'https://api.stubhub.com/search/inventory/v2'

    def _init(self, *args, **kwargs):
        r = requests.post(self.url, headers=HEADERS, data=BODY)
        token_response = r.json()
        user_GUID = r.headers['X-StubHub-User-GUID']
        HEADERS['Authorization'] = 'Bearer ' + token_response['access_token']
        HEADERS['Accept'] = 'application/json'
        HEADERS['Accept-Encoding'] = 'application/json'
        HEADERS['User-agent'] = "Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US) AppleWebKit/525.19 (KHTML, like Gecko) Chrome/1.0.154.53 Safari/525.19"
        inventory = requests.get(self.inventory_url, headers=HEADERS, params=DATA)
        inv = inventory.json()
        rows = inv['rows']
        start = inv['start']
        total_listings = inv['totalListings']
        list_of_tickets = self.make_request_to_url(self.inventory_url, rows, start, total_listings)
        final_df = self.create_and_return_data_frame(list_of_tickets)
        csv_file_name = "_%s_%s_tickets_listing.csv" % (datetime.datetime.today().strftime('%Y_%m_%d'), total_listings)
        final_df.to_csv(csv_file_name, index=False)


    def make_request_to_url(self, url, rows, start, total):
        all_listings = []
        DATA = {
            'eventid': '103128027',
            'sort': 'quantity desc',
            'start': start,
            'rows': 100
        }
        while DATA['start'] < total:
            inventory = requests.get(self.inventory_url, headers=HEADERS, params=DATA)
            inv = inventory.json()
            all_listings = all_listings + inv['listing']
            logger.debug("Retrieving listings starting at %s" % (DATA['start']))
            DATA['start'] = DATA['start'] + inv['rows']
        return all_listings


    def create_and_return_data_frame(self, list_of_tickets):
        listing_df = pd.DataFrame(list_of_tickets)
        listing_df['current_price'] = listing_df.apply(lambda x: x['currentPrice']['amount'], axis=1)
        listing_df['listed_price'] = listing_df.apply(lambda x: x['listingPrice']['amount'], axis=1)
        listing_df['snapshotDate'] = datetime.datetime.today().strftime('%Y-%m-%d %H:%m')
        listing_df['eventName'] = 'World Series'
        listing_df['eventDate'] = '2017-10-24'
        listing_df['venue'] = 'Dodgers Stadium'
        my_col = [
            'snapshotDate',
            'eventName',
            'eventDate',
            'venue',
            'sectionName',
            'row',
            'seatNumbers',
            'quantity',
            'sellerOwnInd',
            'current_price',
            'listed_price',
            'listingId',
        ]
        final_df = listing_df[my_col]
        return final_df


if __name__ == '__main__':
    task_run = StuHubEventSearch()
    task_run._init()
    print "\nTask finished at %s\n" % str(datetime.datetime.now())
