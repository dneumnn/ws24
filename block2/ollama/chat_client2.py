from openai import OpenAI

client = OpenAI(
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

# ['Config', 'choices', 'construct', 'copy', 'created', 'dict', 'from_orm', 'id', 'json', 
#  'model', 'model_construct', 'model_dump', 'model_dump_json', 'model_fields_set', 'object', 
#  'parse_file', 'parse_obj', 'parse_raw', 'schema', 'schema_json', 'service_tier', 'system_fingerprint', 'to_dict', 'to_json', 
#   'update_forward_refs', 'usage', 'validate']
response = client.chat.completions.create(
  model="llama3.2:latest",
  messages=messages,
)

# 'alias_generator', 'allow_inf_nan', 'allow_mutation', 'allow_population_by_field_name', 'anystr_lower', 'anystr_strip_whitespace', 
# 'anystr_upper', 'arbitrary_types_allowed', 'copy_on_model_validation', 'error_msg_templates', 'extra', 'fields', 'frozen', 
# 'get_field_info', 'getter_dict', 'json_dumps', 'json_encoders', 'json_loads', 'keep_untouched', 'max_anystr_length', 
# 'min_anystr_length', 'orm_mode', 'post_init_call', 'prepare_field', 'schema_extra', 'smart_union', 'title', 
# 'underscore_attrs_are_private', 'use_enum_values', 'validate_all', 'validate_assignment']

#config = response.Config
#print("Config : ", config.fields)

print("Choices: ",len(response.choices))
# finish_reason, index, logprobs, 
# message=ChatCompletionMessage(content="", refusal=None, role='assistant', audio=None, function_call=None, tool_calls=None)

for choice in response.choices:
    print("role   : ",choice.message.role)
    print("message: ",choice.message.content)
