from sqlalchemy import select
from sqlalchemy.orm import Session
from database import engine
from models_reflect import metadata

# Reflect tables
HomeworkSubmission = metadata.tables.get("myapp_homeworksubmission")
Homework = metadata.tables.get("myapp_homework")
GapAnalysis = metadata.tables.get("myapp_gapanalysis")
Student = metadata.tables.get("Users_student")

def get_student_homework(student_id, limit=5):
    data = []
    with Session(engine) as session:
        stmt = (
            select(HomeworkSubmission)
            .where(HomeworkSubmission.c.student_id == student_id)
            .order_by(HomeworkSubmission.c.id.desc())
            .limit(limit)
        )
        results = session.execute(stmt).fetchall()

        for row in results:
            hw = row._mapping
            data.append({
                "homework_id": hw.get("id"),
                "homework_title": hw.get("title", "Untitled Homework"),
                "submission_date": str(hw.get("submitted_at", "")),
                "score": hw.get("score", None),
                "total": hw.get("total_marks", None)
            })
    return data


def get_student_gap_analysis(student_id, limit=5):
    data = []
    with Session(engine) as session:
        stmt = (
            select(GapAnalysis)
            .where(GapAnalysis.c.student_id == student_id)
            .order_by(GapAnalysis.c.id.desc())
            .limit(limit)
        )
        results = session.execute(stmt).fetchall()
        for row in results:
            ga = row._mapping
            data.append({
                "chapter": ga.get("chapter_name", ""),
                "weak_concept": ga.get("weak_concept", ""),
                "remarks": ga.get("remarks", "")
            })
    return data


def get_student_json(student_id):
    homework_data = get_student_homework(student_id)
    gaps = get_student_gap_analysis(student_id)
    return {
        "student_id": student_id,
        "homeworks": homework_data,
        "gap_analysis": gaps
    }

if __name__ == "__main__":
    student_id = 1  # change to real ID from Users_student
    student_json = get_student_json(student_id)
    print(student_json)
