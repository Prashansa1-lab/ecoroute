import './App.css'
import RouteSearchForm from './components/RouteSearchForm'

function App() {
  return (
    <main className="app">
      <header className="header">
        <div className="brand">
          <span className="brand-mark">E</span>
          <span>EcoRoute</span>
        </div>
      </header>

      <section className="hero">
        <p className="eyebrow">SMARTER ROAD TRIPS</p>

        <h1>
          Find a better way
          <br />
          to get there.
        </h1>

        <p className="subtitle">
          Compare fast, eco-friendly, and scenic routes for your next trip.
        </p>

        <RouteSearchForm />
      </section>
    </main>
  )
}

export default App