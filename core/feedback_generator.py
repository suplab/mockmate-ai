# core/feedback_generator.py
from core.interviewer_agent import evaluate_answer
import re

def generate_feedback(answer: str, context: str, persona: dict) -> dict:
    """
    Generate structured feedback for a candidate answer using persona-aware prompts.
    """
    raw_dict = evaluate_answer(answer, context, persona)  # pass persona
    raw_text = raw_dict['raw']

    m = re.search(r"(\d+(?:\.\d+)?)", raw_text)
    score = None
    if m:
        try:
            score = float(m.group(1))
        except:
            score = None

    return {
        'raw': raw_text,
        'score': score
    }

