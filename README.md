# Ticet Price Modeling 

Matt Christy

Goal: Use open APIs and web scraping to gather event ticket data and 
create a recommendatino algorithm to optimize ticket purchases

## Data Sources

### Seat Geek API

Create a developer account at [SeatGeek](https://seatgeek.com/account/develop) and create an API. You need to do this step to generate your `client_id` and `client_secret`

[Seatgeek API Docs](https://platform.seatgeek.com/)

`client_id`: your_client_id
`client_secret`: your_api_secret

Example: 
```{curl}
curl https://api.seatgeek.com/2/events?client_id={my_client_id}
```

note: apparently just the client id is able to authenticate cURL requests sent to the events API

#### Working Queries:

Event specific:
`curl https://api.seatgeek.com/2/events/5461967?client_id={client_id}`

#### Queries that don't work but would be really useful

key word search:
`curl https://api.seatgeek.com/2/events?q=boston+celtics?client_id={client_id}`

Using perfomer slug: 
`curl https://api.seatgeek.com/2/events?performers.slug=new-york-mets?client_id={client_id}`

getting all sports: 
`curl https://api.seatgeek.com/2/events?taxonomies.name=sports?client_id={client_id}`


## Analysis Process

Use python's requests package + pandas & sqlite3 to pull data and save to a DB

...