import streamlit as st
# from gym_trainer.autogen.agents import start_chat
import time

from gym_trainer.autogen.agents import get_chat_session

# Initialize session state for chat history and input field
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "user_input" not in st.session_state:
    st.session_state.user_input = ""

user, manager = get_chat_session()

# Streamlit app layout
st.set_page_config(page_title="Gym Workout Planner ☍", layout="centered")
st.write("## Gym Workout Planner ☍")

# Chat history display
for chat in st.session_state.chat_history:
    with st.chat_message("user"):
        st.write(chat["user"])

    with st.chat_message("assistant"):
        st.write(chat["bot"])

# Input and button in the same row with proper vertical alignment
user_input = st.chat_input(
    "Type your message here", 
    # label_visibility="hidden",
    # value=st.session_state.user_input, 
    key="input", 
)

# Process the input when the button is clicked
if user_input:
    with st.status("Fetching Response", expanded = True, state="running") as status:
        
        responses = user.initiate_chat(manager, message=user_input)
        chat = list(map(lambda ch: {
                   "name": ch["name"],
                   "content": ch["content"]
               }, responses.chat_history))

        st.write("chat")
        st.write(chat)
        st.session_state.chat_history.append(chat)
        status.update(label="Fetched!", state="complete")
    # with st.spinner("Bot is typing..."):
        # response = start_chat(st.session_state.user_input)
        # st.session_state.chat_history.append({"user": st.session_state.user_input, "bot": response})
        # st.session_state.user_input = ""  # Clear input field
    # st.rerun()  # Refreshes the app to show the updated chat
