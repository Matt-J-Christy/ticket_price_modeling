"""
Set up a schedule to 
run the scraper every 8 hours 
"""

import schedule
import time
import gcp_get_event_ids
import gcp_get_seatgeek_data

def job():
    """
    Create a job function 
    that executes the scraper
    """

    gcp_get_event_ids.GetEventIds()
    gcp_get_seatgeek_data.GetTicketData()

    return print("SeatGeek Ticket Data Acquired")

# define the schedule 
# run  every 8 hours starting at 8 am 
schedule.every(8).hours.at("08:00").do(job)

while True:
    schedule.run_pending()
    time.sleep(1)
