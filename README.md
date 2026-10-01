# HireFlow Pro: AI Recruitment Platform

HireFlow Pro helps recruiters screen candidates faster. It analyses a CV against a job description with **Google Gemini** and returns a structured report: match score, matched and missing skills, learning priorities, a hire/shortlist/reject recommendation, and tailored interview questions.

## What the analysis returns

- **Match score** (0-100) and **resume quality** score
- **Matched vs. missing skills**, plus **priority gaps** ranked by importance with an estimated time to learn
- **Experience match** and a short culture-fit hint
- **Recommendation**: Hire / Shortlist / Reject, with a written rationale
- **Suggested career paths** and **custom interview questions** for the candidate
- **Graceful fallback**: if the Gemini call fails, a built-in keyword-based analyser produces the same response format, so the API never returns an empty result

## Tech stack

| Layer | Technology |
|---|---|
| Backend | Python, FastAPI |
| AI | Google Gemini (`gemini-2.0-flash`) |
| Database | Supabase |
| Frontend | React, Vite |

The API is organised into route modules for authentication, jobs, candidates, AI analysis, analytics, skills, ranking and feedback.

## Getting started

```bash
git clone https://github.com/noorfatima1123/hireflow-pro.git
cd hireflow-pro

# Backend
pip install fastapi uvicorn python-dotenv google-generativeai
cp .env.example .env     # add your own keys
python main.py           # http://localhost:8000/docs

# Frontend
npm install
npm run dev
```

## Author

**Noor Fatima**: [GitHub](https://github.com/noorfatima1123) · [LinkedIn](https://www.linkedin.com/in/engr-noor-fatima-a4a142290)
