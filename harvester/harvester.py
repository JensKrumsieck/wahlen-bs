import os;
from urllib.request import urlopen;
import json
import pandas as pd
from utils import fixElectionName, urlExists, translateField, renameField;
from urllib.parse import urljoin;
from pathlib import Path;


cwd = os.path.dirname(__file__)

# read available endpoints
with open(cwd + '/endpoints.json') as file:
    endpoints = json.load(file)

if (not endpoints):
    print("No endpoints found")
    exit()

def getAvailableElections(endpoint) -> list[str]:
    url = endpoint["baseUrl"] + endpoint["id"] + "/api/termine.json"
    with urlopen(url) as response:
        raw = response.read().decode("UTF-8")
        data = json.loads(raw)
    dates = data["termine"]
    return set([date["url"].replace("praesentation/", "") for date in dates])

def buildUrl(date: str, endpoint) -> str:
    url = urljoin(base=endpoint["baseUrl"], url=date)
    openData = url + "daten/opendata/open_data.json"
    if not urlExists(openData):
            openData = url + "api/praesentation/open_data.json"
    return openData

for endpoint in endpoints:
    dates = getAvailableElections(endpoint)
    for date in dates:
        openData = buildUrl(date, endpoint)
        if not urlExists(openData):
            print("No open data found for", date) 
            continue
        # process data
        with urlopen(openData) as response:
            raw = response.read().decode("UTF-8")
            data = json.loads(raw)

            files = data["csvs"] # get csv filenames
            
            elections = set([file["wahl"] for file in files]) # get unique elections       
            # select "Stadtbezirk" level (hardcoded for braunschweig currently!)
            csvs = [file for file in files if file["wahl"] in elections and "Stadtbezirk" in file["ebene"]] 
            
            if not csvs:
                print("No csvs found for", date)
                continue

            year = date.split("/")[1][:4]

            # process selected csvs
            for i, csv in enumerate(csvs):
                fields= data["dateifelder"][i]["felder"]
                parties = data["dateifelder"][i]["parteien"]
                csvUrl = urljoin(base=openData, url=csv["url"])
                if(not urlExists(csvUrl)):
                    csvUrl = urljoin(base=openData.replace("api", ""), url=csv["url"])
                if(not urlExists(csvUrl)):
                    print("No csv found for", csv["wahl"], "at", csvUrl)
                    continue
                
                electionName = fixElectionName(csv["wahl"])
                p = Path(cwd + "/data/" + endpoint["name"] +"/"+  electionName + "/")
                p.mkdir(exist_ok=True, parents=True)
                
                df = pd.read_csv(csvUrl, delimiter=";")
                # alter columns
                df["gebiet-nr"] = df["gebiet-name"].str[:3]
                df.drop(columns=["max-schnellmeldungen", "anz-schnellmeldungen", "A1", "A2", "A3", "B1"], inplace=True)
                df.rename(
                    columns={
                        "A": "Wahlberechtigte", 
                        "B": "Wähler", 
                        "C": translateField(fields, "C"), 
                        "D": translateField(fields, "D"), 
                        "E": translateField(fields, "E"),
                        "F": translateField(fields, "F"),
                    }, inplace=True)
                # add party columns
                for i in range(1, len(parties) + 1):
                    renameField(df, i, parties)
                #save
                df.to_csv(p / (year + ".csv"), index=False, sep=";")
