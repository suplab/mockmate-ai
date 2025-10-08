# core/interviewer_agent.py
from core.llm_wrapper import ask_system
from utils.prompt_templates import INTERVIEW_SYSTEM_PROMPT, INTERVIEW_Q_PROMPT
from utils.prompt_templates import FEEDBACK_PROMPT

MAX_SKILLS = 8 # only top 8 skills

def generate_question(persona: dict, resume_excerpt: str, max_chars=2000) -> str:
    sys = INTERVIEW_SYSTEM_PROMPT
    user = INTERVIEW_Q_PROMPT.format(
        role=persona['role'],
        seniority=persona['seniority'],
        candidate_name=persona['candidate_name'],
        skills=', '.join(persona['expertise'][:MAX_SKILLS]),
        resume_excerpt=resume_excerpt or ''
        )
    
    # truncate prompt safely by characters
    if len(prompt) > max_chars:
        prompt = prompt[:max_chars]

    resp = ask_system(sys, user, temperature=0.3)
    return resp.strip()

def evaluate_answer(answer: str, context: str, persona: dict) -> dict:
    """
    Evaluate candidate answer using persona-aware feedback prompt.
    
    Returns a dictionary with:
        - raw: raw feedback string from LLM
        - score: optional numeric score (if parseable)
    """

    user_prompt = FEEDBACK_PROMPT.format(
        role=persona['role'],
        seniority=persona['seniority'],
        candidate_name=persona['candidate_name'],
        skills=', '.join(persona['expertise']),
        answer=answer,
        context=context
    )

    resp = ask_system(INTERVIEW_SYSTEM_PROMPT, user_prompt, temperature=0.2)
    return {
        'raw': resp.strip(),
        'score': None  # optionally parse score from resp if structured
    }

