# Student Matcher User Flow

## Main User Flow

1. Student opens the Student Matcher website.
2. Student uploads their CV as a PDF.
3. Student enters their preferred role.
4. Student enters their preferred location.
5. System extracts text from the CV.
6. System identifies skills, education, projects, and experience.
7. System compares the student profile with available jobs and internships.
8. System displays matched opportunities.

## Result Page

For each job or internship, the system shows:

- Job title
- Company name
- Location
- Match score
- Why the role matches
- Skills found in the CV
- Missing skills
- Recommended courses for missing skills
- Apply button

## Learning Recommendation Flow

1. System detects missing skills.
2. Each missing skill is matched with relevant online courses.
3. Course names are clickable links.
4. Student is redirected to platforms like Coursera, edX, GitHub Skills, or Udemy.

## Career Gap Analysis

The system shows how learning certain skills could increase the student's number of matching opportunities.

Example:

Current matching opportunities: 12  
After learning SQL: 24  
After learning SQL + Git: 35

## MVP Goal

The first version should allow a student to:

- Upload a CV
- Extract CV text
- View sample job matches
- See match scores
- See missing skills
- Click recommended courses