# models_reflect.py
from sqlalchemy import MetaData, Table, inspect
from database import engine

metadata = MetaData()
metadata.reflect(bind=engine)

print("✅ Tables detected in your database:")
for table_name in metadata.tables.keys():
    print(" -", table_name)

# Example: if you want ORM-mapped classes
from sqlalchemy.orm import declarative_base
Base = declarative_base()

# Example: reflect 'homework' table as ORM class
if 'homework' in metadata.tables:
    class Homework(Base):
        __table__ = metadata.tables['homework']
