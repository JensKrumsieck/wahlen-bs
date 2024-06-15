import json
import re
from urllib.request import urlopen
from urllib.parse import urljoin;
import pandas as pd

def urlExists(url: str) -> bool:
    try:
        with urlopen(url) as response:
            return response.status == 200
    except:
        return False
    
def fixElectionName(input: str) -> str:
    if "Niedersächsischen" in input:
        input = "Landtagswahl"
    if "Deutschen Bundestag" in input:
        input = "Bundestagswahl"
    input = input.split(" ")[0]
    return input

def fixPartyName(input: str) -> str:
    output = input
    party_mapping = {
            "Christlich Demokratische Union": "CDU",
            "Sozialdemokratische Partei": "SPD",
            "BÜNDNIS 90/DIE GRÜNEN": "GRÜNE",
            "Freie Demokratische Partei": "FDP",
            "Alternative für Deutschland": "AfD",
            "Die Linke": "DIE LINKE",
            "DIE LINKE": "DIE LINKE",
            "Marxistisch-Leninistische Partei": "MLPD",
            "Partei für Arbeit, Rechtsstaat, Tierschutz, Elitenförderung und basisdemokratische Initiative": "Die PARTEI",
            "Piratenpartei": "PIRATEN",
            "DER DRITTE WEG": "III. Weg",
            "Nationaldemokratische Partei Deutschlands": "NPD",
            "Ökologisch-Demokratische Partei": "ÖDP",
            "PARTEI MENSCH UMWELT TIERSCHUTZ": "Tierschutzpartei",
            "Mensch Umwelt Tierschutz": "Tierschutzpartei",
            "Deutsche Kommunistische Partei": "DKP",
            "Sozialistische Gleichheitspartei": "SGP",
            "Partei für Soziale Gleichheit, Sektion der Vierten Internationale": "SGP",
            "V-Partei³": "V³",
            "Partei des Fortschritts": "PdF",
            "Partei der Humanisten": "PdH",
            "DIE RECHTE": "DIE RECHTE",
            "Deutsche Zentrumspartei": "ZENTRUM",
            "Partei des Demokratischen Sozialismus": "PDS",
            "NATURGESETZ PARTEI": "Naturgesetz",
            "Parlament aufmischen - Stimme der Letzten Generation": "Letzte Generation",
            "Bündnis Sahra Wagenknecht": "BSW",
            "Basisdemokratische Partei Deutschland": "dieBasis",
            "Bürgerinitiative Braunschweig": "BIBS",
            "Volt": "Volt",
            "FW FREIE WÄHLER": "Freie Wähler",
            "Europäische Partei LIEBE": "LIEBE",
            "Partei für Gesundheitsforschung": "Gesundheitsforschung",
            "Partei der Vernunft": "PdV",
            "Demokratische Allianz für Vielfalt und Aufbruch": "DAVA",
            "Klimaliste": "Klimaliste",
            "Allianz für Menschenrechte, Tier- und Naturschutz": "Tierschutzallianz",
            "Aufbruch für Bürgerrechte": "AUFBRUCH",
            "Ab jetzt...Demokratie durch Volksabstimmung": "Volksabstimmung",
            "Aktion Partei für Tierschutz": "Tierschutz hier!",
            "Bund freier Bürger": "BfB",
            "Bündnis für Innovation & Gerechtigkeit": "BIG",
            "Bündnis Grundeinkommen": "BGE",
            "Bürgerrechtsbewegung Solidarität": "BüSo",
            "Demokratie in Europa": "DiEM25",
            "Die Grauen": "DIE GRAUEN",
            "DEUTSCHE VOLKSUNION": "DVU",
            "Feministische Partei DIE FRAUEN": "DIE FRAUEN",
            "FÜR VOLKSENTSCHEIDE": "Volksentscheide",
            "Partei der Arbeitslosen und Sozial Schwachen": "Partei der Arbeitslosen",
            "Plus Das Generation": "PLUS",
            "Rentnerinnen und Rentner Partei": "Rentner",
        }
    for key in party_mapping:
        if key in input:
            output = party_mapping[key]
    output = output.split("-")[0].split("–")[0]
    output = re.sub(r' \d+', '', output)
    return output.strip()

def fixColumnNames(df: pd.DataFrame, fields):
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

def translateField(haystack, needle: str) -> str:
    for field in haystack:
        if needle in field["feld"]:
            return field["wert"]
    return needle

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

def getType(electionName: str) -> str:
        if "europa" in electionName.lower():
            return "europawahl"
        if "bund" in electionName.lower():
            return "bundestagswahl"
        if "land" in electionName.lower():
            return "landtagswahl"
        if "rat" in electionName.lower():
            return "ratswahl"
        return "buergermeisterwahl"