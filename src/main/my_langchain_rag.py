import streamlit as st
import os
from dotenv import load_dotenv

from langchain_community.llms import HuggingFaceTextGenInference
from langchain.output_parsers import CommaSeparatedListOutputParser
from langchain_core.output_parsers import StrOutputParser
from langchain_community.chat_models.huggingface import ChatHuggingFace
from langchain_community.llms.huggingface_endpoint import HuggingFaceEndpoint
from langchain_core.prompts import HumanMessagePromptTemplate, SystemMessagePromptTemplate, ChatPromptTemplate, MessagesPlaceholder
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationChain

# Load dot_env 
load_dotenv()

prompt_template = """
<|system|>
You are a helpful assistant. Follow the user's instruction to the best of your capabilities. </s>
<|user|>
{user_input}</s>
<|assistant|>
"""

llm = HuggingFaceEndpoint(
    endpoint_url=os.environ['LLM_ENDPOINT'], 
    huggingfacehub_api_token=os.getenv('HF_TOKEN'), 
    task="text2text-generation",
    model_kwargs={
        "max_new_tokens": 200
    }
)
system_prompt = SystemMessagePromptTemplate.from_template(f"You are a helpful assistant. Follow the user's instruction to the best of your capabilities")
chat_prompt = ChatPromptTemplate.from_messages(
                    [
                        system_prompt, 
                        #MessagesPlaceholder(variable_name="chat_history"),
                        HumanMessagePromptTemplate.from_template("{user_input}")
                    ])

conversation_buf = ConversationBufferMemory(return_messages=True, input_key="chat_history")
   
chat_model = ChatHuggingFace(llm=llm)

#chain = (chat_prompt | chat_model | CommaSeparatedListOutputParser())
conversation_chain = ConversationChain(prompt=chat_prompt, llm=chat_model, memory=conversation_buf)

def main():
    user_input = 'C'
    while (user_input == 'C' or user_input == 'c'):        
        user_input = input('\n Enter the Prompt >> ')
        #print(conversation_chain.invoke({"user_input": user_input, "chat_history": conversation_buf.chat_memory.messages}))
        print(conversation_chain.predict(user_input))
        user_input = input('\nType X to Exit OR C to continue \n >> ')
        
    
if __name__ == '__main__':
    main()

"""
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
           
    st.session_state['chat-history'].append({
        "role": "ai",
        "message": chain.invoke({"user_input": user_input})
    })
    
if 'chat-history' in st.session_state:
    for i in range(0, len(st.session_state['chat-history'])):
        msg = st.session_state['chat-history'][i]
        st.chat_message(msg['role']).write(msg['message'])
"""