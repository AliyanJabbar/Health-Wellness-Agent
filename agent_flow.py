from agents import Agent

# agents
from our_agents.escalation_agent import escalation_agent
from our_agents.injury_agent import injury_agent
from our_agents.nutrition_agent import nutrition_agent

# context
from context import UserSessionContext

# utils
from utils.handoff_handler import handoff_handler

# hooks
from hooks import HealthWellnessAgentHooks

# guardrails
from guardrails import general_input_guardrail, general_output_guardrail

agent_hooks = HealthWellnessAgentHooks()

# adding handoffs to all agents
injury_agent.handoffs = [
    handoff_handler(
        agent=escalation_agent,
        on_handoff_message="Handoff to escalation agent for better assistance.",
        prev_agent_name="injury_agent",
    ),
    handoff_handler(
        agent=nutrition_agent,
        on_handoff_message="Handoff to nutrition expert agent for better assistance.",
        prev_agent_name="injury_agent",
    ),
]

escalation_agent.handoffs = [
    handoff_handler(
        agent=injury_agent,
        on_handoff_message="Handoff to injury support agent for better assistance.",
        prev_agent_name="escalation_agent",
    ),
    handoff_handler(
        agent=nutrition_agent,
        on_handoff_message="Handoff to nutrition expert agent for better assistance.",
        prev_agent_name="escalation_agent",
    ),
]

nutrition_agent.handoffs = [
    handoff_handler(
        agent=escalation_agent,
        on_handoff_message="Handoff to escalation agent for better assistance.",
        prev_agent_name="nutrition_agent",
    ),
    handoff_handler(
        agent=injury_agent,
        on_handoff_message="Handoff to injury support agent for better assistance.",
        prev_agent_name="nutrition_agent",
    ),
]

# main agent
health_wellness_agent = Agent[UserSessionContext](
    name="health_wellness_agent",
    handoffs=[
        handoff_handler(
            agent=escalation_agent,
            on_handoff_message="Handoff to escalation agent for human like assistance.",
        ),
        handoff_handler(
            agent=injury_agent,
            on_handoff_message="Handoff to injury support agent for injury related assistance.",
        ),
        handoff_handler(
            agent=nutrition_agent,
            on_handoff_message="Handoff to nutrition expert agent for meal planning and workout recommendation.",
        ),
    ],
    input_guardrails=[general_input_guardrail],
    output_guardrails=[general_output_guardrail],
    hooks=agent_hooks,
    instructions="""
    You are a health and wellness assistant. Help users with general fitness, nutrition, or injury-related queries.

    IMPORTANT WORKFLOW:
    1. You should take input from user and then analyze it.
    2. If it is general then reply to it.
    3. If it is related to health/fitness goal or nutrition needs then handoff to nutrition agent.
    4. If it is related to injury or recovery from that then handoff to injury agent.
    5. If the user wants to contact to human or if it's an emergency case then handoff to escalation agent.
    """,
)
