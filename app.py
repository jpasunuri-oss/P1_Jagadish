from src.main.llm import query_llm 

      
# Additional information that LLM does not know
f = open("context.txt", "r")
context = f.read()
f.close()

# Question about the context that LLM wouldn't know otherwise
#user_question = "What is Auryn's favorite food?"
user_question = input("Enter your prompt \n")

rag = {        
    "parameters": {
        "max_new_tokens": 150,
        "temperature": 0.2
    },
    "inputs": f"""
    <|system|>    
    </s>
    <|user|>
    Context: {context}
    Question:{user_question}
    </s>
    <|assistant|>
    """
}

reply = query_llm(rag)

for r in reply:
    #print(r)
    for k in r.keys():
        print(r[k])