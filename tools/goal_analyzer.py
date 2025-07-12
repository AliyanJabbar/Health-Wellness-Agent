from agents import (
    Agent,function_tool,
    RunContextWrapper,
    Runner,
    AsyncOpenAI,
    OpenAIChatCompletionsModel,
)
from context import UserSessionContext
from dotenv import load_dotenv
import os

from guardrails import goal_input_guardrail,goal_output_guardrail,GoalOutput

load_dotenv()

gemini_key = os.getenv("GEMINI_API_KEY")

external_client = AsyncOpenAI(
    api_key=gemini_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

external_model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash", openai_client=external_client
)
goal_format_agent = Agent[UserSessionContext](
    name="Goal Format Checker",
    instructions="Using input/output guardrails give structured goal.",
    output_type=GoalOutput,
    model=external_model,
    input_guardrails=[goal_input_guardrail],
    output_guardrails=[goal_output_guardrail],
)

@function_tool()
async def goal_analyzer(ctx: RunContextWrapper[UserSessionContext], goal_input: str) -> str:
    # REMOVED MANUAL PRINTS - HOOKS HANDLE THIS NOW
    
    # Now guardrails run automatically
    result = await Runner.run(goal_format_agent, goal_input, context=ctx.context)
    final: GoalOutput = result.final_output

    if not final.is_valid:
        return "Your goal seems unclear. Could you specify how much and in how long?"

    ctx.context.goal = final

    return f"Great! You want to {final.action} {final.entity} {final.quantity} in {final.duration}."