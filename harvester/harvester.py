import json
import pandas as pd
from urllib.request import urlopen
from datetime import datetime
from urllib.parse import urljoin
from database import Database
from utils import uniqueBy, urlExists, fixElectionName, getElectionType
from util_types import Election, Endpoint, ElectionDate

default_endpoint: Endpoint = Endpoint({
    "id": "03101000",
    "name": "Braunschweig",
    "state": "Niedersachsen",
    "baseUrl": "https://votemanager.kdo.de/"
})

default_layer: str = "Stadtbezirk"

class Harvester:
    def __init__(self, endpoint: Endpoint = default_endpoint):
        self.endpoint = endpoint
        self.__readData()

    dates: list[ElectionDate] = []
    db: Database = Database()

    def __readData(self):
        url = self.endpoint.baseUrl + self.endpoint.id + "/api/termine.json"
        with urlopen(url) as response:
            dates = uniqueBy(json.loads(response.read().decode("UTF-8"))["termine"], "url")
            self.dates = [ElectionDate(date) for date in dates]
        for date in self.dates:
            base = urljoin(self.endpoint.baseUrl, date.url.replace("praesentation/", ""))
            date.url =  base + "daten/opendata/open_data.json"
            if not urlExists(date.url):
                date.url = base + "api/praesentation/open_data.json"
        self.dates = [date for date in self.dates if urlExists(date.url)]

    async def harvest(self):
        for date in self.dates:
            with urlopen(date.url) as response:
                data = json.loads(response.read().decode("UTF-8"))
            csvs = [file for file in data["csvs"] if default_layer in file["ebene"]]
            for csv in csvs:                
                name = fixElectionName(csv["wahl"])
                df = self.__read_csv(csv, date)
                if df is None:
                    continue
                election = await self.db.insertElection(Election(datetime.strptime(date.date, "%d.%m.%Y"), name, getElectionType(name)))

    def __read_csv(self, csv: dict, date: ElectionDate) -> pd.DataFrame | None:
        url = urljoin(date.url, csv["url"])
        if not urlExists(url):
           url = urljoin(date.url.replace("api", ""), csv["url"])
        if not urlExists(url):
            return None
        return pd.read_csv(url, delimiter=";")
        
        