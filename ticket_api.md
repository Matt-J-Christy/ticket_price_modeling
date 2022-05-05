
# Seat Geek API

note: apparently just the client id is able to authenticate cURL requests sent to the events API

client id: OTA5NzcyOXwxNjUwNDc5ODY2LjU3NzU0MTQ
secret: 431796fba1b9621a7619acfa3c5f6179d9d2645033613cd22256816bfee0b91b

Example: 
- curl https://api.seatgeek.com/2/events?client_id=OTA5NzcyOXwxNjUwNDc5ODY2LjU3NzU0MTQ&client_secret=431796fba1b9621a7619acfa3c5f6179d9d2645033613cd22256816bfee0b91b

## Working queries

Event specific:
curl https://api.seatgeek.com/2/events/5461967?client_id=OTA5NzcyOXwxNjUwNDc5ODY2LjU3NzU0MTQ

## Queries that don't work but would be really useful

key word search:
curl https://api.seatgeek.com/2/events?q=boston+celtics?client_id=OTA5NzcyOXwxNjUwNDc5ODY2LjU3NzU0MTQ&client_secret=431796fba1b9621a7619acfa3c5f6179d9d2645033613cd22256816bfee0b91b

curl https://api.seatgeek.com/2/events/?q=boston+celtics&client_id=OTA5NzcyOXwxNjUwNDc5ODY2LjU3NzU0MTQ

curl https://api.seatgeek.com/2/events?geoip=98.213.245.205&range=12mi?client_id=OTA5NzcyOXwxNjUwNDc5ODY2LjU3NzU0MTQ

curl https://api.seatgeek.com/2/events?performers.slug=new-york-mets?client_id=OTA5NzcyOXwxNjUwNDc5ODY2LjU3NzU0MTQ

getting all sports: 
curl https://api.seatgeek.com/2/events?taxonomies.name=sports?client_id=OTA5NzcyOXwxNjUwNDc5ODY2LjU3NzU0MTQ