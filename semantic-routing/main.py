from semantic_router import __version__ as semantic_router_version
from semantic_router import Route

if __name__ == "__main__":
    print(semantic_router_version)
    politics = Route(
        name="politics",
        utterances=[
            "isn't politics the best thing ever",
            "why don't you tell me about your political opinions",
            "don't you just love the president",
            "don't you just hate the president",
            "they're going to destroy this country!",
            "they will save the country!",
        ],
    )
    chitchat = Route(
        name="chitchat",
        utterances=[
            "how's the weather today?",
            "how are things going?",
            "lovely weather today",
            "the weather is horrendous",
            "let's go to the chippy",
        ],
    )

    # we place both of our decisions together into single list
    routes = [politics, chitchat]
    route_names = [route.name for route in routes]

    route_names = []
    utterances = []
    for route in routes:
        route_names.extend(len(route.utterances)*[route.name])
        utterances.extend(route.utterances)
    #print("utterances", len(utterances))

    from encoders.ollama import OllamaEncoder
    encoder = OllamaEncoder(name="something")
    
    embeddings = encoder(docs=utterances)
    #print("embeddings", len(embeddings))

    # Build a local Index
    from semantic_router.index.local import LocalIndex
    local_index = LocalIndex()
    local_index.dimensions = len(embeddings[0])
    local_index.add(embeddings=embeddings, routes=route_names, utterances=utterances)

    from semantic_router import SemanticRouter
    sr = SemanticRouter(encoder=encoder, routes=routes, index=local_index, top_k=2)
    
    #print("index", sr.index.index.shape)
    #print("index", sr.routes)

    for question in ["How is the weather in Florida?", "Do like the president?", "Is math realy important?", "Politics is cool!"]:
        for threshold in [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]:
            sr.set_threshold(threshold=threshold)
            embeddings = encoder(docs=[question])
            choice = sr(text=question, vector=embeddings[0])
            print(sr.get_thresholds(), choice.name)
        print(20*"=")
