# Assignment from Mvideo

## Description:

Make Web API in Python with one endpoint that takes sku as a parameter and returns a list of all products recommended for that sku. It should be possible to specify optional parameter of minimum proximity threshold for recommendations.

RUN:
```
docker-compose up --build
```

It should be possible to specify optional parameter of minimum proximity threshold for recommendations.

## Limitations
The task must be solved without using third-party libraries and services (like databases). It is allowed to use only standard Python library.

Exception: you can use Flask or AIOHTTP to implement Web API, but implementation only on standard library is a plus.
The sqlite3 module cannot be used.

The CSV file can be pre-prepared with another tool if needed.
Maximum API response time on request - 500ms.
Maximum RAM consumption by the server is 5 GB.

When choosing between lower speed of response on the request and lower consumption of RAM, preference should be given to the lower speed of response.

## Results
API response time 6~ ms
RAM 12.6~ GB