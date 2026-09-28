"""Streamlit UI for the Customer Support Agent (Hindsight memory)."""
import uuid

import streamlit as st

from agent import (
    generate_reply,
    recall_history,
    reflect_profile,
    save_interaction,
)

st.set_page_config(page_title="Memory-Powered Support Agent", page_icon="🎧", layout="wide")


def ensure_profile_state():
    if "chats" not in st.session_state:
        st.session_state.chats = {}
    if "custom_profile" not in st.session_state:
        st.session_state.custom_profile = None
    if "show_create_form" not in st.session_state:
        st.session_state.show_create_form = False
    if "show_replace_confirm" not in st.session_state:
        st.session_state.show_replace_confirm = False


def create_customer_profile(name: str):
    clean_name = (name or "").strip()
    if not clean_name:
        raise ValueError("Name is required.")

    profile = {
        "id": f"customer-{uuid.uuid4().hex}",
        "name": clean_name,
        "plan": "",
        "env": "",
    }
    st.session_state.custom_profile = profile
    st.session_state.chats[profile["id"]] = []
    st.session_state.show_create_form = False
    st.session_state.show_replace_confirm = False
    return profile


ensure_profile_state()

# ---------------- Sidebar ----------------
with st.sidebar:
    st.header("Controls")
    st.subheader("Customer Profile")

    customer = st.session_state.custom_profile

    if customer is not None:
        selected_customer = st.selectbox(
            "Customer Profile",
            [customer],
            index=0,
            format_func=lambda c: c["name"],
        )
        st.session_state.custom_profile = selected_customer
        customer = selected_customer

    if st.button("+ Create New Profile", use_container_width=True):
        if st.session_state.custom_profile is not None:
            st.session_state.show_replace_confirm = True
        else:
            st.session_state.show_create_form = True

    if st.session_state.get("show_replace_confirm"):
        st.warning("A customer profile already exists. Creating a new profile will start a fresh customer profile and conversation. Continue?")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Continue", use_container_width=True):
                old_id = st.session_state.custom_profile["id"] if st.session_state.custom_profile else None
                if old_id and old_id in st.session_state.chats:
                    del st.session_state.chats[old_id]
                st.session_state.custom_profile = None
                st.session_state.show_replace_confirm = False
                st.session_state.show_create_form = True
                st.rerun()
        with col2:
            if st.button("Cancel", use_container_width=True):
                st.session_state.show_replace_confirm = False
                st.rerun()

    if st.session_state.get("show_create_form"):
        with st.form("create_profile_form", clear_on_submit=False):
            st.subheader("Create Customer Profile")
            name = st.text_input("Name")
            submitted = st.form_submit_button("Create Profile")
            if submitted:
                try:
                    create_customer_profile(name)
                    st.rerun()
                except ValueError as e:
                    st.error(str(e))

    if customer is not None:
        st.divider()
        if st.button("Clear this chat", use_container_width=True):
            st.session_state.chats[customer["id"]] = []
            st.rerun()

        st.divider()
        st.subheader("🧠 What the AI remembers")
        if st.button("View What the AI Remembers", use_container_width=True):
            with st.spinner("Reflecting on memories..."):
                try:
                    st.write(reflect_profile(customer))
                except Exception as e:
                    st.error(f"Reflect failed: {e}")

# ---------------- Main ----------------
customer = st.session_state.custom_profile

if customer is None:
    st.title("🎧 Memory-Powered Customer Support Agent")
    st.info("Create a customer profile to begin.")
else:
    st.title("🎧 Memory-Powered Customer Support Agent")
    st.caption(f"Talking as **{customer['name']}**")
    use_memory = st.toggle("Use Hindsight memory", value=True,
                           help="Turn OFF to show the generic 'no memory' agent.")

    chat = st.session_state.chats.setdefault(customer["id"], [])

    for turn in chat:
        with st.chat_message(turn["role"]):
            st.write(turn["content"])
            if turn["role"] == "assistant" and turn.get("memories"):
                with st.expander(f"Memories used ({len(turn['memories'])})"):
                    for m in turn["memories"]:
                        st.write("•", m)
            if turn["role"] == "assistant" and turn.get("note"):
                st.caption(f"Saved to memory: {turn['note']}")

    user_msg = st.chat_input("Type the customer's message...")

    if user_msg:
        chat.append({"role": "user", "content": user_msg})
        with st.chat_message("user"):
            st.write(user_msg)

        with st.chat_message("assistant"):
            with st.spinner("Recalling history and thinking..."):
                try:
                    memories = recall_history(customer, user_msg) if use_memory else []
                    reply = generate_reply(customer, chat, memories, use_memory)
                    st.write(reply)
                    note = None
                    try:
                        note = save_interaction(customer, user_msg, reply)
                    except Exception as e:
                        st.warning(f"Reply OK, but memory save failed: {e}")
                    chat.append({"role": "assistant", "content": reply,
                                 "memories": memories, "note": note})
                    if memories:
                        with st.expander(f"Memories used ({len(memories)})"):
                            for m in memories:
                                st.write("•", m)
                    if note:
                        st.caption(f"Saved to memory: {note}")
                except Exception as e:
                    st.error(f"Something went wrong: {e}")
