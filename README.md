Snake Game with AI (Python + Pygame)

# Overview

This project is a classic **Snake Game** inspired by old Nokia phones, built using **Python and Pygame**.
It includes both **manual gameplay** and an **AI-controlled mode** powered by a pathfinding algorithm.

The project demonstrates core concepts of:

* Object-Oriented Programming (OOP)
* Game loop architecture
* Event-driven programming
* Basic Artificial Intelligence (AI)

---

# Features

# Gameplay

* Classic snake movement
* Food spawning system
* Score tracking
* Collision detection (wall & self)

# Game System

* Game Over screen
* Restart option (`R` key)
* Quit option (`Q` key)

# AI Mode

* Toggle AI using `A` key
* AI uses **Breadth-First Search (BFS)** to find shortest path to food
* Fallback logic to avoid immediate collisions if no path is found

---

# AI Logic

The AI uses **Breadth-First Search (BFS)** to:

* Explore all possible paths from the snake’s head
* Avoid collisions with walls and its own body
* Find the shortest safe path to the food

If no path is found:

* The AI selects a **safe adjacent move** to survive temporarily

---

# Technologies Used

* **Python 3**
* **Pygame**
* **Collections (deque)** for BFS implementation

---

# Project Structure

```text
snake_game/
│
├── game.py        # Main game file
├── old.py         # first game file(old)
└── README.md      # Project documentation
```

---

# How to Run

1. Install dependencies:

```bash
pip install pygame
```

2. Run the game:

```bash
python game.py
```

---

# Controls

| Key     | Action                         |
| ------- | ------------------------------ |
| ↑ ↓ ← → | Move snake (manual mode)       |
| A       | Toggle AI mode                 |
| R       | Restart game (after game over) |
| Q       | Quit game                      |

---

# Learning Outcomes

Through this project, the following concepts were implemented:

* Game loop design (`update → draw → repeat`)
* Object-Oriented Programming (classes & responsibilities)
* Event handling in Pygame
* Collision detection logic
* Graph traversal using BFS
* Basic AI decision-making

---

# Future Improvements

* Smarter AI (survival-based path planning)
* Dynamic speed increase
* High score saving system
* Improved UI/UX (menus, animations, sounds)
* Mobile or web version

---

# Author

**Ejaj**

* Aspiring Data Analyst / AI Enthusiast
* Interested in Python, AI, and system design

---

# License

This project is for educational and portfolio purposes.

---

# Final Note

This project marks a transition from basic programming to building **interactive systems with AI behavior**.

---
