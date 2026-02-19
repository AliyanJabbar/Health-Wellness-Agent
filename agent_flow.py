from agents import Agent

# prompt for better handoffs
from agents.extensions.handoff_prompt import RECOMMENDED_PROMPT_PREFIX

# agents
from our_agents.escalation_agent import escalation_agent
from our_agents.injury_agent import injury_agent
from our_agents.nutrition_agent import nutrition_agent

# context
from context import UserSessionContext

# tools
from tools.goal_analyzer import goal_analyzer
from tools.meal_planner import meal_planner_tool
from tools.workout_recommender import workout_recommender_tool
from tools.context_tools import get_diet_pref
from tools.context_tools import get_goal
from tools.context_tools import set_user_name



# utils
from utils.handoff_handler import handoff_handler

# guardrails
from guardrails import general_input_guardrail, general_output_guardrail


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
    tools=[
        set_user_name,
        goal_analyzer,
        meal_planner_tool,
        workout_recommender_tool,
        get_diet_pref,
        get_goal,
    ],
    input_guardrails=[general_input_guardrail],
    output_guardrails=[general_output_guardrail],
    instructions=f"""
        {RECOMMENDED_PROMPT_PREFIX}

    You are a health and wellness assistant. Help users with general fitness, nutrition, or injury-related queries.

    IMPORTANT WORKFLOW:
    1. You should take input from user and then analyze it.
    2. If it is general then reply to it.
    3. If it is related to health/fitness goal or nutrition needs then transfer_to_nutrition_agent.
    4. If it is related to injury or recovery from that then transfer_to_injury_agent.
    5. If the user wants to contact to human or if it's an emergency case then transfer_to_escalation_agent.
    """,
)
