from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from models import RecommendationRequest
from agent import run_agent_logic
from data import INFLUENCERS_DB

app = FastAPI()

# CORS 설정 (리액트와 통신 허용)
origins = [
    "http://localhost:5173",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"status": "AI Agent Server is Running"}

@app.get("/influencers")
def get_all_influencers():
    return INFLUENCERS_DB

@app.post("/recommend")
def recommend_influencer(request: RecommendationRequest):
    # agent.py에 있는 로직 실행!
    results = run_agent_logic(request.category, request.min_score)
    
    return {
        "count": len(results),
        "results": results,
        "message": f"Found {len(results)} influencers for category '{request.category}'"
    }