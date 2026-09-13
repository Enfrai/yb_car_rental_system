import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import { PathUserLogin, PathUserDashboad } from "../Config";
import "../App.css";
import API from "../API";
import { UserRegisterUrl } from "../Config";
import LoadingModal from "../components/LoadingModel";
import Toast from "../components/Toast";
import { useUser, type User } from "../UserContext";

export default function RegisterPage() {
  const navigate = useNavigate();
  const { setUser } = useUser();

  // Local state for the registration form inputs
  const [formData, setFormData] = useState({
    username: "",
    email: "",
    password: "",
    auto_login: true,
    role: "customer",
  });

  const [apiStatus, setLoading] = useState({
    loading: false,
    title: "Loading",
  });

  const [toast, showToast] = useState("");

  //   const navigate = useNavigate();

  // Handle value updates for all form controls
  const handleChange = (
    e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>,
  ) => {
    const { name, value } = e.target;

    console.log(`select ${name}: ${value}`);

    setFormData((prevData) => ({
      ...prevData,
      [name]: value,
    }));
  };

  // Handle form submission
  const handleSubmit = (e: React.SubmitEvent<HTMLFormElement>) => {
    e.preventDefault();
    console.log("Registration submitted:", formData);

    new API(
      UserRegisterUrl,
      formData,
      () => {
        console.log("registering...");
        setLoading({ loading: true, title: "Registering..." });
      },
      (code: string, message: string, detail: string) => {
        console.log("error >> ", `${code} | ${message} | ${detail}`);
        setLoading({ loading: false, title: "Loading" });
        showToast(detail);
      },
      (data: User) => {
        console.log("success >> ", data);
        setLoading({ loading: false, title: "Loading" });

        setUser(data);

        if (formData.auto_login) {
          navigate(PathUserDashboad);
        } else {
          navigate(PathUserLogin);
        }
      },
    ).post();
  };

  return (
    <main id="center">
      <h2>Create Account</h2>

      <form className="register-form" onSubmit={handleSubmit}>
        {/* Username Input */}
        <div className="input-group">
          <label htmlFor="username">Username</label>
          <input
            type="text"
            id="username"
            name="username"
            className="input-field"
            placeholder="Enter your username"
            value={formData.username}
            onChange={handleChange}
            required
          />
        </div>

        {/* Email Input */}
        <div className="input-group">
          <label htmlFor="email">Email Address</label>
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

        {/* Password Input */}
        <div className="input-group">
          <label htmlFor="password">Password</label>
          <input
            type="password"
            id="password"
            name="password"
            className="input-field"
            placeholder="Create a password"
            value={formData.password}
            onChange={handleChange}
            required
          />
        </div>

        {/* User Type Selection */}
        <div className="input-group">
          <label htmlFor="userType">User Type</label>
          <select
            id="userType"
            name="role"
            className="select-field"
            value={formData.role}
            onChange={handleChange}
            required
          >
            <option value="customer">Customer</option>
            <option value="admin">Admin</option>
          </select>
        </div>

        {/* Submit Button */}
        <button type="submit" className="btn-submit">
          Sign Up
        </button>
      </form>

      <LoadingModal isOpen={apiStatus.loading} message={apiStatus.title} />

      <Toast
        message={toast}
        onClose={() => {
          showToast("");
        }}
      />
    </main>
  );
}
