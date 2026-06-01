import { useState } from "react";
import api from "../api/axios";

export default function Analyze() {
  const [file, setFile] = useState(null);
  const [jobDescription, setJobDescription] = useState("");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!file || !jobDescription) return;
    setLoading(true);
    setError("");
    setResult(null);

    const formData = new FormData();
    formData.append("file", file);
    formData.append("job_description", jobDescription);

    try {
      const res = await api.post("/analysis/", formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });
      setResult(res.data);
    } catch (err) {
      setError(err.response?.data?.detail || "Analysis failed");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={styles.container}>
      <h1 style={styles.title}>Analyze Resume</h1>

      <div style={styles.card}>
        <form onSubmit={handleSubmit}>
          <div style={styles.field}>
            <label style={styles.label}>Upload Resume (PDF)</label>
            <input type="file" accept=".pdf"
              onChange={e => setFile(e.target.files[0])}
              style={styles.fileInput} required />
          </div>
          <div style={styles.field}>
            <label style={styles.label}>Job Description</label>
            <textarea style={styles.textarea}
              placeholder="Paste the job description here..."
              value={jobDescription}
              onChange={e => setJobDescription(e.target.value)}
              rows={6} required />
          </div>
          {error && <p style={styles.error}>{error}</p>}
          <button style={styles.btn} type="submit" disabled={loading}>
            {loading ? "Analyzing..." : "Analyze Resume"}
          </button>
        </form>
      </div>

      {result && (
        <div style={styles.results}>
          <div style={styles.scoreCard}>
            <p style={styles.scoreNum}>{result.ats_score}%</p>
            <p style={styles.scoreLabel}>ATS Match Score</p>
          </div>

          <div style={styles.keywordsGrid}>
            <div style={styles.keywordCard}>
              <h3 style={{ color: "#a6e3a1" }}>✓ Matched Keywords ({result.matched_keywords.length})</h3>
              <div style={styles.tags}>
                {result.matched_keywords.map(k => (
                  <span key={k} style={{ ...styles.tag, background: "#a6e3a120", color: "#a6e3a1" }}>{k}</span>
                ))}
              </div>
            </div>
            <div style={styles.keywordCard}>
              <h3 style={{ color: "#f38ba8" }}>✗ Missing Keywords ({result.missing_keywords.length})</h3>
              <div style={styles.tags}>
                {result.missing_keywords.map(k => (
                  <span key={k} style={{ ...styles.tag, background: "#f38ba820", color: "#f38ba8" }}>{k}</span>
                ))}
              </div>
            </div>
          </div>

          {result.ai_feedback && (
            <div style={styles.feedbackCard}>
              <h3 style={styles.feedbackTitle}>AI Feedback</h3>
              <p style={styles.assessment}>{result.ai_feedback.overall_assessment}</p>

              <h4 style={styles.feedbackSub}>Strengths</h4>
              <ul style={styles.list}>
                {result.ai_feedback.strengths?.map((s, i) => <li key={i}>{s}</li>)}
              </ul>

              <h4 style={styles.feedbackSub}>Improvements</h4>
              <ul style={styles.list}>
                {result.ai_feedback.improvements?.map((s, i) => <li key={i}>{s}</li>)}
              </ul>

              <h4 style={styles.feedbackSub}>Keyword Tips</h4>
              <p style={styles.tip}>{result.ai_feedback.keyword_tips}</p>
            </div>
          )}
        </div>
      )}
    </div>
  );
}

const styles = {
  container: { maxWidth: "900px", margin: "2rem auto", padding: "0 1rem" },
  title: { color: "white", fontSize: "1.8rem", marginBottom: "1.5rem" },
  card: { background: "#313244", padding: "1.5rem", borderRadius: "12px", marginBottom: "2rem" },
  field: { marginBottom: "1rem" },
  label: { display: "block", color: "#cdd6f4", marginBottom: "0.5rem", fontWeight: "500" },
  fileInput: { color: "white", width: "100%" },
  textarea: { width: "100%", padding: "0.75rem", borderRadius: "6px", border: "1px solid #45475a", background: "#1e1e2e", color: "white", fontSize: "0.95rem", resize: "vertical", boxSizing: "border-box" },
  error: { background: "#f38ba820", color: "#f38ba8", padding: "0.75rem", borderRadius: "6px", marginBottom: "1rem" },
  btn: { width: "100%", padding: "0.75rem", background: "#89b4fa", color: "#1e1e2e", border: "none", borderRadius: "6px", fontWeight: "bold", cursor: "pointer", fontSize: "1rem" },
  results: { display: "flex", flexDirection: "column", gap: "1.5rem" },
  scoreCard: { background: "#313244", padding: "2rem", borderRadius: "12px", textAlign: "center" },
  scoreNum: { color: "#89b4fa", fontSize: "3rem", fontWeight: "bold", margin: "0 0 0.25rem" },
  scoreLabel: { color: "#9399b2", margin: 0, fontSize: "1.1rem" },
  keywordsGrid: { display: "grid", gridTemplateColumns: "1fr 1fr", gap: "1rem" },
  keywordCard: { background: "#313244", padding: "1.5rem", borderRadius: "12px" },
  tags: { display: "flex", flexWrap: "wrap", gap: "0.5rem", marginTop: "0.75rem" },
  tag: { padding: "0.25rem 0.75rem", borderRadius: "20px", fontSize: "0.85rem" },
  feedbackCard: { background: "#313244", padding: "1.5rem", borderRadius: "12px" },
  feedbackTitle: { color: "white", marginTop: 0 },
  feedbackSub: { color: "#89b4fa", marginTop: "1rem" },
  assessment: { color: "#cdd6f4", lineHeight: 1.6 },
  list: { color: "#cdd6f4", lineHeight: 1.8, paddingLeft: "1.5rem" },
  tip: { color: "#cdd6f4", lineHeight: 1.6 },
};