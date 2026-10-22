# Local AI Chatbot

A small beginner-friendly chatbot project made with Python, Streamlit, and Ollama.
It runs on your computer and saves conversations as JSON files.

## Features

- Chat with the local `qwen3:0.6b` model.
- Keep earlier messages in the current conversation.
- Start a new chat.
- Open saved conversations from the sidebar.
- Save chats locally so they are still available after restarting.
- Show a helpful message if Ollama is not available.

## Requirements

- Python 3.10 or newer
- Visual Studio Code (recommended)
- Ollama
- Internet access for the initial software/model downloads

## Setup on Windows

1. Install Python from https://www.python.org/downloads/
2. Install Ollama from https://ollama.com/download
3. Open Command Prompt or the VS Code terminal.
4. Go to this project folder:

   ```powershell
   cd path\to\Local_AI_Chatbot
   ```

5. Create a virtual environment:

   ```powershell
   python -m venv venv
   ```

6. Activate it:

   ```powershell
   .\venv\Scripts\activate
   ```

7. Install the libraries:

   ```powershell
   pip install -r requirements.txt
   ```

8. Download the model:

   ```powershell
   ollama pull qwen3:0.6b
   ```

9. Start Ollama if it is not already running. Then start the app:

   ```powershell
   streamlit run app.py
   ```

10. Streamlit should open the app in your browser. If it does not, open the local URL printed in the terminal (usually http://localhost:8501).

## How to use it

- Type a message in the input at the bottom and press Enter.
- The chatbot sends the conversation history to Ollama.
- Click **New Chat** to begin a separate conversation.
- Choose a saved conversation in the sidebar to reopen it.

## Where chats are saved

Each conversation is stored in its own JSON file inside the `chats` folder. Do not delete those files if you want to keep your conversations.

## Troubleshooting

- If the model is missing, run `ollama pull qwen3:0.6b`.
- If the app cannot connect, make sure Ollama is installed and running.
- If `streamlit` is not recognized, activate the virtual environment and run `pip install -r requirements.txt` again.
