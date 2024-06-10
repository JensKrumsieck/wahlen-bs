import pandas as pd;

def parse(input: pd.DataFrame) -> pd.DataFrame:
    input.rename(columns={"Wahl zum/zur Oberbürgermeister/in": "Oberbürgermeisterwahl"}, inplace=True)
    input.drop("Demographische Struktur der Bevölkerung", inplace=True, axis=1, level=0)

    input.drop([col for col in input.columns.get_level_values(1).unique() if "Gewi" in str(col)], axis=1, level=1, inplace=True)
    level1cols = input.columns.get_level_values(1).unique()
    level1cols = [col for col in level1cols if len(str(col)) > 4]
    level1cols = [col for col in level1cols if not "vorläufig" in str(col)]
    input.drop(level1cols[1:], inplace=True, axis=1, level=1)
    level2cols = input.columns.get_level_values(2).unique()
    level2cols = [col for col in level2cols if str(col).startswith("Stimmen") or str(col).startswith("Stärkste")]
    input.drop(level2cols, inplace=True, axis=1, level=2)

    districts = input.columns.get_level_values(0).unique()[0]
    df = pd.DataFrame(columns=[districts + "Id", districts, "Wahl", "Jahr", "Messung", "Wert"])

    for _, row in input.iterrows():
        district = row[districts].values[0]
        id = district.split(" ")[0]
        if(not id.isdigit()):
            continue
        elections = row.index.get_level_values(0).unique()[1:]
        for election in elections:
            years = row[election].index.get_level_values(0).unique()
            for year in years:
                measures = row[election][year]
                for measure in measures.index:
                    value = measures[measure]
                    series = pd.Series([id, district, election, str(year)[:4], measure, value], index=df.columns)
                    df = df._append(series, ignore_index=True)
    return df

def read_file(filename: str, electoralDistricts = False) -> pd.DataFrame:
    sheet = "12 Stadtbezirke"
    if(electoralDistricts): sheet = "175 Wahlbezirke"
    df = pd.read_excel(filename, sheet_name=sheet, header=[0,1,2])
    return parse(df)
    