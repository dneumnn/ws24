import os
import json

from gliner import GLiNER
from typing import Tuple, List

from llama_index.core.schema import BaseNode
from llama_index.core import Document
from llama_index.core.node_parser import SentenceSplitter

def _load_text(file_path: str) -> str:
    with open(file_path, "r") as f:
        text = f.read()
    return text

def _load_metadata(file_path: str) -> str:
    with open(file_path, "r") as f:
        metadata = json.loads(f.read())
    return metadata

def chunker(text:str, metadata={}, chunk_size=200) -> Tuple[Document, List[BaseNode]]:  
    document = Document(text=text, metadata=metadata)
    splitter = SentenceSplitter(
        chunk_size=chunk_size,     #words
        chunk_overlap=20,
    )
    nodes = splitter.get_nodes_from_documents([document])
    return (document, nodes)

if __name__ == "__main__":

    model = GLiNER.from_pretrained("urchade/gliner_medium-v2.1")

    file_path = f"..{os.sep}youtube{os.sep}data"
    file_path += f"{os.sep}PL05umP7R6ij3NTWIdtMbfvX7Z-4WEXRqD{os.sep}BHBAnUAdeyE"
    
    text_file = f"{file_path}{os.sep}grammar_corrected_sentences.txt"
    text = _load_text(text_file)
    metadata_file = f"{file_path}{os.sep}video.json"
    metadata = _load_metadata(metadata_file)

    labels = ["person", "machine learning", "knowledge area", "organization", "place"]

    (document, nodes) = chunker(text=text, metadata=metadata, chunk_size=200)

    entities_in_nodes = {}
    for node in nodes:
        entities = model.predict_entities(node.text, labels)
        node.metadata['entities'] = []
        for entity in entities:
            name = str(entity["text"]).lower()
            entity["text"] = name
            label = entity["label"]
            node.metadata['entities'].append((name, label))
            if name not in entities_in_nodes:
                entities_in_nodes[name] = set()
            entities_in_nodes[name].add(node.node_id)
    

        print(node.metadata['entities'])
