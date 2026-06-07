from fastapi import FastAPI, UploadFile, Form
import shutil
import os

from app.ats.parsing import parse_pdf
from app.ats.scoring import final_score, missing_keywords
from app.ats.suggestions import generate_suggestions
from app.ats.rewriting import rewrite_resume

app = FastAPI()


# ensure uploads folder exists
os.makedirs("uploads", exist_ok=True)


@app.get("/")
def home():
    return {"message": "ATS API Running 🚀"}


@app.post("/analyze")
async def analyze(file: UploadFile, jd: str = Form(...)):
    try:
        path = f"uploads/{file.filename}"

        with open(path, "wb") as f:
            shutil.copyfileobj(file.file, f)

        resume = parse_pdf(path)

        score, breakdown = final_score(resume, jd)
        missing = missing_keywords(resume, jd)
        suggestions = generate_suggestions(resume, missing)

        return {
            "score": score,
            "breakdown": breakdown,
            "missing": missing,
            "suggestions": suggestions
        }

    except Exception as e:
        return {"error": str(e)}


@app.post("/rewrite")
async def rewrite(text: str = Form(...), jd: str = Form(...)):
    return {"result": rewrite_resume(text, jd)}