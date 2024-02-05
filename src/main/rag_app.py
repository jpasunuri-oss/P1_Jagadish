from dotenv import load_dotenv
import os
import chromadb
import csv
from csv import reader
from huggingface_embedding import HuggingFaceEmbeddingInference
from llm import query_llm 
import streamlit as st

# Load dot_env 
load_dotenv()

def getContext(user_input):
  
    # Create Persistent Chroma DB
    client = chromadb.PersistentClient(path = "./chroma")
    
    # Create Collection
    try:
        client.delete_collection(name="proj2")
        #print("deleted the collection")
    except ValueError:
        print(f"proj2 collection does not exist. creating new collection")

    embedding_fun = HuggingFaceEmbeddingInference(url=os.getenv("EMBEDDINGMODEL_URL"), key=os.getenv("HUGGING_FACE_KEY"))
    
    collection = client.get_or_create_collection(name="proj2", embedding_function=embedding_fun)
    
    # Read Data from csv file
    with open("./resources/menu_items.csv") as file:
        file_data = list(csv.reader(file))
        
    # Create Documents, Metadatas & Ids list
    
    docs = [col[1] for col in file_data]
    metadatas = [{"title":col[0]} for col in file_data]
    ids = [str(i) for i in range(len(file_data))]

    # Chunk the documents
    chunk_size = 25
    doc_chunks = [docs[i:i + chunk_size] for i in range(0, len(docs), chunk_size)]
    id_chunks = [ids[i:i + chunk_size] for i in range(0, len(ids), chunk_size)]
    metadata_chunks = [metadatas[i:i + chunk_size] for i in range(0, len(metadatas), chunk_size)]
    
    # Load the chunked documents in to the collection  
      
    for id_chunks, doc_chunks, metadata_chunks in zip(id_chunks, doc_chunks, metadata_chunks):
        collection.add(documents=doc_chunks, metadatas=metadata_chunks, ids=id_chunks)

    results = collection.query(query_texts=[user_input], include=["documents"], n_results=2)
    
    context = ', '.join(results["documents"][0])
    
    #print("Context", context)
    
    return context

def queryLLM(context, user_input):
    
    # LLM
    prompt = {        
        "parameters": {
            "max_new_tokens": 150,
            "temperature": 0.2
        },
        "inputs": f"""
        <|system|>    
        </s>
        <|user|>
        Context: {context}
        Question:{user_input}
        </s>
        <|assistant|>
        """
    }
    
    reply = query_llm(prompt)
           
    return reply 


context = ""

if 'chat-history' not in st.session_state:
    st.session_state['chat-history'] = [
    {
        "role": "ai",
        "message": "welcome!"
    }
]
  
user_input = st.chat_input("Message:")

if user_input:
                   
    st.session_state['chat-history'].append({
        "role": "user",
        "message": user_input
    })       
    
    if context == "":      
        context = getContext(user_input)  
        st.session_state['chat-history'].append({
            "role": "ai",
           "message": "Context: " + context
        })        
    
    print("Context", context)
    
    llm_response = queryLLM(context, user_input)

    ai_response = llm_response[0]["generated_text"]
    
    #if "<|assistant|>" in ai_response:
        #ai_response = ai_response[ai_response.index("<|assistant|>") + len("<|assistant|>"):]
    
    st.session_state['chat-history'].append({
        "role": "ai",
        "message": ai_response
    })
    
if 'chat-history' in st.session_state:
    for i in range(0, len(st.session_state['chat-history'])):
        msg = st.session_state['chat-history'][i]
        st.chat_message(msg['role']).write(msg['message'])