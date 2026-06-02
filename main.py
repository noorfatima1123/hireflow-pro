from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.auth_routes import router as auth_router
from routes.job_routes import router as job_router
from routes.candidate_routes import router as candidate_router
from routes.ai_routes import router as ai_router
from routes.analytics_routes import router as analytics_router
from routes.voice_routes import router as voice_router
from routes.skill_routes import router as skill_router
from routes.ranking_routes import router as ranking_router
from routes.feedback_routes import router as feedback_router



app = FastAPI(title="AI Recruitment Platform v2.0")

# CORS - Allow everything
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(job_router)
app.include_router(candidate_router)
app.include_router(ai_router)
app.include_router(analytics_router)
app.include_router(voice_router)
app.include_router(skill_router)
app.include_router(ranking_router)
app.include_router(feedback_router)


@app.get("/")
def home():
    return {"message": "AI Recruitment API v2.0 Ready! 🚀"}

@app.options("/{path:path}")
async def options_handler(path: str):
    return {"ok": "ok"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)