# agents
from agent_flow import health_wellness_agent
from our_agents.nutrition_agent import nutrition_agent
from our_agents.escalation_agent import escalation_agent
from our_agents.injury_agent import injury_agent


# asyncio for asyncronous programming
import asyncio

# utils
from utils.streaming import streamed_response
# configuration from utils 
from utils.agent_sdk_gemini_configuration import configuration

# context
from context import UserSessionContext

# hooks
from hooks import HealthWellnessRunHooks


async def main():
    # initialize the user session context
    user_context = UserSessionContext(
        name="ali",
        uid=1,
        history=[],
        diet_preferences="vegetarian",
    )
    
    # configuration from utils
    config = configuration("run")

    # Create run_hooks instance
    run_hooks = HealthWellnessRunHooks()

    # function to get the current agent
    def get_agent(ctx: UserSessionContext):
        agents = {
            "nutrition_agent": nutrition_agent,
            "injury_agent": injury_agent,
            "escalation_agent": escalation_agent,
            "health_wellness_agent": health_wellness_agent,
        }
        current_agent_name = ctx.current_agent or "health_wellness_agent"
        if current_agent_name not in agents:
            current_agent_name = "health_wellness_agent"
        main_agent = agents[current_agent_name]
        return main_agent

    condition = True
    while condition:
        print(f"\ncurrent_agent_name: {get_agent(user_context).name}")
        user_input = input("message: ")
        user_context.history.append({"role": "user", "content": user_input})

        if user_input.lower() == "e":
            condition = False
            print("Exiting the chat. Goodbye!")
        else:
            output = ""
            try:
                async for chunk in streamed_response(
                    get_agent(user_context),
                    user_context.history,
                    config,
                    user_context,
                    run_hooks,
                ):
                    print(chunk, end="", flush=True)
                    output += chunk
                print("")
                user_context.history.append({"role": "assistant", "content": output})
            except Exception as e:
                print(f"\n❌ Error in streaming: {str(e)}")


if __name__ == "__main__":
    asyncio.run(main())
