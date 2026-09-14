from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes.documents import router as documents_router
from app.routes.search import router as search_router
from app.routes.chat import router as chat_router


app = FastAPI(
    title="QueryAI",
    description="Intelligent Document Assistant",
    version="1.0.0",
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173",
                   "https://query-ai-docs.vercel.app",],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(documents_router)
app.include_router(search_router)
app.include_router(chat_router)


@app.get("/")
def root():
    return {
        "message": "QueryAI API is running"
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }