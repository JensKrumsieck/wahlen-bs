import os;
from urllib.request import urlopen;
import json
from datetime import datetime
import numpy as np
import pandas as pd
import utils as util
from urllib.parse import urljoin;
from prisma import Prisma;
import re;

async def main():
    cwd = os.path.dirname(__file__)
    prisma = Prisma()
    await prisma.connect()

    # read available endpoints
    with open(cwd + '/endpoints.json') as file:
        endpoints = json.load(file)

    if (not endpoints):
        exit()    
        
    for endpoint in endpoints:
        dates = util.getAvailableElections(endpoint)
        for date in dates:
            openData = util.buildUrl(date, endpoint)
            if not util.urlExists(openData):
                print("No open data found for", date) 
                continue       

            # process data
            with urlopen(openData) as response:
                data = json.loads(response.read().decode("UTF-8"))
                files = data["csvs"] # get csv filenames                
                elections = set([file["wahl"] for file in files]) # get unique elections      

                # select "Stadtbezirk" level (hardcoded for braunschweig currently!)
                csvs = [file for file in files if file["wahl"] in elections and "Stadtbezirk" in file["ebene"]] 
                
                if not csvs:
                    print("No csvs found for", date)
                    continue

                # process selected csvs
                for i, csv in enumerate(csvs):
                    fields= data["dateifelder"][i]["felder"]
                    parties = data["dateifelder"][i]["parteien"]

                    csvUrl = urljoin(base=openData, url=csv["url"])
                    if(not util.urlExists(csvUrl)):
                        csvUrl = urljoin(base=openData.replace("api", ""), url=csv["url"])
                    if(not util.urlExists(csvUrl)):
                        print("No csv found for", csv["wahl"], "at", csvUrl)
                        continue
                    
                    electionName = util.fixElectionName(csv["wahl"])
                    
                    df = pd.read_csv(csvUrl, delimiter=";")
                    util.fixColumnNames(df, fields)
                    # add party columns
                    for party in parties:
                        i = re.search("\d+",party["feld"]).group()
                        dual = False
                        if "F1" in df.columns:
                            dual = True
                        df.rename(columns=lambda x: re.sub(f'D{i}$|D{i}\D', party["wert"] + " " + ("Erststimme" if dual else ""), x).strip(), inplace=True)
                        df.rename(columns=lambda x: re.sub(f'F{i}$|F{i}\D', party["wert"] + " " + ("Zweitstimme" if dual else ""), x).strip(), inplace=True)
                    date = datetime.strptime(df["datum"][0], "%d.%m.%Y")
                    election = await prisma.election.find_first(where={"election_name": electionName, "election_date" : date})
                    if not election:
                        election = await prisma.election.create(
                            data={
                                "election_date": date,
                                "election_name": electionName,
                                "election_type": util.getType(electionName),
                                })
                    take:bool = False
                    for col in df.columns:            
                        if col == "datum":
                            take = False
                        if take:
                            if "summe" in col or "liste" in col:
                                continue
                            partyName = util.fixPartyName(col)
                            party = await prisma.party.find_first(where={"party_name": partyName})
                            if not party:
                                party = await prisma.party.create(data={"party_name": partyName})
                        if col == "Gültige Stimmen":
                            take = True
                    for i, row in df.iterrows():
                        if np.isnan(row["Wahlberechtigte"]): # no data :(
                            continue

                        district = await prisma.district.find_first(where={"district_name": row["gebiet-name"], "city": endpoint["name"], "election_id": election.election_id})
                        if not district:
                            district = await prisma.district.create(data={
                                "district_name": row["gebiet-name"].replace("SBZ", "").strip(),
                                "city": endpoint["name"],
                                "state": endpoint["state"],
                                "registered_voters": row["Wahlberechtigte"],
                                "voters_voted": row["Wähler"],
                                "election_id": election.election_id
                                })
                        # add votes
                        for col in df.columns:
                            partyName = util.fixPartyName(col)
                            party = await prisma.party.find_first(where={"party_name": partyName})
                            if not party or not type(row[col]) is int:
                                continue
                            vote_type = "primary_vote" if "Erststimme" in col else "secondary_vote"
                            election = await prisma.election.find_first(where={"election_name": electionName, "election_date": date})
                            vote = {
                                "party_id": party.party_id,
                                "district_id": district.district_id,
                                "election_id": election.election_id,
                                "vote_count": int(row[col]),
                                "vote_type": vote_type
                            }
                            ex_vote = await prisma.vote.find_first(where={"party_id": party.party_id, "district_id": district.district_id, "election_id": election.election_id, "vote_type": vote_type})
                            if not ex_vote:
                                await prisma.vote.create(data=vote)
                                