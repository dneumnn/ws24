import asyncio

from pydantic import BaseModel
from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIModel

from openai import AsyncOpenAI

client = AsyncOpenAI(api_key="ollama", base_url="http://localhost:11434/v1")

model = OpenAIModel("llama3.2:latest", openai_client=client)

class CityLocation(BaseModel):
    city: str
    country: str

agent = Agent(model=model, result_type=CityLocation)

async def run(prompt):
    return await agent.run(prompt)
    
if __name__ == "__main__":
    prompt = "Where does the olympics held in 2012?"
    result = asyncio.run(run(prompt=prompt))
    print(result)

