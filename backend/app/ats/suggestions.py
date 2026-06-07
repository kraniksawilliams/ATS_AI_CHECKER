def generate_suggestions(resume, missing):
    tips = []

    if missing:
        tips.append("Add missing keywords: " + ", ".join(missing))

    if "%" not in resume:
        tips.append("Add measurable achievements (e.g., improved accuracy by 20%)")

    if "project" not in resume:
        tips.append("Include a Projects section")

    tips.append("Use strong action verbs: Built, Developed, Optimized")

    return tips