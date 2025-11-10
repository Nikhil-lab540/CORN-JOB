from sqlalchemy import create_engine, inspect

DATABASE_URL = (
    "postgresql+psycopg2://doadmin:AVNS_FtaTHZQtmY1WSQsZ6yM@"
    "edtechdatabase-do-user-18137285-0.f.db.ondigitalocean.com:25061/schools-pool"
    "?sslmode=require"
)

engine = create_engine(DATABASE_URL)
inspector = inspect(engine)

table_name = "myapp_homeworksubmission"

columns = inspector.get_columns(table_name)

print(f"\n📋 Columns in table '{table_name}':\n")
for col in columns:
    print(f"{col['name']:<30} | {col['type']}")
