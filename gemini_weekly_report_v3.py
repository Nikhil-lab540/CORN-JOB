"""
gemini_weekly_report_v3.py
--------------------------
✅ Handles multiple students under one phone number
✅ Compresses data to prevent token overflow
✅ Generates Gemini report per student
✅ Writes all reports to 'weekly_reports.txt'
✅ Optimized for speed + safety
"""

import json
import google.generativeai as genai
from datetime import datetime
import os
import textwrap

# ======================================================
# 1️⃣  CONFIGURE GEMINI
# ======================================================
genai.configure(api_key="YOUR_API_KEY_HERE")  # Replace with your key
MODEL_NAME = "gemini-2.5-flash"

# ======================================================
# 2️⃣  DATA COMPRESSION FUNCTION
# ======================================================
def compress_data(homework_json, recent_n=3):
    """
    Simplify the homework JSON by keeping essential info
    for the latest N submissions only.
    """
    data = homework_json.get("data", [])[-recent_n:]
    compressed = []
    for hw in data:
        hw_summary = {
            "homework_id": hw.get("homework_id"),
            "date": hw.get("submission_date", "")[:10],
            "scores": [],
        }
        for q in hw.get("question", {}).get("questions", []):
            hw_summary["scores"].append({
                "topic": q.get("topic"),
                "score": q.get("total_score"),
                "max": q.get("max_score"),
                "category": q.get("answer_category"),
            })
        compressed.append(hw_summary)
    return compressed


# ======================================================
# 3️⃣  GEMINI REPORT GENERATOR
# ======================================================
def generate_weekly_report(student_name, homework_json):
    """
    Generate one student's concise performance report using Gemini.
    """
    model = genai.GenerativeModel(MODEL_NAME)
    compressed = compress_data(homework_json)

    # If there’s no data, skip safely
    if not compressed:
        return f"⏭️ {student_name}: No recent homework data.\n"

    # Build short prompt
    prompt = textwrap.dedent(f"""
    You are an educational AI assistant for SmartLearners.ai.
    Generate a short weekly performance report for the student '{student_name}'
    based on these recent homework summaries.

    Include:
    - Average score and completion
    - Correct / Partial / Unattempted count
    - Strong and weak concepts
    - 2 motivational sentences for the student
    - 1 short note for parents

    Keep it friendly, encouraging, and concise. Use emojis.
    
    Summarized data (keep analysis high-level, do not restate JSON):
    {json.dumps(compressed, indent=2)}
    """)

    try:
        response = model.generate_content(
            prompt,
            generation_config={
                "temperature": 0.5,
                "max_output_tokens": 500,  # safe lower bound
            }
        )
        return f"📘 Report for {student_name}:\n{response.text.strip()}\n\n"
    except Exception as e:
        return f"❌ Error generating report for {student_name}: {e}\n"


# ======================================================
# 4️⃣  MULTI-STUDENT LOOP + FILE SAVE
# ======================================================
def generate_reports_for_students(students_homework):
    """
    Loop through all students under a parent phone number and
    generate their weekly Gemini reports.
    """
    reports = []

    for student_name, data in students_homework.items():
        print(f"🧠 Generating report for {student_name}...")
        report_text = generate_weekly_report(student_name, data)
        reports.append(report_text)

    # Save all reports to file
    filename = f"weekly_reports_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    with open(filename, "w", encoding="utf-8") as f:
        f.writelines(reports)

    print(f"\n✅ All reports saved to {filename}\n")
    return filename


# ======================================================
# 5️⃣  SAMPLE EXECUTION
# ======================================================
if __name__ == "__main__":
    print("📘 SmartLearners.ai – Multi-Student Weekly Report Generator (Optimized)\n")

    # Example mock data for multiple students under one parent phone number
    sample_students = {
        "10HPS24": { "data": [  # student 1 data
            {
                "homework_id": "HW005",
                "submission_date": "2025-06-30T06:01:00Z",
                "question": {
                    "questions": [
                        {"topic": "Quadratic Equations", "total_score": 8, "max_score": 10, "answer_category": "Correct"},
                        {"topic": "Probability", "total_score": 4, "max_score": 6, "answer_category": "Partially-Correct"}
                    ]
                }
            }
        ]},
        "10HPS17": { "data": [  # student 2 data
            {
                "homework_id": "HW007",
                "submission_date": "2025-06-29T06:00:00Z",
                "question": {
                    "questions": [
                        {"topic": "Derivatives", "total_score": 7, "max_score": 10, "answer_category": "Correct"},
                        {"topic": "Integration", "total_score": 5, "max_score": 10, "answer_category": "Partially-Correct"}
                    ]
                }
            }
        ]}
    }

    print("⏳ Generating all reports (fast mode)...\n")
    generate_reports_for_students(sample_students)
