import '../App.css';
import type React from 'react';
import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
// import { useUser } from '../UserContext';
import {UserLoginUrl} from '../Config';
import API from '../API';

export default function LoginPage() {
  const [formData, setFormData] = useState({
    email: '',
    password: '',
  });

  const navigate = useNavigate();
//   const { user, setUser } = useUser();

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
    
    new API(UserLoginUrl, formData, () => {

    }, (code: string, message: string, detail: string) => {
        console.log(code, message, detail)
    }, (data: Map<string, Object>) => {
        console.log(data)
    }).post()

    // setUser({  })
    
    navigate('/dashboard');
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
    </main>
  );
}