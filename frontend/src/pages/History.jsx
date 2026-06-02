import { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import api from "../api/axios";

export default function History() {
  const [history, setHistory] = useState([]);
  const [loading, setLoading] = useState(true);
  const [deleteError, setDeleteError] = useState("");

  useEffect(() => {
    api.get("/analysis/")
      .then(res => setHistory(res.data))
      .catch(err => console.error("Failed to load history:", err))
      .finally(() => setLoading(false));
  }, []);

  const handleDelete = async (id, e) => {
    e.preventDefault();
    setDeleteError("");
    try {
      await api.delete(`/analysis/${id}`);
      setHistory(prev => prev.filter(a => a.id !== id));
    } catch (err) {
      setDeleteError("Failed to delete analysis. Please try again.");
    }
  };

  const getScoreStyle = (score) => ({
    color: score >= 70 ? "#a6e3a1" : score >= 40 ? "#f9e2af" : "#f38ba8",
    fontWeight: "bold",
    fontSize: "1.2rem",
    textDecoration: "none",
  });

  if (loading) return <div style={styles.loading}>Loading...</div>;

  return (
    <div style={styles.container}>
      <h1 style={styles.title}>Analysis History</h1>
      {deleteError && <p style={styles.deleteError}>{deleteError}</p>}
      {history.length === 0 ? (
        <p style={styles.empty}>No analyses yet. <Link to="/analyze">Start analyzing</Link></p>
      ) : (
        history.map(a => (
          <div key={a.id} style={styles.item}>
            <Link to={`/history/${a.id}`} style={styles.itemLink}>
              <div style={styles.itemInfo}>
                <p style={styles.filename}>{a.filename}</p>
                <p style={styles.jd}>{(a.job_description || "").substring(0, 80)}...</p>
                <p style={styles.date}>{new Date(a.created_at).toLocaleString()}</p>
              </div>
              <div style={styles.itemScore}>
                <span style={getScoreStyle(a.ats_score)}>{a.ats_score}%</span>
              </div>
            </Link>
            <button onClick={(e) => handleDelete(a.id, e)} style={styles.deleteBtn}>Delete</button>
          </div>
        ))
      )}
    </div>
  );
}

const styles = {
  container: { maxWidth: "900px", margin: "2rem auto", padding: "0 1rem" },
  title: { color: "white", fontSize: "1.8rem", marginBottom: "1.5rem" },
  deleteError: { background: "#f38ba820", color: "#f38ba8", padding: "0.75rem", borderRadius: "6px", marginBottom: "1rem" },
  loading: { color: "white", textAlign: "center", marginTop: "5rem" },
  empty: { color: "#9399b2" },
  item: {
    display: "flex", alignItems: "center",
    background: "#313244", padding: "1.25rem 1.5rem", borderRadius: "10px", marginBottom: "1rem",
  },
  itemLink: { display: "flex", flex: 1, alignItems: "center", justifyContent: "space-between", textDecoration: "none" },
  itemInfo: { flex: 1 },
  itemScore: { marginRight: "1rem" },
  filename: { color: "white", fontWeight: "bold", margin: "0 0 0.25rem" },
  jd: { color: "#9399b2", fontSize: "0.85rem", margin: "0 0 0.25rem" },
  date: { color: "#6c7086", fontSize: "0.8rem", margin: 0 },
  deleteBtn: {
    background: "#f38ba820", color: "#f38ba8", border: "1px solid #f38ba8",
    padding: "0.3rem 0.75rem", borderRadius: "6px", cursor: "pointer", fontSize: "0.85rem",
  },
};