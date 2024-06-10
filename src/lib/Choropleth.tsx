import { DSVRowString } from "d3";
import { useEffect, useState } from "react";
import Plot from "react-plotly.js";

export default function Choropleth(props: { data: DSVRowString<string>[] | null }) {
    const [measure, setMeasure] = useState<string | null>(null)
    const [plotData, setPlotData] = useState<DSVRowString<string>[] | null>(null)
    const [geoPath, setGeoPath] = useState<string>("");

    useEffect(() => {
        var measures = props.data?.map(d => d.Messung);
        if (!measures) return;
        var def = measures.find(d => d == "GRÜNE") || "GRÜNE (Zweitstimmen)";
        setMeasure(def)
    }, [props.data]);

    useEffect(() => {
        if (!props.data) return;
        var usedData = props.data.filter(d => d.Messung == measure);
        setGeoPath(usedData.length != 12 ? "geodata_old.json" : "geodata.json")
        setPlotData(usedData)
    }, [props.data, measure]);


    return (
        <>
            <div className="block">
                <div>
                    <p>Kartendarstellung {measure}</p>
                    <select title="Kartendarstellung auswählen" value={String(measure)} onChange={(e) => setMeasure(e.target.value)}>
                        {[...new Set(props.data?.map(d => d.Messung))]?.map(d => <option key={d} value={d}>{d}</option>)}
                    </select>
                </div>
                <Plot
                    className="w-auto h-96"
                    style={{display: "block"}}
                    data={[
                        {
                            type: 'choropleth',
                            locations: plotData?.map(d => d.StadtbezirkeId),
                            locationmode: 'geojson-id',
                            z: plotData?.map(d => d.Wert),
                            zmin: 0,
                            text: plotData?.map(d => d.Stadtbezirke),
                            //@ts-ignore
                            geojson: geoPath,
                            featureidkey: "properties.BEZNUM",
                            colorbar: {
                                title: `${measure}`,
                                thickness: 10,
                                ticksuffix: `${measure != "Wahlberechtigte" ? "%" : ""}`,
                            },
                            marker: {
                                line: {
                                    color: 'rgb(255,255,255)',
                                    width: 2
                                }
                            }
                        }
                    ]}
                    layout={
                        {
                            autosize: true,
                            geo: {
                                fitbounds: "geojson",
                                resolution: 50,
                                scope: 'europe',
                            },
                            margin: { l: 0, r: 0, t: 50, b: 0 },
                            title: `Kartendarstellung ${measure}`,
                        }
                    }
                    config={{ responsive: true }}
                    useResizeHandler
                />
            </div>
        </>
    )
}
