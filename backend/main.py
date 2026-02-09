from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from backend.routes import validate_csv as validate_csv_route

app = FastAPI(title="Data Validator API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"message": "Data Validator API"}


@app.get("/health")
async def health():
    return {"status": "healthy"}


@app.post("/validate")
async def validate_csv_endpoint(file: UploadFile = File(...)):
    return await validate_csv_route(file)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
