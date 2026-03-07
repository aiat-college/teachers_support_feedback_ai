import { useNavigate, NavLink } from "react-router-dom";
import { useEffect } from "react";
import {
  FaTachometerAlt,
  FaBook,
  FaClipboardCheck,
  FaChartLine,
  FaSignOutAlt,
} from "react-icons/fa";
import "../App.css";

export default function Dashboard() {
  const navigate = useNavigate(); // ✅ Declare first
  const token = localStorage.getItem("token");
  const username = localStorage.getItem("username") || "Teacher";

  // ✅ Check login & fetch data
  useEffect(() => {
    if (!token) {
      navigate("/");
      return;
    }

    fetch("http://127.0.0.1:8000/dashboard", {
      headers: {
        Authorization: `Bearer ${token}`, // ✅ Fixed
      },
    })
      .then((res) => res.json())
      .then((data) => {
        console.log("Dashboard Data:", data);
      })
      .catch((err) => {
        console.error("Error:", err);
      });
  }, [token, navigate]);

  return (
    <div className="dashboard-page">
      {/* ================= SIDEBAR ================= */}
      <aside className="sidebar">
        <div className="logo">TeachAI</div>

        <nav>
          <NavLink
            to="/dashboard"
            className={({ isActive }) => (isActive ? "active" : "")}
          >
            <FaTachometerAlt className="nav-icon" />
            Dashboard
          </NavLink>

          <NavLink
            to="/lesson-planner"
            className={({ isActive }) => (isActive ? "active" : "")}
          >
            <FaBook className="nav-icon" />
            Lesson Planner
          </NavLink>

          <NavLink
            to="/homework"
            className={({ isActive }) => (isActive ? "active" : "")}
          >
            <FaClipboardCheck className="nav-icon" />
            Homework Analysis
          </NavLink>

          <NavLink
            to="/student-progress"
            className={({ isActive }) => (isActive ? "active" : "")}
          >
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
          <h2>Welcome, {username}</h2>
          <div className="profile">👤</div>
        </div>

        {/* ================= CONTENT ================= */}
        <div>
          <div className="section">
            <div className="section-title">BIAT</div>

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
