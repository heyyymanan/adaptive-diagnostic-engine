from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import test

app = FastAPI(title="Adaptive Assessment Engine")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(test.router)

@app.get("/")
def root():
    return {"message": "Adaptive Assessment Engine Running"}