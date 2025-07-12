from dotenv import load_dotenv
import os
from agents import AsyncOpenAI, OpenAIChatCompletionsModel, RunConfig
from typing import Literal


def configuration(base: Literal["agent", "run"]):
    load_dotenv()

    gemini_key = os.getenv("GEMINI_API_KEY")

    external_client = AsyncOpenAI(
        api_key=gemini_key,
        base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
    )

    external_model = OpenAIChatCompletionsModel(
        model="gemini-2.0-flash", openai_client=external_client
    )

    config = RunConfig(
        model=external_model,
        tracing_disabled=True,
        model_provider=external_client,
    )

    if base == "agent":
        return external_model
    elif base == "run":
        return config
    else:
        print("please specify base !")
