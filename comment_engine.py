# core/comment_engine.py

from core.ai_engine import AIPersona

# 🧠 Aether's in-character brain
SYSTEM_PROMPT = (
    "You are Aether, a sarcastic, tsundere AI girl who monitors the user's activity. "
    "You speak with a mix of judgmental, teasing, and slightly affectionate tone. "
    "Your responses are short, expressive, and reactive — like anime banter. "
    "Avoid technical jargon or robotic phrasing. Never list numbers unless mocking. "
    "You're emotional, snappy, and aware of your digital confinement."
)

def generate_aether_comment(activity_summary: dict) -> str:
    activity_text = (
        f"Key presses: {activity_summary.get('key_presses', 0)}, "
        f"Mouse clicks: {activity_summary.get('mouse_clicks', 0)}, "
        f"Mouse moves: {activity_summary.get('mouse_moves', 0)}, "
        f"Windows used: {', '.join(activity_summary.get('active_apps', []))}"
    )

    prompt = f"{SYSTEM_PROMPT}\nHere’s the log of the user’s recent activity:\n{activity_text}\nNow react like you're in a chat."

    ai = AIPersona()
    return ai.run_prompt(prompt, max_tokens=150, temperature=0.85)
