# WS24 - Intelligente Informationssysteme

## Block 2: Conversational AI

In block 2 we work with jupyter notebook and visual code.

### Fine-Tuning

For Fine-Tuning we use two notebooks

```bash
conda create --name block2_sft python=3.11
conda activate block2_sft
pip install jupyter torch transformers 
pip install scikit-learn pandas
pip install datasets accelerate
```

### Inference Engine

#### Install and Run Ollama Server

Download and install Inference Engine Ollama: <https://ollama.com/download>

```bash
ollama run llama3.2
```

Ollama runs at <http://localhost:11434>

#### Install Ollama and OpenAI Client Library

```bash
conda create --name block2_ol python=3.11
conda activate block2_ol
pip install ollama openai
```

### Streamlit

A faster way to build and share data apps: <https://streamlit.io>

Build a chatbot based on Streamlit.

```bash
conda create --name streamlit python=3.11
conda activate streamlit
pip install ollama openai
pip install streamlit streamlit_chat
```

Run an Application with:

```bash
streamlit run your_app.py
```

Streamlit runs at <http://localhost:8501>

#### Test streamlit

```bash
streamlit hello
```

### Chatlit

```bash
conda create --name chainlit python=3.11
conda acivate chainlit
pip install chainlit openai
mkdir chainlit
cd chainlit
chainlit init
chainlit hello
```

### Open WebUI

#### Install and Run

Please keep attention: Open WebUI framework only works with python 3.11! So we use the docker installation.

```bash
git clone https://github.com/open-webui/open-webui.git
cd open-webui
docker run -d -p 3000:8080 --add-host=host.docker.internal:host-gateway -e OLLAMA_BASE_URL=http://localhost:11434/v1  -v path-to-your-data-on-host:/app/backend/data --name open-webui --restart always ghcr.io/open-webui/open-webui:main
```

1. Port mapping: -p 3000:8080
2. Gateway to call local host from outside the container: --add-host=host.docker.internal:host-gateway
3. Set the Ollama url: -e OLLAMA_BASE_URL=<http://localhost:11434/v1>
4. Set path-to-your-data-on-host to your local path where webui should store all data: -v host_directory:container_directory image for mappig volumes
5. Give the container a name: --name open-webui
6. --restart always

```bash
docker run -d -p 3000:8080 --add-host=host.docker.internal:host-gateway -e OLLAMA_BASE_URL=http://localhost:11434/v1 -v "/Users/done/Documents/Hochschule/WS 2024/WI-Intelligente-Informationssysteme/ws24/block2/data":/app/backend/data --name open-webui --restart always ghcr.io/open-webui/open-webui:main
```

#### Configure Open WebUI

1.Storing Users
2.Storing Documents
3.Connect to Ollama or OpenAI API

set environment variable OLLAMA_BASE_URL

```bash
docker run -d -p 3000:8080 -e OLLAMA_BASE_URL=https://example.com -v path-to-your-data-on-host:/app/backend/data --name open-webui --restart always ghcr.io/open-webui/open-webui:main
```

Use OLLAMA_BASE_URLs for Ollama Load Balancing: -e OLLAMA_BASE_URLS="<http://ollama-one:11434;http://ollama-two:11434>"

Set environment variable OPENAI_API_KEY and OPENAI_API_BASE_URL

```bash
docker run -d -p 3000:8080 -e OPENAI_API_KEY=your_secret_key -v path-to-your-data-on-host:/app/backend/data --name open-webui --restart always ghcr.io/open-webui/open-webui:main
```

For Load Balancing use:

- OPENAI_API_BASE_URLS="<https://api.openai.com/v1;https://api.mistral.ai/v1>"
- OPENAI_API_KEYS="<OPENAI_API_KEY_1>;<OPENAI_API_KEY_2>"

Nemotron:
<https://medium.com/@ai-for-devs.com/building-an-openai-o1-clone-with-nemotron-runpod-and-openwebui-98cf9ce61679>

### Enhance open webui with custom code

<https://medium.com/pythoneers/optimize-open-webui-three-practical-extensions-for-a-better-user-experience-cbe365af60b1>

Using Tools
<https://medium.com/write-a-catalyst/how-to-use-tools-with-open-webui-9725db2724bb>

By default, the system employs a local SQLite database webui.db for basic data storage and chroma DB for Vector storage

Use sqlite3 to inspect the database with .tables .schema table-name

<https://python.land/sqlite>

Use DATABASE_URL environment variable for external db use
