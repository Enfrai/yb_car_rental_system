import '../App.css';
import type React from 'react';
import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useUser, type User } from '../UserContext';
import { PathUserDashboad } from '../Config';
import {UserLoginUrl} from '../Config';
import API from '../API';
import LoadingModal from '../components/LoadingModel';
import Toast from '../components/Toast';

export default function LoginPage() {
  const [formData, setFormData] = useState({
    email: '',
    password: '',
  });

  const [apiStatus, setLoading] = useState({
    loading: false,
    title: 'Loading'
  });

  const [toast, showToast] = useState("")

  const navigate = useNavigate();
  const { user, setUser } = useUser();

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: value,
    }));
  };

  const handleSubmit = (e: React.SubmitEvent<HTMLFormElement>) => {
    e.preventDefault();
    console.log('login data:', formData);

    new API(
      UserLoginUrl, formData, 
      () => {
          console.log('logging...')
          setLoading({loading: true, title: 'Logging in...'})
      },
      (code: string, message: string, detail: string) => {
          console.log('error >> ', `${code} | ${message} | ${detail}`);
          setLoading({loading: false, title: "Loading"});
          showToast(detail);
      },
      (data: User) => {
          console.log("success >> ", data)
          setLoading({loading: false, title: "Loading"})

          setUser(data)

          navigate(PathUserDashboad);
      }
    ).post();
    
    navigate(PathUserDashboad);
  };

  return (
    <main id="center">
      <h2>User Login</h2>
      
      <form className="login-form" onSubmit={handleSubmit}>
        <div className="input-group">
          <label htmlFor="email">Email address</label>
          <input
            type="email"
            id="email"
            name="email"
            className="input-field"
            placeholder="name@example.com"
            value={formData.email}
            onChange={handleChange}
            required
          />
        </div>

        <div className="input-group">
          <label htmlFor="password">Password</label>
          <input
            type="password"
            id="password"
            name="password"
            className="input-field"
            placeholder="Please input password"
            value={formData.password}
            onChange={handleChange}
            required
          />
        </div>

        <button type="submit" className="btn-submit">
          Login
        </button>
      </form>
      
      <LoadingModal isOpen={apiStatus.loading}
        message={apiStatus.title}/>

      <Toast message={toast}
        onClose={() => { showToast("") }}/>
    </main>
  );
}