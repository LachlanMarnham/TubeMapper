# TubeMapper
A backend + API which constructs a representation of the London Underground system and allows the user to ask questions 
about it. A few notes:
- We only scrape data with requests made in series, as requested in the [Wikipedia API etiquette](https://www.mediawiki.org/wiki/API:Etiquette#Request_limit)
- We only perform the scraping once per day, so that the information is never out of date by more than 24 hours. This is
obviously still overkill, with new stations having a several-years build time...but it doesn't hurt us to run the scraper
once per day.
- Scraped data is cached as a json blob in Redis for quick retrieval. In the event that a request to the API spawns a 
new WSGI thread, the data is fetched from Redis and an instance of TubeGraph is instantiated globally (with respect to)
that thread at module-import time. TubeGraph exposes a psuedo-read-only API to the rest of the code which can be used at 
request time. The time-cost for instantiating a new TubeGraph is paid by the first user to make a request to that WSGI 
thread, but then it will persist.
