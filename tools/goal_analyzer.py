from agents import (
    Agent,function_tool,
    RunContextWrapper,
    Runner,
)
# context
from context import UserSessionContext
# guardrails
from guardrails import goal_input_guardrail,goal_output_guardrail,GoalOutput
# utils configuration
from utils.agent_sdk_gemini_configuration import configuration

external_model = configuration("agent")
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