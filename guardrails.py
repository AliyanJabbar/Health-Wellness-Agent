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
from utils.agent_sdk_gemini_configuration import low_external_model


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
    model=low_external_model,
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
