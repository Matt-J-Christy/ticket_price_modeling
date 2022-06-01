#Deriving the latest base image
FROM python:3.8
COPY requirements.txt ./

# install dependencies
RUN pip install -r ./requirements.txt


#Labels as key value pair
LABEL Maintainer="matt_christy"


# Any working directory can be chosen as per choice like '/' or '/home' etc
WORKDIR /c/Users/chris/Documents/Analytical_Projects/ticket_price_modeling

#to COPY the remote file at working directory in container
COPY gcp_get_event_ids.py gcp_get_seatgeek_data.py helper_funcs.py config.py gcp_creds.json ./
# Now the structure looks like this '/c/Users/chris/Documents/Analytical_Projects/ticket_price_modeling/'

# grab event ids for the scraping script
RUN python ./gcp_get_event_ids.py

#CMD instruction should be used to run the software
#contained by your image, along with any arguments.

# run the scraper
CMD [ "python", "./gcp_get_seatgeek_data.py"]
