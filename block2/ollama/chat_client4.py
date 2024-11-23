import asyncio
from openai import AsyncOpenAI

client = AsyncOpenAI(
    base_url = 'http://localhost:11434/v1',
    api_key='ollama', # required, but unused
)

messages = [
  {
      'role': 'system', 
      'content': 'You are a helpful assistant.',
  },
  {
      'role': 'user',
      'content': 'Why is the sky blue?',
  },
]

async def main() -> None:
    response =  await client.chat.completions.create(
        model="llama3.2:latest",
        messages=messages
    )
    print(response)


asyncio.run(main())








