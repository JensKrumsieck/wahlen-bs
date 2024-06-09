import pandas as pd;
import plot;
from dash import Dash, html, dcc, Input, Output
import dash_bootstrap_components as dbc

df = pd.read_csv('./data/districts.csv')

supportedElections = df["Wahl"].unique()

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.layout = dbc.Container([
    html.H1("lol"),
    dcc.Dropdown(id="election", options=supportedElections, value="Bundestagswahl"),
    dcc.Dropdown(id="years", options=[]),
    ])
@app.callback(
    Output("years", "options"),
    Input("election", "value")
)
def update_years(election):
    print(election)
    return df[(df["Wahl"] == election)]["Jahr"].unique()

fig = plot.chloropleth(df, "Bundestagswahl", 2021, "GRÜNE (Zweitstimmen)", './data/geodata.json')

if __name__ == '__main__':
    app.run_server(debug=False, port=8002)