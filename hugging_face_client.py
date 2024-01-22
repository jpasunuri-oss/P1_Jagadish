import requests
from dotenv import load_dotenv
import os

# Load dot_env 
load_dotenv()
   
def query_llm(prompt):

    #TODO
    api_url = os.environ['HUGGINGFACE_API_URL']
    api_key = os.environ['HUGGINGFACE_API_KEY']
    
    req_header = {
        "Authorization": f"Bearer {api_key}"
    }
    #print("Request Header", req_header)
    # TODO: For additional configuration, go to https://huggingface.co/docs/api-inference/detailed_parameters#text-generation-task

    #print("Request Body", prompt)
    #TODO
    response = requests.post(api_url, headers=req_header, json=prompt)    
    #print("Response Body", response.json())
    return response.json()