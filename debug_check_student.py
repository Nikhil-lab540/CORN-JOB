from database import SessionLocal
from models import Student, HomeworkSubmission

def debug_check(mobile_number):
    db = SessionLocal()
    try:
        student = db.query(Student).filter(Student.phone_number == mobile_number).first()
        if not student:
            print("❌ No student found for that number")
            return

        print("✅ Found student:")
        print("   ID:", student.id)
        print("   Username:", student.username)
        print("   Phone:", student.phone_number)

        # show how student_id is stored in submissions
        print("\n🔍 Checking homework submissions with student_id matches:")
        submissions = db.query(HomeworkSubmission).limit(10).all()
        for s in submissions:
            print(f"Submission ID: {s.id}, student_id: {s.student_id}, homework_id: {s.homework_id}")

    finally:
        db.close()

if __name__ == "__main__":
    debug_check("7569630144")  # change to your test number
