from agents import function_tool, RunContextWrapper
from context import UserSessionContext

# tools for context management


# for goal
@function_tool
def get_goal(wrapper: RunContextWrapper[UserSessionContext]):
    return ("current goal is : ", wrapper.context.goal)


# for diet preferences
@function_tool
def get_diet_pref(wrapper: RunContextWrapper[UserSessionContext]):
    return ("current diet pref is : ", wrapper.context.diet_preferences)


# for workout plan
@function_tool
def get_workout_plan(wrapper: RunContextWrapper[UserSessionContext]):
    return ("current diet pref is : ", wrapper.context.workout_plan)


# for setting name
@function_tool
def set_user_name(wrapper: RunContextWrapper[UserSessionContext], user_name: str):
    wrapper.context.name = user_name
    print("name set to : ", wrapper.context.name)
