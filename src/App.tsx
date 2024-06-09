import './index.css'
import Elections from './lib/Elections'

function App() {

  return (
    <>
      <header>
        <nav>
          <div className='container mx-auto px-4 flex justify-between py-5'>
            <div>
              <p className='text-5xl font-black italic tracking-tight'>Wahlanalyse</p>
              <p className='text-lg text-right font-bold text-green-900'>von <a href="https://jenskrumsieck.de" target='_blank'>Dr. Jens Krumsieck</a></p>
            </div>
          </div>
        </nav>
      </header>
      <article className='container mx-auto px-4 py-5'>
        <Elections />
        <p className="read-the-docs">
          Datenquellen:
          <ul>
            <li>
              Stadt Braunschweig - <a href="https://www.braunschweig.de/leben/stadtplanung_bauen/geoinformationen/ogd_stadtbezirke.php">Open GeoData</a>, 2024, Lizenz: <a href="https://www.govdata.de/dl-de/by-2-0">dl-de/by-2-0</a>.
            </li>
            <li>
              Stadt Braunschweig <a href="https://www.braunschweig.de/politik_verwaltung/fb_institutionen/fachbereiche_referate/fb01/ref0120/stadtforschung/index.php">Referat Stadtentwicklung, Statistik und Vorhabenplanung</a>.
            </li>
          </ul>
          Eigene Darstellung
        </p>
      </article>
    </>
  )
}


export default App
