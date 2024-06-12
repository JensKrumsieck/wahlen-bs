from urllib.request import urlopen
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

def translateField(haystack, needle: str) -> str:
    for field in haystack:
        if needle in field["feld"]:
            return field["wert"]
    return needle

def renameField(df:pd.DataFrame, i:int, parties) -> None:
    if "/" in parties[0]["feld"]:        
        df.rename(columns={f"D{i}": translateField(parties, f"D{i}") + " (Erststimmen)"}, inplace=True)
        df.rename(columns={f"F{i}": translateField(parties, f"F{i}") + " (Zweitstimmen)"}, inplace=True)
    df.rename(columns={f"D{i}": translateField(parties, f"D{i}")}, inplace=True)