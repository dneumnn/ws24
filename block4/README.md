# WS24 - Intelligente Informationssysteme

## Block 4: Agentic Systems

### Installation

```bash
conda create --name "block4" python=3.11
conda activate block4
pip install jupyter
pip install pydantic-ai
pip install instructor 
```

### Instructor

Get struictured outputs from LLMs.

see:

- <https://python.useinstructor.com>

### Natural Language Embedded Programs (NLEPs)

NLEP involves prompting a language model to create and execute a Python program to solve a user’s query, and then output the solution as natural language.

see:

- <https://news.mit.edu/2024/technique-improves-reasoning-capabilities-large-language-models-0614>
- <https://arxiv.org/pdf/2309.10814>
- <https://github.com/luohongyin/LangCode>

### Program of Thoughts

PoT prompting has the LLM generate reasoning steps as programming language statements,  which are then executed by an external interpreter like Python.

While Chain-of-Thought uses LLMs for both reasoning and computation, PoT uses LLMs only for reasoning, but instead of using plain text for computations, it leverages code.

see:

- <https://medium.com/ai-advances/next-generation-in-chain-of-thought-program-of-thoughts-5c6ca75ee4fa>
- <https://github.com/TIGER-AI-Lab/Program-of-Thoughts>
- <https://arxiv.org/pdf/2211.12588>