import pandas as pd

df = pd.read_csv('./data/districts.csv')

targetElection = "Bundestagswahl"
targetYear = 202

df = df[(df["Wahl"] == targetElection) & (df["Jahr"] == targetYear)]
print(df.head(10))