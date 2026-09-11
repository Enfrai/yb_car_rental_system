import { useState } from 'react'
import './App.css'

function App() {
  const handleLogin = () => {

  }

  const handleRegister = () => {

  }

  const [isLoggedIn, setIsLoggedIn] = useState(false)

  return (
      <section id="center">
        <div style={{ margin: '0px 24px' }}>
          <h1>Welcome to Automate Rental System</h1>
        </div>
        <button
          style={{ width: '180px', justifyContent: 'center', alignItems: 'center', marginTop: '124px' }}
          type="button"
          className="counter"
          onClick={handleLogin}
        >
          Login
        </button>
        <button
          style={{ width: '180px', justifyContent: 'center', alignItems: 'center' }}
          type="button"
          className="counter"
          onClick={handleRegister}
        >
          Register
        </button>
      </section>
  )
}

export default App
