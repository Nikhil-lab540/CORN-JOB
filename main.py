"""
main.py — Multi-student Parent-Aware Version (Final, FIXED)
-----------------------------------------------------------
✅ Handles parents with multiple children
✅ Matches both student_id (varchar) and student_name_id (bigint)
✅ OUTER JOIN ensures homework still appears if FK is null
✅ Accepts agent_analysis_data OR result_json OR fallback score
✅ Generates Gemini report and stores in a file
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy import create_engine, select, MetaData, or_
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import json, logging
from gemini_weekly_report import generate_weekly_report  # your LLM function

# ======================================================
# ✅ DATABASE CONFIG
# ======================================================
DATABASE_URL="postgresql+psycopg2://doadmin:AVNS_FtaTHZQtmY1WSQsZ6yM@edtechdatabase-do-user-18137285-0.f.db.ondigitalocean.com:25061/schools-pool?sslmode=require"


engine = create_engine(DATABASE_URL, echo=False, future=True)
SessionLocal = sessionmaker(bind=engine)
metadata = MetaData()
metadata.reflect(bind=engine)

students_table = metadata.tables["Users_student"]
homework_table = metadata.tables["myapp_homeworksubmission"]

app = FastAPI(title="SmartLearners.ai Weekly Report Generator")

class WeeklyReportRequest(BaseModel):
    mobile_number: str
    homework: bool = True

# ======================================================
# ✅ ENDPOINT — WEEKLY REPORT
# ======================================================
@app.post("/generate_weekly_report/")
def generate_weekly_report_endpoint(request: WeeklyReportRequest):
    db = SessionLocal()
    try:

        # ✅ 1. Find students linked to this phone
        students = db.execute(
            select(students_table)
            .where(students_table.c.phone_number == request.mobile_number)
        ).fetchall()

        if not students:
            raise HTTPException(status_code=404, detail="No students found for this mobile number.")

        print(f"\n📱 Found {len(students)} student(s) for {request.mobile_number}")

        all_student_data = {}

        # ✅ 2. Loop students and fetch homework
        for student in students:
            student_id = student.id
            username = student.username

            print(f"\n🔍 Checking homework for {username} (ID={student_id})")

            submissions = db.execute(
                select(
                    homework_table,
                    students_table.c.fullname.label("student_name"),
                    students_table.c.class_name_id.label("student_class"),
                    students_table.c.section.label("student_section")
                )
                .select_from(
                    homework_table.outerjoin(
                        students_table,
                        homework_table.c.student_name_id == students_table.c.id
                    )
                )
                .where(
                    or_(
                        homework_table.c.student_name_id == student_id,    # FK match
                        homework_table.c.student_id == username            # String match
                    )
                )
                .order_by(homework_table.c.id.desc())
                .limit(5)
            ).fetchall()

            if not submissions:
                print(f"⚠️ No homework found for {username}")
                continue

            student_json = {"data": []}

            # ✅ Accept agent_analysis_data, fallback to result_json or minimal stats
            for sub in submissions:
                parsed = None

                if sub.agent_analysis_data:
                    parsed = sub.agent_analysis_data

                elif sub.result_json:
                    parsed = sub.result_json

                else:
                    parsed = {
                        "submission_id": sub.id,
                        "score": sub.score,
                        "percentage": sub.percentage,
                        "grade": sub.grade
                    }

                # Convert string → dict if necessary
                if isinstance(parsed, str):
                    try:
                        parsed = json.loads(parsed)
                    except:
                        parsed = {"raw_text": parsed}

                student_json["data"].append(parsed)

            if student_json["data"]:
                all_student_data[username] = student_json

        if not all_student_data:
            return {"message": "No valid homework data found for any student."}

        # ✅ 3. Generate file with Gemini reports
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = f"weekly_reports_{timestamp}.txt"

        with open(output_file, "w", encoding="utf-8") as f:
            for username, hw_json in all_student_data.items():
                f.write(f"\n===== 🧮 {username} =====\n")
                report = generate_weekly_report(hw_json)
                f.write(report + "\n")

        return {
            "message": "Weekly reports generated successfully.",
            "students_processed": list(all_student_data.keys()),
            "output_file": output_file
        }

    except Exception as e:
        logging.exception("Error generating report:")
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        db.close()
