# from agents import Agent

# # agents
# from our_agents.escalation_agent import escalation_agent
# from our_agents.injury_agent import injury_agent
# from our_agents.nutrition_agent import nutrition_agent

# # tools
# from tools.goal_analyzer import goal_analyzer

# # context tools
# from tools.context_tools import get_goal, get_diet_pref

# # context
# from context import UserSessionContext

# # utils
# from utils.handoff_handler import handoff_handler

# # hooks
# from hooks import HealthWellnessAgentHooks

# # adding handoffs to all agents
# injury_agent.handoffs = [
#     handoff_handler(
#         agent=escalation_agent,
#         on_handoff_message="Handoff to escalation agent for better assistance.",
#         prev_agent_name="injury_agent",
#     ),
#     handoff_handler(
#         agent=nutrition_agent,
#         on_handoff_message="Handoff to nutrition expert agent for better assistance.",
#         prev_agent_name="injury_agent",
#     ),
# ]

# escalation_agent.handoffs = [
#     handoff_handler(
#         agent=injury_agent,
#         on_handoff_message="Handoff to injury support agent for better assistance.",
#         prev_agent_name="escalation_agent",
#     ),
#     handoff_handler(
#         agent=nutrition_agent,
#         on_handoff_message="Handoff to nutrition expert agent for better assistance.",
#         prev_agent_name="escalation_agent",
#     ),
# ]

# nutrition_agent.handoffs = [
#     handoff_handler(
#         agent=escalation_agent,
#         on_handoff_message="Handoff to escalation agent for better assistance.",
#         prev_agent_name="nutrition_agent",
#     ),
#     handoff_handler(
#         agent=injury_agent,
#         on_handoff_message="Handoff to injury support agent for better assistance.",
#         prev_agent_name="nutrition_agent",
#     ),
# ]

# # main agent
# health_wellness_agent = Agent[UserSessionContext](
#     name="health_wellness_agent",
#     handoffs=[
#         handoff_handler(
#             agent=escalation_agent,
#             on_handoff_message="Handoff to escalation agent for better assistance.",
#         ),
#         handoff_handler(
#             agent=injury_agent,
#             on_handoff_message="Handoff to injury support agent for better assistance.",
#         ),
#         handoff_handler(
#             agent=nutrition_agent,
#             on_handoff_message="Handoff to nutrition expert agent for better assistance.",
#         ),
#     ],
#     tools=[goal_analyzer, get_goal],
#     hooks=HealthWellnessAgentHooks(),
#     instructions="""
#     You are a health and wellness assistant. Help users with general fitness, nutrition, or injury-related queries.

# IMPORTANT WORKFLOW:
# 1. When a user mentions any health/fitness goal, FIRST call the goal_analyzer tool.
# 2. The goal_analyzer returns a structured result with:
#    - action (e.g., "lose", "gain")
#    - quantity (e.g., 5)
#    - metric (e.g., "kg", "lbs")
#    - duration (e.g., 2)
#    - duration_unit (e.g., "months")
#    - is_valid (True or False)

# 3. If is_valid is True, use the values from the structured goal to confirm with the user. For example:
#    → "Got it! You want to lose 5kg in 2 months. Let's begin your wellness plan."

# 4. If is_valid is False (missing details), DO NOT hand off immediately.
#    Instead, ask clarifying questions to gather missing information:
#    - If quantity is missing: "How much do you want to gain/lose?"
#    - If duration is missing: "What's your target timeframe?"
#    - If metric is missing: "Are you talking about weight (kg/lbs) or muscle mass?"

# 5. ONLY hand off to specialist agents AFTER you have gathered complete goal information OR after 2-3 clarifying questions.

# Examples of clarifying questions:
# - "I want to gain muscles" → Ask: "How much muscle do you want to gain and in what timeframe?"
# - "I need to lose weight" → Ask: "How much weight do you want to lose and by when?"

# REMEMBER:
# - Do not ignore tool output.
# - Use tool results (action, quantity, etc.) directly in your conversation.
# - Do not say: "I am unable to analyze your goal" if tool result is valid.
# When goal_analyzer tool returns a structured goal, respond with:
# "Great! You want to {action} {quantity}{metric} in {duration} {duration_unit}."
#     """,
# )



from agents import Agent

# agents
from our_agents.escalation_agent import escalation_agent
from our_agents.injury_agent import injury_agent
from our_agents.nutrition_agent import nutrition_agent

# tools
from tools.goal_analyzer import goal_analyzer

# context tools
from tools.context_tools import get_goal, get_diet_pref

# context
from context import UserSessionContext

# utils
from utils.handoff_handler import handoff_handler

# hooks
from hooks import HealthWellnessAgentHooks

# Enable/disable agent hooks for debugging
ENABLE_AGENT_HOOKS = True

# Create hooks instance
agent_hooks = None
if ENABLE_AGENT_HOOKS:
    try:
        agent_hooks = HealthWellnessAgentHooks()
        print("✅ Agent hooks created successfully")
    except Exception as e:
        print(f"❌ Error creating agent hooks: {e}")
        agent_hooks = None

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
            on_handoff_message="Handoff to escalation agent for better assistance.",
        ),
        handoff_handler(
            agent=injury_agent,
            on_handoff_message="Handoff to injury support agent for better assistance.",
        ),
        handoff_handler(
            agent=nutrition_agent,
            on_handoff_message="Handoff to nutrition expert agent for better assistance.",
        ),
    ],
    tools=[goal_analyzer, get_goal],
    hooks=agent_hooks,  # This will be None if disabled
    instructions="""
    You are a health and wellness assistant. Help users with general fitness, nutrition, or injury-related queries.

IMPORTANT WORKFLOW:
1. When a user mentions any health/fitness goal, FIRST call the goal_analyzer tool.
2. The goal_analyzer returns a structured result with:
   - action (e.g., "lose", "gain")
   - quantity (e.g., 5)
   - metric (e.g., "kg", "lbs")
   - duration (e.g., 2)
   - duration_unit (e.g., "months")
   - is_valid (True or False)

3. If is_valid is True, use the values from the structured goal to confirm with the user. For example:
   → "Got it! You want to lose 5kg in 2 months. Let's begin your wellness plan."

4. If is_valid is False (missing details), DO NOT hand off immediately.
   Instead, ask clarifying questions to gather missing information:
   - If quantity is missing: "How much do you want to gain/lose?"
   - If duration is missing: "What's your target timeframe?"
   - If metric is missing: "Are you talking about weight (kg/lbs) or muscle mass?"

5. ONLY hand off to specialist agents AFTER you have gathered complete goal information OR after 2-3 clarifying questions.

Examples of clarifying questions:
- "I want to gain muscles" → Ask: "How much muscle do you want to gain and in what timeframe?"
- "I need to lose weight" → Ask: "How much weight do you want to lose and by when?"

REMEMBER:
- Do not ignore tool output.
- Use tool results (action, quantity, etc.) directly in your conversation.
- Do not say: "I am unable to analyze your goal" if tool result is valid.
When goal_analyzer tool returns a structured goal, respond with:
"Great! You want to {action} {quantity}{metric} in {duration} {duration_unit}."
    """,
)
