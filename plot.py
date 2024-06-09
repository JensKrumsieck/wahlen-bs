import pandas as pd;
import plotly.graph_objects as go;
import plotly.express as px
import json;


def chloropleth(df: pd.DataFrame, targetElection:str, targetYear: int, measure:str, geojson: str) -> go.Figure:
    with open(geojson) as response:
        bezirke = json.load(response)

    df = df[(df["Wahl"] == targetElection) & (df["Jahr"] == targetYear) & (df["Messung"] == measure)]

    fig = px.choropleth(df, geojson=bezirke, color="Wert",
                        locations="StadtbezirkeId", featureidkey="properties.BEZNUM",
                        projection="mercator", color_continuous_scale=px.colors.sequential.speed,
                        hover_data=["Stadtbezirke", "Messung", "Wert"], title=f"{measure} in {targetYear} ({targetElection})", labels={"Wert": measure})
    fig.update_geos(fitbounds="locations", visible=False)
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    return fig