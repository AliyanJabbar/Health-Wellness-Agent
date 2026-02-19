from agents import RunHooks, AgentHooks, RunContextWrapper
from context import UserSessionContext
from typing import Any


class HealthWellnessRunHooks(RunHooks[UserSessionContext]):
    """Global lifecycle hooks for logging tool and agent activities"""

    async def on_agent_start(
        self, wrapper: RunContextWrapper[UserSessionContext], agent: Any
    ):
        print("-" * 30, f"{agent.name} started", "-" * 30)

    async def on_agent_end(
        self, wrapper: RunContextWrapper[UserSessionContext], agent: Any, result: Any
    ):
        print("-" * 30, f"{agent.name} ended", "-" * 30)

    async def on_tool_start(
        self, wrapper: RunContextWrapper[UserSessionContext], agent: Any, tool: Any
    ):
        print("-" * 30, f"tool {tool.name} started (Agent: {agent.name})", "-" * 30)

    async def on_tool_end(
        self,
        wrapper: RunContextWrapper[UserSessionContext],
        agent: Any,
        tool: Any,
        result: Any,
    ):
        print("-" * 30, f"tool {tool.name} ended (Agent: {agent.name})", "-" * 30)
        print("-" * 30, f"wrapper.context.goal: {wrapper.context.goal} ", "-" * 30)


# class HealthWellnessAgentHooks(AgentHooks[UserSessionContext]):
#     """Per-agent lifecycle hooks"""

#     async def on_start(
#         self, wrapper: RunContextWrapper[UserSessionContext], agent: Any
#     ):
#         print("-" * 30, f"Session started: {agent.name}", "-" * 30)

#     async def on_end(
#         self, wrapper: RunContextWrapper[UserSessionContext], agent: Any, result: Any
#     ):
#         print("-" * 30, f"Session ended: {agent.name}", "-" * 30)
