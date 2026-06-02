import { useState, useEffect } from "react";
import { useParams, useNavigate, Link } from "react-router-dom";
import api from "../api/axios";

export default function AnalysisDetail() {
  const { id } = useParams();
  const navigate = useNavigate();
  const [analysis, setAnalysis] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    api.get(`/analysis/${id}`)
      .then(res => setAnalysis(res.data))
      .catch(() => setError("Analysis not found or could not be loaded."))
      .finally(() => setLoading(false));
  }, [id]);

  if (loading) return <div style={styles.loading}>Loading...</div>;
  if (error) return (
    <div style={styles.container}>
      <p style={styles.error}>{error}</p>
      <Link to="/history" style={styles.backLink}>← Back to History</Link>
    </div>
  );

  const fb = analysis.ai_feedback;

  return (
    <div style={styles.container}>
      <Link to="/history" style={styles.backLink}>← Back to History</Link>
      <h1 style={styles.title}>{analysis.filename || "Resume Analysis"}</h1>
      <p style={styles.date}>{new Date(analysis.created_at).toLocaleString()}</p>

      <div style={styles.scoreCard}>
        <p style={styles.scoreNum}>{analysis.ats_score}%</p>
        <p style={styles.scoreLabel}>ATS Match Score</p>
      </div>

      <div style={styles.keywordsGrid}>
        <div style={styles.keywordCard}>
          <h3 style={{ color: "#a6e3a1" }}>✓ Matched Keywords ({analysis.matched_keywords.length})</h3>
          <div style={styles.tags}>
            {analysis.matched_keywords.map(k => (
              <span key={k} style={{ ...styles.tag, background: "#a6e3a120", color: "#a6e3a1" }}>{k}</span>
            ))}
          </div>
        </div>
        <div style={styles.keywordCard}>
          <h3 style={{ color: "#f38ba8" }}>✗ Missing Keywords ({analysis.missing_keywords.length})</h3>
          <div style={styles.tags}>
            {analysis.missing_keywords.map(k => (
              <span key={k} style={{ ...styles.tag, background: "#f38ba820", color: "#f38ba8" }}>{k}</span>
            ))}
          </div>
        </div>
      </div>

      {fb && (
        <div style={styles.feedbackCard}>
          <h3 style={styles.feedbackTitle}>AI Feedback</h3>
          <p style={styles.assessment}>{fb.overall_assessment}</p>
          <h4 style={styles.feedbackSub}>Strengths</h4>
          <ul style={styles.list}>{fb.strengths?.map((s, i) => <li key={i}>{s}</li>)}</ul>
          <h4 style={styles.feedbackSub}>Improvements</h4>
          <ul style={styles.list}>{fb.improvements?.map((s, i) => <li key={i}>{s}</li>)}</ul>
          <h4 style={styles.feedbackSub}>Keyword Tips</h4>
          <p style={styles.tip}>{fb.keyword_tips}</p>
          <h4 style={styles.feedbackSub}>Formatting Tips</h4>
          <p style={styles.tip}>{fb.formatting_tips}</p>
        </div>
      )}

      <div style={styles.jdCard}>
        <h3 style={styles.feedbackTitle}>Job Description</h3>
        <p style={styles.jdText}>{analysis.job_description}</p>
      </div>

      <div style={styles.actions}>
        <button onClick={() => navigate("/analyze")} style={styles.btn}>+ New Analysis</button>
      </div>
    </div>
  );
}

const styles = {
  container: { maxWidth: "900px", margin: "2rem auto", padding: "0 1rem" },
  loading: { color: "white", textAlign: "center", marginTop: "5rem" },
  backLink: { color: "#89b4fa", textDecoration: "none", fontSize: "0.95rem" },
  title: { color: "white", fontSize: "1.8rem", margin: "1rem 0 0.25rem" },
  date: { color: "#6c7086", fontSize: "0.85rem", marginBottom: "1.5rem" },
  error: { color: "#f38ba8", background: "#f38ba820", padding: "0.75rem", borderRadius: "6px" },
  scoreCard: { background: "#313244", padding: "2rem", borderRadius: "12px", textAlign: "center", marginBottom: "1.5rem" },
  scoreNum: { color: "#89b4fa", fontSize: "3rem", fontWeight: "bold", margin: "0 0 0.25rem" },
  scoreLabel: { color: "#9399b2", margin: 0, fontSize: "1.1rem" },
  keywordsGrid: { display: "grid", gridTemplateColumns: "1fr 1fr", gap: "1rem", marginBottom: "1.5rem" },
  keywordCard: { background: "#313244", padding: "1.5rem", borderRadius: "12px" },
  tags: { display: "flex", flexWrap: "wrap", gap: "0.5rem", marginTop: "0.75rem" },
  tag: { padding: "0.25rem 0.75rem", borderRadius: "20px", fontSize: "0.85rem" },
  feedbackCard: { background: "#313244", padding: "1.5rem", borderRadius: "12px", marginBottom: "1.5rem" },
  feedbackTitle: { color: "white", marginTop: 0 },
  feedbackSub: { color: "#89b4fa", marginTop: "1rem" },
  assessment: { color: "#cdd6f4", lineHeight: 1.6 },
  list: { color: "#cdd6f4", lineHeight: 1.8, paddingLeft: "1.5rem" },
  tip: { color: "#cdd6f4", lineHeight: 1.6 },
  jdCard: { background: "#313244", padding: "1.5rem", borderRadius: "12px", marginBottom: "1.5rem" },
  jdText: { color: "#9399b2", lineHeight: 1.7, whiteSpace: "pre-wrap" },
  actions: { textAlign: "center", marginBottom: "2rem" },
  btn: { padding: "0.75rem 2rem", background: "#89b4fa", color: "#1e1e2e", border: "none", borderRadius: "6px", fontWeight: "bold", cursor: "pointer", fontSize: "1rem" },
};