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
  const pr = analysis.parsed_resume;

  return (
    <div style={styles.container}>
      <Link to="/history" style={styles.backLink}>← Back to History</Link>
      <h1 style={styles.title}>{analysis.filename || "Resume Analysis"}</h1>
      <p style={styles.date}>{new Date(analysis.created_at).toLocaleString()}</p>

      <div style={styles.scoreCard}>
        <p style={styles.scoreNum}>{analysis.ats_score}%</p>
        <p style={styles.scoreLabel}>Job Match Score</p>
        {analysis.keyword_score != null && analysis.semantic_score != null && (
          <div style={styles.scoreBreakdown}>
            <div style={styles.scoreBreakdownItem}>
              <span style={styles.scoreBreakdownLabel}>Keyword Match</span>
              <span style={styles.scoreBreakdownValue}>{analysis.keyword_score}%</span>
            </div>
            <div style={styles.scoreBreakdownItem}>
              <span style={styles.scoreBreakdownLabel}>Semantic Match</span>
              <span style={styles.scoreBreakdownValue}>{analysis.semantic_score}%</span>
            </div>
          </div>
        )}
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

      {analysis.skill_gap && (
        <div style={styles.keywordsGrid}>
          <div style={styles.keywordCard}>
            <h3 style={{ color: "#a6e3a1" }}>✓ Matching Skills ({analysis.skill_gap.matching_skills.length})</h3>
            <div style={styles.tags}>
              {analysis.skill_gap.matching_skills.map(s => (
                <span key={s} style={{ ...styles.tag, background: "#a6e3a120", color: "#a6e3a1" }}>{s}</span>
              ))}
            </div>
          </div>
          <div style={styles.keywordCard}>
            <h3 style={{ color: "#f38ba8" }}>✗ Missing Skills ({analysis.skill_gap.missing_skills.length})</h3>
            <div style={styles.tags}>
              {analysis.skill_gap.missing_skills.map(s => (
                <span key={s} style={{ ...styles.tag, background: "#f38ba820", color: "#f38ba8" }}>{s}</span>
              ))}
            </div>
          </div>
        </div>
      )}

      {pr && (
        <div style={styles.feedbackCard}>
          <h3 style={styles.feedbackTitle}>Parsed Resume</h3>

          {pr.full_name && <p style={styles.assessment}><strong>Name:</strong> {pr.full_name}</p>}
          {pr.email && <p style={styles.assessment}><strong>Email:</strong> {pr.email}</p>}
          {pr.phone && <p style={styles.assessment}><strong>Phone:</strong> {pr.phone}</p>}

          {pr.skills?.length > 0 && (
            <>
              <h4 style={styles.feedbackSub}>Skills</h4>
              <div style={styles.tags}>
                {pr.skills.map((s, i) => (
                  <span key={i} style={{ ...styles.tag, background: "#89b4fa20", color: "#89b4fa" }}>{s}</span>
                ))}
              </div>
            </>
          )}

          {pr.experience?.length > 0 && (
            <>
              <h4 style={styles.feedbackSub}>Experience</h4>
              <ul style={styles.list}>
                {pr.experience.map((e, i) => (
                  <li key={i}>
                    <strong>{e.title}</strong> at {e.company}
                    {(e.start_date || e.end_date) && ` (${e.start_date || "?"} – ${e.end_date || "present"})`}
                  </li>
                ))}
              </ul>
            </>
          )}

          {pr.education?.length > 0 && (
            <>
              <h4 style={styles.feedbackSub}>Education</h4>
              <ul style={styles.list}>
                {pr.education.map((ed, i) => (
                  <li key={i}>
                    {ed.degree ? `${ed.degree}` : ""}{ed.field_of_study ? ` in ${ed.field_of_study}` : ""}
                    {ed.degree || ed.field_of_study ? " — " : ""}{ed.institution}
                  </li>
                ))}
              </ul>
            </>
          )}

          {pr.projects?.length > 0 && (
            <>
              <h4 style={styles.feedbackSub}>Projects</h4>
              <ul style={styles.list}>
                {pr.projects.map((p, i) => (
                  <li key={i}>
                    <strong>{p.name}</strong>
                    {p.description && ` — ${p.description}`}
                  </li>
                ))}
              </ul>
            </>
          )}

          {pr.certifications?.length > 0 && (
            <>
              <h4 style={styles.feedbackSub}>Certifications</h4>
              <ul style={styles.list}>
                {pr.certifications.map((c, i) => (
                  <li key={i}>{c.name}{c.issuer && ` — ${c.issuer}`}</li>
                ))}
              </ul>
            </>
          )}
        </div>
      )}

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
  scoreBreakdown: { display: "flex", justifyContent: "center", gap: "2rem", marginTop: "1rem", paddingTop: "1rem", borderTop: "1px solid #45475a" },
  scoreBreakdownItem: { display: "flex", flexDirection: "column", alignItems: "center", gap: "0.25rem" },
  scoreBreakdownLabel: { color: "#9399b2", fontSize: "0.8rem" },
  scoreBreakdownValue: { color: "#cdd6f4", fontSize: "1.1rem", fontWeight: "bold" },
};