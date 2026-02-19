from agents import (
    Agent,
    function_tool,
    RunContextWrapper,
    Runner,
)

# context
from context import UserSessionContext

# utils configuration
from utils.agent_sdk_gemini_configuration import low_external_model

# pydantic model for validation
from pydantic import BaseModel


# schema to follow
class GoalOutput(BaseModel):
    is_valid: bool
    action: str
    entity: str
    quantity: str
    duration: str


goal_format_checker = Agent[UserSessionContext](
    name="goal_format_checker",
    instructions="Extract action, entity, quantity and duration and set is_valid if all are present. e.g: I want to lose(action) 2kg(quantity) weight(entity) in 2months(duration). If something is missing then set is_valid to False also set that item to None.",
    output_type=GoalOutput,
    model=low_external_model,
)


@function_tool()
async def goal_analyzer(
    wrapper: RunContextWrapper[UserSessionContext], goal_input: str
) -> str:
    """
    function_tool to check if the goal is clear.

    args:
        goal_input: str (a detailed goal like 'I want to lose 2kg weight in 7days')

    return:
        str
    """
    result = await Runner.run(goal_format_checker, goal_input, context=wrapper.context)
    goal: GoalOutput = result.final_output

    if not goal.is_valid:
        return "Your goal seems unclear. Please specify your goal like ' I want to lose 2kg weight in 7days'"

    wrapper.context.goal = goal
    return f"Great! You want to {goal.action} {goal.entity} {goal.quantity} in {goal.duration}. Is that clear ?"
