from pydantic import BaseModel
from typing import List, Optional

class FitnessAssessmentOutput(BaseModel):
    bmi: float
    fitness_level: str
    health_conditions: Optional[List[str]] = []  # Default to an empty list if no conditions are provided

class FitnessGoalsOutput(BaseModel):
    short_term_goals: List[str]  # Goals to achieve in the next few weeks
    long_term_goals: List[str]  # Goals to achieve over several months

class Exercise(BaseModel):
    name: str
    sets: int
    reps: int
    weight: Optional[float] = None  # Include weight if applicable, e.g., for strength training

class ExercisePlanOutput(BaseModel):
    exercises: List[Exercise]  # List of exercises in the plan
    total_duration_minutes: int  # Total time required to complete the workout

class Meal(BaseModel):
    time_of_day: str  # e.g., "Breakfast", "Lunch", "Dinner", or "Snack"
    description: str  # A brief description of the meal
    calories: int
    macronutrients: Optional[dict] = None  # Include macronutrient details (protein, carbs, fat)

class DietPlanOutput(BaseModel):
    daily_meal_plan: List[Meal]  # List of meals for the day
    total_calories: int  # Total calories for the day

class ScheduleEntry(BaseModel):
    day: str  # e.g., "Monday"
    activity: str  # e.g., "Workout", "Rest", or specific workout type
    duration_minutes: int

class ScheduleOptimizationOutput(BaseModel):
    weekly_schedule: List[ScheduleEntry]  # A weekly plan detailing workouts and rest days

class SummaryOutput(BaseModel):
    fitness_assessment: FitnessAssessmentOutput
    fitness_goals: FitnessGoalsOutput
    exercise_plan: ExercisePlanOutput
    diet_plan: DietPlanOutput
    schedule_optimization: ScheduleOptimizationOutput