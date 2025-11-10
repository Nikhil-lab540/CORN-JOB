from sqlalchemy import create_engine, select, MetaData
from sqlalchemy.orm import sessionmaker

DATABASE_URL = (
    "postgresql+psycopg2://doadmin:AVNS_FtaTHZQtmY1WSQsZ6yM@"
    "edtechdatabase-do-user-18137285-0.f.db.ondigitalocean.com:25061/schools-pool"
    "?sslmode=require"
)

engine = create_engine(DATABASE_URL, echo=False, future=True)
SessionLocal = sessionmaker(bind=engine)
metadata = MetaData()
metadata.reflect(bind=engine)

students_table = metadata.tables["Users_student"]
homework_table = metadata.tables["myapp_homeworksubmission"]

db = SessionLocal()

student = db.execute(
    select(students_table)
    .where(students_table.c.phone_number == "7569630144")
).fetchone()

if not student:
    print("❌ No student found for this mobile.")
else:
    print(f"✅ Student found: {student.username} (id={student.id})")

    results = db.execute(
        select(
            homework_table.c.id,
            homework_table.c.student_id,
            homework_table.c.student_name_id,
            homework_table.c.homework_id
        )
    ).fetchall()

    print("\n🧩 Sample homework rows (to debug mapping):\n")
    for row in results[:20]:
        print(f"id={row.id}, student_id={row.student_id}, student_name_id={row.student_name_id}, hw={row.homework_id}")

db.close()
