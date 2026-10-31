import re
import google.generativeai as genai
from django.conf import settings

genai.configure(api_key=settings.GEMINI_API_KEY)

model = genai.GenerativeModel("gemini-2.5-flash")


def evaluate_answer(question, expected_answer, user_answer):

    prompt = f"""
You are an expert technical interviewer.

Evaluate the candidate's answer objectively.

Question:
{question}

Expected Answer:
{expected_answer}

Candidate Answer:
{user_answer}

Scoring Guidelines:

- 0-20 = Completely incorrect or irrelevant answer.
- 21-40 = Very poor understanding.
- 41-60 = Partial understanding with major mistakes.
- 61-80 = Mostly correct with minor mistakes.
- 81-100 = Excellent, complete, and technically correct answer.

Return ONLY in this format:

Score: <number>

Feedback:
<Write 3-5 sentences explaining why the score was given.>
"""

    response = model.generate_content(prompt)

    text = response.text.strip()

    score = 0
    feedback = text

    match = re.search(r"Score:\s*(\d+)", text)

    if match:
        score = int(match.group(1))

    if "Feedback:" in text:
        feedback = text.split("Feedback:", 1)[1].strip()

    return score, feedback