from core.llm_wrapper import ask_system

def summarize_resume(skills: list, raw_text: str) -> str:
    prompt = f"""
    Summarize the following resume focusing on the candidate’s skills and technical experience.
    Only return a concise summary for interview context.
    Skills : {', '.join(skills)}
    Resume text: {raw_text[:1500]}  # truncate long text for efficiency
    """
    summary = ask_system(
        "You are a concise summarizer that outputs skill-focused summaries for interview context.",
        prompt,
        temperature=0.2
    )
    return summary.strip()
