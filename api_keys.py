import yaml

try:
    keys = yaml.safe_load(open('api_tokens.yaml','r+'))
    open_api_key = keys["openai"]["open_api_key"]
    hugging_face_api_key = keys["huggingface"]["hugging_face_api_key"]
    pinecone_api_key = keys["pinecone"]["pinecone_api_key"]
    pinecone_environment = keys["pinecone"]["pinecone_environment"]
except:
    print ("Configure your Keys in api_tokens.yaml")
