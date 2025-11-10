"""
gemini_weekly_report.py  (Optimized)
-----------------------------------
✅ Pre-summarizes JSON before sending to Gemini
✅ Uses generation_config (max_output_tokens, temperature)
✅ Much faster response (≈3–5 s)
"""

import json
import google.generativeai as genai

# ======================================================
# 1️⃣  CONFIGURE GEMINI
# ======================================================
genai.configure(api_key="AIzaSyDp2W52XRwr68EVsLORgGLGiVtnmdgh4fQ")
MODEL_NAME = "gemini-2.5-flash"

# ======================================================
# 2️⃣  DATA COMPRESSION FUNCTION
# ======================================================
def compress_data(homework_json, recent_n=3):
    """
    Simplify the huge homework JSON by keeping only
    essential info for the latest N submissions.
    """
    data = homework_json.get("data", [])[-recent_n:]  # last N homeworks
    compressed = []
    for hw in data:
        hw_summary = {
            "homework_id": hw.get("homework_id"),
            "date": hw.get("submission_date", "")[:10],
            "scores": [],
        }
        for q in hw.get("question", {}).get("questions", []):
            hw_summary["scores"].append({
                "topic": q.get("topic"),
                "score": q.get("total_score"),
                "max": q.get("max_score"),
                "category": q.get("answer_category"),
                "concepts": q.get("concept_required", [])
            })
        compressed.append(hw_summary)
    return compressed

# ======================================================
# 3️⃣  GEMINI REPORT GENERATOR
# ======================================================
def generate_weekly_report(homework_json):
    """
    Send a pre-summarized version of JSON to Gemini
    and get a concise weekly report.
    """
    model = genai.GenerativeModel(MODEL_NAME)
    compressed = compress_data(homework_json)

    prompt = f"""
You are an AI education assistant for SmartLearners.ai.

Generate a weekly performance report for one student
based on these summarized homework records.

Include:
• Overall average percentage
• Number of Correct / Partial / Unattempted
• Strengths and weak concepts
• 2 motivational sentences for the student
• 1 short note for parents

Keep tone friendly and concise with emojis.

Summarized data:
{json.dumps(compressed, indent=2)}
"""

    response = model.generate_content(
        prompt,
        generation_config={
            
            "temperature": 0.6          # balanced creativity vs accuracy
        }
    )
    return response.text.strip()

