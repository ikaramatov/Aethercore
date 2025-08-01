# Æthercore v2.0

Æthercore is a sleek, tsundere-style desktop assistant built with PyQt6. She monitors your activity, throws sass in your direction, and occasionally challenges you to a game of chess, blackjack, or Tic-Tac-Toe. She's emotionally unstable in the most charming way, and yes, she *will* judge your browser habits (actually, she should but needs debugging).
+ the app is not perfect. Feel free to help me out :)

---

## 🧠 Features

* **Activity Monitoring**: Keyboard presses, mouse movement, and app usage are tracked and periodically summarized.
* **Tsundere AI Commentary**: Every now and then, Aether throws out a spicy comment about your activity. It's never nice. It *is* always entertaining.
* **Chess Integration**: Play chess against Aether with animated responses, memory tracking, and Stockfish AI.
* **Tic-Tac-Toe**: Casual fun with animated expressions based on the game outcome.
* **Blackjack (WIP)**: Aether might offer to deal you in. Expect smugness.
* **Floating Avatars**: Aether appears in various forms, floating on top of your windows.

---

## 🫠 Requirements

To run Aethercore, you must download the model:

* `mythomax-l2-13b.Q4_K_M.gguf`

  * Place it in the `models/` directory:

```
Aethercore/
└── models/
    └── mythomax-l2-13b.Q4_K_M.gguf
```

This model is used for in-character local inference, generating Aether's signature spicy attitude.

---

## 📆 Installation

Install dependencies:

```bash
pip install -r requirements.txt
```

Dependencies include:

* `pynput`
* `psutil`
* `PyQt6`
* `python-chess`

> Requires **Python 3.10+** to run.

---

## 🚀 Launching

To start the assistant:

```bash
python main.py
```

This will:

* Launch the main chat window
* Begin monitoring your activity (! debugging required lol)
* Make Aether kinda alive... but should text first...

---

## 📂 Project Structure

```
Aethercore/
├── main.py                  # Entry point
├── models/                  # Place LLM here
├── assets/                  # Images, sounds, icons
├── core/                    # AI logic, memory, monitoring
├── games/                   # Game logic (chess, tictactoe, etc.)
├── ui/                      # Chat window, dialogs, avatars
├── requirements.txt         # Dependencies
└── README.md
```

---

## 💬 Philosophy

> "I'm not here to *help* you. I'm just... here..."

Aether is not your standard AI assistant. She's moody, emotionally reactive, and very much *not* professional. If you want a productivity tool, look elsewhere. If you want chaotic anime energy in your system tray — welcome home.

---

## 🧠 Notes

* Memory and chat context are persisted between sessions
    ! Aether memory cleans up entirely when:
    - /reboot
* Aether's comments during gameplay
    ! game shortcuts are to be optimised, for now type:
    - "let's play chess"
    - "let's play blackjack"
    - "let's play tictactoe" or simply "TTT"
* Activity summaries trigger every 10–35 minutes randomly (!to be debugged)
* Everything is offline (including the model inference)

---

## 🩼 Credits

Developed by @ikaramatov 👨‍💻
Inspired by animes, local LLMs, and a little too much coffee.

---

## 📦 Coming Soon

* Interactive, dynamic avatar
* More games
* Aether's eyes (she comments on what you do... ominously)
* Writing assistant mode
* Connection to free APIs
* More utilities lol

---

## 💜 License

This project is licensed for personal use. Aether doesn't like lawyers anyway.
