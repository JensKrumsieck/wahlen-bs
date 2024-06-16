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