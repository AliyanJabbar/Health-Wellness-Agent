from agents import function_tool, RunContextWrapper, Agent, Runner
from context import UserSessionContext
from pydantic import BaseModel
from typing import List, Dict, Optional


# utils configuration
from utils.agent_sdk_gemini_configuration import configuration

external_model = configuration("agent")


class MealPlan(BaseModel):
    plan_name: str
    duration_days: int
    daily_meals: List[Dict[str, str]]  # day, breakfast, lunch, dinner, snacks
    dietary_preferences: str
    estimated_calories_per_day: int
    shopping_list: List[str]


meal_planning_agent = Agent[UserSessionContext](
    name="Meal Planning Agent",
    instructions="""
    You are a nutrition expert that creates detailed meal plans based on user goals and dietary preferences.
    
    Create a structured meal plan that includes:
    - Daily meals (breakfast, lunch, dinner, snacks)
    - Consideration of dietary preferences (vegetarian, vegan, keto, etc.)
    - Calorie estimates based on goals (weight loss, gain, maintenance)
    - A shopping list of ingredients needed
    - Meal prep suggestions
    
    For weight loss goals: aim for calorie deficit
    For weight gain goals: aim for calorie surplus
    For maintenance: aim for maintenance calories
    
    IMPORTANT: Return the response in the exact format specified by the MealPlan model.
    """,
    output_type=MealPlan,
    model=external_model,
)


@function_tool()
async def meal_planner_tool(
    ctx: RunContextWrapper[UserSessionContext],
    duration_days: int = 7,
    specific_preferences: Optional[str] = None,
) -> str:
    """
    Generate a personalized meal plan based on user's goals and dietary preferences.

    Args:
        duration_days: Number of days for the meal plan (default 7)
        specific_preferences: Additional dietary preferences or restrictions
    """
    print("-" * 50)
    print("[Tool] Running meal planner")

    try:
        # Get user context - Handle GoalOutput object properly
        user_goal = ctx.context.goal
        if not user_goal:
            return "Please set your fitness goal first like: 'I want to lose 2kg weight in 1 month'. using the goal analyzer."

        # Extract goal information properly
        if hasattr(user_goal, "action"):
            goal_description = f"{user_goal.action} {user_goal.quantity} {user_goal.entity} in {user_goal.duration}"
        else:
            goal_description = str(user_goal)

        diet_prefs = ctx.context.diet_preferences or "no specific preferences"

        if specific_preferences:
            diet_prefs += f", {specific_preferences}"

        # Create meal plan prompt
        prompt = f"""
        Create a {duration_days}-day meal plan for:
        - Goal: {goal_description}
        - Dietary preferences: {diet_prefs}
        - User name: {ctx.context.name}
        
        Include specific meals, portions, and a shopping list.
        Make sure to provide all required fields: plan_name, duration_days, daily_meals, dietary_preferences, estimated_calories_per_day, shopping_list.
        """

        print(f"[Tool] Sending prompt to meal planning agent")

        result = await Runner.run(meal_planning_agent, prompt, context=ctx.context)
        meal_plan: MealPlan = result.final_output

        print(f"[Tool] Received meal plan: {meal_plan.plan_name}")

        # Store in context
        ctx.context.meal_plan = meal_plan.daily_meals

        print(f"[Tool] Generated {duration_days}-day meal plan")
        print("-" * 50)

        return f"""
        🍽️ **{meal_plan.plan_name}**
        
        **Duration:** {meal_plan.duration_days} days
        **Dietary Preferences:** {meal_plan.dietary_preferences}
        **Estimated Daily Calories:** {meal_plan.estimated_calories_per_day}
        
        **Daily Meals:**
        {chr(10).join([f"**Day {i+1}:** {meal.get('day', f'Day {i+1}')} - {meal.get('breakfast', 'N/A')} | {meal.get('lunch', 'N/A')} | {meal.get('dinner', 'N/A')}" for i, meal in enumerate(meal_plan.daily_meals[:3])])}
        
        **Shopping List:** {', '.join(meal_plan.shopping_list[:10])}...
        
        Your meal plan has been saved to your profile!
        """

    except Exception as e:
        print(f"[Tool] Error in meal planner: {str(e)}")
        print(f"[Tool] Error type: {type(e)}")
        return f"❌ Error creating meal plan: {str(e)}. Please try again or contact support."
