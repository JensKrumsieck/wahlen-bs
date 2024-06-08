import pandas as pd;
import config;
import json;
# geographie keys: id, name, features, themes, ...
# features keys: id, name
# themes keys: name, properties, indicators
# indicators keys: name, values, date (measure!)...

# table: WahlbezirkID Wahlbezirk Wahl Jahr Measure Value
def parse_districts(districts) -> pd.DataFrame:
    df = pd.DataFrame(columns=[districts["id"] + "Id", districts["id"], "Wahl", "Jahr", "Messung", "Wert"])

    district_table = []

    for district in districts["features"]:
        district_table.append({districts["id"] + "Id": district["id"], districts["id"]: district["name"]})
    for theme in districts["themes"]:
        election = theme["name"].strip()
        if not (election.endswith("wahl")):
            continue
        for indicator in theme["indicators"]:
            year = indicator["name"].strip()
            if not len(year) == 4:
                continue
            measure = indicator["date"]
            if measure in ["Stimmenmehrheiten", "Stärkste Partei", "Stimmenmehrheiten Erststimmen", "Stimmenmehrheiten Zweitstimmen", "Stärkste Partei Erststimmen", "Stärkste Partei Zweitstimmen"]:
                continue
            for i, value in enumerate(indicator["values"]):
                series = pd.Series([district_table[i][districts["id"] + "Id"], district_table[i][districts["id"]], election, year, measure, value], index=df.columns)
                df = df._append(series, ignore_index=True)
    return df

def read_file(filename: str, electoralDistricts = False) -> pd.DataFrame:
    with open(filename) as data:
        json_data = json.load(data)
        geographies = json_data["geographies"]
        # geographies:
        # [X] Wahlbezirke
        # [ ] Wahl-Ortsteile
        # [X] Stadtbezirke
        # [ ] Gemeindewahlbereiche
        # [ ] Landtagswahlkreise
        districts = geographies[2]
        if(electoralDistricts): districts = geographies[0]
        return parse_districts(districts)