import streamlit as st
import time
from gym_trainer.autogen.agents import get_chat_session
from pprint import pprint

st.cache_data.clear()
st.cache_resource.clear()

# Initialize session state for chat history and input field
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "user_input" not in st.session_state:
    st.session_state.user_input = ""

user, manager, groupchat = get_chat_session(st.session_state.chat_history)

def filter_chat_history():
    chats = st.session_state.chat_history
    n_chats = len(chats)
    user_input_indices = [i for i in range(n_chats) if chats[i]["name"] == "user" and chats[i]["role"] == "user"]

    chat_groups = []
    for i in range(len(user_input_indices)-1):
        ind1 = user_input_indices[i]
        ind2 = user_input_indices[i+1]
        chat_groups.append(chats[ind1:ind2])

    ind = user_input_indices[-1]
    chat_groups.append(chats[ind:])
    return chat_groups

st.set_page_config(page_title="Gym Workout Planner ☍", layout="centered")

n_chats = len(st.session_state.chat_history)

if n_chats == 0:
    st.write("# Welcome to the Gym Workout Planner")
    st.write("""
Provide the following information in the prompt below:\n
Age (in years)\n
Height (in cm)\n
Weight (in kg)\n

Have you ever gymmed before?\n
Do you have any physical injuries or medical conditions? Mention any specific guidelines mentioned by your doctor to follow.
""")
    pass
else:
    # Chat history display
    st.write("## Gym Workout Planner ☍")
    chat_groups = filter_chat_history()
    for chat_group in chat_groups:
        if chat_group[0]["content"] == "":
            continue

        with st.chat_message("human"):
            st.write(chat_group[0]["content"])

        n_res = len(chat_group)-1
        if n_res > 0:
            tab_names = ["Fitness Assessment", "Goals", "Exercises", "Diet Plan", "Optimized Schedule"][:n_res]
            tabs = st.tabs(tab_names)
            for x in range(n_res):
                tabs[x].write(chat_group[x+1]["content"])

# Input and button in the same row with proper vertical alignment
user_input = st.chat_input(
    "Type your message here",
    key="input", 
)

# Process the input when the button is clicked
if user_input:
    with st.status("Fetching Response", expanded = True, state="running") as status:
        n_chats = len(st.session_state.chat_history)
        if n_chats == 0:
            user.initiate_chat(manager,
                                       message=user_input,
                                       clear_history=False,
                                       silent=True)
        else:
            user_prompt = { "name": "user", "role": "user", "content": user_input }
            st.session_state.chat_history.extend([user_prompt])
            last_agent, last_message = manager.resume(st.session_state.chat_history)
            last_agent.initiate_chat(manager, message=last_message, clear_history=False)

        # pprint(groupchat.messages)
        st.session_state.chat_history = groupchat.messages
        status.update(label="Fetched!", state="complete")
        st.rerun()

