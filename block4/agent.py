'''
from smolagents import ToolCallingAgent, OpenAIServerModel, tool

@tool
def weather_tool(city: dict, date: str) -> str:
    """
    Retrievs the weather at any given city at any given date. Returns a string representation of the result.

    Args:
        city: The city to retrieve the weather information.
        date: The date to retrieve the weather information.
    """
    return f"The current weather in {city} at {date} is fine"

agent = ToolCallingAgent(
    tools=[weather_tool],
    model=OpenAIServerModel("meta-llama/Meta-Llama-3.1-8B-Instruct", api_base="http://localhost:11434/v1", api_key="ollama"),
)
'''
from smolagents.agents import ToolCallingAgent
from smolagents import tool, OpenAIServerModel
from typing import Optional

model = OpenAIServerModel("llama3.2:latest", api_base="http://localhost:11434/v1", api_key="ollama")

@tool
def get_weather(location: str, date: Optional[str] = None) -> str:
    """
    Get weather in the next days at given location.

    Args:
        location: the location
        date: the date
    """
    if date:
        return f"The weather in {location} at {date} is fine"
    else:
         return f"The weather in {location} is always fine"


agent = ToolCallingAgent(tools=[get_weather], model=model)

#print(agent.run("What's the weather like in Paris?"))

print(agent.run("How is the weather in London today?"))
