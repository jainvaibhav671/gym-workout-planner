import streamlit as st
from gym_trainer.crewai.actions import answer

# Function to handle chatbot logic
def chatbot_response(user_input):
    return answer(user_input)

# Initialize session state for chat history and input field
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "user_input" not in st.session_state:
    st.session_state.user_input = ""

# Streamlit app layout
st.set_page_config(page_title="Gym Workout Planner ☍", layout="centered")
st.write("## Gym Workout Planner ☍")

# Chat history display
st.write("### Chat History")
for chat in st.session_state.chat_history:
    # User input styled on the right
    st.markdown(
        f"""
        <div style='display: flex; flex-direction: column;'>
            <div style='align-self: flex-end; background-color: #f1f1f1ff; border-radius: 999px; padding: 5px 10px; margin-bottom: 10px; width: fit-content; max-width: 70%;'>
                {chat['user']}
            </div>
        </div>
        <div style='margin-bottom: 10px;'>
            <span>{chat['bot']}</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

# Input and button in the same row with proper vertical alignment
col1, col2 = st.columns([4, 1], vertical_alignment="bottom")
with col1:
    user_input = st.text_input(
        "Type your message here", 
        label_visibility="hidden",
        value=st.session_state.user_input, 
        key="input", 
        placeholder="Enter your message...", 
        on_change=lambda: st.session_state.update({"user_input": st.session_state.input})
    )

with col2:
    send_button = st.button("Send")

# Process the input when the button is clicked
if send_button and st.session_state.user_input:
    print(st.session_state.user_input)
    with st.spinner("Bot is typing..."):
        response = chatbot_response(st.session_state.user_input)
        st.session_state.chat_history.append({"user": st.session_state.user_input, "bot": response})
        st.session_state.user_input = ""  # Clear input field
    st.rerun()  # Refreshes the app to show the updated chat
