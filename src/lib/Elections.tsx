import { useEffect, useState } from 'react'
import * as d3 from 'd3';
import Choropleth from './Choropleth';

export default function Elections() {
    const [data, setData] = useState<d3.DSVRowArray | null>(null)
    const [election, setElection] = useState<string | null>(null)
    const [year, setYear] = useState<number | null>(null)

    const [validElections, setValidElections] = useState<string[] | null>(null)
    const [validYears, setValidYears] = useState<Number[] | null>(null)

    const [currentData, setCurrentData] = useState<d3.DSVRowString[] | null>(null)

    var dataUrl = new URL('../../data/districts.csv', import.meta.url).href;
    useEffect(() => {
        d3.csv(dataUrl).then(df => {
            setData(df)
            setValidElections([...new Set(df.map(d => d.Wahl))])
            setElection(df[0].Wahl)
        })
    }, []);
    useEffect(() => {
        setValidYears([...new Set(data?.filter(d => d.Wahl == election).map(d => Number(d.Jahr)))])
        setYear(Number(data?.filter(d => d.Wahl == election)[0].Jahr))
    }, [election]);

    useEffect(() => {
        if (!data) return
        setCurrentData(data?.filter(d => d.Wahl == election && Number(d.Jahr) == year))
    }, [data, year, election]);

    return (
        <>
            {!data
                ? <p>Lese Daten...</p>
                : <>
                    <div>Ergebnisse der {election} {year}</div>
                    {!validElections || !validYears
                        ? <p>Lese Daten...</p>
                        : <>
                            <select title="Wahl auswählen" value={String(election)} onChange={(e) => setElection(e.target.value)}>
                                {validElections.map(d => <option key={d} value={d}>{d}</option>)}
                            </select>

                            <select title="Jahr auswählen" value={String(year)} onChange={(e) => setYear(Number(e.target.value))}>
                                {validYears.map(d => <option key={String(d)} value={String(d)}>{String(d)}</option>)}
                            </select>
                            <Choropleth data={currentData} />
                        </>
                    }
                </>
            }
        </>
    )
}
