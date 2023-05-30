import yaml
import os
try:
    keys = yaml.safe_load(open('api_tokens.yaml','r+'))
    if "OPENAI_API_KEY" in os.environ:
        open_api_key = os.environ["OPENAI_API_KEY"]
    else:
        open_api_key = keys["openai"]["open_api_key"]
    hugging_face_api_key = keys["huggingface"]["hugging_face_api_key"]
    pinecone_api_key = keys["pinecone"]["pinecone_api_key"]
    pinecone_environment = keys["pinecone"]["pinecone_environment"]
except:
    print ("Configure your Keys in api_tokens.yaml")