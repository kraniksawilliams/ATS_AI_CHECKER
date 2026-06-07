import re
import yake
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer, util

model = None  # lazy loading


def get_model():
    global model
    if model is None:
        model = SentenceTransformer('all-MiniLM-L6-v2')
    return model


def clean(text):
    return re.sub(r'\W+', ' ', text.lower())


def tfidf_score(resume, jd):
    tfidf = TfidfVectorizer(stop_words='english')
    matrix = tfidf.fit_transform([resume, jd])
    return cosine_similarity(matrix)[0][1] * 100


def bert_score(resume, jd):
    model = get_model()
    e1 = model.encode(resume, convert_to_tensor=True)
    e2 = model.encode(jd, convert_to_tensor=True)
    return float(util.cos_sim(e1, e2)[0][0]) * 100

def detect_sections(text):
    sections = ["skills", "projects", "experience", "education"]
    return sum([1 for s in sections if s in text]) / 4 * 100


def readability(text):
    words = text.split()
    return min(100, len(words) / 4)


def extract_keywords(text):
    kw = yake.KeywordExtractor(top=20)
    return [k[0] for k in kw.extract_keywords(text)]


def missing_keywords(resume, jd):
    r = extract_keywords(resume)
    j = extract_keywords(jd)
    return [k for k in j if k not in r][:10]


def final_score(resume, jd):
    resume = clean(resume)
    jd = clean(jd)

    t = tfidf_score(resume, jd)
    b = bert_score(resume, jd)
    s = detect_sections(resume)
    r = readability(resume)

    score = (t * 0.3 + b * 0.4 + s * 0.15 + r * 0.15)

    return round(score, 2), {
        "tfidf": round(t, 2),
        "bert": round(b, 2),
        "sections": round(s, 2),
        "readability": round(r, 2)
    }