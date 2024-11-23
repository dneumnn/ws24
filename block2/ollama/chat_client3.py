# Get all available models

from openai import OpenAI

client = OpenAI(
    base_url = 'http://localhost:11434/v1',
    api_key='ollama', # required, but unused
)

# 'api_key', 'audio', 'auth_headers', 'base_url', 'batches', 'beta', 'chat', 'close', 'completions', 'copy', 'custom_auth', 
# 'default_headers', 'default_query', 'delete', 'embeddings', 'files', 'fine_tuning', 'get', 'get_api_list', 'images', 'is_closed', 
# 'max_retries', 'models', 'moderations', 'organization', 'patch', 'platform_headers', 'post', 'project', 'put', '
# 'qs', 'request', 'timeout', 'uploads', 'user_agent', 'with_options', 'with_raw_response', 'with_streaming_response'


# ['delete', 'list', 'retrieve', 'with_raw_response', 'with_streaming_response']
models = client.models.list()
for model in models:
    print(model.id)
