import os, json
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def analyze_cv(cv_text, job_title, job_description):
    try:
        return gemini_analyze(cv_text, job_title, job_description)
    except Exception as e:
        print(f"Gemini Error: {e}")
        return smart_fallback(cv_text, job_title, job_description)

def gemini_analyze(cv_text, job_title, job_description):
    model = genai.GenerativeModel('gemini-2.0-flash')
    
    prompt = f"""
    Analyze this CV against the job requirements. Return ONLY valid JSON, no other text.

    JOB TITLE: {job_title}
    JOB DESCRIPTION: {job_description}
    CV CONTENT: {cv_text[:3000]}

    Return this exact JSON structure:
    {{
        "score": <0-100>,
        "resume_quality": <0-100>,
        "reasoning": "<2-3 sentences explaining the score>",
        "matched_skills": ["skill1", "skill2"],
        "missing_skills": ["skill1", "skill2"],
        "priority_gaps": [{{"skill": "name", "importance": "critical/high/medium", "learn_in": "2 weeks/1 month"}}],
        "career_paths": ["path1"],
        "experience_match": "good/average/poor",
        "culture_fit_hint": "<brief insight>",
        "recommendation": "Hire/Shortlist/Reject",
        "questions": ["q1", "q2", "q3"]
    }}
    """
    
    response = model.generate_content(prompt)
    text = response.text.strip()
    
    if text.startswith("```json"): text = text[7:]
    if text.endswith("```"): text = text[:-3]
    
    result = json.loads(text)
    return format_result(result)

def format_result(r):
    return {
        "score": r.get("score", 50),
        "resume_quality": r.get("resume_quality", 50),
        "reasoning": r.get("reasoning", ""),
        "matched_skills": r.get("matched_skills", []),
        "missing_skills": r.get("missing_skills", []),
        "priority_gaps": r.get("priority_gaps", []),
        "career_paths": r.get("career_paths", []),
        "experience_match": r.get("experience_match", "average"),
        "culture_fit_hint": r.get("culture_fit_hint", ""),
        "recommendation": r.get("recommendation", "Shortlist"),
        "questions": r.get("questions", [])
    }

def smart_fallback(cv_text, job_title, job_description):
    cv_lower = cv_text.lower()
    job_lower = (job_title + " " + job_description).lower()

    skill_categories = {
        "technical": ["python", "javascript", "react", "node", "sql", "aws", "docker", "git", "rest api", "mongodb", "postgresql", "typescript", "java", "c++", "c#", "html", "css", "express", "redux", "bootstrap"],
        "ai_data": ["machine learning", "ai", "deep learning", "nlp", "data analysis", "spss", "tableau", "excel"],
        "soft": ["leadership", "communication", "teamwork", "problem solving", "agile", "scrum", "project management", "team player"],
        "domain": ["embedded", "iot", "android", "ios", "web", "mobile", "cloud", "devops", "full stack"]
    }

    cv_skills = []
    for cat, skills in skill_categories.items():
        for s in skills:
            if s in cv_lower:
                cv_skills.append(s)

    job_skills = []
    for cat, skills in skill_categories.items():
        for s in skills:
            if s in job_lower:
                job_skills.append(s)

    matched = [s for s in cv_skills if s in job_skills]
    missing = [s for s in job_skills if s not in cv_skills]

    score = min(100, int((len(matched) / max(len(job_skills), 1)) * 100))

    word_count = len(cv_text.split())
    resume_quality = min(100, max(20, word_count // 10)) if word_count < 300 else min(100, 60 + (word_count - 300) // 20)

    priority_gaps = []
    for i, skill in enumerate(missing[:5]):
        priority_gaps.append({"skill": skill, "importance": "critical" if i == 0 else "high" if i < 3 else "medium", "learn_in": "2 weeks" if i < 2 else "1 month"})

    career_paths = []
    if "python" in cv_skills or "javascript" in cv_skills:
        career_paths.append("Software Engineer → Senior Developer → Tech Lead")
    if "react" in cv_skills or "node" in cv_skills:
        career_paths.append("Full Stack Developer → Solution Architect → CTO")
    if not career_paths:
        career_paths = ["Developer → Senior → Lead"]

    return {
        "score": score,
        "resume_quality": resume_quality,
        "reasoning": f"Matched {len(matched)}/{len(job_skills)} skills. Strong in: {', '.join(cv_skills[:5]) or 'general skills'}.",
        "matched_skills": matched[:8],
        "missing_skills": missing[:6],
        "priority_gaps": priority_gaps,
        "career_paths": career_paths[:2],
        "experience_match": "good" if score > 60 else "average",
        "culture_fit_hint": "Structured thinker" if len(cv_skills) > 5 else "Growth potential",
        "recommendation": "Hire" if score > 65 else ("Shortlist" if score > 35 else "Reject"),
        "questions": [
    f"Can you elaborate on your experience with {matched[0]}? What specific projects did you use it in?",
    f"Your CV mentions {cv_skills[0] if len(cv_skills)>0 else 'technical skills'}. Can you describe a challenging problem you solved using it?",
    f"You have experience with {', '.join(cv_skills[:3]) if cv_skills else 'various technologies'}. How do you stay updated with new technologies?",
    f"Looking at the job requirements, you're missing {missing[0] if missing else 'some skills'}. How would you bridge this gap?",
    f"Describe a situation where you had to work under pressure to meet a deadline.",
    f"How do you handle disagreements with team members or stakeholders?"
] if matched else [
    "Walk me through your most impressive project or achievement.",
    "What skills are you currently learning or want to develop?",
    "Describe your ideal work environment and team culture.",
    "How do you prioritize tasks when everything seems important?",
    "Where do you see yourself professionally in the next 2-3 years?",
    "Tell me about a time you failed and what you learned."
]
    }