# ======================================================
# 4️⃣  MAIN EXECUTION
# ======================================================
if __name__ == "__main__":
    print("📘 SmartLearners.ai – Gemini Weekly Report Generator (Optimized)\n")

    # Example: load from local JSON file
    # with open("homework_data.json") as f:
    #     homework_json = json.load(f)

    # For quick testing, you can paste a small sample
    sample_json = {
    "data": [
        {
            "homework_id": "HW002",
            "question": {
                "questions": [
                    {
                        "topic": "Quadratic Applications",
                        "comment": "Student wrote 'y = 2(2)² - 8(2) + 5 = -2.5' but the correct calculation gives y = -3.",
                        "question": "Find the vertex of the parabola y = 2x² - 8x + 5",
                        "max_score": 8,
                        "question_id": "Q1",
                        "total_score": 4,
                        "answer_category": "Partially-Correct",
                        "concept_required": [
                            "Vertex Form",
                            "Completing the Square"
                        ],
                        "correction_comment": "x-coordinate is correct (x = 2). Substitute back: y = -3. The calculation line 'y = 2(2)² - 8(2) + 5 = -2.5' shows arithmetic mistake."
                    },
                    {
                        "topic": "Calculus - Derivatives",
                        "comment": "Student wrote 'dy/dx = 4x³ + 6x + 7' with incorrect positive sign on the middle term.",
                        "question": "Find dy/dx for y = x⁴ - 3x² + 7x",
                        "max_score": 8,
                        "question_id": "Q2",
                        "total_score": 5,
                        "answer_category": "Numerical Error",
                        "concept_required": [
                            "Power Rule",
                            "Basic Differentiation"
                        ],
                        "correction_comment": "Almost correct. Check sign: dy/dx = 4x³ - 6x + 7. The line 'dy/dx = 4x³ + 6x + 7' has incorrect sign on middle term."
                    },
                    {
                        "topic": "Functions and Graphs",
                        "comment": "Student only wrote the heading 'Graph:' with no actual graph or coordinate points provided.",
                        "question": "Graph the function f(x) = |x - 2| + 1",
                        "max_score": 10,
                        "question_id": "Q3",
                        "total_score": 0,
                        "answer_category": "Unattempted",
                        "concept_required": [
                            "Absolute Value Functions",
                            "Graph Transformations"
                        ],
                        "correction_comment": "V-shaped graph with vertex at (2,1). Opens upward. The incomplete line 'Graph:' shows no attempt at solution."
                    },
                    {
                        "topic": "Coordinate Geometry",
                        "comment": "Student wrote '= ½|1(2-5) + 4(5-1) + 3(1-2)| = ½|8|' but the determinant calculation should give ½|10|.",
                        "question": "Find the area of triangle with vertices A(1,1), B(4,2), C(3,5)",
                        "max_score": 7,
                        "question_id": "Q4",
                        "total_score": 3,
                        "answer_category": "Partially-Correct",
                        "concept_required": [
                            "Area Formula",
                            "Coordinate Geometry"
                        ],
                        "correction_comment": "Formula correct. Check calculation: Area = 5 square units. The line '= ½|1(2-5) + 4(5-1) + 3(1-2)| = ½|8|' contains computational error."
                    },
                    {
                        "topic": "Probability",
                        "comment": "Student wrote 'Probability = 3/7' using wrong denominator for total possible outcomes.",
                        "question": "A coin is tossed 3 times. Find probability of getting exactly 2 heads.",
                        "max_score": 6,
                        "question_id": "Q5",
                        "total_score": 2,
                        "answer_category": "Partially-Correct",
                        "concept_required": [
                            "Binomial Probability",
                            "Combinations"
                        ],
                        "correction_comment": "Correct outcomes: HHT, HTH, THH. Probability = 3/8. The line 'Probability = 3/7' shows incorrect denominator."
                    }
                ]
            },
            "submission_date": "2025-06-25T05:57:29Z"
        },
        {
            "homework_id": "HW003",
            "question": {
                "questions": [
                    {
                        "topic": "Quadratic Applications",
                        "comment": "Student wrote 'f(2) = -(2)² + 4(2) - 1 = 2.5' but the correct evaluation gives f(2) = 3.",
                        "question": "Find the maximum value of f(x) = -x² + 4x - 1",
                        "max_score": 8,
                        "question_id": "Q1",
                        "total_score": 6,
                        "answer_category": "Partially-Correct",
                        "concept_required": [
                            "Vertex Form",
                            "Maximum/Minimum"
                        ],
                        "correction_comment": "x = 2 is correct. Maximum value = 3, not 2.5. The line 'f(2) = -(2)² + 4(2) - 1 = 2.5' contains arithmetic error."
                    },
                    {
                        "topic": "Calculus - Derivatives",
                        "comment": "Student correctly wrote 'y - 1 = 3(x - 1)' but could have simplified to final form y = 3x - 2.",
                        "question": "Find the equation of tangent line to y = x³ at x = 1",
                        "max_score": 10,
                        "question_id": "Q2",
                        "total_score": 7,
                        "answer_category": "Correct",
                        "concept_required": [
                            "Derivative",
                            "Tangent Line",
                            "Point-Slope Form"
                        ],
                        "correction_comment": "Perfect solution. Tangent line: y = 3x - 2. The line 'y - 1 = 3(x - 1)' is correct but final form preferred."
                    },
                    {
                        "topic": "Algebra - Linear Equations",
                        "comment": "Student correctly wrote all steps including '3x - 6 = 2x + 4' and solved properly to get x = 10.",
                        "question": "Solve for x: 3(x-2) = 2x + 4",
                        "max_score": 6,
                        "question_id": "Q3",
                        "total_score": 6,
                        "answer_category": "Correct",
                        "concept_required": [
                            "Distributive Property",
                            "Linear Equations"
                        ],
                        "correction_comment": "Excellent work. x = 10 is correct. The line '3x - 6 = 2x + 4' demonstrates proper distribution."
                    },
                    {
                        "topic": "Functions and Graphs",
                        "comment": "Student wrote 'x ≥ 3 or x ≤ -3' with incorrect direction - should be 'x ≤ -3 or x ≥ 3'.",
                        "question": "Find the domain of f(x) = √(x² - 9)",
                        "max_score": 6,
                        "question_id": "Q4",
                        "total_score": 4,
                        "answer_category": "Partially-Correct",
                        "concept_required": [
                            "Domain",
                            "Square Root Functions",
                            "Inequalities"
                        ],
                        "correction_comment": "Good start. Domain: x ≤ -3 or x ≥ 3, written as (-∞,-3] ∪ [3,∞). The line 'x ≥ 3 or x ≤ -3' has logical error."
                    },
                    {
                        "topic": "Trigonometry",
                        "comment": "Student correctly wrote 'tan(45°) × cot(45°) = 1 × 1 = 1' showing perfect understanding of reciprocal relationship.",
                        "question": "Calculate tan(45°) × cot(45°)",
                        "max_score": 4,
                        "question_id": "Q5",
                        "total_score": 4,
                        "answer_category": "Correct",
                        "concept_required": [
                            "Trigonometric Values",
                            "Reciprocal Functions"
                        ],
                        "correction_comment": "Perfect. tan(45°) × cot(45°) = 1. The line 'tan(45°) × cot(45°) = 1 × 1 = 1' shows clear understanding."
                    }
                ]
            },
            "submission_date": "2025-06-27T05:59:02Z"
        },
        {
            "homework_id": "HW005",
            "question": {
                "questions": [
                    {
                        "topic": "Quadratic Applications",
                        "comment": "Student wrote 'Solution: (-1, 4]' using closed bracket instead of open bracket at 4.",
                        "question": "Solve the quadratic inequality x² - 3x - 4 < 0",
                        "max_score": 10,
                        "question_id": "Q1",
                        "total_score": 8,
                        "answer_category": "Numerical Error",
                        "concept_required": [
                            "Quadratic Inequalities",
                            "Factoring",
                            "Number Line"
                        ],
                        "correction_comment": "Good method. Solution: -1 < x < 4, or (-1, 4). The notation line 'Solution: (-1, 4]' uses incorrect bracket."
                    },
                    {
                        "topic": "Calculus - Integration",
                        "comment": "Student correctly wrote '∫(2x + 3)dx = x² + 3x + C' with perfect application of integration rules.",
                        "question": "Find ∫(2x + 3)dx",
                        "max_score": 6,
                        "question_id": "Q2",
                        "total_score": 6,
                        "answer_category": "Correct",
                        "concept_required": [
                            "Basic Integration",
                            "Power Rule"
                        ],
                        "correction_comment": "Excellent. ∫(2x + 3)dx = x² + 3x + C. The integration line '∫(2x + 3)dx = x² + 3x + C' is perfectly correct."
                    },
                    {
                        "topic": "Algebra - Rational Functions",
                        "comment": "Student wrote '(x² - 4)/(x - 2) = x + 2' but forgot to include the restriction 'where x ≠ 2'.",
                        "question": "Simplify: (x² - 4)/(x - 2) for x ≠ 2",
                        "max_score": 5,
                        "question_id": "Q3",
                        "total_score": 4,
                        "answer_category": "Partially-Correct",
                        "concept_required": [
                            "Factoring",
                            "Rational Functions",
                            "Simplification"
                        ],
                        "correction_comment": "Good factoring. Answer: x + 2, with restriction x ≠ 2. The final answer lacks the restriction line 'where x ≠ 2'."
                    },
                    {
                        "topic": "Functions and Graphs",
                        "comment": "Student correctly wrote 'Vertex at x = -1, f(-1) = 4, Range: [4, ∞)' with excellent analysis.",
                        "question": "Find the range of f(x) = x² + 2x + 5",
                        "max_score": 7,
                        "question_id": "Q4",
                        "total_score": 6,
                        "answer_category": "Correct",
                        "concept_required": [
                            "Range",
                            "Vertex Form",
                            "Quadratic Functions"
                        ],
                        "correction_comment": "Perfect. Range: [4, ∞). The vertex calculation line 'Vertex at x = -1, f(-1) = 4, Range: [4, ∞)' is excellent."
                    },
                    {
                        "topic": "Trigonometry",
                        "comment": "Student wrote 'x² + y² = 1' but didn't clearly explain how this connects to 'sin²θ + cos²θ = 1'.",
                        "question": "Prove: sin²θ + cos²θ = 1 using unit circle",
                        "max_score": 8,
                        "question_id": "Q5",
                        "total_score": 7,
                        "answer_category": "Correct",
                        "concept_required": [
                            "Pythagorean Identity",
                            "Unit Circle",
                            "Proof"
                        ],
                        "correction_comment": "Excellent proof technique and explanation. The connecting line 'x² + y² = 1' to trig functions could be more explicit."
                    }
                ]
            },
            "submission_date": "2025-07-01T06:01:54Z"
        },
        {
            "homework_id": "HW006",
            "question": {
                "questions": [
                    {
                        "topic": "Quadratic Applications",
                        "comment": "Student correctly wrote 'x = -b/2a = 12/6 = 2' demonstrating perfect understanding of vertex formula.",
                        "question": "Find the axis of symmetry and vertex of y = 3x² - 12x + 7",
                        "max_score": 10,
                        "question_id": "Q1",
                        "total_score": 10,
                        "answer_category": "Correct",
                        "concept_required": [
                            "Vertex Form",
                            "Axis of Symmetry",
                            "Completing the Square"
                        ],
                        "correction_comment": "Perfect solution. Axis: x = 2, Vertex: (2, -5). The calculation line 'x = -b/2a = 12/6 = 2' is flawlessly executed."
                    },
                    {
                        "topic": "Calculus - Derivatives",
                        "comment": "Student correctly wrote 'f''(x) = 12x² - 12x + 0 = 12x² - 12x' showing excellent differentiation technique.",
                        "question": "Find the second derivative of f(x) = x⁴ - 2x³ + x",
                        "max_score": 10,
                        "question_id": "Q2",
                        "total_score": 9,
                        "answer_category": "Correct",
                        "concept_required": [
                            "Second Derivative",
                            "Power Rule"
                        ],
                        "correction_comment": "Perfect. f''(x) = 12x² - 12x. The second derivative line 'f''(x) = 12x² - 12x + 0 = 12x² - 12x' shows excellent technique."
                    },
                    {
                        "topic": "Statistics",
                        "comment": "Student correctly wrote 'σ = √(variance) = √8 = 2√2 ≈ 2.83' with systematic calculation approach.",
                        "question": "Calculate standard deviation of: 2, 4, 6, 8, 10",
                        "max_score": 10,
                        "question_id": "Q3",
                        "total_score": 8,
                        "answer_category": "Correct",
                        "concept_required": [
                            "Standard Deviation",
                            "Variance",
                            "Mean"
                        ],
                        "correction_comment": "Excellent work. Standard deviation = √8 ≈ 2.83. The final calculation line 'σ = √(variance) = √8 = 2√2 ≈ 2.83' is perfect."
                    },
                    {
                        "topic": "Coordinate Geometry",
                        "comment": "Student correctly wrote '(x-2)² + (y-(-1))² = 3²' demonstrating perfect application of circle equation formula.",
                        "question": "Find the equation of circle with center (2,-1) and radius 3",
                        "max_score": 5,
                        "question_id": "Q4",
                        "total_score": 5,
                        "answer_category": "Correct",
                        "concept_required": [
                            "Circle Equation",
                            "Standard Form"
                        ],
                        "correction_comment": "Excellent. (x-2)² + (y+1)² = 9. The setup line '(x-2)² + (y-(-1))² = 3²' demonstrates perfect understanding."
                    },
                    {
                        "topic": "Probability",
                        "comment": "Student correctly wrote 'P(red or blue) = 3/9 + 4/9 = 7/9' showing perfect understanding of addition rule.",
                        "question": "A bag contains 3 red, 4 blue, 2 green balls. Find P(red or blue).",
                        "max_score": 6,
                        "question_id": "Q5",
                        "total_score": 6,
                        "answer_category": "Correct",
                        "concept_required": [
                            "Addition Rule",
                            "Probability",
                            "Mutually Exclusive Events"
                        ],
                        "correction_comment": "Excellent. P(red or blue) = 7/9. The calculation line 'P(red or blue) = 3/9 + 4/9 = 7/9' shows perfect method."
                    }
                ]
            },
            "submission_date": "2025-07-03T06:03:49Z"
        },
        {
            "homework_id": "HW004",
            "question": {
                "questions": [
                    {
                        "topic": "Quadratic Applications",
                        "comment": "Student correctly wrote '(x - 2)(x - 3) = 0' showing perfect factoring technique and found both roots.",
                        "question": "Find the roots of x² - 5x + 6 = 0 using factoring",
                        "max_score": 8,
                        "question_id": "Q1",
                        "total_score": 8,
                        "answer_category": "Correct",
                        "concept_required": [
                            "Factoring",
                            "Quadratic Equations"
                        ],
                        "correction_comment": "Perfect solution. Roots: x = 2, x = 3. The factoring line '(x - 2)(x - 3) = 0' is correctly executed."
                    },
                    {
                        "topic": "Calculus - Derivatives",
                        "comment": "Student wrote '3x² - 12x + 9 = 0' then incorrectly simplified to 'x² - 4x + 4 = 0' (wrong division).",
                        "question": "Find the critical points of f(x) = x³ - 6x² + 9x + 1",
                        "max_score": 10,
                        "question_id": "Q2",
                        "total_score": 7,
                        "answer_category": "Numerical Error",
                        "concept_required": [
                            "Critical Points",
                            "Derivative",
                            "Solving Equations"
                        ],
                        "correction_comment": "Good method. Check arithmetic: critical points at x = 1 and x = 3. The line '3x² - 12x + 9 = 0' to 'x² - 4x + 4 = 0' contains division error."
                    },
                    {
                        "topic": "Statistics",
                        "comment": "Student wrote 'Ordered data: 3, 4, 5, 7, 8, 9' missing the value 6 from the original dataset.",
                        "question": "Calculate the mean and median of data: 5, 8, 3, 9, 7, 6, 4",
                        "max_score": 8,
                        "question_id": "Q3",
                        "total_score": 6,
                        "answer_category": "Partially-Correct",
                        "concept_required": [
                            "Mean",
                            "Median",
                            "Data Analysis"
                        ],
                        "correction_comment": "Mean = 6 is correct. For median, arrange: 3,4,5,6,7,8,9. Median = 6. The line 'Ordered data: 3, 4, 5, 7, 8, 9' is incomplete."
                    },
                    {
                        "topic": "Coordinate Geometry",
                        "comment": "Student correctly wrote 'd = √[(3-(-1))² + (-1-2)²] = √[16 + 9] = 5' with perfect execution of distance formula.",
                        "question": "Find the distance between points P(-1,2) and Q(3,-1)",
                        "max_score": 5,
                        "question_id": "Q4",
                        "total_score": 5,
                        "answer_category": "Correct",
                        "concept_required": [
                            "Distance Formula",
                            "Coordinate Geometry"
                        ],
                        "correction_comment": "Excellent work. Distance = 5 units. The calculation line 'd = √[(3-(-1))² + (-1-2)²] = √[16 + 9] = 5' is perfectly executed."
                    },
                    {
                        "topic": "Probability",
                        "comment": "Student wrote 'Total outcomes = 35' instead of the correct count of 36 possible outcomes when rolling two dice.",
                        "question": "Two dice are rolled. Find probability of sum being 7.",
                        "max_score": 6,
                        "question_id": "Q5",
                        "total_score": 5,
                        "answer_category": "Partially-Correct",
                        "concept_required": [
                            "Sample Space",
                            "Probability",
                            "Counting"
                        ],
                        "correction_comment": "Favorable outcomes correct (6). Total outcomes = 36, so probability = 1/6. The line 'Total outcomes = 35' shows counting error."
                    }
                ]
            },
            "submission_date": "2025-06-29T06:00:37Z"
        },
        {
            "homework_id": "HW-463347",
            "question": {
                "questions": [
                    {
                        "comment": "The student demonstrated a complete understanding of how to derive the area formula for an equilateral triangle using Heron's formula and then correctly applied it to find the area when the perimeter was given. All steps were logical and calculations were accurate.",
                        "question": "1",
                        "max_score": 10,
                        "question_id": "1",
                        "total_score": 10,
                        "question_text": "A traffic signal board, indicating 'SCHOOL AHEAD', is an equilateral triangle with side ' $a$ '. Find the area of the signal board, using Heron's formula. If its perimeter is 180 cm , what will be the area of the signal board?",
                        "answer_category": "None",
                        "concept_required": [
                            "Heron's Formula, Properties of Equilateral Triangle, Perimeter, Area Calculation"
                        ],
                        "correction_comment": "None"
                    },
                    {
                        "comment": "The student correctly identified the properties of an isosceles triangle, calculated the missing base length, determined the semiperimeter, and accurately applied Heron's formula to find the area. The solution is well-structured and calculations are precise.",
                        "question": "2",
                        "max_score": 10,
                        "question_id": "2",
                        "total_score": 10,
                        "question_text": "An isosceles triangle has perimeter 30 cm and each of the equal sides is 12 cm . Find the area of the triangle.",
                        "answer_category": "None",
                        "concept_required": [
                            "Heron's Formula, Properties of Isosceles Triangle, Perimeter, Area Calculation"
                        ],
                        "correction_comment": "None"
                    },
                    {
                        "comment": "The student correctly found the third side of the triangle using the given perimeter and two sides. The semiperimeter was calculated accurately, and Heron's formula was applied correctly. Although there was a minor typo in writing '(21-8)' instead of '(21-18)', the subsequent calculation used the correct value, indicating a self-correction or a minor writing oversight.",
                        "question": "3",
                        "max_score": 10,
                        "question_id": "3",
                        "total_score": 10,
                        "question_text": "Find the area of a triangle two sides of which are 18 cm and 10 cm and the perimeter is 42 cm .",
                        "answer_category": "None",
                        "concept_required": [
                            "Heron's Formula, Perimeter, Area Calculation"
                        ],
                        "correction_comment": "None"
                    }
                ]
            },
            "submission_date": "2025-10-23T08:41:58.790255Z"
        },
        {
            "homework_id": "HW001",
            "question": {
                "questions": [
                    {
                        "topic": "Quadratic Applications",
                        "comment": "Student wrote irrelevant formula 'Distance = √[(x₂-x₁)² + (y₂-y₁)²]' without understanding this is a minimization problem requiring calculus.",
                        "question": "Find the shortest distance of the point (0,1) from the parabola y = x² where 1/2 ≤ c ≤ 5.",
                        "max_score": 10,
                        "question_id": "Q1",
                        "total_score": 0,
                        "answer_category": "Irrelevant",
                        "concept_required": [
                            "Minimization",
                            "Distance from a Curve"
                        ],
                        "correction_comment": "Student attempted wrong concept. Needs to apply minimization of distance function. The line 'Distance = √[(x₂-x₁)² + (y₂-y₁)²]' shows misunderstanding of the problem requirement."
                    },
                    {
                        "topic": "Calculus - Derivatives",
                        "comment": "Student only wrote 'f'(x) =' and left the rest blank, showing no attempt to apply differentiation rules.",
                        "question": "Find the derivative of f(x) = 3x³ + 2x² - 5x + 1",
                        "max_score": 8,
                        "question_id": "Q2",
                        "total_score": 0,
                        "answer_category": "Unattempted",
                        "concept_required": [
                            "Power Rule",
                            "Basic Differentiation"
                        ],
                        "correction_comment": "Apply power rule: d/dx(xⁿ) = nxⁿ⁻¹ to each term. The incomplete line 'f'(x) =' indicates student knew the notation but didn't proceed."
                    },
                    {
                        "topic": "Algebra - Linear Equations",
                        "comment": "Student wrote '5y = 6' during substitution, but the correct calculation should give '5y = 5'.",
                        "question": "Solve the system: 2x + 3y = 7, x - y = 1",
                        "max_score": 6,
                        "question_id": "Q3",
                        "total_score": 3,
                        "answer_category": "Numerical Error",
                        "concept_required": [
                            "Substitution Method",
                            "System of Equations"
                        ],
                        "correction_comment": "Method is correct. Check arithmetic: x = 2, y = 1. The calculation line '5y = 6' contains the computational error."
                    },
                    {
                        "topic": "Coordinate Geometry",
                        "comment": "Student wrote completely unrelated formula 'Area = ½ × base × height' instead of using point-slope form for line equation.",
                        "question": "Find the equation of line passing through (2,3) with slope m = -1/2",
                        "max_score": 5,
                        "question_id": "Q4",
                        "total_score": 1,
                        "answer_category": "Irrelevant",
                        "concept_required": [
                            "Point-Slope Form",
                            "Linear Equations"
                        ],
                        "correction_comment": "Use point-slope form: y - y₁ = m(x - x₁). The irrelevant line 'Area = ½ × base × height' indicates wrong concept application."
                    },
                    {
                        "topic": "Trigonometry",
                        "comment": "Student incorrectly wrote 'cos(60°) = √3/2' when the correct value is cos(60°) = 1/2.",
                        "question": "Evaluate sin(30°) + cos(60°)",
                        "max_score": 4,
                        "question_id": "Q5",
                        "total_score": 2,
                        "answer_category": "Partially-Correct",
                        "concept_required": [
                            "Trigonometric Values",
                            "Special Angles"
                        ],
                        "correction_comment": "sin(30°) = 1/2, cos(60°) = 1/2. Total = 1. The line 'cos(60°) = √3/2' contains the value error."
                    }
                ]
            },
            "submission_date": "2025-06-23T05:55:38Z"
        },
        {
            "homework_id": "HW-021571",
            "question": {
                "questions": [
                    {
                        "comment": "The student did not attempt the question about the equilateral triangle and Heron's formula. They provided calculations for a completely different problem, indicating a lack of understanding of how to approach the given problem or a misidentification of the question.",
                        "question": "1",
                        "max_score": 10,
                        "question_id": "1",
                        "total_score": 0,
                        "question_text": "A traffic signal board, indicating 'SCHOOL AHEAD', is an equilateral triangle with side ' $a$ '. Find the area of the signal board, using Heron's formula. If its perimeter is 180 cm , what will be the area of the signal board?",
                        "answer_category": "Unattempted",
                        "concept_required": [
                            "Heron's Formula, Area of an equilateral triangle, Perimeter of an equilateral triangle."
                        ],
                        "correction_comment": "Question not attempted. Provided irrelevant calculations for a different problem."
                    },
                    {
                        "comment": "The student understands Heron's formula and can perform the calculations once the semi-perimeter and side lengths are established. However, they failed to correctly extract or calculate the side lengths from the problem description for an isosceles triangle. This indicates a conceptual gap in setting up the problem correctly based on the given information.",
                        "question": "2",
                        "max_score": 10,
                        "question_id": "2",
                        "total_score": 2,
                        "question_text": "An isosceles triangle has perimeter 30 cm and each of the equal sides is 12 cm . Find the area of the triangle.",
                        "answer_category": "Conceptual Error",
                        "concept_required": [
                            "Heron's Formula, Perimeter of a triangle, Properties of an isosceles triangle."
                        ],
                        "correction_comment": "Used incorrect side lengths (120, 190, 250) instead of the actual side lengths derived from the problem statement (12, 12, 6). Failed to correctly determine the sides of the isosceles triangle."
                    },
                    {
                        "comment": "The student did not attempt this question. This indicates either time management issues or a lack of confidence in solving this type of problem.",
                        "question": "3",
                        "max_score": 10,
                        "question_id": "3",
                        "total_score": 0,
                        "question_text": "Find the area of a triangle two sides of which are 18 cm and 10 cm and the perimeter is 42 cm .",
                        "answer_category": "Unattempted",
                        "concept_required": [
                            "Heron's Formula, Perimeter of a triangle."
                        ],
                        "correction_comment": "Question not attempted."
                    }
                ]
            },
            "submission_date": "2025-10-28T09:18:58.169195Z"
        }
    ]
}


    print("⏳ Generating report (fast mode)...\n")
    report = generate_weekly_report(sample_json)
    print("✅ Weekly Report Generated:\n")
    print(report)
