import json
import uuid
from datetime import datetime
from pathlib import Path

import ollama
import streamlit as st

MODEL_NAME = "qwen3:0.6b"
CHAT_FOLDER = Path("chats")
CHAT_FOLDER.mkdir(exist_ok=True)


def make_chat():
    chat_id = str(uuid.uuid4())
    return {
        "id": chat_id,
        "title": "New Chat",
        "messages": [],
        "updated_at": datetime.now().isoformat(timespec="seconds"),
    }


def save_chat(chat):
    chat["updated_at"] = datetime.now().isoformat(timespec="seconds")
    file_path = CHAT_FOLDER / f"{chat['id']}.json"
    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(chat, file, ensure_ascii=False, indent=2)


def load_chats():
    chats = []
    for file_path in CHAT_FOLDER.glob("*.json"):
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                chat = json.load(file)
            if "id" in chat and "messages" in chat:
                chats.append(chat)
        except (json.JSONDecodeError, OSError):
            # Ignore a damaged file so the other chats can still be opened.
            continue
    chats.sort(key=lambda item: item.get("updated_at", ""), reverse=True)
    return chats


def ask_model(messages):
    # Ollama receives the full conversation so it can answer follow-up questions.
    response = ollama.chat(model=MODEL_NAME, messages=messages)
    return response["message"]["content"]


st.set_page_config(page_title="Local AI Chatbot", page_icon="💬", layout="centered")
st.title("💬 Local AI Chatbot")
st.caption(f"A simple local chatbot using Ollama and {MODEL_NAME}")

if "chat" not in st.session_state:
    saved_chats = load_chats()
    st.session_state.chat = saved_chats[0] if saved_chats else make_chat()

if "chat_list" not in st.session_state:
    st.session_state.chat_list = load_chats()

with st.sidebar:
    st.header("Chats")
    if st.button("＋ New Chat", use_container_width=True):
        st.session_state.chat = make_chat()
        st.rerun()

    st.divider()
    st.subheader("Saved conversations")
    st.session_state.chat_list = load_chats()
    chats = st.session_state.chat_list

    if chats:
        chat_options = {chat["id"]: chat for chat in chats}
        current_id = st.session_state.chat["id"]
        ids = list(chat_options.keys())
        selected_index = ids.index(current_id) if current_id in ids else 0
        selected_id = st.selectbox(
            "Open a saved chat",
            options=ids,
            index=selected_index,
            format_func=lambda chat_id: chat_options[chat_id].get("title", "Chat"),
        )
        if selected_id != st.session_state.chat["id"]:
            st.session_state.chat = chat_options[selected_id]
            st.rerun()
    else:
        st.caption("Saved chats will appear here.")

    st.divider()
    st.caption("Make sure Ollama is running on your computer.")

chat = st.session_state.chat

for message in chat["messages"]:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

user_text = st.chat_input("Type your message here...")
if user_text:
    chat["messages"].append({"role": "user", "content": user_text})

    if chat["title"] == "New Chat":
        chat["title"] = user_text.strip().replace("\n", " ")[:35]
        if len(user_text.strip()) > 35:
            chat["title"] += "..."

    save_chat(chat)

    with st.chat_message("user"):
        st.markdown(user_text)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                answer = ask_model(chat["messages"])
                st.markdown(answer)
                chat["messages"].append({"role": "assistant", "content": answer})
                save_chat(chat)
            except Exception as error:
                st.error(
                    "I could not connect to Ollama. Please check that Ollama is "
                    "installed and running, and that the model is downloaded."
                )
                st.caption(f"Technical details: {error}")
