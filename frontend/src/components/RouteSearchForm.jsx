import { useState } from 'react'

function RouteSearchForm() {
  const [start, setStart] = useState('')
  const [destination, setDestination] = useState('')

  function handleSubmit(event) {
    event.preventDefault()

    console.log({
      start,
      destination,
    })
  }

  return (
    <form className="route-form" onSubmit={handleSubmit}>
      <div className="input-group">
        <label htmlFor="start">Starting point</label>
        <input
          id="start"
          type="text"
          placeholder="San Marcos, TX"
          value={start}
          onChange={(event) => setStart(event.target.value)}
          required
        />
      </div>

      <div className="input-group">
        <label htmlFor="destination">Destination</label>
        <input
          id="destination"
          type="text"
          placeholder="Austin, TX"
          value={destination}
          onChange={(event) => setDestination(event.target.value)}
          required
        />
      </div>

      <button type="submit">Find routes</button>
    </form>
  )
}

export default RouteSearchForm