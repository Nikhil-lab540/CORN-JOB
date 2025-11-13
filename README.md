# CORN-JOB

AI-powered weekly report generator for SmartLearners.ai students.

## Overview

FastAPI service that generates personalized academic performance reports using Google's Gemini AI. The system analyzes student homework submissions from a PostgreSQL database and creates comprehensive weekly reports for parents.

## Features

- Multi-student support (one parent phone → multiple children)
- AI-generated performance analysis with Gemini
- Automatic homework data retrieval from PostgreSQL
- Detailed reports with strengths, weaknesses, and motivational feedback

## Setup

### Prerequisites

- Python 3.8+
- PostgreSQL database access
- Google Gemini API key

### Installation

1. Clone the repository
```bash
cd CORN-JOB
```

2. Create virtual environment
```bash
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

4. Configure environment variables

Create a `.env` file:
```env
DATABASE_URL=postgresql+psycopg2://user:password@host:port/database?sslmode=require
WHATSAPP_ACCESS_TOKEN=your_token_here
PHONE_NUMBER_ID=your_phone_id
```

5. Update Gemini API key in `gemini_weekly_report.py`:
```python
genai.configure(api_key="YOUR_GEMINI_API_KEY")
```

## Running

Start the FastAPI server:
```bash
uvicorn main:app --reload
```

Server runs at: `http://localhost:8000`

## API Usage

### Generate Weekly Report

**Endpoint:** `POST /generate_weekly_report/`

**Request:**
```json
{
  "mobile_number": "+1234567890",
  "homework": true
}
```

**Response:**
```json
{
  "message": "Weekly reports generated successfully.",
  "students_processed": ["student1", "student2"],
  "output_file": "weekly_reports_20251113_143022.txt"
}
```

The report is saved to a timestamped text file in the project directory.

## Project Structure

- `main.py` - FastAPI application and main endpoint
- `database.py` - Database connection setup
- `models.py` - SQLAlchemy ORM models
- `gemini_weekly_report.py` - Gemini AI report generator
- `gemini_weekly_report_v3.py` - Optimized version with data compression
- `debug_*.py` - Database inspection and debugging utilities

## Database Schema

Key tables:
- `Users_student` - Student information
- `myapp_homeworksubmission` - Homework submissions with AI analysis
- `myapp_homework` - Homework definitions

## License

Proprietary - SmartLearners.ai
