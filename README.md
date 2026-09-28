# Memory-Powered Customer Support Agent

A simple support assistant that learns from live customer conversations and stores only useful long-term context with Hindsight.

## What this project does
- Creates a customer profile from the app UI
- Gives each customer a unique Hindsight memory bank
- Stores useful long-term details such as preferences, device information, recurring issues, and past fixes
- Recalls the most relevant memories before responding
- Keeps the answer short and focused on the current question
- Keeps customer memory isolated per profile

## Core flow
1. User creates a new customer profile in the sidebar
2. A unique Hindsight bank is created for that profile
3. The user chats with the agent
4. The agent retains only useful support context
5. Later requests trigger Hindsight recall
6. The LLM answers with short, personalized help

## How Hindsight is used
- `retain` stores useful long-term customer information in the profile memory bank
- `recall` fetches the most relevant memory for the current message
- `reflect` summarizes the customer's pattern and support history

## Setup
1. Create a Python environment if needed
2. Install dependencies: `pip install -r requirements.txt`
3. Add your keys in the `.env` file:
   - `GROQ_API_KEY`
   - `HINDSIGHT_URL`
   - `HINDSIGHT_API_KEY`
4. Run: `streamlit run app.py`

## Hackathon demo flow
1. Open the app and click `+ Create New Profile`
2. Enter a customer name
3. Start a conversation such as: "I use Android and prefer short answers."
4. Continue the chat and let the agent learn useful context
5. Start a fresh conversation and ask a follow-up question
6. The app should answer using relevant memory from that profile only

## Project files
- `app.py` – Streamlit UI and profile creation flow
- `agent.py` – Hindsight + Groq logic, remember/recall/reflect behavior
- `.env` – environment configuration for API keys
