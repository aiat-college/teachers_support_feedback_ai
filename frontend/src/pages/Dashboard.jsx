import { useNavigate, NavLink } from "react-router-dom";
import { useEffect, useState } from "react";
import axios from "axios";
import {
  FaTachometerAlt,
  FaBook,
  FaClipboardCheck,
  FaChartLine,
  FaSignOutAlt,
} from "react-icons/fa";
import "../App.css";


export default function Dashboard() {

const navigate = useNavigate();

const [user, setUser] = useState({
username: "",
profile_image: ""
});

useEffect(() => {
  

const fetchUser = async () => {
  try {

    const token = localStorage.getItem("token");

    const res = await axios.get("http://localhost:8000/dashboard", {
      headers: {
        Authorization: `Bearer ${token}`
      }
    });

    setUser(res.data);

  } catch (error) {
    console.log(error);
  }
};

fetchUser();

}, []);

  return (
    <div className="dashboard-page">
      {/* ================= SIDEBAR ================= */}
      <aside className="sidebar">
        <div className="logo">TeachAI</div>

        <nav>
          <NavLink
            to="/dashboard">
            <FaTachometerAlt className="nav-icon" />
            Dashboard
          </NavLink>

          <NavLink
            to="/lesson-planner">
            <FaBook className="nav-icon" />
            Lesson Planner
          </NavLink>

          <NavLink
            to="/homework">
            <FaClipboardCheck className="nav-icon" />
            Homework Analysis
          </NavLink>

          <NavLink
            to="/student-progress">
            <FaChartLine className="nav-icon" />
            Student Progress
          </NavLink>
        </nav>

        <div
          className="logout"
          onClick={() => {
            localStorage.clear();
            navigate("/");
          }}
        >
          <FaSignOutAlt className="nav-icon" />
          Logout
        </div>
      </aside>

      {/* ================= MAIN ================= */}
      <main className="dashboard-main">
        <div className="dashboard-header">
          <h2>Welcome, {user.username}</h2>
          <div className="profile">
          {user.profile_image ? (
            <img
              src={`http://localhost:8000/${user.profile_image}`}
              alt="profile"
              style={{ width: "36px", height: "36px", borderRadius: "50%" }}
            />
          ) : (
            "👤"
          )}
        </div>
        </div>

        {/* ================= CONTENT ================= */}
        <div>
          {/* AIAT */}
          <div className="section">
            <div className="section-title">AIAT</div>

            <div className="grid">
              <div className="grid-card">
                <h4>1st Year</h4>
                <div className="actions">
                  <button
                    className="btn-light"
                    onClick={() => navigate("/write")}
                  >
                    Write
                  </button>
                    <button
                      type="button"
                      className="btn-primary"
                      onClick={() => navigate("/view")}
                    >
                      View
                    </button>
                </div>
              </div>

              <div className="grid-card">
                <h4>2nd Year</h4>
                <div className="actions">
                  <button
                    className="btn-light"
                    onClick={() => navigate("/write")}
                  >
                    Write
                  </button>
                  <button
                    className="btn-primary"
                    onClick={() => navigate("/view")}
                  >
                    View
                  </button>
                </div>
              </div>
            </div>
          </div>

          {/* UDAVI */}
          <div className="section">
            <div className="section-title">Udavi</div>

            <div className="grid">
              <div className="grid-card">
                <h4>11th Std</h4>
                <div className="actions">
                  <button
                    className="btn-light"
                    onClick={() => navigate("/write")}
                  >
                    Write
                  </button>
                  <button
                    className="btn-primary"
                    onClick={() => navigate("/view")}
                  >
                    View
                  </button>
                </div>
              </div>

              <div className="grid-card">
                <h4>5th Std</h4>
                <div className="actions">
                  <button
                    className="btn-light"
                    onClick={() => navigate("/write")}
                  >
                    Write
                  </button>
                  <button
                    className="btn-primary"
                    onClick={() => navigate("/view")}
                  >
                    View
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
}
