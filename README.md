# Gym Workout Planner

**Gym Workout Planner** is a multi-agent system designed to create personalized fitness plans tailored to user preferences, goals, and fitness levels. It leverages intelligent agents working collaboratively to handle different aspects of fitness planning, including gathering user input, setting goals, designing workout routines, creating meal plans, and scheduling workouts.

## Features

- **User Input Handling**: Collects and summarizes user-provided information, ensuring all necessary details are captured for planning.
- **Goal Setting**: Defines short-term and long-term fitness goals based on user objectives.
- **Workout Planning**: Generates structured workout routines with specific exercises, sets, reps, and weights, referencing an exercise database for precision.
- **Diet Planning**: Creates meal plans tailored to fitness goals, including calorie and macronutrient breakdowns.
- **Scheduling**: Organizes workout and rest days into a balanced weekly schedule.

## How It Works

The system employs five specialized agents:

1. **UserInputAgent**: Gathers user information and summarizes it for other agents. It ensures all necessary details are collected and asks for clarification if required.
2. **GoalsAgent**: Sets measurable fitness goals based on user preferences and summarized input.
3. **ExercisePlannerAgent**: Designs workout plans using an exercise database. It filters exercises based on the user's fitness level, goals, and available equipment.
4. **DietPlannerAgent**: Suggests balanced meal plans that align with the user's workout regimen and fitness objectives.
5. **SchedulingAgent**: Develops a weekly schedule for workouts and rest days, ensuring a balanced routine.

## Technologies Used

- **Python**: Core programming language for developing the agents.
- **pandas**: Used for managing and querying the exercise database (CSV file).
- **Streamlit**: Provides an interactive web-based UI for user interactions.
- **RAG (Retrieval-Augmented Generation)**: Enables the `ExercisePlannerAgent` to dynamically reference a CSV-based exercise database.

## Setup Instructions

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/your-username/gym-workout-planner.git
   cd gym-workout-planner
