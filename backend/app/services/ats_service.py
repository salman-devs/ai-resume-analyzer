import re
from typing import Set


STOP_WORDS: Set[str] = {
    # articles, prepositions, conjunctions
    "and", "or", "the", "a", "an", "in", "on", "at", "to", "for",
    "of", "with", "is", "are", "was", "were", "be", "been", "have",
    "has", "had", "do", "does", "did", "will", "would", "could",
    "should", "may", "might", "can", "this", "that", "these", "those",
    "we", "you", "he", "she", "it", "they", "i", "my", "your", "our",
    "as", "by", "from", "up", "about", "into", "through", "during",
    "also", "than", "then", "so", "if", "but", "not", "no", "more",
    "all", "any", "both", "each", "few", "most", "other", "some",
    "such", "nor", "only", "own", "same", "too", "very", "just",
    "its", "their", "them", "who", "which", "how", "when", "where",
    "there", "here", "new", "get", "use", "work", "make", "good",
    "well", "own", "must", "need", "want", "like", "know", "look",
    "time", "year", "way", "day", "man", "us", "one", "out", "per",
    # job description filler words
    "looking", "join", "seeking", "hiring", "candidate", "candidates",
    "position", "role", "opportunity", "apply", "please", "send",
    "resume", "cv", "cover", "letter", "references", "available",
    "immediate", "urgently", "required", "preferred", "plus", "bonus",
    # common verbs that are not skills
    "write", "written", "writing", "develop", "developing", "developed",
    "design", "designing", "designed", "build", "building", "built",
    "create", "creating", "created", "manage", "managing", "managed",
    "lead", "leading", "led", "maintain", "maintaining", "maintained",
    "deploy", "deploying", "deployed", "monitor", "monitoring", "monitored",
    "collaborate", "collaborating", "collaborated", "participate", "participating",
    "review", "reviewing", "reviewed", "solve", "solving", "solved",
    "implement", "implementing", "implemented", "support", "supporting",
    "ensure", "ensuring", "ensured", "provide", "providing", "provided",
    "improve", "improving", "improved", "define", "defining", "defined",
    "identify", "identifying", "identified", "drive", "driving", "drove",
    # common adjectives/adverbs that are not skills
    "strong", "excellent", "good", "great", "best", "better", "fast",
    "clean", "clear", "simple", "complex", "large", "small", "high",
    "low", "long", "short", "hard", "easy", "able", "similar",
    "scalable", "reliable", "efficient", "effective", "flexible",
    "innovative", "creative", "dynamic", "proactive", "motivated",
    # generic nouns that are not skills
    "experience", "skill", "skills", "knowledge", "ability", "abilities",
    "requirement", "requirements", "responsibility", "responsibilities",
    "qualification", "qualifications", "detail", "details", "attention",
    "problem", "problems", "solution", "solutions", "approach", "process",
    "team", "teams", "member", "members", "company", "organization",
    "business", "product", "products", "service", "services", "system",
    "systems", "application", "applications", "platform", "platforms",
    "environment", "environments", "framework", "frameworks", "tool", "tools",
    "language", "languages", "technology", "technologies", "methodology",
    "methodologies", "practice", "practices", "standard", "standards",
    "communication", "collaboration", "teamwork", "ownership", "integrity",
    "familiar", "familiarity", "proficient", "proficiency", "understanding",
    "including", "include", "includes", "following", "follow", "follows",
    "least", "years", "year", "month", "months", "equivalent", "related",
    "relevant", "current", "currently", "previous", "previously", "prior",
    "across", "within", "between", "multiple", "various", "different",
    "software", "engineer", "developer", "development", "engineering",
}

BIGRAM_PATTERNS = [
    r"machine learning", r"deep learning", r"natural language",
    r"computer vision", r"data science", r"data analysis",
    r"software engineering", r"product management", r"project management",
    r"cloud computing", r"ci/cd", r"rest api", r"restful api",
    r"unit test", r"test driven", r"agile methodology", r"scrum master",
    r"version control", r"object oriented", r"microservices architecture",
    r"full stack", r"front end", r"back end", r"open source",
]

# Only these are valid technical/domain keywords worth matching
TECH_KEYWORDS: Set[str] = {
    # languages
    "python", "javascript", "typescript", "java", "kotlin", "swift",
    "golang", "rust", "ruby", "php", "scala", "cpp", "csharp",
    "html", "css", "sql", "bash", "shell", "r",
    # frontend
    "react", "angular", "vue", "nextjs", "redux", "tailwind",
    "webpack", "vite", "sass", "jquery",
    # backend
    "fastapi", "django", "flask", "nodejs", "express", "spring",
    "graphql", "rest", "apis", "api", "backend", "frontend",
    # databases
    "mysql", "postgresql", "mongodb", "redis", "sqlite", "oracle",
    "cassandra", "elasticsearch", "firebase", "supabase",
    # devops / cloud
    "docker", "kubernetes", "aws", "azure", "gcp", "terraform",
    "ansible", "jenkins", "github", "gitlab", "bitbucket", "git",
    "linux", "nginx", "apache",
    # ai / ml
    "tensorflow", "pytorch", "sklearn", "pandas", "numpy", "opencv",
    "huggingface", "llm", "nlp", "mlops",
    # methodologies
    "agile", "scrum", "kanban", "devops", "tdd", "bdd",
    # other tech
    "microservices", "serverless", "oauth", "jwt", "websocket",
    "rabbitmq", "kafka", "celery", "airflow",
}


def extract_keywords(text: str) -> Set[str]:
    """
    Extract meaningful keywords from text.
    Captures important bigrams first, then filters single-word tokens.
    """
    text_lower = text.lower()
    found: Set[str] = set()

    # 1. extract known bigrams
    for pattern in BIGRAM_PATTERNS:
        if re.search(pattern, text_lower):
            found.add(pattern)

    # 2. clean and tokenize
    cleaned = re.sub(r"[^a-z0-9\+\#\.\s]", " ", text_lower)
    words = cleaned.split()

    # 3. keep only tokens that are: length > 1, not a stop word, and in TECH_KEYWORDS
    for word in words:
        word = word.strip(".")
        if len(word) > 1 and word not in STOP_WORDS and word in TECH_KEYWORDS:
            found.add(word)

    return found


def calculate_ats_score(resume_text: str, job_description: str) -> dict:
    """
    Compare resume against job description.
    Returns ATS score (0-100), matched keywords, and missing keywords.
    """
    if not resume_text or not job_description:
        raise ValueError("Resume text and job description cannot be empty.")

    jd_keywords = extract_keywords(job_description)
    resume_keywords = extract_keywords(resume_text)

    matched = jd_keywords & resume_keywords
    missing = jd_keywords - resume_keywords

    score = round((len(matched) / len(jd_keywords)) * 100) if jd_keywords else 0
    score = min(score, 100)

    return {
        "ats_score": score,
        "matched_keywords": sorted(matched),
        "missing_keywords": sorted(missing),
        "total_jd_keywords": len(jd_keywords),
        "total_matched": len(matched),
    }