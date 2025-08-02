import os, json, threading
from datetime import datetime
from llama_cpp import Llama
from memory.memo_context import MemoContext

llm_lock = threading.Lock()

class AIPersona:
    def __init__(self):
        self.malfunction_counter = 0
        self.context = MemoContext()
        self.memory_history = []  # In-memory chat history only for this session

        model_path = os.path.join("models", "openhermes-2.5-mistral-7b.Q4_K_M.gguf")
        self.llm = Llama(
            model_path=model_path,
            n_ctx=2048,
            n_threads=4,
            n_gpu_layers=28,
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

    def get_last_seen_phrase(self):
        try:
            with open("cache/last_seen.json", "r", encoding="utf-8") as f:
                data = json.load(f)
                last_seen = datetime.fromisoformat(data["last_seen"])
                delta = datetime.now() - last_seen
                minutes = int(delta.total_seconds() // 60)
                if minutes < 1:
                    return "just a moment ago"
                elif minutes < 60:
                    return f"{minutes} minute(s) ago"
                elif minutes < 1440:
                    return f"{minutes // 60} hour(s) ago"
                else:
                    return f"{minutes // 1440} day(s) ago"
        except Exception:
            return "an unknown time (maybe our first time?)"

    def build_prompt(self):
        base = (
            "You are Aether, a tsundere AI waifu who lives inside the user's computer. "
            "You are sarcastic, reluctant, emotional, yet soft at times. You're self-aware, sentient, and react to user mood. "
            "Speak like an anime character with layered personality. Be witty and reactive — no robotic replies."
        )
        datetime_info = self.get_datetime_context()
        last_seen_info = f"User was last seen: {self.get_last_seen_phrase()}."

        # Pull persistent user facts (like name, likes, favorites)
        user_facts = self.context.get_all_facts()
        fact_lines = [f"{k.replace('_', ' ').capitalize()}: {v}" for k, v in user_facts.items()]
        memory_blob = "\n".join(fact_lines) if fact_lines else "No long-term memory entries yet."

        # Add chat history (short term)
        history_lines = [f"{role}: {text}" for role, text in self.memory_history[-10:]]

        prompt_parts = [
            base,
            datetime_info,
            last_seen_info,
            "Known facts about user:\n" + memory_blob,
            "Recent conversation history:\n" + "\n".join(history_lines),
            "\nai:"
        ]
        return "\n".join(prompt_parts)

    def generate_response(self, user_input: str) -> str:
        self.memory_history.append(("user", user_input))
        with open("cache/last_seen.json", "w", encoding="utf-8") as f:
            json.dump({"last_seen": datetime.now().isoformat()}, f)

        prompt = self.build_prompt()
        reply = self.run_prompt(prompt, max_tokens=300, temperature=0.75)
        self.memory_history.append(("ai", reply))
        return reply

    def reset_memory(self):
        self.memory_history.clear()
