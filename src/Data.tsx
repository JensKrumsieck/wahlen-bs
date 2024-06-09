import { useEffect, useState } from 'react';
import Plot from 'react-plotly.js';
import * as d3 from 'd3';

export default function Data() {
    const [data, setData] = useState<d3.DSVRowArray | null>(null)
    const [validElections, setValidElections] = useState<string[] | null>(null)
    const [validYears, setValidYears] = useState<number[] | null>(null)
    const [validMeasures, setValidMeasures] = useState<string[] | null>(null)
    const [election, setElection] = useState<string | null>(null)
    const [measure, setMeasure] = useState<string | null>(null)
    const [year, setYear] = useState<number | null>(null)
    const [plotData, setPlotData] = useState<d3.DSVRowString[] | undefined | null>(null)
    const [geoPath, setGeoPath] = useState<string>("../data/geodata.json");
    var dataUrl = new URL('../data/districts.csv', import.meta.url).href;
    useEffect(() => {
        d3.csv(dataUrl).then(df => {
            setData(df);
        }).catch((error) => {
            console.error('Error:', error);
        });
    }, []);

    useEffect(() => {
        var elections = data?.map(d => d.Wahl);
        if (!elections) return;
        setValidElections([...new Set(elections)]);
        setCurrentElection(elections[0]);
    }, [data]);

    useEffect(() => {
        var years = data?.filter(d => d.Wahl == election).map(d => Number(d.Jahr));
        if (!years) return;
        setValidYears([...new Set(years)]);
        setCurrentYear(years[0]);
    }, [election]);

    useEffect(() => {
        var measures = data?.filter(d => Number(d.Jahr) == year).map(d => d.Messung);
        if (!measures) return;
        setMeasure(measures[0])
    }, [year]);

    useEffect(() => {
        var plot = data?.filter(d => d.Wahl == election && Number(d.Jahr) == year && d.Messung == measure);
        setGeoPath(plot?.find(d => d.StadtbezirkeId == "331") ? "../data/geodata_old.json" : "../data/geodata.json");
        setPlotData(plot)
    }, [measure]);

    const setCurrentElection = (election: string) => {
        setElection(election);
        var years = data?.filter(d => d.Wahl == election).map(d => Number(d.Jahr));
        setValidYears([...new Set(years)]);
    }

    const setCurrentYear = (year: number) => {
        setYear(year);
        var measures = data?.filter(d => Number(d.Jahr) == year).map(d => d.Messung);
        setValidMeasures([...new Set(measures)]);
    }

    return (
        <>
            <select onChange={e => setCurrentElection(e.target.value)}>
                {validElections?.map(e => <option key={e} value={e}>{e}</option>)}
            </select>
            <select onChange={e => setCurrentYear(Number(e.target.value))}>
                {validYears?.map(e => <option key={e} value={e}>{e}</option>)}
            </select>
            <select onChange={e => setMeasure(e.target.value)}>
                {validMeasures?.map(e => <option key={e} value={e}>{e}</option>)}
            </select>
            <div>
                <Plot
                    data={[
                        {
                            type: 'choropleth',
                            locations: plotData?.map(d => d.StadtbezirkeId),
                            locationmode: 'geojson-id',
                            z: plotData?.map(d => d.Wert),
                            text: plotData?.map(d => d.Stadtbezirke),
                            //@ts-ignore
                            geojson: geoPath,
                            featureidkey: "properties.BEZNUM"
                        }
                    ]}
                    layout={
                        {
                            geo: {
                                fitbounds: "geojson",
                                resolution: 50,
                                scope: 'europe',
                                showframe: false,
                            }
                        }
                    }
                    config={
                        {
                            responsive: true,
                        }
                    }
                    useResizeHandler={true}
                    className={"w-full"} />
            </div>
        </>
    )

}

