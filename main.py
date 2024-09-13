from fastapi import FastAPI
from routers import generate_transcribe

app = FastAPI()
app.include_router(generate_transcribe.router,prefix="/api",tags=["generate _transcribe from audio"])


app.get("/")
def read_root():
    return  {"message":"For generate transcribe from audio use /api/generate_transcribe\nor use /docs for more info"}
