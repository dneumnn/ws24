# Web Serach Agent with PydanticAI

from openai import AsyncOpenAI
from openai import OpenAI

from pydantic_ai.models.openai import OpenAIModel
from pydantic_ai import Agent, ModelRetry, RunContext

client = OpenAI(api_key="ollama", base_url="http://localhost:11434/v1")


############ Web Search API ##########
from googlesearch import search, SearchResult
results = search("What are large reasoning models?", 
                 num_results=10,
                 advanced=True)

for result in results:
    print(result.title)
    print(result.url)
    print(result.description)
    print("="*40)
