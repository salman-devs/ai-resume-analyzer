import { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import api from "../api/axios";

export default function History() {
  const [history, setHistory] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    api.get("/analysis/").then(res => {
      setHistory(res.data);
      setLoading(false);
    });
  }, []);

  const handleDelete = async (id) => {
    await api.delete(`/analysis/${id}`);
    setHistory(history.filter(a => a.id !== id));
  };

  if (loading) return <div style={styles.loading}>Loading...</div>;

  return (
    <div style={styles.container}>
      <h1 style={styles.title}>Analysis History</h1>
      {history.length === 0 ? (
        <p style={styles.empty}>No analyses yet. <Link to="/analyze">Start analyzing</Link></p>
      ) : (
        history.map(a => (
          <div key={a.id} style={styles.item}>
            <div style={styles.itemInfo}>
              <p style={styles.filename}>{a.filename}</p>
              <p style={styles.jd}>{a.job_description.substring(0, 80)}...</p>
              <p style={styles.date}>{new Date(a.created_at).toLocaleString()}</p>
            </div>
            <div style={styles.itemActions}>
              <span style={getScoreStyle(a.ats_score)}>{a.ats_score}%</span>
              <button onClick={() => handleDelete(a.id)} style={styles.deleteBtn}>Delete</button>
            </div>
          </div>
        ))
      )}
    </div>
  );
}

function getScoreStyle(score) {
  const color = score >= 70 ? "#a6e3a1" : score >= 50 ? "#f9e2af" : "#f38ba8";
  return { color, fontWeight: "bold", fontSize: "1.3rem" };
}

const styles = {
  container: { maxWidth: "900px", margin: "2rem auto", padding: "0 1rem" },
  title: { color: "white", fontSize: "1.8rem", marginBottom: "1.5rem" },
  item: { background: "#313244", borderRadius: "12px", padding: "1.25rem", marginBottom: "1rem", display: "flex", justifyContent: "space-between", alignItems: "center" },
  itemInfo: { flex: 1 },
  filename: { color: "white", fontWeight: "bold", margin: "0 0 0.25rem" },
  jd: { color: "#9399b2", fontSize: "0.85rem", margin: "0 0 0.25rem" },
  date: { color: "#6c7086", fontSize: "0.8rem", margin: 0 },
  itemActions: { display: "flex", flexDirection: "column", alignItems: "center", gap: "0.5rem" },
  deleteBtn: { background: "#f38ba820", color: "#f38ba8", border: "none", padding: "0.3rem 0.75rem", borderRadius: "6px", cursor: "pointer" },
  empty: { color: "#9399b2" },
  loading: { color: "white", textAlign: "center", marginTop: "5rem" },
};