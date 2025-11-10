from sqlalchemy import create_engine, select, MetaData
from sqlalchemy.orm import sessionmaker

# ✅ DB CONFIG  (paste same URL from main.py)
DATABASE_URL = "postgresql+psycopg2://doadmin:AVNS_FtaTHZQtmY1WSQsZ6yM@edtechdatabase-do-user-18137285-0.f.db.ondigitalocean.com:25061/schools-pool?sslmode=require"


engine = create_engine(DATABASE_URL, echo=False, future=True)
SessionLocal = sessionmaker(bind=engine)
metadata = MetaData()
metadata.reflect(bind=engine)

students_table = metadata.tables["Users_student"]

PARENT_PHONE = "9000961240"  # ✅ change here


def check_students():
    db = SessionLocal()
    print("\n✅ Connected to DB\n")

    # ✅ Fetch students linked to phone
    students = db.execute(
        select(
            students_table.c.id,
            students_table.c.username,
            students_table.c.fullname
        )
        .where(students_table.c.phone_number == PARENT_PHONE)
    ).fetchall()

    count = len(students)

    print(f"📱 Phone: {PARENT_PHONE}")
    print(f"👨‍👩‍👧 Total students found: {count}")

    if count == 0:
        print("❌ No students linked to this number.")
    else:
        print("\n✅ Student List:")
        for s in students:
            print(f"   ID={s.id}, USERNAME={s.username}, NAME={s.fullname}")

    db.close()
    print("\n✅ Done.\n")


if __name__ == "__main__":
    check_students()
