import './App.css';
import { UserProvider } from './UserContext';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import HomePage from './pages/HomePage';
import LoginPage from './pages/LoginPage';
import RegisterPage from './pages/RegisterPage';
import { PathUserLogin, PathUserRegister } from './Config';

function App() {
  return (
    <UserProvider>
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path={PathUserLogin} element={<LoginPage />} />
          <Route path={PathUserRegister} element={<RegisterPage />} />
        </Routes>
      </BrowserRouter>
    </UserProvider>
  );
}

export default App
