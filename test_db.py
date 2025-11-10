from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL not set in .env")

# Good defaults for managed Postgres (DigitalOcean)
engine = create_engine(DATABASE_URL, pool_pre_ping=True, echo=False)

def main():
    try:
        with engine.connect() as conn:
            # Simple connectivity checks
            one = conn.execute(text("SELECT 1")).scalar_one()
            print("✅ SELECT 1 ->", one)

            version = conn.execute(text("SELECT version()")).scalar_one()
            print("✅ Server version ->", version)

            current = conn.execute(text("SELECT current_user")).scalar_one()
            print("✅ Current user ->", current)

    except Exception as e:
        print("❌ Connection failed:", e)

if __name__ == "__main__":
    main()
