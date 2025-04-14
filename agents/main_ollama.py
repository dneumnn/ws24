model_id = "qwq" #"llama3.2:latest"

from pydantic_ai.models.ollama import OllamaModel
model = OllamaModel(model_id)

#from pydantic_ai.models.openai import OpenAIModel
#from openai import AsyncOpenAI
#client = AsyncOpenAI(api_key="ollama", base_url="http://localhost:11434/v1")

#model = OpenAIModel("qwq", openai_client=client)

from pydantic import BaseModel
class ShoppingCart(BaseModel):
    product: str
    amount: int

from pydantic_ai import Agent
agent = Agent(model=model,result_type=ShoppingCart) #, system_prompt="You are a webshop agent selling food and beverages")

import asyncio

async def run():
    result = await agent.run(user_prompt="Carol puts 7 cans of peas in the shopping cart")


asyncio.run(run())