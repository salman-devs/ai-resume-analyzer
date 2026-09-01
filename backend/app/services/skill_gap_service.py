def analyze_skill_gap(resume_skills: list[str], required_skills: list[str], preferred_skills: list[str]) -> dict:
    """
    Compare resume skills against job-required/preferred skills.
    Returns matching and missing skills (exact, case-insensitive match).
    """
    resume_skills_lower = {s.lower().strip() for s in resume_skills}
    all_jd_skills = list(dict.fromkeys(required_skills + preferred_skills))  # dedupe, preserve order

    matching = []
    missing = []

    for jd_skill in all_jd_skills:
        if jd_skill.lower().strip() in resume_skills_lower:
            matching.append(jd_skill)
        else:
            missing.append(jd_skill)

    return {
        "matching_skills": matching,
        "missing_skills": missing,
    }