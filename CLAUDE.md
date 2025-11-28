# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**CORN-JOB** is a FastAPI-based weekly report generator for SmartLearners.ai, an educational platform. The system generates AI-powered (Gemini) academic reports for students by analyzing their homework submissions stored in a PostgreSQL database on DigitalOcean.

## Database Architecture

The application connects to a PostgreSQL database with the following key tables:

- **Users_student**: Student records with fields `id` (bigint), `username` (varchar), `phone_number`, `fullname`, `class_name_id`, `section`
- **myapp_homeworksubmission**: Homework submissions with fields `id`, `student_id` (varchar), `student_name_id` (bigint FK), `homework_id`, `submission_date`, `agent_analysis_data` (TEXT/JSON), `result_json` (TEXT/JSON), `score`, `percentage`, `grade`
- **myapp_homework**: Homework definitions with `id`, `homework_code`

**Critical Database Quirk**: The `myapp_homeworksubmission` table has BOTH:
- `student_id` (varchar) - stores username string
- `student_name_id` (bigint) - foreign key to Users_student.id

Queries must use `OR` logic to match either field when fetching student homework. Use OUTER JOIN to handle cases where the FK is null.

## Core Application Files

### main.py
The primary FastAPI application with a single endpoint:
- `POST /generate_weekly_report/` - Takes mobile number, finds all students linked to that phone, fetches their recent homework (max 5), and generates Gemini reports saved to a timestamped file

Key logic:
1. Queries students by phone number
2. For each student, fetches homework using: `WHERE (homework_table.c.student_name_id == student_id OR homework_table.c.student_id == username)`
3. Parses homework data from `agent_analysis_data` OR `result_json` (fallback to score fields)
4. Calls `generate_weekly_report()` from gemini_weekly_report.py
5. Writes all reports to `weekly_reports_YYYYMMDD_HHMMSS.txt`

### Gemini Report Generators (3 versions)

**gemini_weekly_report.py** (v1 - Production)
- Used by main.py endpoint
- `generate_weekly_report(homework_json)` - Sends full JSON to Gemini
- Detailed prompt requesting 10-15 line reports with trends and parent notes

**gemini_weekly_report_v2.py** (Optimized)
- Adds `compress_data()` function to reduce token usage
- Keeps only last 3 submissions with essential fields
- Uses `temperature: 0.6` for balanced output

**gemini_weekly_report_v3.py** (Multi-student batch)
- `compress_data()` - Reduces JSON payload
- `generate_weekly_report(student_name, homework_json)` - Takes student name as parameter
- `generate_reports_for_students()` - Batch processor for multiple students
- Uses `max_output_tokens=500` for speed

### database.py
Database connection setup:
- Loads DATABASE_URL from .env
- Creates SQLAlchemy engine with `pool_pre_ping=True` for connection health checks
- Provides `SessionLocal` sessionmaker and `get_db()` dependency for FastAPI

### models.py
SQLAlchemy ORM models (declarative) for Student, Homework, HomeworkSubmission tables

## Environment Configuration

Required `.env` variables:
- `DATABASE_URL` - PostgreSQL connection string (format: `postgresql+psycopg2://user:pass@host:port/db?sslmode=require`)
- `WHATSAPP_ACCESS_TOKEN` - (present but not currently used in main.py)
- `PHONE_NUMBER_ID` - (present but not currently used in main.py)

**Security Note**: Credentials are hardcoded in several files:
- `main.py` - DATABASE_URL is hardcoded (duplicates .env)
- `gemini_weekly_report.py` and `gemini_weekly_report_v2.py` - Gemini API keys hardcoded

## Running the Application

### Development Server
```bash
# Activate virtual environment (Windows)
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run FastAPI server
uvicorn main:app --reload
```

### Testing the Endpoint
```bash
curl -X POST "http://localhost:8000/generate_weekly_report/" \
  -H "Content-Type: application/json" \
  -d '{"mobile_number": "+1234567890", "homework": true}'
```

## Key Dependencies

- **FastAPI** + **Uvicorn** - Web framework and ASGI server
- **SQLAlchemy** - ORM and database toolkit
- **psycopg2** - PostgreSQL adapter
- **python-dotenv** - Environment variable management
- **google-generativeai** - Gemini API client (**must be installed separately**: `pip install google-generativeai`)

## Common Development Tasks

### Database Inspection Scripts
- `check_columns.py` - Inspects table column names and types
- `fetch_student_data.py` - Retrieves student records
- `count_students_by_phone.py` - Counts students per phone number
- `debug_check_student.py` - Student lookup debugging
- `debug_homework_check.py` - Homework query debugging
- `debug_homework_link.py` - Foreign key relationship debugging
- `models_reflect.py` - Uses SQLAlchemy reflection to discover schema
- `test_db.py` - Database connection test

## Parent-Student Relationship

The system supports **one parent phone number → multiple student accounts**. The `/generate_weekly_report/` endpoint:
1. Finds ALL students with matching `phone_number`
2. Generates separate reports for each student
3. Outputs all reports to a single file with student usernames as section headers

## JSON Data Structure

Homework analysis data (`agent_analysis_data` field) contains:
```json
{
  "data": [
    {
      "homework_id": "HW001",
      "submission_date": "ISO-8601 timestamp",
      "question": {
        "questions": [
          {
            "question_id": "Q1",
            "topic": "topic name",
            "question": "question text",
            "max_score": 10,
            "total_score": 7,
            "answer_category": "Correct|Partially-Correct|Unattempted|Irrelevant|Numerical Error|Conceptual Error",
            "concept_required": ["concept1", "concept2"],
            "comment": "feedback on student's answer",
            "correction_comment": "detailed correction"
          }
        ]
      }
    }
  ]
}
```

## Code Architecture Notes

- **Database connection**: main.py creates its own engine/session instead of using database.py's setup
- **Metadata reflection**: Tables are accessed via `metadata.reflect(bind=engine)` rather than ORM models in production endpoints
- **Error handling**: Limited try/except in endpoint with generic 500 responses
- **Logging**: Basic logging configured but minimal usage
- **File outputs**: Reports written to working directory with timestamp naming
