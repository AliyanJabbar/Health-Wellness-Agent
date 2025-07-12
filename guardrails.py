from agents import (
    Agent,
    input_guardrail,
    output_guardrail,
    GuardrailFunctionOutput,
    RunContextWrapper,
    Runner,
    TResponseInputItem,
    AsyncOpenAI,
    OpenAIChatCompletionsModel,
)
from pydantic import BaseModel
from context import UserSessionContext
from dotenv import load_dotenv
import os


class GoalOutput(BaseModel):
    is_valid: bool
    action: str
    entity: str
    quantity: str
    duration: str


load_dotenv()

gemini_key = os.getenv("GEMINI_API_KEY")

external_client = AsyncOpenAI(
    api_key=gemini_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

external_model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash", openai_client=external_client
)

# Agent to parse and validate the user's input
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
    wrapper.context.goal = output
    
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
    if ok:
        wrapper.context.goal = tool_output
    return GuardrailFunctionOutput(output_info=tool_output, tripwire_triggered=not ok)
