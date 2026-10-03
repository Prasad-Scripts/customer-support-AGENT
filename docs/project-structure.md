# Project Structure

## Files

- `app.py` is the Streamlit entry point. It manages customer profiles, chat history, and the support interface.
- `agent.py` connects the interface to Groq for replies and Hindsight for customer memory.
- `requirements.txt` lists the Python packages needed to run the application.
- `.devcontainer/devcontainer.json` configures the VS Code development container.
- `Images/architecture-diagram.png` shows how the application components interact.
- `.env` stores local service settings and API keys. Keep it out of version control.

## Request Flow

1. The operator selects a customer profile in the Streamlit app.
2. The app passes that customer's ID to the agent, which uses it as the Hindsight bank ID.
3. The agent recalls relevant context, asks Groq to generate a reply, and extracts a short note from the exchange.
4. The note is retained in that customer's Hindsight bank.

## Run Locally

Install dependencies with `python -m pip install -r requirements.txt`, configure `GROQ_API_KEY` and the Hindsight service settings in `.env`, then start the app with `streamlit run app.py`.