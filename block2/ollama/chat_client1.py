import ollama

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


#reponse dict_keys(['model', 'created_at', 'message', 'done_reason', 'done', 'total_duration', 'load_duration', 
#                   'prompt_eval_count', 'prompt_eval_duration', 'eval_count', 'eval_duration'])
response = ollama.chat(model='llama3.2:latest', messages=messages)


print("--------------------------------------")
print("role    : ",response.message.role)    #response['message']['role'])
print("message : ",response.message.content) #response['message']['content'])
print("count   : ",response.eval_duration)
print("duration: ",response.prompt_eval_duration)
print("model   : ",response.model)

