import streamlit as st
from llm import query_llm

st.title("Streamlit Demo")
# Additional information that LLM does not know
context = """
    Auryn is a gray, medium hair cat born in March, 2012. She is a maine coon mix who sports a medium sized mane and cute tufts on her ears and toes. She is clicker trained, and she can perform tricks such as sit, sit pretty, high five, high ten, and turn. She loves to eat, except when she is nervous. Her favorite food is chicken and pork. 
"""
# st.write(context)


if 'chat-history' not in st.session_state:
    st.session_state['chat-history'] = [
        {
            "role": "ai",
            "message": "welcome!"
        }
    ]


user_input = st.chat_input("Message:")

if user_input:
    prompt = f"<|system|>You're an assistant answering user's question. Answer the users question Only using the context given. Context: {context}</s><|user|>{user_input}<|assistant|>answer:"

    # prompt # rendering elements with "magic"

    st.session_state['chat-history'].append({
        "role": "user",
        "message": user_input
    })

    llm_response = query_llm(prompt)

    st.session_state['chat-history'].append({
        "role": "ai",
        "message": llm_response[0]["generated_text"]
    })

if 'chat-history' in st.session_state:
    for i in range(0, len(st.session_state['chat-history'])):
        msg = st.session_state['chat-history'][i]
        st.chat_message(msg['role']).write(msg['message'])