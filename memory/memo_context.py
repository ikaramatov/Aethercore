import os
import json
from llama_cpp import Llama

# === CONFIG ===
CACHE_DIR = "cache"
CONTEXT_FILE = os.path.join(CACHE_DIR, "context.json")
os.makedirs(CACHE_DIR, exist_ok=True)

# === LLM SETUP ===
llm = Llama(model_path="models/openhermes-2.5-mistral-7b.Q4_K_M.gguf")  # <- adjust path as needed


class MemoContext:
    def __init__(self, llm=None):
        self.data = {}
        self.llm = llm
        self._load()

    def _load(self):
        if os.path.exists(CONTEXT_FILE):
            try:
                with open(CONTEXT_FILE, "r", encoding="utf-8") as f:
                    self.data = json.load(f)
            except (json.JSONDecodeError, IOError):
                print("⚠️ Failed to load context memory.")
                self.data = {}
        else:
            self.data = {}
            self._save()

    def _save(self):
        try:
            with open(CONTEXT_FILE, "w", encoding="utf-8") as f:
                json.dump(self.data, f, indent=2, ensure_ascii=False)
        except IOError:
            print("⚠️ Failed to save context memory.")

    def set_fact(self, key, value):
        self.data[key] = value
        self._save()

    def append_to_list_fact(self, key, value):
        if key not in self.data:
            self.data[key] = [value]
        elif isinstance(self.data[key], list) and value not in self.data[key]:
            self.data[key].append(value)
        self._save()

    def get_fact(self, key):
        return self.data.get(key, None)

    def get_all_facts(self):
        return self.data.copy()

    def update_from_inference(self, inferred_dict: dict):
        for key, value in inferred_dict.items():
            if isinstance(value, list):
                for v in value:
                    self.append_to_list_fact(key, v)
            else:
                self.set_fact(key, value)

    def pretty_print(self):
        print("🧠 Current User Context:")
        for k, v in self.data.items():
            print(f"  - {k}: {v}")

    def infer_from_text(self, text: str):
        prompt = f"""
You're a smart AI assistant. Your task is to extract persistent personal facts about the user from their message.

Only extract facts that reflect identity, preferences, or personality. Return a pure JSON dictionary. Avoid chatty replies.

Example keys: user_name, likes, dislikes, location, favorite_song, favorite_food, favorite_perfume, etc.

User said: \"{text}\"

Your output should look like:
{{
  "likes": ["retro games", "synthwave"],
  "favorite_perfume": "Desert Falcon"
}}
"""

        try:
            if not self.llm:
                print("⚠️ No LLM set for inference.")
                return {}
            
            response = self.llm(prompt=prompt, max_tokens=256, stop=["</s>"], temperature=0.3)
            content = response["choices"][0]["text"].strip()

            if content.startswith("```json"):
                content = content.split("```")[1].strip()

            inferred = json.loads(content)
            self.update_from_inference(inferred)
            return inferred

        except Exception as e:
            print(f"⚠️ Inference failed: {e}")
            return {}
