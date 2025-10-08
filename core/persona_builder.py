from typing import Dict

def build_persona(parsed_resume: Dict) -> Dict:
    """
    Build a candidate persona from parsed resume data.

    Args:
        parsed_resume (Dict): Dictionary containing at least 'skills', 'name', 'raw_text'

    Returns:
        Dict: Persona containing candidate_name, role, seniority, expertise, tone
    """
    skills = [s.lower() for s in parsed_resume.get('skills', [])]
    name = parsed_resume.get('name') or 'Candidate'
    raw = parsed_resume.get('raw_text', '').lower()

    # Determine seniority
    seniority = 'mid'
    if any(x in raw for x in ['senior', 'lead', 'principal']):
        seniority = 'senior'
    elif any(x in raw for x in ['intern', 'junior', 'associate']):
        seniority = 'junior'

    # Determine role based on skills
    role = 'Software Engineer'
    if any(k in skills for k in ['ml', 'tensorflow', 'pytorch', 'numpy', 'pandas']):
        role = 'Data Scientist / ML Engineer'
    elif any(k in skills for k in ['aws', 'docker', 'kubernetes']):
        role = 'DevOps / Cloud Engineer'
    elif any(k in skills for k in ['as400', 'rpgle', 'ibmi', 'synon']):
        role = 'Legacy IBM i Developer'

    persona = {
        'candidate_name': name,
        'role': role,
        'seniority': seniority,
        'expertise': skills,
        'tone': 'professional'
    }

    return persona