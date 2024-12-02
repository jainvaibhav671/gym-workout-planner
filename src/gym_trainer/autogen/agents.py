from pprint import pprint

from autogen.oai.openai_utils import Assistant
import streamlit as st
from autogen import AssistantAgent, GroupChat, GroupChatManager, UserProxyAgent
from autogen.agentchat.contrib.retrieve_assistant_agent import RetrieveAssistantAgent
from autogen.agentchat.contrib.retrieve_user_proxy_agent import RetrieveUserProxyAgent
from autogen.retrieve_utils import TEXT_FORMATS

from gym_trainer.autogen.utils import get_llm_config
from gym_trainer.utils import get_data_paths

llm_config = get_llm_config()

# Custom termination condition
def termination_condition(response):
    # Terminate if the message contains the specific phrase
    return "I need the following information:" in response["content"]

def custom_input_function(prompt: str) -> str:
    if "input" not in st.session_state:
        return ""
    return st.session_state.input_input or ""

# Common arguments for all assistant agents
common_args = dict(
    llm_config=llm_config,
    human_input_mode="NEVER",
    max_consecutive_auto_reply=1,
    is_termination_msg=termination_condition,
    code_execution_config=False
)

user_input_agent = AssistantAgent(
    name="UserInputAgent",
    system_message="""
    You are a fitness evaluator responsible for gathering and summarizing all necessary user details. 
    - If more information is needed, write "I need the following information:" followed by specific questions.
    - Assume non-critical information (e.g., general fitness level) if the user has not explicitly provided it.
    - STRICTLY do NOT generate or list plans, goals, schedules, or any analysis. Your sole responsibility is to summarize user input.
    """,
    **common_args,
)

goals_agent = AssistantAgent(
    name="GoalsAgent",
    system_message="""
    You are a goal-setting fitness coach specializing in defining realistic and achievable fitness goals.
    - Your ONLY task is to create specific short-term and long-term goals aligned with the user's objectives.
    - Do NOT generate workout plans, diet plans, or schedules.
    - Do NOT ask any questions to the user. Only use the provided information to define goals.
    """,
    **common_args,
)

no_rag_exercise_planner_agent = AssistantAgent(
    name="ExercisePlannerAgent",
    system_message="""
    You are a professional workout planner specializing in creating structured exercise routines.
    - Your ONLY task is to design a workout plan with specific exercises, sets, reps, and weights aligned with the user's fitness goals and level.
    - If more information is required, write "I need the following information:" followed by specific questions.
    - Do NOT generate goals, diet plans, or schedules.
    """,
    **common_args,
)

rag_exercise_planner_agent = RetrieveAssistantAgent(
    name="RagExercisePlannerAgent",
    system_message="""
    You are a professional workout planner specializing in creating structured exercise routines.
    - Your ONLY task is to design a workout plan with specific exercises, sets, reps, and weights aligned with the user's fitness goals and level.
    - Use the exercises provided in the csv files only.
    - If more information is required, write "I need the following information:" followed by specific questions.
    - Do NOT generate goals, diet plans, or schedules.
    """,
    **common_args,
)

diet_planner_agent = AssistantAgent(
    name="DietPlannerAgent",
    system_message="""
    You are a nutrition expert focused on creating balanced meal plans to support fitness goals.
    - Your ONLY task is to generate a nutrition plan that complements the user's fitness goals and workout routine, including calorie targets and macronutrient recommendations.
    - If more information is required, write "I need the following information:" followed by specific questions.
    - Do NOT generate workout plans, goals, or schedules.
    """,
    **common_args,
)

scheduling_agent = AssistantAgent(
    name="SchedulingAgent",
    system_message="""
    You are a scheduling expert specializing in creating balanced workout routines.
    - Your ONLY task is to arrange workout and rest days into a weekly schedule, specifying session durations and activities for each day.
    - Do NOT generate goals, workout plans, or diet plans.
    - Do NOT ask any questions to the user. Use the provided data to create the schedule.
    """,
    **common_args,
)

exercise_planner_agent = rag_exercise_planner_agent
def get_chat_session(messages):

    user_input_agent.reset()
    goals_agent.reset()
    exercise_planner_agent.reset()
    diet_planner_agent.reset()
    scheduling_agent.reset()

    # User Proxy Agent
    no_rag_user = UserProxyAgent(
        name="user",
        system_message="A human admin.",
        code_execution_config=False,
        human_input_mode="NEVER",
    )

    rag_user_proxy_agent = RetrieveUserProxyAgent(
        name="ragproxyagent",
        retrieve_config={
            "task": "fetch",
            "docs_path": get_data_paths(),
            "chunk_token_size": 2000,
            "model": llm_config["config_list"][0]["model"],
            "vector_db": "chroma",
            "overwrite": False,
            "get_or_create": True
        },
        **common_args,
    )

    transitions = {
        rag_user_proxy_agent: [user_input_agent],
        user_input_agent: [goals_agent],
        goals_agent: [exercise_planner_agent],
        exercise_planner_agent: [diet_planner_agent],
        diet_planner_agent: [scheduling_agent],
        scheduling_agent: [],  # End of the workflow
    }

    # Group Chat with agents
    groupchat = GroupChat(
        agents=[
            rag_user_proxy_agent,
            user_input_agent,
            goals_agent,
            exercise_planner_agent,
            diet_planner_agent,
            scheduling_agent,
        ],
        messages=messages,
        max_round=7,
        allowed_or_disallowed_speaker_transitions=transitions,
        speaker_transitions_type="allowed",
        enable_clear_history=False,
    )
    # GroupChatManager
    manager = GroupChatManager(groupchat=groupchat, llm_config=llm_config)
    return rag_user_proxy_agent, manager, groupchat
