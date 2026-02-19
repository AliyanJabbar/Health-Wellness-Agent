from agents import RunContextWrapper, handoff
from context import UserSessionContext


# one time handoff function to handle the handoff logic
def handoff_handler(
    agent, on_handoff_message: str, prev_agent_name: str = "health_wellness_agent"
):
    def handoff_callback(wrapper: RunContextWrapper[UserSessionContext]):
        print(on_handoff_message)
        # 1.adding handoff logs
        if hasattr(wrapper, "context") and hasattr(wrapper.context, "add_handoff_log"):
            wrapper.context.add_handoff_log(
                {
                    "from": prev_agent_name,
                    "to": agent.name,
                    "message": on_handoff_message,
                }
            )
        # 2.updating current agent
        if hasattr(wrapper, "context") and hasattr(wrapper.context, "current_agent"):
            wrapper.context.current_agent = str(agent.name)

        # return agent #we don't need this

    return handoff(
        agent=agent,
        on_handoff=handoff_callback,
    )
