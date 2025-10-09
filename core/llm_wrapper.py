from dotenv import load_dotenv
import os

# Load .env file (if exists)
load_dotenv()

USE_LLAMA = os.getenv('USE_LLAMA', 'false').lower() == 'true'
LLAMA_PATH = os.getenv('LLAMA_PATH', '')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', '')
OLLAMA_CONTEXT_LENGTH = int(os.getenv('OLLAMA_CONTEXT_LENGTH', 4096))
OLLAMA_KV_CACHE_TYPE = os.getenv('OLLAMA_KV_CACHE_TYPE', 'q4_0')

class LLMWrapper:
    def __init__(self):
        self.use_llama = USE_LLAMA and LLAMA_PATH
        if self.use_llama:
            try:
                from llama_cpp import Llama
                self.model = Llama(model_path=LLAMA_PATH)
            except Exception as e:
                print('Failed to init llama-cpp:', e)
                self.use_llama = False

    def chat(self, messages, temperature=0.2, max_tokens=512):
        if self.use_llama:
            prompt = '\n'.join([f"{m['role'].upper()}: {m['content']}" for m in messages])
            resp = self.model(prompt, max_tokens=max_tokens, temperature=temperature)
            return resp.get('choices', [{}])[0].get('text', '')
        else:
            try:
                import openai
                openai.api_key = OPENAI_API_KEY
                resp = openai.ChatCompletion.create(
                    model='gpt-3.5-turbo',
                    messages=messages,
                    temperature=temperature,
                    max_tokens=max_tokens,
                )
                return resp['choices'][0]['message']['content']
            except Exception as e:
                print('OpenAI call failed (ensure API key or local llama):', e)
                return "[LLM unavailable]"


llm = LLMWrapper()

def ask_system(system_prompt: str, user_prompt: str, temperature=0.2):
    messages = [
        {'role': 'system', 'content': system_prompt},
        {'role': 'user', 'content': user_prompt}
    ]
    
    return llm.chat(messages, temperature=temperature)
