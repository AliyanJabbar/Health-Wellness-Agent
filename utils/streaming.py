# from agents import (
#     Runner,
#     InputGuardrailTripwireTriggered,
#     OutputGuardrailTripwireTriggered,
# )
# from openai.types.responses import ResponseTextDeltaEvent


# async def streamed_response(agent, user_input, run_config, user_context, run_hooks):
#     """Centralized streaming response handler"""

#     try:
#         result = Runner.run_streamed(
#             agent,
#             input=user_input,
#             run_config=run_config,
#             context=user_context,
#             hooks=run_hooks,
#         )

#         async for event in result.stream_events():
#             if event.type == "raw_response_event" and isinstance(
#                 event.data, ResponseTextDeltaEvent
#             ):
#                 yield event.data.delta

#     except InputGuardrailTripwireTriggered:
#         yield f"\n⚠️ Input guardrail triggered. Please refine your input."
#     except OutputGuardrailTripwireTriggered:
#         yield f"\n⚠️ Output guardrail triggered. Agent's response was blocked."
#     except Exception as e:
#         yield f"\n❌ Streaming error: {str(e)}"




from agents import (
    Runner,
    InputGuardrailTripwireTriggered,
    OutputGuardrailTripwireTriggered,
)
from openai.types.responses import ResponseTextDeltaEvent


async def streamed_response(agent, user_input, run_config, user_context, run_hooks=None):
    """Centralized streaming response handler"""

    try:
        # Pass hooks to Runner.run_streamed if available
        if run_hooks:
            result = Runner.run_streamed(
                agent, input=user_input, run_config=run_config, context=user_context, hooks=run_hooks
            )
        else:
            result = Runner.run_streamed(
                agent, input=user_input, run_config=run_config, context=user_context
            )

        async for event in result.stream_events():
            if event.type == "raw_response_event" and isinstance(
                event.data, ResponseTextDeltaEvent
            ):
                yield event.data.delta

    except InputGuardrailTripwireTriggered:
        yield f"\n⚠️ Input guardrail triggered. Please refine your input."
    except OutputGuardrailTripwireTriggered:
        yield f"\n⚠️ Output guardrail triggered. Agent's response was blocked."
    except Exception as e:
        yield f"\n❌ Streaming error: {str(e)}"
        import traceback
        traceback.print_exc()
