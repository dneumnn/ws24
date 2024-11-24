###############################################################################
# Chatbot
# run the app with streamlit run ./streamlit/chat.py
#
# This code is based on the example from Heiko Hotz: 
# https://towardsdatascience.com/build-your-own-chatgpt-like-app-with-streamlit-20d940417389 
###############################################################################

import logging
import streamlit as st
from streamlit_chat import message
from openai import OpenAI

logging.basicConfig(filename='./streamlit/chat.log', filemode='w+', level=logging.INFO)
logger = logging.getLogger('chat_app')
logger.setLevel(logging.INFO)

# Parameters
system_prompt = """You are a restaurant with a local menu. You serve local specialities.
                    Special of today is:
                    - Flädlesuppe
                    - Rahmhackbraten mit Champigion, Spätzle und Salat
                    - Sauerbraten
                """

# Initialize openai API and connect to Ollama
client = OpenAI(
    base_url = 'http://localhost:11434/v1',
    api_key='ollama', # required, but unused
)

# Initialize session state variables
if 'generated' not in st.session_state:
    st.session_state['generated'] = []
    logging.info("session state generated initialized.")
if 'past' not in st.session_state:
    st.session_state['past'] = []
    logging.info("session state past initialized.")
if 'number_tokens' not in st.session_state:
    st.session_state['number_tokens'] = []
if 'total_tokens' not in st.session_state:
    st.session_state['total_tokens'] = []

# Keeping track of conversation history: 
# the model understands the conversation context if we pass the conversation history to the API
if 'messages' not in st.session_state:
    st.session_state['messages'] = [
        {"role": "system", "content": system_prompt}
    ]
    logging.info("session state messages initialized with system prompt: '%s'.", system_prompt)

if 'models' not in st.session_state:
    models = client.models.list()
    models = [model.id for model in models]
    st.session_state['models'] = models
    logging.info("session state models initialized with list of available models: %s.", models)

def initialize_model():
    if "llama3.2:latest" in st.session_state['models']:
        _selected_model = "llama3.2:latest"
    else: 
        _selected_model = st.session_state['models'][0]
    logging.info("session state selected model initialized with: %s.", _selected_model)
    return _selected_model

if 'selected_model' not in st.session_state:
    selected_model = initialize_model()
    st.session_state['selected_model'] = []

######################### page title and header
# see https://docs.streamlit.io/develop/api-reference/configuration/st.set_page_config
st.set_page_config(page_title="Chatbot", page_icon=None, layout="centered", initial_sidebar_state="auto", menu_items=None)
st.markdown("<h1 style='text-align: center;'> Our first chatbot </h1>", unsafe_allow_html=True)

######################### Sidebar #########################
# https://docs.streamlit.io/develop/api-reference/widgets/st.selectbox
st.sidebar.title("Sidebar")
selected_model  = st.sidebar.selectbox("Choose a model:", st.session_state['models'])
logging.info("selected model changed to: %s.", selected_model)
placeholder = st.sidebar.empty()
placeholder.write( f"Total tokens: {sum(st.session_state['total_tokens'])}")
clear_button = st.sidebar.button("Clear Conversation", key="clear")

######################### Reset Chat Conversation #########
if clear_button:
    st.session_state['generated'] = []
    st.session_state['past'] = []
    st.session_state['messages'] = [
        {"role": "system", "content": system_prompt}
    ]
    selected_model = initialize_model()
    st.session_state['selected_model'] = []
    st.session_state['total_tokens'] = []
    placeholder.write(f"Total tokens: {sum(st.session_state['total_tokens'])}")

######################### Generate a response
def generate_response(prompt):
    st.session_state['messages'].append({"role": "user", "content": prompt})
    logging.info("selected model used was: %s.", selected_model)
    completion = client.chat.completions.create(
        model=selected_model,
        messages=st.session_state['messages']
    )
    response = completion.choices[0].message.content
    st.session_state['messages'].append({"role": "assistant", "content": response})

    # print(st.session_state['messages'])
    total_tokens = completion.usage.total_tokens
    prompt_tokens = completion.usage.prompt_tokens
    completion_tokens = completion.usage.completion_tokens
    return response, total_tokens, prompt_tokens, completion_tokens

###################### Container for chat history
response_container = st.container()
###################### Container for text box
container = st.container()

####################### Displaying the conversation
with container:
    with st.form(key='my_form', clear_on_submit=True):
        user_input = st.text_area("You:", key='input', height=100)
        submit_button = st.form_submit_button(label='Send')

    if submit_button and user_input:
        output, total_tokens, prompt_tokens, completion_tokens = generate_response(user_input)
        st.session_state['past'].append(user_input)
        st.session_state['generated'].append(output)
        st.session_state['selected_model'].append(selected_model)
        st.session_state['total_tokens'].append(total_tokens)

if st.session_state['generated']:
    with response_container:
        for i in range(len(st.session_state['generated'])):
            message(st.session_state["past"][i], is_user=True, key=str(i) + '_user')
            message(st.session_state["generated"][i], key=str(i))
            st.write(f"Model used: {st.session_state['selected_model'][i]}; Number of tokens: {st.session_state['total_tokens'][i]}")
            placeholder.write( f"Total tokens: {sum(st.session_state['total_tokens'])}")
