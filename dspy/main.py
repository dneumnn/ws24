import dspy


model_id = "llama3.2:latest"
'''
model_id = "Teuken-7B-instruct-commercial-v0.4-GGUF:latest"
user="Hi!"
lang_code = "DE"
system_messages={
            "EN": "A chat between a human and an artificial intelligence assistant."
            " The assistant gives helpful and polite answers to the human's questions.",
            "DE": "Ein Gespräch zwischen einem Menschen und einem Assistenten mit künstlicher Intelligenz."
            " Der Assistent gibt hilfreiche und höfliche Antworten auf die Fragen des Menschen.",
        }
system_prompt = f"System: {system_messages[lang_code]}"
'''
 
#Use the default settings
model = dspy.OllamaLocal(model=model_id, 
                         model_type="chat",
                         base_url="http://localhost:11434",
                         timeout_s=120, 
                         temperature=0, 
                         max_tokens= 50, 
                         top_p=1, 
                         top_k=20, 
                         frequency_penalty=0, 
                         presence_penalty=0, 
                         n= 1, 
                         num_ctx=1024, 
                         format= None, #Literal['json'] 
                         system=None
                         )

response = model("say hello")

print(response)