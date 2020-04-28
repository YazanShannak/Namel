# Namel

> When ants travel, they follow a chemical trail left by other ants

Namel derived from the Arabic word (نمل) means "ants", is a distributed real-time web crawling and analysis framework.

The design of the system is inspired by ants behavior when looking for food, usually ants are not aware of other ants through direct communication, although they follow each 

other's paths left by pheromones.

Similarly this system doesn't follow the traditional master-slave or peer-peer design principles, it's a queue based design where each node isn't aware of the other.



## Design

### Core Components

- Kafka](https://kafka.apache.org/), an open source real-time messaging broker,  with three main topics:
  - Domains
  - URLs
  - Data

- URL Parsers: A cluster of nodes whom main responsibility is to parse all URL from a specific domain

- Data Scrapers: Another cluster who search for the required data in the domain, and eventually yielding them if they exist in any given link of the domain

## Workflow

1. A domain is produced to the `domains` topic in kafka
2. An `url parser` node from the `url parsers consumer group` consumes this message when available, the `url parser` will parse are urls from the first page and go through each page to parse more urls recursively, all while  **asynchronously** producing the urls to the `urls` kafka topic
3. A `data scraper` node from the `data scrapers consumer group` will consume a message when available to look for the required data form the domain based on **xpath queries**, if they do exist in the page the data scraper will append the scraped data to the url object and produce it to the `data` topic



