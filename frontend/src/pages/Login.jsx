import { useState } from "react";
import { useNavigate } from "react-router-dom";
import "../App.css";

export default function Login() {
  const navigate = useNavigate();
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [showPassword, setShowPassword] = useState(false);

  const handleLogin = async () => {
  try {
    const res = await fetch("/login", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ username, password }),
    });

    if (!res.ok) {
      throw new Error("Invalid credentials");
    }

    const data = await res.json();

    localStorage.setItem("token", data.access_token);
    // localStorage.setItem("username", JSON.stringify(res.data.username));

    navigate("/dashboard");
  } catch (err) {
    alert("Invalid username or password");
  }
};

  const handleClick = () => {
    navigate("/auth/login");   // open admin page
  };

  return (
    <div className="login-page">
    <div className="profile-container">
      <div className="profile-icon" onClick={handleClick}>
        👤
      </div>
      <h2>Admin</h2>
    </div>

    
      <div className="login-card">
        <div className="icon">👤</div>
        <h2>Welcome to Teacher Support AI</h2>
        <p className="subtitle">Login to your account</p>

        <label>Username</label>
        <input
          value={username}
          onChange={(e) => setUsername(e.target.value)}
          placeholder="Enter your username"
        />

            <label>Password</label>
            <div className="password-wrapper">
              <input
                type={showPassword ? "text" : "password"}
                placeholder="Enter your password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
              />

              <span
                className="eye-icon"
                onMouseDown={(e) => e.preventDefault()}
                onClick={() => setShowPassword(!showPassword)}
              >
                {showPassword ? "🙈" : "👁"}
              </span>
            </div>
        <button onClick={handleLogin}>Login</button>
      </div>
    </div>
  );
}
