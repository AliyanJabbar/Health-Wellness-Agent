from agents import (
    Agent,
    input_guardrail,
    output_guardrail,
    GuardrailFunctionOutput,
    RunContextWrapper,
    Runner,
    TResponseInputItem,
)
from pydantic import BaseModel
from context import UserSessionContext

# utils configuration
from utils.agent_sdk_gemini_configuration import configuration

external_model = configuration("agent")

# 1. FOR GENERAL INPUT/OUTPUT
# input validation schema
class GeneralInputValidation(BaseModel):
    is_appropriate: bool
    category: str  # nutrition, injury, escalation, general
    sanitized_input: str


# Agent to validate general input appropriateness
input_validation_agent = Agent[UserSessionContext](
    name="Input Validation Agent",
    instructions="""
    Analyze user input for appropriateness and categorization:
    - Check if input is appropriate for a health/wellness context
    - Categorize as: nutrition, injury, escalation, or general
    - Sanitize input by removing inappropriate content
    """,
    output_type=GeneralInputValidation,
    model=external_model,
)


@input_guardrail
async def general_input_guardrail(
    wrapper: RunContextWrapper[UserSessionContext],
    agent,  # required parameter
    user_input: str | list[TResponseInputItem],
) -> GuardrailFunctionOutput:
    """General input validation for main health wellness agent"""
    result = await Runner.run(
        input_validation_agent, user_input, context=wrapper.context
    )
    validation = result.final_output

    return GuardrailFunctionOutput(
        output_info=validation, tripwire_triggered=not validation.is_appropriate
    )


@output_guardrail
async def general_output_guardrail(
    wrapper: RunContextWrapper[UserSessionContext],
    agent,  # required parameter
    agent_response: str,
) -> GuardrailFunctionOutput:
    """Simple output validation - check if response is good or not"""
    # Simple checks for good response
    is_good = (
        len(agent_response.strip()) > 10  # Not too short
        and not any(
            word in agent_response.lower()
            for word in ["error", "failed", "inappropriate"]
        )  # No error words
        and agent_response.strip() != ""  # Not empty
    )

    return GuardrailFunctionOutput(
        output_info={"is_good": is_good}, tripwire_triggered=not is_good
    )


# 2. FOR GOALS:
# schema to follow
class GoalOutput(BaseModel):
    is_valid: bool
    action: str
    entity: str
    quantity: str
    duration: str


# Agent to validate user's input

goal_guardrail_agent = Agent[UserSessionContext](
    name="Goal Format Checker",
    instructions="Extract action, entity, quantity and duration and set is_valid if all are present. e.g: I want to lose(action) 2kg(quantity) weight(entity) in 2months(duration). If something is missing then set is_valid to False also set that item to None.",
    output_type=GoalOutput,
    model=external_model,
)


@input_guardrail
async def goal_input_guardrail(
    wrapper: RunContextWrapper[UserSessionContext],
    agent,  # required parameter
    user_input: str | list[TResponseInputItem],
) -> GuardrailFunctionOutput:
    result = await Runner.run(goal_guardrail_agent, user_input, context=wrapper.context)
    output = result.final_output

    return GuardrailFunctionOutput(
        output_info=output, tripwire_triggered=not output.is_valid
    )


@output_guardrail
async def goal_output_guardrail(
    wrapper: RunContextWrapper[UserSessionContext],
    agent,  # required parameter
    tool_output: GoalOutput,
) -> GuardrailFunctionOutput:
    ok = (
        bool(tool_output.action)
        and bool(tool_output.quantity)
        and bool(tool_output.entity)
        and (tool_output.duration) not in ["", "None", "none", None]
    )
    return GuardrailFunctionOutput(output_info=tool_output, tripwire_triggered=not ok)
