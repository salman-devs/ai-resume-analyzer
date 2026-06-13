import { Link, useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";

export default function Navbar() {
  const { isAuthenticated, logout, user } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate("/login");
  };

  return (
    <nav style={styles.nav}>
      <Link to="/" style={styles.brand}>ResumeAI</Link>
      {isAuthenticated && (
        <div style={styles.links}>
          <Link to="/dashboard" style={styles.link}>Dashboard</Link>
          <Link to="/analyze" style={styles.link}>Analyze</Link>
          <Link to="/history" style={styles.link}>History</Link>
          <Link to="/jobs" style={styles.link}>Find Jobs</Link>
          {user && <span style={styles.username}>👤 {user.username}</span>}
          <button onClick={handleLogout} style={styles.btn}>Logout</button>
        </div>
      )}
    </nav>
  );
}

const styles = {
  nav: {
    display: "flex", justifyContent: "space-between", alignItems: "center",
    padding: "1rem 2rem", background: "#1e1e2e", color: "white",
  },
  brand: {
    color: "white", textDecoration: "none", fontSize: "1.3rem", fontWeight: "bold",
  },
  links: { display: "flex", gap: "1.5rem", alignItems: "center" },
  link: { color: "#cdd6f4", textDecoration: "none", fontSize: "0.95rem" },
  username: { color: "#a6e3a1", fontSize: "0.9rem" },
  btn: {
    background: "#f38ba8", color: "white", border: "none",
    padding: "0.4rem 1rem", borderRadius: "6px", cursor: "pointer",
  },
};