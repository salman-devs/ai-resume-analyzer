# AI Resume Analyzer

A full-stack web application that analyzes resumes against job descriptions using ATS (Applicant Tracking System) keyword matching and AI-powered feedback via Google Gemini.

Built as a final year project to help job seekers understand how well their resume matches a given job description and get actionable suggestions to improve it.

---

## Features

- **Resume Parsing** — Upload your resume as a PDF and extract its content automatically
- **ATS Score** — Get a percentage score showing how well your resume matches the job description
- **Keyword Analysis** — See exactly which keywords you matched and which ones are missing
- **AI Feedback** — Receive detailed feedback on strengths, improvements, and keyword tips powered by Google Gemini
- **Analysis History** — View and manage all your past analyses in one place
- **User Authentication** — Secure register and login with JWT-based authentication

---

## Tech Stack

**Backend**
- Python 3.11
- FastAPI
- SQLAlchemy + SQLite
- Google Gemini API (`google-genai`)
- PDFMiner (resume parsing)
- JWT Authentication (python-jose)
- Bcrypt (password hashing)

**Frontend**
- React 18
- Vite
- React Router v6
- Axios

---

## Project Structure

```
ai-resume-analyzer/
├── backend/
│   ├── main.py
│   ├── requirements.txt
│   └── app/
│       ├── core/
│       │   ├── config.py
│       │   ├── database.py
│       │   ├── deps.py
│       │   └── security.py
│       ├── models/
│       │   ├── user.py
│       │   └── analysis.py
│       ├── routers/
│       │   ├── auth.py
│       │   └── analysis.py
│       ├── schemas/
│       │   ├── auth.py
│       │   └── analysis.py
│       └── services/
│           ├── ai_service.py
│           ├── ats_service.py
│           └── pdf_service.py
└── frontend/
    ├── index.html
    ├── package.json
    ├── vite.config.js
    └── src/
        ├── App.jsx
        ├── api/
        │   └── axios.js
        ├── context/
        │   └── AuthContext.jsx
        ├── components/
        │   ├── Navbar.jsx
        │   └── ProtectedRoute.jsx
        └── pages/
            ├── Login.jsx
            ├── Register.jsx
            ├── Dashboard.jsx
            ├── Analyze.jsx
            ├── History.jsx
            └── AnalysisDetail.jsx
```

---

## Getting Started

### Prerequisites

- Python 3.11+
- Node.js 18+
- A Google Gemini API key — get one free at [https://aistudio.google.com/apikey](https://aistudio.google.com/apikey)

### 1. Clone the repository

```bash
git clone https://github.com/your-username/ai-resume-analyzer.git
cd ai-resume-analyzer
```

### 2. Backend Setup

```bash
cd backend

# Create and activate virtual environment
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

Create a `.env` file inside the `backend/` folder:

```env
SECRET_KEY=your_secret_key_here
GEMINI_API_KEY=your_gemini_api_key_here
DATABASE_URL=sqlite:///./resume_analyzer.db
```

Start the backend server:

```bash
uvicorn main:app --reload
```

The API will be running at `http://127.0.0.1:8000`  
Interactive API docs available at `http://127.0.0.1:8000/docs`

### 3. Frontend Setup

```bash
cd frontend

# Install dependencies
npm install
```

Create a `.env` file inside the `frontend/` folder:

```env
VITE_API_URL=http://127.0.0.1:8000
```

Start the frontend dev server:

```bash
npm run dev
```

The app will be running at `http://localhost:5173`

---

## API Endpoints

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/auth/register` | Register a new user | No |
| POST | `/auth/login` | Login and get JWT token | No |
| GET | `/auth/me` | Get current user profile | Yes |
| POST | `/analysis/` | Analyze a resume | Yes |
| GET | `/analysis/` | Get all analyses for current user | Yes |
| GET | `/analysis/stats` | Get analysis statistics | Yes |
| GET | `/analysis/{id}` | Get a specific analysis | Yes |
| DELETE | `/analysis/{id}` | Delete an analysis | Yes |

---

## Environment Variables

**Backend `.env`**

| Variable | Description |
|----------|-------------|
| `SECRET_KEY` | Secret key for JWT signing (use a long random string) |
| `GEMINI_API_KEY` | Your Google Gemini API key |
| `DATABASE_URL` | Database connection string (default: SQLite) |

**Frontend `.env`**

| Variable | Description |
|----------|-------------|
| `VITE_API_URL` | Backend API base URL |

---

## How It Works

1. User uploads a PDF resume and pastes a job description
2. The backend extracts text from the PDF using PDFMiner
3. Both texts are scanned for technical keywords using a curated whitelist of real skills and tools
4. An ATS score is calculated based on how many job description keywords appear in the resume
5. The resume text, job description, score, and keywords are sent to Google Gemini for AI-generated feedback
6. Results are saved to the database and returned to the frontend

---

## Known Limitations

- Only PDF resumes are supported (no DOCX)
- AI feedback depends on Gemini API availability and free tier quota
- ATS scoring is keyword-based and does not account for context or synonyms

---

## Author

**Salman**  
Computer Science Graduate  
[GitHub](https://github.com/your-username) · [LinkedIn](https://linkedin.com/in/your-profile)

---

## License

This project is open source and available under the [MIT License](LICENSE).