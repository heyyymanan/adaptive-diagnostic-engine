# AI-Driven Adaptive Diagnostic Engine

## Overview

This project implements a **1-Dimensional Adaptive Testing Engine** that dynamically estimates a student's proficiency level by selecting questions based on their previous responses.

Unlike static quizzes where every student receives the same questions, this system adapts in real-time using an **Item Response Theory (IRT) inspired model** to update the learner’s ability score. The result is a diagnostic engine capable of quickly estimating a student's skill level and generating a **personalized learning plan** based on weaknesses detected during the test.



## My Journey & Thoughtful AI Integration

I built this project to deepen my understanding of adaptive algorithms, full-stack architecture, and real-world API management. While I leveraged AI assistance to accelerate development, I intentionally used AI as a thought partner-guiding the architecture and solving technical constraints thoughtfully, rather than relying on it to blindly generate code.

**Key Engineering Decisions:**

1.  **Strategic Token Optimization (Cost Management):**
    Running this engine on free-tier LLM plans posed a significant challenge regarding token limits and request costs. I realized that sending unchecked session histories (like missed topics and difficulty scores) to the AI for study plan generation would quickly exhaust the quota. To solve this, I designed a **token-optimization heuristic**. Instead of using heavy, model-specific dependencies like `tiktoken` (which would bloat the project), I instructed the AI to help me implement a generalized 4-characters-per-token mathematical approximation. My algorithm dynamically truncates the least critical context when approaching token boundaries, ensuring the LLM integration remains cost-effective, performant, and perfectly tailored for a free-tier environment.

2.  **Item Response Theory (IRT) Implementation:**
    To make the test truly adaptive, I independently researched IRT models to calculate the probability of a correct answer using logistic curves. I then guided the project to translate these mathematical models into a performant Python algorithm (`get_next_question` and `update_ability`), ensuring rigorous criteria were met for updating the student's ability using gradient descent.

3.  **Resilient LLM Provider Architecture:**
    To prevent vendor lock-in and ensure high availability, I engineered the system to support multiple LLM providers (Google Gemini and OpenAI). If one API reaches its free-tier limit, the system can seamlessly switch to the other via simple environment configuration.

---

## System Architecture

The system is designed using a **modular backend architecture** to ensure clear separation of concerns:

- **FastAPI Backend:** Provides high-performance, asynchronous REST API endpoints.
- **MongoDB:** Stores session data, question banks, and learning progression dynamically.
- **Vanilla JS/CSS Frontend:** A clean, glassmorphism-inspired UI that communicates seamlessly with the backend.

---

## Instructions on How to Run the Project

1. **Clone the repository** to your local machine.
2. **Set up a Python virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
4. **Set up environment variables** locally in a `.env` file at the root. You need:
   ```env
   MONGO_URI=mongodb+srv://<user>:<password>@<cluster>.mongodb.net/?appName=<AppName>
   DB_NAME=adaptive_engine
   LLM_PROVIDER=gemini
   GEMINI_API_KEY=your_gemini_api_key_here
   OPENAI_API_KEY=your_openai_api_key_here
   ```
5. **Seed the database** with the initial questions:
   ```bash
   python seed_questions.py
   ```
6. **Run the FastAPI application:**
   ```bash
   uvicorn app.main:app --reload
   ```
   _The API will be available at `http://127.0.0.1:8000/docs` (Swagger UI)._
