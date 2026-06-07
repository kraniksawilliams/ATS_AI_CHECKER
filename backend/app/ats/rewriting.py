import requests

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "llama3"

def rewrite_resume(text, jd):
    prompt = f"""
You are an expert ATS resume writer.

Task:
Rewrite the resume to match the job description.

Resume:
{text}

Job Description:
{jd}

Make it:
- ATS friendly
- professional
- keyword optimized
"""

    response = requests.post(OLLAMA_URL, json={
        "model": MODEL,
        "prompt": prompt,
        "stream": False
    })

    return response.json()["response"]