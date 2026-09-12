import './App.css';
import { UserProvider } from './UserContext';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import HomePage from './pages/HomePage';
import LoginPage from './pages/LoginPage';
import RegisterPage from './pages/RegisterPage';
import DashboardPage from './pages/DashboardPage';
import BookingCarPage from './pages/BookingCarPage';
import BookingConfirmPage from './pages/BookingConfirmPage';
import BookingHistoryPage from './pages/BookingHistoryPage';
import BookingRegisterCarPage from './pages/BookingRegisterCarPage';
import { PathUserLogin, PathUserRegister, PathUserDashboad, PathBookingCar, PathBookingConfirm, PathBookingHisgory, PathCarRegister, PathCarSearch } from './Config';

function App() {
  return (
    <UserProvider>
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path={PathUserLogin} element={<LoginPage />} />
          <Route path={PathUserRegister} element={<RegisterPage />} />
          <Route path={PathUserDashboad} element={<DashboardPage />} />
          <Route path={PathCarRegister} element={<BookingRegisterCarPage />} />
          <Route path={PathBookingHisgory} element={<BookingHistoryPage />} />
          <Route path={PathBookingConfirm} element={<BookingConfirmPage />} />
          <Route path={PathBookingCar} element={<BookingCarPage />} />
          <Route path={PathCarSearch} element={<DashboardPage />} />
        </Routes>
      </BrowserRouter>
    </UserProvider>
  );
}

export default App
