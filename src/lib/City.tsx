import { DSVRowString } from "d3";
import * as d3 from "d3";
import Plot from "react-plotly.js";

export default function City(props: { data: DSVRowString<string>[] | null }) {
}
/**return (
  <>
    <div className="block">
      <div>
        <p>Wahlergebnis</p>
      </div>
      <Plot className="w-auto h-96"
        data={[
          {
            type: 'bar',
            x: plotData?.map(d => d.Messung),
            y: plotData?.map(d => d.Wert),
          }
        ]}
        layout={
          {}
        } />
    </div>
  </>
)
}
*/