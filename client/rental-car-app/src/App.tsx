import './App.css';
import { UserProvider } from './UserContext';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import HomePage from './pages/HomePage';
import LoginPage from './pages/LoginPage';
import RegisterPage from './pages/RegisterPage';
import DashboardPage from './pages/Dashboard';
import { PathUserLogin, PathUserRegister, PathUserDashboad } from './Config';

function App() {
  return (
    <UserProvider>
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path={PathUserLogin} element={<LoginPage />} />
          <Route path={PathUserRegister} element={<RegisterPage />} />
          <Route path={PathUserDashboad} element={<DashboardPage />} />
        </Routes>
      </BrowserRouter>
    </UserProvider>
  );
}

export default App
