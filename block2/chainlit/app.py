import chainlit as cl
from chainlit.input_widget import Select

from openai import OpenAI

# Initialize openai API and connect to Ollama
client = OpenAI(
    base_url = 'http://localhost:11434/v1',
    api_key='ollama', # required, but unused
)


system_prompt = """You are a restaurant with a local menu. You serve local specialities.
                    Special of today is:
                    - Flädlesuppe
                    - Rahmhackbraten mit Champigion, Spätzle und Salat
                    - Sauerbraten
                """

selected_model = "llama3.2:latest"

messages = [
    {"role": "system", "content": system_prompt}
]

@cl.on_chat_start
async def start():
    settings = await cl.ChatSettings(
        [
            Select(
                id="Model",
                label="Ollama hosted models",
                values=[model.id for model in client.models.list()],
                initial_index=0,
            )
        ]
    ).send()
    selected_model = settings["Model"]

def generate(messages, model):
    response = client.chat.completions.create(
        model= model,
        messages=  messages,
    )

    return response.choices[0].message.content

@cl.on_message
async def main(message: cl.Message):
    # Your custom logic goes here...
    messages.append({"role": "user", "content": message.content})
    response = generate(messages, selected_model)
    messages.append({"role": "assistant", "content": response})

    # Send a response back to the user
    await cl.Message(
        content = response,
    ).send()

