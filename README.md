# MockMate-AI — Resume to Interviewer (Hackathon MVP)

MockMate-AI is a hackathon-ready MVP that converts a candidate's resume into a tailored interviewer persona and runs a simulated interview with live questions and feedback. This project is optimized for quick demos and can use a small local LLM (llama-cpp-python) or OpenAI as a fallback. It also includes optional offline TTS for question playback.

## 🚀 Key Features

| Feature | Description |
|----------|-------------|
| 🧾 **Resume Parsing** | Automatically extracts name, skills, experience, and summary from `.pdf` or `.docx` resumes. |
| 🧠 **Persona Builder** | Creates a mock interviewer persona based on your role, seniority, and technical stack. |
| 🎤 **Voice Mode (Optional)** | Supports TTS via **pyttsx3** or **ElevenLabs**; allows microphone-based interaction (if enabled). |
| 💬 **Conversational AI** | Uses a local lightweight LLM (Llama-cpp or Gemma-mini) for offline, latency-free mock interviews. |
| 🪄 **Feedback Generator** | Provides personalized feedback and improvement suggestions after each mock round. |
| 🌐 **Offline First** | Runs fully offline with local models and minimal dependencies (perfect for hackathon demos). |

---

## Repo Structure
```
mockmate-ai/
├── app.py
├── README.md
├── requirements.txt
├── requirements-lite.txt
├── setup.sh
├── .env.example
├── core/
│   ├── parser.py
│   ├── persona_builder.py
│   ├── llm_wrapper.py
│   ├── interviewer_agent.py
│   └── feedback_generator.py
├── utils/
│   └── prompt_templates.py
└── data/
    └── samples/
```

## ⚙️ Setup

### 🧩 1. Clone the Repository
```bash
git clone https://github.com/<username>/mockmate-ai.git
cd mockmate-ai
```

### 🧩 2. Run Lightweight Setup Script
```bash
bash setup.sh
```

### 🧩 3. Run the App
```bash
streamlit run app.py
```

## 🎙️ Optional: Enable ElevenLabs Voice Output

If you want lifelike AI interviewer voice, add your ElevenLabs API key in .env:
```bash
ELEVENLABS_API_KEY=your_api_key_here
USE_ELEVENLABS_TTS=true
```

The system will gracefully fall back to pyttsx3 if unavailable.

## 🧠 Model Configuration

By default, the system uses a lightweight local LLM:

- llama-cpp-python (for Llama 2/3 GGUF models)
- Optional: HuggingFace Transformers backend for online use

To use a specific model, update .env:
```bash
LLM_MODEL_PATH=models/llama-2-7b.gguf
```

You can also switch to Ollama or Gemma-mini with minimal code change in llm_wrapper.py.

## 🧩 Supported Skills (Sample)

#### Technical Skills:
`AS400, RPGLE, IBMi, SYNON, Spring Boot, REST, Microservices, AWS`

#### Role-Based Skills:
`Project Management, Team Mentoring, Stakeholder Management, Agile Delivery, Requirement Estimation, Delivery Planning`

The interviewer dynamically generates relevant questions from these.

## 🧪 Example Interaction
```
👩‍💼 AI Interviewer: Hi there! I noticed you’ve got solid AS400 and Spring Boot experience.
Could you walk me through how you integrated legacy IBM i systems with modern microservices?

🧑 Candidate: Sure, we used message queues with SQS and built REST interfaces using Spring Boot...

👩‍💼 AI Interviewer: Interesting. What was your approach to transaction reliability and retry logic?

💬 Feedback: Good coverage! You might elaborate on SQS DLQs and error handling patterns next time.
```
