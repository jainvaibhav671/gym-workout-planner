from crewai import Agent, Task, Crew, Process
import json
import os
import pprint

# (TEMPORARY)
# Load env variables
# import toml
# env = toml.load("./.streamlit/secrets.toml")
# for key in env.keys():
#     os.environ[key] = env.get(key)

from gym_trainer.crewai.utils import get_llm
from tools import gym_rag_tool, stretch_rag_tool
from models import *

fitness_assessment_agent = Agent(
    role='Fitness Assessor',
    goal="Evaluate user's current fitness level and gather all required baseline data.",
    backstory=(
        "A fitness evaluator who ensures all necessary details are gathered before planning begins."
    ),
    llm=get_llm()
)

fitness_assessment_task = Task(
    description="Summarize the user provided data and assess the fitness of ther user {user_data}",
    expected_output="A summary of user's fitness level with complete baseline information.",
    agent=fitness_assessment_agent,
    output_pydantic=FitnessAssessmentOutput
)

goal_setting_agent = Agent(
    role='Goal Setter',
    goal="Define specific, achievable fitness goals aligned with the user's objectives.",
    backstory="A goal-oriented fitness coach skilled in setting realistic, motivating targets.",
    llm=get_llm(),
)

goal_setting_task = Task(
    description="Define short- and long-term fitness goals based on the user's preferences and fitness assessment results.",
    expected_output="A list of defined fitness goals with target timelines.",
    agent=goal_setting_agent,
    context=[fitness_assessment_task],
    output_pydantic=FitnessGoalsOutput
)

exercise_planner_agent = Agent(
    role='Exercise Planner',
    goal="Design a workout plan that aligns with the user's goals and fitness level.",
    backstory="An expert workout planner who tailors exercises for diverse goals and conditions.",
    llm=get_llm(),
    verbose=True,
    tools=[gym_rag_tool, stretch_rag_tool],  # Integrate both RAG tools
)

exercise_plan_task = Task(
    description=(
        "Use the available exercise data to select exercises, sets, reps, and weights based on the user's goals, "
        "experience level, and equipment availability. For gym-based exercises, use the Gym Exercises CSV; for stretching, "
        "refer to the Stretching Exercises CSV. Include a mix of exercises suited to the user's preferences and fitness level."
    ),
    tools=[gym_rag_tool, stretch_rag_tool],
    expected_output="A structured exercise plan with specific exercises, sets, reps, and weights.",
    agent=exercise_planner_agent,
    context=[fitness_assessment_task, goal_setting_task],
    output_pydantic=ExercisePlanOutput
)

dietary_advisor_agent = Agent(
    role='Dietary Advisor',
    goal="Suggest a nutrition plan that supports the user's workout regimen for optimal progress.",
    backstory="A nutritionist focused on creating balanced meal plans to support fitness goals.",
    llm=get_llm()
)

diet_plan_task = Task(
    description="Suggest dietary adjustments and meal plans that support the user's workout goals.",
    expected_output="A daily meal plan with calorie targets and macronutrient recommendations.",
    agent=dietary_advisor_agent,
    context=[fitness_assessment_task, exercise_plan_task],
    output_pydantic=DietPlanOutput,
)

schedule_optimizer_agent = Agent(
    role='Schedule Optimizer',
    goal='Organize the workout schedule to maximize efficiency and recovery.',
    backstory="An organized planner specializing in balanced routines for optimal results.",
    llm=get_llm()
)

schedule_optimization_task = Task(
    description="Arrange workout days, rest days, and the session duration for a balanced training schedule.",
    expected_output="A weekly workout schedule including workout and rest days.",
    agent=schedule_optimizer_agent,
    context=[exercise_plan_task, diet_plan_task],
    output_pydantic=ScheduleOptimizationOutput
)

# Define Summary Agent
summary_agent = Agent(
    role='Summary Agent',
    goal='Summarize the outputs from all previous agents into a final comprehensive report.',
    backstory="A skilled summarizer who can compile detailed information into a concise report.",
    llm=get_llm()
)

# Summary Task that consolidates outputs from all other tasks
summary_task = Task(
    description="""
    Summarize all outputs from previous tasks, including the 
    fitness assessment, goal setting, exercise plan, diet plan, and schedule.
    """,
    expected_output="A final comprehensive report combining all task results.",
    agent=summary_agent,
    async_execution=True,
    context=[
        fitness_assessment_task,
        goal_setting_task,
        exercise_plan_task,
        diet_plan_task,
        schedule_optimization_task,
    ],
    output_pydantic=SummaryOutput
)

crew = Crew(
    agents=[
        fitness_assessment_agent,
        goal_setting_agent,
        exercise_planner_agent,
        dietary_advisor_agent,
        schedule_optimizer_agent,
        summary_agent
    ],
    tasks=[
        fitness_assessment_task,
        goal_setting_task,
        exercise_plan_task,
        diet_plan_task,
        schedule_optimization_task,
        summary_task
    ],
    process=Process.sequential,
    max_rpm=3
)


# if __name__ == "__main__":
#     import os
#     import litellm
#     litellm.set_verbose=True
#     os.environ['LITELLM_LOG'] = 'DEBUG'

#     user_data = {
#         "age": 22,
#         "height": 170,
#         "weight": 72,
#         "experience_level": "Beginner",
#         # "health_conditions": "asthma"
#     }
#     user_data = json.dumps(user_data, separators=(',', ':'), indent=0)
#     print("User Data", user_data)
#     try:
#         # Start the Crew process with the user data
#         response = crew.kickoff(inputs={ "user_data": user_data })
#         print("\n"*10)
#         print("--"*10)
#         print("Usage: ", response.token_usage)
#         print("--"*10)
#         print("Response")
#         pprint.pprint([
#             {
#                 "name": task_output.agent,
#                 "data": task_output.raw
#             } 
#             for task_output in response.tasks_output
#         ])
#         print("--"*10)
#         #   print_markdown(response.raw)
#     except Exception as e:
#         print(str(e))