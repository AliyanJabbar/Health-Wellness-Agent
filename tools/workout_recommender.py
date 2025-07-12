from agents import function_tool, RunContextWrapper, Agent, Runner
from pydantic import BaseModel
from typing import List

# context
from context import UserSessionContext

# utils configuration
from utils.agent_sdk_gemini_configuration import configuration


class WorkoutPlan(BaseModel):
    plan_name: str
    goal_type: str
    experience_level: str
    frequency: int
    exercises: List[str]
    equipment_needed: List[str]


external_model = configuration("agent")

workout_planning_agent = Agent[UserSessionContext](
    name="Workout Planning Agent",
    instructions="""Create a structured workout plan based on user goals and fitness level.
    Include exercises, equipment needed, and adjust intensity based on experience level.""",
    output_type=WorkoutPlan,
    model=external_model,
)


@function_tool()
async def workout_recommender_tool(
    ctx: RunContextWrapper[UserSessionContext],
    experience_level: str = "beginner",
    workout_days_per_week: int = 3,
) -> str:
    """Generate a personalized workout plan based on user's fitness goals."""

    if not ctx.context.goal:
        return "Please set your fitness goal first using the goal analyzer."

    # FIX: Handle GoalOutput object properly
    user_goal = ctx.context.goal
    if hasattr(user_goal, "action"):
        goal_description = f"{user_goal.action} {user_goal.quantity} {user_goal.entity} in {user_goal.duration}"
    else:
        goal_description = str(user_goal)

    prompt = f"""
    Create a {workout_days_per_week}-day workout plan for:
    - Goal: {goal_description}
    - Experience level: {experience_level}
    - User: {ctx.context.name}
    """

    result = await Runner.run(workout_planning_agent, prompt, context=ctx.context)
    workout_plan: WorkoutPlan = result.final_output

    # Store in context
    ctx.context.workout_plan = workout_plan.dict()

    return f"""
    💪 **{workout_plan.plan_name}**
    
    **Goal:** {workout_plan.goal_type.title()}
    **Experience:** {workout_plan.experience_level.title()}
    **Frequency:** {workout_plan.frequency} days/week
    
    **Equipment:** {', '.join(workout_plan.equipment_needed)}
    
    Your workout plan has been saved!
    """
