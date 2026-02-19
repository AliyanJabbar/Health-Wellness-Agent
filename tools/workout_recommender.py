from agents import function_tool, RunContextWrapper, Agent, Runner
from pydantic import BaseModel

# context
from context import UserSessionContext

# utils configuration
from utils.agent_sdk_gemini_configuration import low_external_model


class WorkoutPlan(BaseModel):
    plan_name: str
    goal_type: str
    experience_level: str
    frequency: int
    exercises: list[str]
    equipment_needed: list[str]


workout_planning_agent = Agent[UserSessionContext](
    name="Workout Planning Agent",
    instructions="""Create a structured workout plan based on user goals and fitness level.
    Include exercises, equipment needed, and adjust intensity based on experience level.""",
    output_type=WorkoutPlan,
    model=low_external_model,
)


@function_tool()
async def workout_recommender_tool(
    wrapper: RunContextWrapper[UserSessionContext],
    experience_level: str,
    workout_days_per_week: int,
) -> str:
    """Generate a personalized workout plan based on user's fitness goals."""

    if not wrapper.context.goal:
        return "Please set your health goal first using the goal analyzer."

    user_goal = wrapper.context.goal
    if hasattr(user_goal, "action"):
        goal_description = f"{user_goal.action} {user_goal.quantity} {user_goal.entity} in {user_goal.duration}"
    else:
        goal_description = str(user_goal)

    prompt = f"""
    Create a {workout_days_per_week}-day workout plan for:
    - Goal: {goal_description}
    - Experience level: {experience_level}
    - User: {wrapper.context.name}
    """

    result = await Runner.run(workout_planning_agent, prompt, context=wrapper.context)
    workout_plan: WorkoutPlan = result.final_output

    # Store in context
    wrapper.context.workout_plan = workout_plan

    return f"""
    💪 **{workout_plan.plan_name}**
    
    **Goal:** {workout_plan.goal_type.title()}
    **Experience:** {workout_plan.experience_level.title()}
    **Frequency:** {workout_plan.frequency} days/week
    
    **Equipment:** {', '.join(workout_plan.equipment_needed)}

    **Exercises:**
    {', '.join(workout_plan.exercises)}
    
    Your workout plan has been saved!
    """
