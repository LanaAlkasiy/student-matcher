from flask import Flask, request, jsonify
from flask_cors import CORS

from cv_parser import extract_text_from_pdf
from matcher import extract_skills, match_jobs
from jobs import get_real_jobs
from fallback_jobs import FALLBACK_JOBS
from recommender import recommend_courses
from career_coach import generate_coaching

app = Flask(__name__)
CORS(app)

MAX_CV_BYTES = 10 * 1024 * 1024  # 10 MB -- the frontend *hints* at this limit
                                  # but never enforced it server-side before.


@app.route("/")
def home():
    return "Welcome to Student Matcher!"


@app.route("/upload-cv", methods=["POST"])
def upload_cv():

    if "cv" not in request.files:
        return jsonify({"error": "No CV file uploaded"}), 400

    cv_file = request.files["cv"]

    if cv_file.filename == "":
        return jsonify({"error": "No selected file"}), 400

    if not cv_file.filename.lower().endswith(".pdf"):
        return jsonify({"error": "Please upload a PDF file"}), 400

    file_bytes = cv_file.read()

    if len(file_bytes) > MAX_CV_BYTES:
        return jsonify({"error": "File too large. Max size is 10 MB."}), 400

    extracted_text = extract_text_from_pdf(file_bytes)
    skills = extract_skills(extracted_text)
    country = request.form.get("country", "us")
    opportunity_type = request.form.get("opportunity_type", "internship")

    # Try live job listings first; fall back to the curated local list if
    # the API key is missing, the request fails, or nothing comes back.
    real_jobs = get_real_jobs(skills, country, opportunity_type)
    jobs_source = real_jobs if real_jobs else FALLBACK_JOBS

    matched_jobs = match_jobs(skills, jobs_source)
    top_job = matched_jobs[0] if matched_jobs else None

    coaching = generate_coaching(top_job, skills) if top_job else None
    course_recommendations = (
        recommend_courses(top_job["missing_skills"]) if top_job else []
    )

    return jsonify({
        "message": "CV uploaded successfully",
        "filename": cv_file.filename,
        "extracted_text": extracted_text,
        "skills": skills,
        "jobs": matched_jobs,
        "job_source": "live" if real_jobs else "local",
        "coaching": coaching,
        "course_recommendations": course_recommendations,
    })


if __name__ == "__main__":
    app.run(debug=True)
