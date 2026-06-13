import { useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import api from "../api/axios";

export default function Register() {
  const [form, setForm] = useState({ username: "", email: "", password: "" });
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError("");
    try {
      await api.post("/auth/register", form);
      navigate("/login");
    } catch (err) {
      const detail = err.response?.data?.detail;
      if (Array.isArray(detail)) {
        setError(detail.map(d => d.msg).join(", "));
      } else {
        setError(detail || "Registration failed");
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={styles.container}>
      <div style={styles.card}>
        <h2 style={styles.title}>Create account</h2>
        <p style={styles.sub}>Start analyzing your resume today</p>
        {error && <p style={styles.error}>{error}</p>}
        <form onSubmit={handleSubmit}>
          <input style={styles.input} type="text" placeholder="Username"
            value={form.username} onChange={e => setForm({ ...form, username: e.target.value })} required />
          <input style={styles.input} type="email" placeholder="Email"
            value={form.email} onChange={e => setForm({ ...form, email: e.target.value })} required />
          <input style={styles.input} type="password" placeholder="Password"
            value={form.password} onChange={e => setForm({ ...form, password: e.target.value })} required />
          <button style={styles.btn} type="submit" disabled={loading}>
            {loading ? "Creating account..." : "Create Account"}
          </button>
        </form>
        <p style={styles.footer}>
          Already have an account? <Link to="/login">Sign in</Link>
        </p>
      </div>
    </div>
  );
}

const styles = {
  container: { minHeight: "100vh", display: "flex", alignItems: "center", justifyContent: "center", background: "#1e1e2e" },
  card: { background: "#313244", padding: "2rem", borderRadius: "12px", width: "100%", maxWidth: "400px" },
  title: { color: "white", margin: "0 0 0.25rem", fontSize: "1.5rem" },
  sub: { color: "#9399b2", marginBottom: "1.5rem" },
  error: { background: "#f38ba820", color: "#f38ba8", padding: "0.75rem", borderRadius: "6px", marginBottom: "1rem" },
  input: { width: "100%", padding: "0.75rem", marginBottom: "1rem", borderRadius: "6px", border: "1px solid #45475a", background: "#1e1e2e", color: "white", fontSize: "0.95rem", boxSizing: "border-box" },
  btn: { width: "100%", padding: "0.75rem", background: "#89b4fa", color: "#1e1e2e", border: "none", borderRadius: "6px", fontWeight: "bold", cursor: "pointer", fontSize: "1rem" },
  footer: { color: "#9399b2", textAlign: "center", marginTop: "1rem" },
};