import { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import api from "../api/axios";

export default function Dashboard() {
  const [stats, setStats] = useState(null);
  const [history, setHistory] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [statsRes, historyRes] = await Promise.all([
          api.get("/analysis/stats"),
          api.get("/analysis/"),
        ]);
        setStats(statsRes.data);
        setHistory(historyRes.data.slice(0, 5));
      } catch (err) {
        console.error(err);
      } finally {
        setLoading(false);
      }
    };
    fetchData();
  }, []);

  if (loading) return <div style={styles.loading}>Loading...</div>;

  return (
    <div style={styles.container}>
      <h1 style={styles.title}>Dashboard</h1>

      <div style={styles.statsGrid}>
        <div style={styles.statCard}>
          <p style={styles.statNum}>{stats?.total || 0}</p>
          <p style={styles.statLabel}>Total Analyses</p>
        </div>
        <div style={styles.statCard}>
          <p style={styles.statNum}>{stats?.avg_score || 0}%</p>
          <p style={styles.statLabel}>Average Score</p>
        </div>
        <div style={styles.statCard}>
          <p style={styles.statNum}>{stats?.best_score || 0}%</p>
          <p style={styles.statLabel}>Best Score</p>
        </div>
        <div style={styles.statCard}>
          <p style={styles.statNum}>{stats?.latest_score || 0}%</p>
          <p style={styles.statLabel}>Latest Score</p>
        </div>
      </div>

      <div style={styles.section}>
        <div style={styles.sectionHeader}>
          <h2 style={styles.sectionTitle}>Recent Analyses</h2>
          <Link to="/analyze" style={styles.analyzeBtn}>+ New Analysis</Link>
        </div>
        {history.length === 0 ? (
          <p style={styles.empty}>No analyses yet. <Link to="/analyze">Upload your first resume</Link></p>
        ) : (
          history.map(a => (
            <Link to={`/history/${a.id}`} key={a.id} style={styles.historyItem}>
              <span style={styles.filename}>{a.filename}</span>
              <span style={getScoreStyle(a.ats_score)}>{a.ats_score}%</span>
              <span style={styles.date}>{new Date(a.created_at).toLocaleDateString()}</span>
            </Link>
          ))
        )}
      </div>
    </div>
  );
}

function getScoreStyle(score) {
  const color = score >= 70 ? "#a6e3a1" : score >= 50 ? "#f9e2af" : "#f38ba8";
  return { color, fontWeight: "bold", minWidth: "50px", textAlign: "center" };
}

const styles = {
  container: { maxWidth: "900px", margin: "2rem auto", padding: "0 1rem" },
  title: { color: "white", fontSize: "1.8rem", marginBottom: "1.5rem" },
  statsGrid: { display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(180px, 1fr))", gap: "1rem", marginBottom: "2rem" },
  statCard: { background: "#313244", padding: "1.5rem", borderRadius: "12px", textAlign: "center" },
  statNum: { color: "#89b4fa", fontSize: "2rem", fontWeight: "bold", margin: "0 0 0.25rem" },
  statLabel: { color: "#9399b2", margin: 0 },
  section: { background: "#313244", borderRadius: "12px", padding: "1.5rem" },
  sectionHeader: { display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: "1rem" },
  sectionTitle: { color: "white", margin: 0 },
  analyzeBtn: { background: "#89b4fa", color: "#1e1e2e", padding: "0.4rem 1rem", borderRadius: "6px", textDecoration: "none", fontWeight: "bold" },
  historyItem: { display: "flex", justifyContent: "space-between", alignItems: "center", padding: "0.75rem", borderRadius: "8px", marginBottom: "0.5rem", background: "#1e1e2e", textDecoration: "none", color: "white" },
  filename: { flex: 1, color: "#cdd6f4" },
  date: { color: "#6c7086", fontSize: "0.85rem" },
  empty: { color: "#9399b2" },
  loading: { color: "white", textAlign: "center", marginTop: "5rem" },
};