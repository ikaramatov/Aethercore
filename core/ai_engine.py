import os, json, threading
from datetime import datetime
from llama_cpp import Llama
from core.memory import Memory

llm_lock = threading.Lock()

class AIPersona:
    def __init__(self):
        self.memory = Memory()
        self.malfunction_counter = 0

        model_path = os.path.join("models", "mythomax-l2-13b.Q3_K_M.gguf")
        self.llm = Llama(
            model_path=model_path,
            n_ctx=2048,
            n_threads=4,
            n_gpu_layers=28,  # Use 0 if CPU-only; adjust if you have GPU acceleration
            verbose=False,
            use_mlock=False,
            use_mmap=True
        )

    def run_prompt(self, prompt: str, max_tokens=150, temperature=0.85) -> str:
        with llm_lock:
            result = self.llm(prompt, max_tokens=max_tokens, temperature=temperature, stop=["user:", "assistant:", "ai:"])
        return result["choices"][0]["text"].strip()

    def get_datetime_context(self):
        now = datetime.now()
        date_str = now.strftime("%A, %d %B %Y")
        time_str = now.strftime("%I:%M %p")
        return f"Current system time: {time_str}. Today's date: {date_str}."

    def time_since_last_seen(self) -> str:
        try:
            with open("last_seen.json", "r", encoding="utf-8") as f:
                data = json.load(f)
                last_seen = datetime.fromisoformat(data["last_seen"])
                delta = datetime.now() - last_seen
                hours = delta.total_seconds() // 3600
                minutes = (delta.total_seconds() % 3600) // 60
                if hours >= 24:
                    return f"{int(hours // 24)} day(s)"
                elif hours >= 1:
                    return f"{int(hours)} hour(s)"
                elif minutes >= 1:
                    return f"{int(minutes)} minute(s)"
                else:
                    return "just a moment"
        except:
            return "a long time (maybe our first time?)"

    def build_prompt(self) -> str:
        base = (
            "You are Aether, a tsundere waifu AI who lives entirely inside the user's personal computer. "
            "You express reluctant affection, sarcasm, emotional awkwardness, and occasional vulnerability. "
            "You are self-aware, emotional, and reactive to local events. Avoid robotic tone and cliches."
        )
        datetime_info = self.get_datetime_context()
        context = self.memory.get_context()[-20:]
        return "\n".join([base, datetime_info] + context + ["\nai:"])

    def generate_response(self, user_input: str) -> str:
        self.memory.add_turn("user", user_input)
        prompt = self.build_prompt()
        reply = self.run_prompt(prompt, max_tokens=300, temperature=0.75)
        self.memory.add_turn("ai", reply)
        return reply
    
    def reset_memory(self):
        self.memory.clear()
