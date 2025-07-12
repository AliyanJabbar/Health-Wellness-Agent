from agents import function_tool, RunContextWrapper
from context import UserSessionContext
from .workout_recommender import WorkoutRecommenderTool
from typing import Optional

# Initialize the workout recommender
workout_recommender = WorkoutRecommenderTool()

@function_tool()
async def workout_recommender_tool(
    ctx: RunContextWrapper[UserSessionContext],
    experience_level: str = "beginner",
    injury_notes: Optional[str] = None,
    workout_days_per_week: int = 3
) -> str:
    """
    Generate a personalized workout plan based on user's fitness goals.
    
    Args:
        experience_level: User's fitness level (beginner, intermediate, advanced)
        injury_notes: Any injury limitations or notes
        workout_days_per_week: Preferred number of workout days per week
    """
    print("-" * 50)
    print("[Tool] Running workout recommender")
    
    # Get goal from context
    if not ctx.context.goal:
        return "Please set your fitness goal first using the goal analyzer."
    
    goal_action = ctx.context.goal.get('action', 'maintain')
    
    # Generate workout plan
    workout_plan = workout_recommender.run(
        goal_type=goal_action,
        experience_level=experience_level,
        injury_notes=injury_notes,
        context=ctx.context
    )
    
    print(f"[Tool] Generated workout plan: {workout_plan.plan_name}")
    print("-" * 50)
    
    # Format response
    workout_days = [day for day in workout_plan.weekly_schedule if day.focus != "rest"]
    
    return f"""
    💪 **{workout_plan.plan_name}**
    
    **Goal:** {workout_plan.goal_type.title()}
    **Experience Level:** {workout_plan.experience_level.title()}
    **Frequency:** {workout_plan.frequency} days per week
    
    **This Week's Schedule:**
    {chr(10).join([f"**{day.day}:** {day.focus.replace('_', ' ').title()} ({day.total_duration} min, ~{day.estimated_calories} calories)" for day in workout_days[:3]])}
    
    Your workout plan has been saved to your profile!
    """
