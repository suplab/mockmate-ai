# app.py - MockMate-AI (Resume -> Interviewer) - Streamlit UI
import streamlit as st
import os
from core.parser import parse_resume_file
from core.persona_builder import build_persona
from core.interviewer_agent import generate_question
from core.feedback_generator import generate_feedback

USE_TTS = os.getenv('USE_TTS', 'true').lower() == 'true'
AUDIO_DIR = os.getenv('AUDIO_DIR', './data/audio')
os.makedirs(AUDIO_DIR, exist_ok=True)

def synthesize_tts(text: str, out_path: str) -> bool:
    try:
        import pyttsx3
        engine = pyttsx3.init()
        engine.save_to_file(text, out_path)
        engine.runAndWait()
        return True
    except Exception as e:
        print('TTS failed:', e)
        return False

st.set_page_config(page_title='MockMate-AI', layout='wide')
st.title('MockMate-AI — Resume to Interviewer (MVP)')

mode = st.sidebar.radio('Mode', ['Upload Resume', 'Live Q&A'])

if mode == 'Upload Resume':
    st.header('Upload a resume (PDF or DOCX)')
    uploaded = st.file_uploader('Resume file', type=['pdf', 'docx', 'doc', 'txt'])
    if uploaded:
        parsed = parse_resume_file(uploaded)
        st.success('Parsed resume')
        st.write('**Name (guess):**', parsed.get('name'))
        st.write('**Email (guess):**', parsed.get('email'))
        st.write('**Phones (guess):**', parsed.get('phones'))
        st.write('**Skills (heuristic):**', parsed.get('skills'))
        st.markdown('---')
        if st.button('Create Interview Persona'):
            persona = build_persona(parsed)
            st.session_state['persona'] = persona
            st.session_state['resume_excerpt'] = '\n'.join(parsed['raw_text'].splitlines()[:20])
            st.success('Persona created — switch to Live Q&A')
            st.json(persona)

elif mode == 'Live Q&A':
    st.header('Live Q&A with AI Interviewer')
    persona = st.session_state.get('persona')
    resume_excerpt = st.session_state.get('resume_excerpt')
    if not persona:
        st.warning('No persona found. First upload a resume and create persona in "Upload Resume" mode.')
    else:
        st.subheader(f"Interviewer for {persona.get('candidate_name')} — {persona.get('role')} ({persona.get('seniority')})")
        if 'qa_history' not in st.session_state:
            st.session_state['qa_history'] = []

        c1, c2 = st.columns([3,1])
        with c1:
            if st.button('Generate Next Question'):
                q = generate_question(persona, resume_excerpt)
                st.session_state['current_question'] = q
                st.session_state['qa_history'].append({'q': q, 'a': None, 'feedback': None})
        with c2:
            st.write('TTS')
            if st.button('Play Last Question'):
                q = st.session_state.get('current_question')
                if not q:
                    st.info('No question yet — generate one first')
                else:
                    out_path = os.path.join(AUDIO_DIR, 'last_q.mp3')
                    ok = False
                    if USE_TTS:
                        ok = synthesize_tts(q, out_path)
                    if ok and os.path.exists(out_path):
                        audio_file = open(out_path, 'rb').read()
                        st.audio(audio_file)
                    else:
                        st.error('TTS not available — showing text instead')

        st.markdown('---')
        st.write('**Question:**')
        st.write(st.session_state.get('current_question', 'No question yet — generate one'))

        answer = st.text_area('Your answer (type below):', key='answer_input')
        if st.button('Submit Answer'):
            ans = st.session_state.get('answer_input')
            current_q = st.session_state.get('current_question')
            if not current_q:
                st.error('No active question — generate one first')
            else:
                for item in reversed(st.session_state['qa_history']):
                    if item['q'] == current_q and item['a'] is None:
                        item['a'] = ans
                        context = f"Candidate: {persona['candidate_name']}\nRole: {persona['role']} ({persona['seniority']})\nSkills: {', '.join(persona['expertise'])}\nQuestion: {current_q}\nResume Excerpt: {resume_excerpt}"
                        fb = generate_feedback(ans, context, persona)
                        item['feedback'] = fb
                        break
                st.success('Answer recorded — feedback below')

        st.markdown('### Session history')
        for i, item in enumerate(st.session_state['qa_history']):
            st.markdown(f"**Q{i+1}:** {item['q']}")
            st.markdown(f"**A{i+1}:** {item.get('a') or 'No answer yet'}")
            if item.get('feedback'):
                st.markdown('**Feedback:**')
                st.write(item['feedback']['raw'])
                if item['feedback']['score'] is not None:
                    st.write('Score:', item['feedback']['score'])
            st.markdown('---')
