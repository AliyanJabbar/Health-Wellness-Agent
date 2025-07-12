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
