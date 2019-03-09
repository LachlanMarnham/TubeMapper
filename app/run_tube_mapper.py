from urllib.parse import urljoin

from bs4 import BeautifulSoup
from requests import Response, Session


class BaseClient:
    def __init__(self) -> None:
        # Instantiate a TCP pool to reduce syn/syn-ack overhead
        self._session = Session()

    def _get(self, url: str) -> Response:
        return self._session.get(url)

    def _get_content_as_text(self, url: str) -> str:
        return self._get(url).text

    def get_content_as_soup(self, url: str) -> BeautifulSoup:
        page_text = self._get_content_as_text(url)
        return BeautifulSoup(page_text, 'html.parser')


class StationsScraper(BaseClient):

    def __init__(self):
        super().__init__()
        self._tube_stations = []
        self._data = {'station_names': set()}

    def get_tube_stations(self, url: str) -> list:
        """
        Get a List of tube stations and links to their associated wikipedia pages. Example:
        [{'station_name': 'Acton Town', 'station_url': 'https://en.wikipedia.org/wiki/Acton_Town_tube_station'}, ...]
        """
        soup = self.get_content_as_soup(url)

        # Currently the table we want to scrape has no id or unique classes. It is the first table on the page, let's
        # hope it stays that way...
        stations_table_body = soup.findChild('table').findChild('tbody')

        # Station names are conveniently used as the row-scoped table headers
        stations = stations_table_body.findChildren('th', attrs={'scope': 'row'})

        for station in stations:
            anchor = station.findChild('a')
            href = anchor.get('href')
            station_name = anchor.string
            self._data['station_names'].add(station_name)
            station_url = urljoin(url, href)
            self._tube_stations.append({'station_name': station_name, 'station_url': station_url})

        self._data['tube_stations'] = self._tube_stations
        return self._tube_stations

    def get_dlr_stations(self, url: str) -> list:
        """
        Works similarly to get_tube_stations, but respects the different layout of the
        """
        dlr_stations = []

    def _get_nearest_neighbours_for_station(self, url: str):
        pass


if __name__ == '__main__':
    client = StationsScraper()
    station_list_url = 'https://en.wikipedia.org/wiki/List_of_London_Underground_stations'
    tube_stations = client.get_tube_stations(station_list_url)
