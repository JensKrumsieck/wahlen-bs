import re
from urllib.request import urlopen
from functools import reduce

def urlExists(url: str) -> bool:
    try:
        with urlopen(url) as response:
            return response.status == 200
    except:
        return False
    
def uniqueBy(list: list, by: str) -> list:
    return reduce(lambda acc, curr: acc if any(x[by] == curr[by] for x in acc) else acc + [curr], list, [])

def list2dict(list: list) -> dict:
    return {item["feld"]: item["wert"] for item in list}

def fixElectionName(input: str) -> str:
    if "Niedersächsischen" in input:
        input = "Landtagswahl"
    if "Deutschen Bundestag" in input:
        input = "Bundestagswahl"
    input = input.split(" ")[0]
    return input

def removeSpecialKeys(input: dict)-> dict:
    # remove party fields in fields
    haystack = list(input.keys())
    [input.pop(x, None) for x in haystack if x.startswith("D") or x.startswith("F") or x.startswith(".") or x.startswith("E")] 
    return input

def unfoldVotes(input: dict)-> dict:   
    if not "D1 / F1" in input:
        return input

    newDict = {}
    for key in input:
        parts = key.split(" / ")
        newDict[parts[0]] = input[key] + " Erststimmen"
        if len(parts) > 1:
            newDict[parts[1]] = input[key] + " Zweitstimmen"
    return newDict

def hasPrimaryVote(election: str) -> bool:
    return election in ["Landtagswahl", "Bundestagswahl"]

def isRatswahl(election: str) -> bool:
    return "Stadtratswahl" in election

def getElectionType(electionName: str) -> str:
        if "europa" in electionName.lower():
            return "europawahl"
        if "bund" in electionName.lower():
            return "bundestagswahl"
        if "land" in electionName.lower():
            return "landtagswahl"
        if "rat" in electionName.lower():
            return "ratswahl"
        return "buergermeisterwahl"

def fixPartyName(input: str) -> str:
    output = input
    party_mapping = {
            "Christlich Demokratische Union": "CDU",
            "Sozialdemokratische Partei": "SPD",
            "GRÜNE": "GRÜNE",
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
            "FREIE WÄHLER": "Freie Wähler",
            "Freie Wähler": "Freie Wähler",
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
    output = output.replace("Erststimmen", "")
    output = output.replace("Zweitstimmen", "")
    if output == "V³":
        output = "V-Partei³"
    if output == "GRÜNE":
        output = "BÜNDNIS 90/DIE GRÜNEN"
    return output.strip()