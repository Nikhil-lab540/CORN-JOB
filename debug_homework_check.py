from sqlalchemy import create_engine, select, MetaData
from sqlalchemy.orm import sessionmaker

# ✅ DB CONFIG
DATABASE_URL="postgresql+psycopg2://doadmin:AVNS_FtaTHZQtmY1WSQsZ6yM@edtechdatabase-do-user-18137285-0.f.db.ondigitalocean.com:25061/schools-pool?sslmode=require"

engine = create_engine(DATABASE_URL, echo=False, future=True)
SessionLocal = sessionmaker(bind=engine)
metadata = MetaData()
metadata.reflect(bind=engine)

students_table = metadata.tables["Users_student"]
homework_table = metadata.tables["myapp_homeworksubmission"]

PARENT_PHONE = "9000961240"   # ✅ Parent phone to test


def run_debug():
    db = SessionLocal()
    print("\n✅ Connected to DB")

    # ✅ 1. Find all students for that parent
    students = db.execute(
        select(
            students_table.c.id,
            students_table.c.username,
            students_table.c.fullname
        )
        .where(students_table.c.phone_number == PARENT_PHONE)
    ).fetchall()

    print(f"\n📱 Students linked to {PARENT_PHONE}:")
    if not students:
        print("❌ No students found for this phone")
        return

    for s in students:
        print(f"   ID={s.id}   USERNAME={s.username}   NAME={s.fullname}")

    # ✅ 2. For each student, search homework
    for s in students:
        print(f"\n🔍 Searching homework for student ID={s.id} username={s.username}")

        rows = db.execute(
            select(
                homework_table.c.id,
                homework_table.c.student_name_id,
                homework_table.c.student_id
            )
            .where(
                (homework_table.c.student_name_id == s.id) |
                (homework_table.c.student_id == s.username)
            )
        ).fetchall()

        print(f"   ✅ Homework found: {rows}")

    print("\n✅ Parent-only debug complete.\n")
    db.close()


if __name__ == "__main__":
    run_debug()
