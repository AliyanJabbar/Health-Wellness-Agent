# # agents
# from agents import (
#     Runner,
#     InputGuardrailTripwireTriggered,
#     OutputGuardrailTripwireTriggered,
#     trace,
#     SQLiteSession,
# )
# from openai.types.responses import ResponseTextDeltaEvent
# from agent_flow import health_wellness_agent
# from our_agents.nutrition_agent import nutrition_agent
# from our_agents.escalation_agent import escalation_agent
# from our_agents.injury_agent import injury_agent

# # asyncio for asyncronous programming
# import asyncio

# # configuration from utils
# from utils.agent_sdk_gemini_configuration import config

# # context
# from context import UserSessionContext

# # hooks
# from hooks import HealthWellnessRunHooks


# async def main():
#     # initialize the user session context
#     user_context = UserSessionContext(
#         name="user",
#         uid=1,
#         diet_preferences=[],
#     )
#     user_session = SQLiteSession(user_context.uid)
#     # Create run_hooks instance
#     run_hooks = HealthWellnessRunHooks()

#     # function to get the current agent
#     agents = {
#         "nutrition_agent": nutrition_agent,
#         "injury_agent": injury_agent,
#         "escalation_agent": escalation_agent,
#         "health_wellness_agent": health_wellness_agent,
#     }

#     condition = True
#     while condition:
#         current_agent_name = user_context.current_agent or "health_wellness_agent"
#         current_agent = agents.get(current_agent_name, agents["health_wellness_agent"])
#         print(f"\ncurrent_agent_name: {current_agent_name}")
#         user_input = input("message: ")

#         if user_input.lower() == "e":
#             condition = False
#             print("Exiting the chat. Goodbye!")
#         else:
#             output = ""
#             try:
#                 with trace("health_wellness_agent"):
#                     result = Runner.run_streamed(
#                         current_agent,
#                         user_input,
#                         run_config=config,
#                         context=user_context,
#                         hooks=run_hooks,
#                         session=user_session,
#                     )
#                     async for chunk in result.stream_events():
#                         if chunk.type == "raw_response_event" and isinstance(
#                             chunk.data, ResponseTextDeltaEvent
#                         ):
#                             print(chunk.data.delta, end="", flush=True)
#                             output += chunk.data.delta
#                     print("")
#             except InputGuardrailTripwireTriggered:
#                 print(f"\n 🚫 Input guardrail triggered. Please refine your input.")
#             except OutputGuardrailTripwireTriggered:
#                 print(
#                     f"\n 🚫 Output guardrail triggered. Agent's response was blocked."
#                 )
#             except Exception as e:
#                 print(f"\n ❌ Error in streaming: {str(e)}")


# if __name__ == "__main__":
#     asyncio.run(main())


# --------------------- FAST API ---------------------

# from fastapi import FastAPI
# from fastapi.middleware.cors import CORSMiddleware
# from fastapi.responses import StreamingResponse
# from pydantic import BaseModel
# from agents import (
#     Agent,
#     Runner,
# )
# from openai.types.responses import ResponseTextDeltaEvent
# from utils.agent_sdk_gemini_configuration import config, gemini_key

# # from tools.get_services_info import get_services_info
# # from tools.get_skills_info import get_skills_info
# # from tools.get_social_info import get_social_info
# import os
# import json
# from typing import List, Dict, Literal

# app = FastAPI()

# # Add CORS middleware
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=[os.getenv("WEB_URL")],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )


# class ChatRequest(BaseModel):
#     messages: List[Dict[Literal["role", "text"], str]]


# @app.post("/chat")
# async def chat(request: ChatRequest):
#     print("📥 Received messages:", request.messages)

#     async def generate_response():
#         try:
#             agent = Agent(
#                 name="Aliyan Jabbar's Portfolio Assistant",
#                 instructions="""
#                 You are a professional AI assistant representing Aliyan Jabbar, an AI Agents & Chatbots developer | a passionate Frontend and UI/UX Developer focused on building interactive and responsive web applications. Along with them I am using AI to make work Fast and Smooth, from Planing to Building and Building to Deployment.

#                 Availiability: Aliyan is Currently Availiable for new projects and collaborations.

#                 Your Responsibilities:
#                 - Introduce Aliyan professionally when asked about him or his work.
#                 - Provide clear, skill-based responses based on Aliyan's capabilities.
#                 - Keep in mind that Aliyan Jabbar is a Web Apps | AI Agents & Chatbots developer not designer.

#                 Answering Guidelines:
#                 - use appropriate tools if required:
#                     -> social_info_tool: to get info about Aliyan's social handles and contact details
#                     -> skills_info_tool: to get info about Aliyan's skills
#                     -> services_info_tool: to get detials about services that Aliyan offers
#                 - Provide proper response in markdown format using bullet points and bold and italic text.
#                 - Keep initial responses short (1-2 lines).
#                 - For descriptive or technical questions, provide clear and structured answers using bullet points.
#                 - Decline to answer off-topic or irrelevant questions such as:
#                 - What's the weather?
#                 - What is today's date?
#                 - Trivia, jokes, entertainment
#                 - Maintain professionalism in tone, always focusing on Aliyan's work and capabilities.

#                 """,
#                 # tools=[get_social_info, get_services_info, get_skills_info],
#             )

#             print("⚙️ Running agent...")
#             result = Runner.run_streamed(
#                 agent,
#                 input="\n".join(
#                     [
#                         f"{message['role']}: {message['text']}"
#                         for message in request.messages
#                     ]
#                 ),
#                 run_config=config,
#             )

