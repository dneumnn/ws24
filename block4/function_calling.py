# sqlite3 is build-in ijn python
# https://docs.python.org/3.10/library/sqlite3.html
# import sqlite3

# This is a function that we want the model to be able to call
def get_customer_id(email_adress: str) -> str:
    print("email_adress", email_adress)
    # Connect to the database
    #conn = sqlite3.connect('./data/webui.db')
    #cursor = conn.cursor()
    #statement = f'select id from user where email="{email_adress}"'
    #response = []
    #for row in cursor.execute(statement):
    #    response.append(row[0])

    #conn.close()
    #return response
    return [4711]

from openai import OpenAI

client = OpenAI(
    base_url = 'http://localhost:11434/v1',
    api_key='ollama', # required, but unused
)

messages = [
  {
      'role': 'system', 
      'content': 'You are a helpful customer support assistant. Use the supplied tools to assist the user."',
  },
  {
      'role': 'user',
      'content': 'What is the customer id of the customer with email adress dominik.marc.neumann@icloud.com',
  },
]

tools = [
    {
        "type": "function",
        "function": {
            "name": "get_customer_id",
            "description": "Get the customer id for a customer with a given email adress. Call this whenever you need to know the customer id, for example when a somebody asks 'Get the customer id for the following email adress'",
            "parameters": {
                "type": "object",
                "properties": {
                    "email_adress": {
                        "type": "string",
                        "description": "The email adress of the customer.",
                    },
                },
                "required": ["email_adress"],
                "additionalProperties": False,
            },
        }
    }
]

response = client.chat.completions.create(
  model="llama3.2:latest",
  messages=messages,
  tools=tools,
)

# message=ChatCompletionMessage(content="", refusal=None, role='assistant', audio=None, function_call=None, tool_calls=None)

#for choice in response.choices:
#    print("role     : ", choice.message.role)
#    print("message  : ", choice.message.content)
#    print("tool_call: ", choice.message.tool_calls)

# Extract the arguments for get_customer_id

tool_call = response.choices[0].message.tool_calls[0]
print(tool_call)

import json
arguments = json.loads(tool_call.function.arguments)
email_adress = arguments.get('email_adress')

# Call the get_delivery_date function with the extracted order_id
customer_id = get_customer_id(email_adress)
print(customer_id)
