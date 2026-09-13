import type React from "react";
import { useState } from "react";
import "../App.css";
import API from "../API";
import { CarRegisterUrl } from "../Config";
import LoadingModal from "../components/LoadingModel";
import Toast from "../components/Toast";
import { useUser } from "../UserContext";

const initialFormData = {
  make: "",
  model: "",
  year: "",
  mileage: "",
  min_rent_period: "1",
  max_rent_period: "0",
};

function BookingRegisterCarPage() {
  const { user } = useUser();
  const [formData, setFormData] = useState(initialFormData);
  const [apiStatus, setLoading] = useState({
    loading: false,
    title: "Loading",
  });
  const [toast, showToast] = useState("");
  const [toastType, setToastType] = useState<"success" | "error">("success");

  const resetForm = () => {
    setFormData(initialFormData);
  };

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setFormData((previousData) => ({
      ...previousData,
      [name]: value,
    }));
  };

  const handleSubmit = (e: React.SubmitEvent<HTMLFormElement>) => {
    e.preventDefault();

    const requestData = {
      ...formData,
      user_id: user?.user_id ?? "",
      year: Number(formData.year),
      mileage: Number(formData.mileage),
      min_rent_period: Number(formData.min_rent_period),
      max_rent_period: Number(formData.max_rent_period),
      rent_status: "available",
    };

    new API(
      CarRegisterUrl,
      requestData,
      () => {
        setLoading({ loading: true, title: "Registering car..." });
      },
      () => {
        setLoading({ loading: false, title: "Loading" });
        setToastType("error");
        showToast("Register Failed");
        resetForm();
      },
      () => {
        setLoading({ loading: false, title: "Loading" });
        setToastType("success");
        showToast("Register Success");
        resetForm();
      },
    ).post();
  };

  return (
    <main id="center">
      <h2>Register a Car</h2>

      <form className="login-form" onSubmit={handleSubmit}>
        <div className="input-group">
          <label htmlFor="make">Make</label>
          <input
            type="text"
            id="make"
            name="make"
            className="input-field"
            placeholder="Enter car make"
            value={formData.make}
            onChange={handleChange}
            required
          />
        </div>

        <div className="input-group">
          <label htmlFor="model">Model</label>
          <input
            type="text"
            id="model"
            name="model"
            className="input-field"
            placeholder="Enter car model"
            value={formData.model}
            onChange={handleChange}
            required
          />
        </div>

        <div className="input-group">
          <label htmlFor="year">Year</label>
          <input
            type="number"
            id="year"
            name="year"
            className="input-field"
            placeholder="Enter manufacture year"
            value={formData.year}
            onChange={handleChange}
            required
          />
        </div>

        <div className="input-group">
          <label htmlFor="mileage">Mileage</label>
          <input
            type="number"
            id="mileage"
            name="mileage"
            className="input-field"
            placeholder="Enter mileage"
            value={formData.mileage}
            onChange={handleChange}
            required
          />
        </div>

        <div className="input-group">
          <label htmlFor="min_rent_period">Minimum rental period (days)</label>
          <input
            type="number"
            id="min_rent_period"
            name="min_rent_period"
            className="input-field"
            placeholder="Enter minimum rental period"
            value={formData.min_rent_period}
            onChange={handleChange}
            min="1"
          />
        </div>

        <div className="input-group">
          <label htmlFor="max_rent_period">Maximum rental period (days)</label>
          <input
            type="number"
            id="max_rent_period"
            name="max_rent_period"
            className="input-field"
            placeholder="Enter maximum rental period"
            value={formData.max_rent_period}
            onChange={handleChange}
            min="0"
          />
        </div>

        <button type="submit" className="btn-submit">
          Register Car
        </button>
      </form>

      <LoadingModal isOpen={apiStatus.loading} message={apiStatus.title} />
      <Toast message={toast} type={toastType} onClose={() => showToast("")} />
    </main>
  );
}

export default BookingRegisterCarPage;
