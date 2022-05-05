drop table if exists ticket_price_log;

create table ticket_price_log as 

with base as (
    select * 
    from ticket_price_dump
)

select 
    type as league,
    name as home_team,
    id,
    popularity,
    slug as sg_team_name,
    away_name as away_team,
    away_popularity as away_popularity,
    away_id,
    away_slug as away_sg_team_name,
    listing_count,
    cast(average_price as real) as average_price,
    cast(lowest_price_good_deals as real) as lowest_price_good_deals,
    cast(lowest_price as real) as lowest_price,
    cast(highest_price as real) as highest_price,
    visible_listing_count,
    cast(median_price as real) as median_price,
    cast(lowest_sg_base_price as real) as lowest_sg_base_price,
    cast(lowest_sg_base_price_good_deals as real) as lowest_sg_base_price_good_deals,
    event_datetime_local,
    event_datetime_utc,
    query_datetime_utc
from base