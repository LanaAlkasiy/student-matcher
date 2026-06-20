from flask import Flask, request, jsonify
from flask_cors import CORS

from cv_parser import extract_text_from_pdf
from matcher import extract_skills, match_jobs
from jobs import get_real_jobs
app = Flask(__name__)
CORS(app, origins=["http://127.0.0.1:5500", "http://localhost:5500"])


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
    extracted_text = extract_text_from_pdf(file_bytes)
    skills = extract_skills(extracted_text)
    country = request.form.get("country", "us")

    # Try live job listings first; fall back to the curated local list if
    # the API key is missing, the request fails, or nothing comes back.
    real_jobs = get_real_jobs(skills, country)
    jobs_source = real_jobs if real_jobs else []

    matched_jobs = match_jobs(skills, jobs_source)

    return jsonify({
        "message": "CV uploaded successfully",
        "filename": cv_file.filename,
        "extracted_text": extracted_text,
        "skills": skills,
        "jobs": matched_jobs,
        "job_source": "live" if real_jobs else "local",
    })


if __name__ == "__main__":
    app.run(debug=True)
