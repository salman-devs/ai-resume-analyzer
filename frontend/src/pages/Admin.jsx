import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import api from "../api/axios";

export default function Admin() {
  const [stats, setStats] = useState(null);
  const [users, setUsers] = useState([]);
  const [analyses, setAnalyses] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [activeTab, setActiveTab] = useState("overview");
  const navigate = useNavigate();

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [statsRes, usersRes, analysesRes] = await Promise.all([
          api.get("/admin/stats"),
          api.get("/admin/users"),
          api.get("/admin/analyses"),
        ]);
        setStats(statsRes.data);
        setUsers(usersRes.data);
        setAnalyses(analysesRes.data);
      } catch (err) {
        if (err.response?.status === 403) {
          setError("You don't have admin access.");
        } else {
          setError("Failed to load admin data.");
        }
      } finally {
        setLoading(false);
      }
    };
    fetchData();
  }, []);

  const styles = {
    container: {
      minHeight: "100vh",
      backgroundColor: "#0f1117",
      color: "#e2e8f0",
      padding: "2rem",
    },
    inner: { maxWidth: "1100px", margin: "0 auto" },
    heading: { fontSize: "2rem", fontWeight: "bold", marginBottom: "0.5rem" },
    subheading: { color: "#94a3b8", marginBottom: "2rem" },
    statsGrid: {
      display: "grid",
      gridTemplateColumns: "repeat(auto-fit, minmax(200px, 1fr))",
      gap: "1rem",
      marginBottom: "2rem",
    },
    statCard: {
      backgroundColor: "#1e2130",
      borderRadius: "12px",
      padding: "1.5rem",
      border: "1px solid #2d3748",
      textAlign: "center",
    },
    statValue: {
      fontSize: "2.5rem",
      fontWeight: "bold",
      color: "#6366f1",
      marginBottom: "0.25rem",
    },
    statLabel: { color: "#94a3b8", fontSize: "14px" },
    tabs: {
      display: "flex",
      gap: "1rem",
      marginBottom: "1.5rem",
      borderBottom: "1px solid #2d3748",
      paddingBottom: "1rem",
    },
    tab: (active) => ({
      padding: "0.5rem 1.25rem",
      borderRadius: "8px",
      border: "none",
      backgroundColor: active ? "#6366f1" : "transparent",
      color: active ? "white" : "#94a3b8",
      fontWeight: "600",
      cursor: "pointer",
      fontSize: "14px",
    }),
    table: {
      width: "100%",
      borderCollapse: "collapse",
      backgroundColor: "#1e2130",
      borderRadius: "12px",
      overflow: "hidden",
    },
    th: {
      padding: "1rem",
      textAlign: "left",
      backgroundColor: "#16182a",
      color: "#94a3b8",
      fontSize: "13px",
      fontWeight: "600",
      borderBottom: "1px solid #2d3748",
    },
    td: {
      padding: "1rem",
      fontSize: "14px",
      borderBottom: "1px solid #1a1d2e",
      color: "#e2e8f0",
    },
    badge: (value) => ({
      padding: "0.2rem 0.6rem",
      borderRadius: "4px",
      fontSize: "12px",
      fontWeight: "600",
      backgroundColor: value ? "#1D9E7522" : "#E24B4A22",
      color: value ? "#1D9E75" : "#E24B4A",
    }),
    error: {
      backgroundColor: "#2d1515",
      border: "1px solid #E24B4A",
      borderRadius: "8px",
      padding: "1.5rem",
      color: "#fc8181",
      textAlign: "center",
    },
    loading: {
      textAlign: "center",
      padding: "3rem",
      color: "#94a3b8",
    },
  };

  if (loading) return <div style={styles.container}><div style={styles.loading}>Loading admin data...</div></div>;
  if (error) return <div style={styles.container}><div style={styles.inner}><div style={styles.error}>{error}</div></div></div>;

  return (
    <div style={styles.container}>
      <div style={styles.inner}>
        <h1 style={styles.heading}>Admin Dashboard</h1>
        <p style={styles.subheading}>Platform overview and user management</p>

        {/* stat cards */}
        <div style={styles.statsGrid}>
          <div style={styles.statCard}>
            <div style={styles.statValue}>{stats.total_users}</div>
            <div style={styles.statLabel}>Total Users</div>
          </div>
          <div style={styles.statCard}>
            <div style={styles.statValue}>{stats.total_analyses}</div>
            <div style={styles.statLabel}>Total Analyses</div>
          </div>
          <div style={styles.statCard}>
            <div style={styles.statValue}>{stats.avg_score}%</div>
            <div style={styles.statLabel}>Average ATS Score</div>
          </div>
          <div style={styles.statCard}>
            <div style={styles.statValue}>{stats.top_score}%</div>
            <div style={styles.statLabel}>Top Score</div>
          </div>
        </div>

        {/* tabs */}
        <div style={styles.tabs}>
          <button style={styles.tab(activeTab === "overview")} onClick={() => setActiveTab("overview")}>Users</button>
          <button style={styles.tab(activeTab === "analyses")} onClick={() => setActiveTab("analyses")}>Recent Analyses</button>
        </div>

        {/* users table */}
        {activeTab === "overview" && (
          <table style={styles.table}>
            <thead>
              <tr>
                <th style={styles.th}>ID</th>
                <th style={styles.th}>Username</th>
                <th style={styles.th}>Email</th>
                <th style={styles.th}>Analyses</th>
                <th style={styles.th}>Admin</th>
                <th style={styles.th}>Active</th>
                <th style={styles.th}>Joined</th>
              </tr>
            </thead>
            <tbody>
              {users.map((u) => (
                <tr key={u.id}>
                  <td style={styles.td}>{u.id}</td>
                  <td style={styles.td}>{u.username}</td>
                  <td style={styles.td}>{u.email}</td>
                  <td style={styles.td}>{u.total_analyses}</td>
                  <td style={styles.td}><span style={styles.badge(u.is_admin)}>{u.is_admin ? "Yes" : "No"}</span></td>
                  <td style={styles.td}><span style={styles.badge(u.is_active)}>{u.is_active ? "Yes" : "No"}</span></td>
                  <td style={styles.td}>{u.created_at ? new Date(u.created_at).toLocaleDateString() : "—"}</td>
                </tr>
              ))}
            </tbody>
          </table>
        )}

        {/* analyses table */}
        {activeTab === "analyses" && (
          <table style={styles.table}>
            <thead>
              <tr>
                <th style={styles.th}>ID</th>
                <th style={styles.th}>Filename</th>
                <th style={styles.th}>ATS Score</th>
                <th style={styles.th}>User ID</th>
                <th style={styles.th}>Date</th>
              </tr>
            </thead>
            <tbody>
              {analyses.map((a) => (
                <tr key={a.id}>
                  <td style={styles.td}>{a.id}</td>
                  <td style={styles.td}>{a.filename}</td>
                  <td style={styles.td}>
                    <span style={{
                      color: a.ats_score >= 70 ? "#1D9E75" : a.ats_score >= 50 ? "#EF9F27" : "#E24B4A",
                      fontWeight: "600",
                    }}>
                      {a.ats_score}%
                    </span>
                  </td>
                  <td style={styles.td}>{a.user_id}</td>
                  <td style={styles.td}>{a.created_at ? new Date(a.created_at).toLocaleDateString() : "—"}</td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>
    </div>
  );
}