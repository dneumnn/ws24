import os

from typing import List, Optional

import ollama

from semantic_router.encoders import DenseEncoder
from semantic_router.schema import EncoderInfo
from semantic_router.utils.logger import logger


model_configs = {
    "nomic-embed-text": EncoderInfo(
        name="nomic-embed-text",
        token_limit=8192,
        threshold=0.7, 
    ),
}

# according to EncoderDefault.OPENAI
OLLAMA = {
    "embedding_model": os.getenv("OLLAMA_MODEL_NAME", "nomic-embed-text"),
    "language_model": os.getenv("OLLAMA_CHAT_MODEL_NAME", "llama3.2"),
}

class OllamaEncoder(DenseEncoder):
    client: Optional[ollama.Client]
    #async_client: Optional[ollama.AsyncClient] not used yet
    token_limit: int = 8192  # default value for nomic-embed-text 

    def __init__(
            self,
            name: Optional[str] = None,
            ollama_base_url: Optional[str] = None,
            score_threshold: Optional[float] = None,
        ):
            # test model name
            if name not in model_configs:
                logger.warning(
                    f"Embedding model not valid: {name}. Using default value {OLLAMA['embedding_model']}."
                )
                name = OLLAMA["embedding_model"] # set default

            if score_threshold is None and name in model_configs:
                set_score_threshold = model_configs[name].threshold
            
            elif score_threshold is None:
                logger.warning(
                    f"Score threshold not set for model: {name}. Using default value."
                )
                set_score_threshold = 0.7
            else:
                set_score_threshold = score_threshold
            super().__init__(
                name=name,
                score_threshold=set_score_threshold,
            )

            base_url = ollama_base_url or os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")

            try:
                self.client = ollama.Client(host=base_url)
                #self.async_client = ollama.AsyncClient(host=base_url) not used yet
            except Exception as e:
                raise ValueError(
                    f"Ollama API client failed to initialize. Error: {e}"
                ) from e

            # if model name is known, set token limit
            if name in model_configs:
                self.token_limit = model_configs[name].token_limit

    def __call__(self, docs: List[str]) -> List[List[float]]:
        if self.client is None:
            raise ValueError("Ollama client is not initialized.")
        try:
            embeds = self.client.embed(model=self.name, input=docs, truncate=None)
            return embeds.embeddings
        except Exception as e:
            raise ValueError(f"Ollama API call failed. Error: {e}") from e