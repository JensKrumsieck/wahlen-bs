import json
import numpy as np
import pandas as pd
from urllib.request import urlopen
from datetime import datetime
from urllib.parse import urljoin
from database import Database
from utils import fixPartyName, list2dict, removeSpecialKeys, unfoldVotes, uniqueBy, urlExists, fixElectionName, getElectionType
from util_types import District, Election, Endpoint, ElectionDate, Vote

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
            for i, csv in enumerate(csvs):                
                name = fixElectionName(csv["wahl"])
                df = self.__read_csv(csv, date)
                if df is None or np.isnan(df["A1"][0]):
                    continue
                
                election = await self.db.insertElection(Election(datetime.strptime(date.date, "%d.%m.%Y"), name, getElectionType(name)))
                result = self.__prepare_cols(df, data, i)   
                specialIndices = [i for i, col in enumerate(df.columns) if col.startswith("D1")]              
                
                await self.__getParties(result, specialIndices[0])
                for i, row in result.iterrows():                    
                    district = await self.db.insertDistrict(District(row["gebiet-name"].replace("SBZ", "").strip(), self.endpoint.name, self.endpoint.state, row["A"], row["B"], election.election_id))
                    for col in result.columns:
                        vote_type = "primary_vote" if "Erststimme" in col else "secondary_vote"
                        party = await self.db.getParty(fixPartyName(col))
                        if not party:
                            continue
                        vote = Vote(district.district_id, election.election_id, party.party_id, row[col], vote_type)
                        await self.db.insertVote(vote)

    def __read_csv(self, csv: dict, date: ElectionDate) -> pd.DataFrame | None:
        url = urljoin(date.url, csv["url"])
        if not urlExists(url):
           url = urljoin(date.url.replace("api", ""), csv["url"])
        if not urlExists(url):
            return None
        return pd.read_csv(url, delimiter=";") 

    def __prepare_cols(self, df: pd.DataFrame, data: dict, i: int) -> pd.DataFrame:      
        fields = removeSpecialKeys(list2dict(data["dateifelder"][i]["felder"]))
        parties = unfoldVotes(list2dict(data["dateifelder"][i]["parteien"]))
        
        if "D1_liste" in df.columns:
            newDict = {}
            for key in parties:
                newDict[key + "_summe_liste_kandidaten"] = parties[key]
            parties = newDict
        selector = list(fields.keys()) + list(parties.keys())
        newDf = df.loc[:, selector]
        newDf.rename(columns=parties, inplace=True)
        return newDf
    
    async def __getParties(self, df: pd.DataFrame, start: int):
        take = False
        for i, col in enumerate(df.columns):
            if col == "datum":
                take = False
            if take:
                partyName = fixPartyName(col)
                await self.db.insertParty(partyName)
            if i >= start:
                take = True