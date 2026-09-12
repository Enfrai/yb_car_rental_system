import '../App.css';
import { useNavigate } from 'react-router-dom';
import { useUser } from '../UserContext';
import { PathBookingCar, PathBookingHisgory } from '../Config';

function DashboardPage() {
    const navigate = useNavigate();
    const { user } = useUser();

    const handleBookingCar = () => {
        navigate(PathBookingCar);
    }

    const handleBookingHistory = () => {
        navigate(PathBookingHisgory);
    }

    console.log(`is_admin: ${user?.is_admin}, is_customer: ${user?.is_customer}`)

    var role = user?.is_customer ? 'Customer' : '';
    if (user?.is_admin) {
        if (role) {
            role += " & ";
        }
        role += 'Admin'
    }

    console.log(`role: ${role}`)

    return (
      <section id="center">
        <div style={{ margin: "0px 24px" }}>
          <h1>Hello {user?.username}, Role: {role}</h1>
        </div>
        <button
          style={{
            width: "180px",
            justifyContent: "center",
            alignItems: "center",
            marginTop: "124px",
          }}
          type="button"
          className="counter"
          onClick={handleBookingCar}
        >
          Book a car
        </button>
        <button
          style={{
            width: "180px",
            justifyContent: "center",
            alignItems: "center",
          }}
          type="button"
          className="counter"
          onClick={handleBookingHistory}
        >
          Booking history
        </button>
      </section>
    );
}

export default DashboardPage