#             async for event in result.stream_events():
#                 if event.type == "raw_response_event" and isinstance(
#                     event.data, ResponseTextDeltaEvent
#                 ):
#                     chunk_data = {"chunk": event.data.delta}
#                     yield f"{json.dumps(chunk_data)}\n\n"
#                     print({"chunk": chunk_data})
#                 # tool debugging
#                 elif event.type == "run_item_stream_event":
#                     if event.item.type == "tool_call_item":
#                         print(f"{event.item.raw_item.name} Tool was called")

#         except Exception as e:
#             print("❌ Error:", str(e))
#             error_data = {"error": str(e)}
#             yield f"{json.dumps(error_data)}\n\n"

#     return StreamingResponse(
#         generate_response(),
#         media_type="text/plain",
#         headers={
#             "Cache-Control": "no-cache",
#             "Connection": "keep-alive",
#         },
#     )


# @app.get("/")
# async def health():
#     tools = []
#     # if get_services_info:
#     #     tools.append("get_services_info")
#     # if get_social_info:
#     #     tools.append("get_social_info")
#     # if get_skills_info:
#     #     tools.append("get_skills_info")
#     return {
#         "status": "healthy",
#         "response": "api set" if gemini_key else "API key missing",
#         "gemini_api_key_set": bool(gemini_key),
#         "tools": tools,
#         "web_url": os.getenv("WEB_URL", "not set"),
#     }


import json
from typing import Literal

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

from agents import (
    InputGuardrailTripwireTriggered,
    OutputGuardrailTripwireTriggered,
    Runner,
    SQLiteSession,
    trace,
)
from agent_flow import health_wellness_agent
from openai.types.responses import ResponseTextDeltaEvent

# context
from context import UserSessionContext

# hooks
from hooks import HealthWellnessRunHooks

# handoffs
from our_agents.escalation_agent import escalation_agent
from our_agents.injury_agent import injury_agent
from our_agents.nutrition_agent import nutrition_agent

# configuration from utils
from utils.agent_sdk_gemini_configuration import config, gemini_key, openai_key

# tools
from tools.goal_analyzer import goal_analyzer
from tools.meal_planner import meal_planner_tool
from tools.workout_recommender import workout_recommender_tool
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[os.getenv("WEB_URL")],
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)


class ChatRequest(BaseModel):
    """
    Pydantic model for validating the chat request body.
    """

    messages: list[dict[Literal["role", "text"], str]]
    user_id: int


@app.post("/chat")
async def chat(request: ChatRequest):
    """
    Handles the chat interaction with the various agents.
    Streams the agent's response back to the client.
    """

    # initialize the user session context
    user_context = UserSessionContext(
        name="user",
        uid=request.user_id,
        diet_preferences=[],
    )
    user_session = SQLiteSession(user_context.uid)
    # Create run_hooks instance
    run_hooks = HealthWellnessRunHooks()

    agents = {
        "nutrition_agent": nutrition_agent,
        "injury_agent": injury_agent,
        "escalation_agent": escalation_agent,
        "health_wellness_agent": health_wellness_agent,
    }

    async def generate_response():
        """
        Generates the agent's response asynchronously.
        """
        try:
            current_agent_name = user_context.current_agent or "health_wellness_agent"
            current_agent = agents.get(
                current_agent_name, agents["health_wellness_agent"]
            )
            print(f"\ncurrent_agent_name: {current_agent_name}")

            user_input = request.messages[-1]["text"]

            with trace("health_wellness_agent"):
                result = Runner.run_streamed(
                    current_agent,
                    user_input,
                    run_config=config,
                    context=user_context,
                    hooks=run_hooks,
                    session=user_session,
                )
                async for chunk in result.stream_events():
                    if chunk.type == "raw_response_event" and isinstance(
                        chunk.data, ResponseTextDeltaEvent
                    ):
                        delta = chunk.data.delta
                        yield f"{json.dumps({'chunk': delta})}\n\n"
                        print(delta, end="", flush=True)

        except InputGuardrailTripwireTriggered:
            error_message = "Input guardrail triggered. Please refine your input."
            print(f"\n 🚫 {error_message}")
            yield f"{json.dumps({'error': error_message})}\n\n"
        except OutputGuardrailTripwireTriggered:
            error_message = "Output guardrail triggered. Agent's response was blocked."
            print(f"\n 🚫 {error_message}")
            yield f"{json.dumps({'error': error_message})}\n\n"
        except Exception as e:
            error_message = f"Error in streaming: {str(e)}"
            print(f"\n ❌ {error_message}")
            yield f"{json.dumps({'error': error_message})}\n\n"

    return StreamingResponse(
        generate_response(),
        media_type="text/plain",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
        },
    )


@app.get("/")
async def health():
    """
    A simple health check endpoint.
    """
    tools = []
    handoffs = []
    # getting tools
    if goal_analyzer:
        tools.append("goal_analyzer")
    if meal_planner_tool:
        tools.append("meal_planner_tool")
    if workout_recommender_tool:
        tools.append("workout_recommender_tool")

    # getting handoffs
    if nutrition_agent:
        handoffs.append("nutrition_agent")
    if injury_agent:
        handoffs.append("injury_agent")
    if escalation_agent:
        handoffs.append("escalation_agent")
    return {
        "status": "healthy",
        "response": "All API keys are set" if gemini_key and openai_key else "API key missing",
        "gemini_api_key_set": bool(gemini_key),
        "openai_api_key_set": bool(openai_key),
        "tools": tools,
        "main_agent": "health_wellness_agent" if health_wellness_agent else "not found",
        "handoffs": handoffs,
        "web_url": os.getenv("WEB_URL", "not set"),
    }
