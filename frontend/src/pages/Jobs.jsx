import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import api from "../api/axios";

export default function Jobs() {
  const [title, setTitle] = useState("");
  const [autoTitle, setAutoTitle] = useState("");
  const [location, setLocation] = useState("india");
  const [jobs, setJobs] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [searched, setSearched] = useState(false);
  const navigate = useNavigate();

  const handleSearch = async () => {
    setLoading(true);
    setError("");
    setJobs([]);

    try {
      const params = { location };
      if (title.trim()) params.title = title;

      const res = await api.get("/jobs/search", { params });
      setJobs(res.data.jobs);
      setAutoTitle(res.data.searched_title);
      setSearched(true);
    } catch (err) {
      if (err.response?.status === 400) {
        setError(err.response.data.detail);
      } else if (err.response?.status === 404) {
        setSearched(true);
        setJobs([]);
      } else {
        setError("Something went wrong. Please try again.");
      }
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    handleSearch();
  }, []);

  const getScoreColor = (score) => {
    if (score >= 70) return "#1D9E75";
    if (score >= 50) return "#EF9F27";
    return "#E24B4A";
  };

  const getScoreLabel = (score) => {
    if (score >= 70) return "Strong Match";
    if (score >= 50) return "Moderate Match";
    return "Weak Match";
  };

  const styles = {
    container: {
      minHeight: "100vh",
      backgroundColor: "#0f1117",
      color: "#e2e8f0",
      padding: "2rem",
    },
    inner: {
      maxWidth: "900px",
      margin: "0 auto",
    },
    heading: {
      fontSize: "2rem",
      fontWeight: "bold",
      marginBottom: "0.5rem",
    },
    subheading: {
      color: "#94a3b8",
      marginBottom: "2rem",
    },
    searchBox: {
      backgroundColor: "#1e2130",
      borderRadius: "12px",
      padding: "1.5rem",
      marginBottom: "2rem",
      display: "flex",
      gap: "1rem",
      flexWrap: "wrap",
    },
    input: {
      flex: 1,
      minWidth: "200px",
      padding: "0.75rem 1rem",
      borderRadius: "8px",
      border: "1px solid #2d3748",
      backgroundColor: "#0f1117",
      color: "#e2e8f0",
      fontSize: "14px",
      outline: "none",
    },
    button: {
      padding: "0.75rem 2rem",
      borderRadius: "8px",
      border: "none",
      backgroundColor: "#6366f1",
      color: "white",
      fontWeight: "600",
      cursor: "pointer",
      fontSize: "14px",
    },
    error: {
      backgroundColor: "#2d1515",
      border: "1px solid #E24B4A",
      borderRadius: "8px",
      padding: "1rem",
      marginBottom: "1.5rem",
      color: "#fc8181",
    },
    noResults: {
      textAlign: "center",
      padding: "3rem",
      color: "#94a3b8",
    },
    jobCard: {
      backgroundColor: "#1e2130",
      borderRadius: "12px",
      padding: "1.5rem",
      marginBottom: "1rem",
      border: "1px solid #2d3748",
      display: "flex",
      justifyContent: "space-between",
      alignItems: "flex-start",
      gap: "1rem",
      flexWrap: "wrap",
    },
    jobLeft: {
      flex: 1,
      minWidth: "200px",
    },
    jobTitle: {
      fontSize: "1.1rem",
      fontWeight: "600",
      marginBottom: "0.25rem",
      color: "#e2e8f0",
    },
    jobCompany: {
      color: "#94a3b8",
      fontSize: "14px",
      marginBottom: "0.25rem",
    },
    jobLocation: {
      color: "#64748b",
      fontSize: "13px",
      marginBottom: "0.75rem",
    },
    jobDesc: {
      color: "#94a3b8",
      fontSize: "13px",
      lineHeight: "1.6",
    },
    jobRight: {
      display: "flex",
      flexDirection: "column",
      alignItems: "flex-end",
      gap: "0.75rem",
      minWidth: "130px",
    },
    scoreBadge: (score) => ({
      backgroundColor: getScoreColor(score) + "22",
      color: getScoreColor(score),
      border: `1px solid ${getScoreColor(score)}`,
      borderRadius: "8px",
      padding: "0.4rem 0.8rem",
      fontWeight: "700",
      fontSize: "1rem",
      textAlign: "center",
    }),
    scoreLabel: (score) => ({
      color: getScoreColor(score),
      fontSize: "12px",
      fontWeight: "500",
    }),
    applyBtn: {
      padding: "0.5rem 1.25rem",
      borderRadius: "8px",
      border: "1px solid #6366f1",
      backgroundColor: "transparent",
      color: "#6366f1",
      fontWeight: "600",
      cursor: "pointer",
      fontSize: "13px",
      textDecoration: "none",
    },
    loadingBox: {
      textAlign: "center",
      padding: "3rem",
      color: "#94a3b8",
    },
    spinner: {
      width: "40px",
      height: "40px",
      border: "4px solid #2d3748",
      borderTop: "4px solid #6366f1",
      borderRadius: "50%",
      animation: "spin 1s linear infinite",
      margin: "0 auto 1rem",
    },
    noResumeBox: {
      backgroundColor: "#1e2130",
      borderRadius: "12px",
      padding: "2rem",
      textAlign: "center",
      border: "1px solid #2d3748",
    },
    noResumeBtn: {
      marginTop: "1rem",
      padding: "0.75rem 2rem",
      borderRadius: "8px",
      border: "none",
      backgroundColor: "#6366f1",
      color: "white",
      fontWeight: "600",
      cursor: "pointer",
      fontSize: "14px",
    },
  };

  return (
    <div style={styles.container}>
      <style>{`@keyframes spin { to { transform: rotate(360deg); } }`}</style>
      <div style={styles.inner}>
        <h1 style={styles.heading}>Find Matching Jobs</h1>
        <p style={styles.subheading}>
          Showing jobs matched to your latest resume.{" "}
          <span
            style={{ color: "#6366f1", cursor: "pointer" }}
            onClick={() => navigate("/analyze")}
          >
            Analyze a new resume
          </span>{" "}
          to update.
        </p>

        <div style={styles.searchBox}>
          <input
            style={styles.input}
            type="text"
            placeholder="Override job title (auto-detected from resume)"
            value={title}
            onChange={(e) => setTitle(e.target.value)}
            onKeyDown={(e) => e.key === "Enter" && handleSearch()}
          />
          <input
            style={styles.input}
            type="text"
            placeholder="Location (e.g. india, london)"
            value={location}
            onChange={(e) => setLocation(e.target.value)}
            onKeyDown={(e) => e.key === "Enter" && handleSearch()}
          />
          <button
            style={styles.button}
            onClick={handleSearch}
            disabled={loading}
          >
            {loading ? "Searching..." : "Search Jobs"}
          </button>
        </div>

        {error && error.includes("No resume") ? (
          <div style={styles.noResumeBox}>
            <p style={{ color: "#94a3b8", marginBottom: "0.5rem" }}>
              You haven't analyzed a resume yet.
            </p>
            <p style={{ color: "#64748b", fontSize: "13px" }}>
              Run an analysis first so we can match your resume against jobs.
            </p>
            <button
              style={styles.noResumeBtn}
              onClick={() => navigate("/analyze")}
            >
              Analyze Resume First
            </button>
          </div>
        ) : error ? (
          <div style={styles.error}>{error}</div>
        ) : null}

        {loading && (
          <div style={styles.loadingBox}>
            <div style={styles.spinner} />
            <p>Fetching and scoring jobs against your resume...</p>
          </div>
        )}

        {!loading && searched && jobs.length === 0 && !error && (
          <div style={styles.noResults}>
            <p style={{ fontSize: "1.2rem", marginBottom: "0.5rem" }}>
              No jobs found
            </p>
            <p style={{ fontSize: "13px" }}>
              Try a different location or override the job title.
            </p>
          </div>
        )}

        {!loading && jobs.length > 0 && (
          <>
            <p style={{ color: "#94a3b8", marginBottom: "0.5rem" }}>
              Found {jobs.length} jobs — sorted by match score
            </p>
            {autoTitle && (
              <p style={{ color: "#94a3b8", marginBottom: "1rem", fontSize: "13px" }}>
                Auto-detected role:{" "}
                <span style={{ color: "#6366f1", fontWeight: "600" }}>
                  {autoTitle}
                </span>
              </p>
            )}
            {jobs.map((job, index) => (
              <div key={index} style={styles.jobCard}>
                <div style={styles.jobLeft}>
                  <div style={styles.jobTitle}>{job.title}</div>
                  <div style={styles.jobCompany}>{job.company}</div>
                  <div style={styles.jobLocation}>{job.location}</div>
                  <div style={styles.jobDesc}>{job.description}</div>
                </div>
                <div style={styles.jobRight}>
                  <div style={styles.scoreBadge(job.match_score)}>
                    {job.match_score}%
                  </div>
                  <div style={styles.scoreLabel(job.match_score)}>
                    {getScoreLabel(job.match_score)}
                  </div>
                    <a                  
                    href={job.redirect_url}
                    target="_blank"
                    rel="noopener noreferrer"
                    style={styles.applyBtn}
                  >
                    View Job →
                  </a>
                </div>
              </div>
            ))}
          </>
        )}
      </div>
    </div>
  );
}