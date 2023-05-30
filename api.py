# Modules for Prompt Design
from kor import create_extraction_chain
from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI

# Standard Helper Libraries
import tiktoken
import pandas as pd
import os

# Internal Libraries
from query_schema import company_job_schema,applicant_schema
from langchain.callbacks import get_openai_callback
import pinecone

# env variables
from api_keys import hugging_face_api_key
from api_keys import pinecone_api_key,pinecone_environment
os.environ["HUGGINGFACEHUB_API_TOKEN"] = hugging_face_api_key
open_api_key = os.environ["OPENAI_API_KEY"]



def get_structured_data(
        llm : object,
        input_text:str,
        schema:object
    ) -> object:
    """_summary_

    Args:
        input_text (str): Job Description as User Input

    Returns:
        object: JSON object Job Data
    """
    chain = create_extraction_chain(
        llm=llm,
        node=schema,
        encoder_or_encoder_class="json"
    )
    prompt_text = chain.prompt.format_prompt("[user_input]").to_string()

    # p50k_base for davinci2 and 3, cl100k_base for gpt4,3.5 turbo, embeddings
    encoding  = tiktoken.get_encoding('cl100k_base')
    print (prompt_text)
    print("")
    print (len(encoding.encode(prompt_text)),"tokens just in prompt\n\n")
    output={}
    with get_openai_callback() as cb:
        # output = chain.predict_and_parse(text=(input_text))["data"]
        # print (output)
        print (f"Total Tokens:{cb.total_tokens}")
        print (f"Prompt Tokens:{cb.prompt_tokens}")
        print (f"Completion Tokens:{cb.completion_tokens}")
        print (f"Number of Requests:{cb.successful_requests }")
        print (f"Total Cost:{cb.total_cost}")
    return output

def get_parsed_llm():
    ## get input texts
    job_text= ""
    applicant_text = ""

    ## LLM Model
    llm = ChatOpenAI(
        model_name='gpt-3.5-turbo',
        # model_name='gpt-4',
        temperature=0.9,
        max_tokens=2000
    )

    ## Embeddings Model
    embed =  ""

    ### Pinecone model
    pinecone.init(
        api_key=pinecone_api_key,
        environment=pinecone_environment
    )
    index_name = "job-search"

    if index_name not in pinecone.list_indexes():
        pinecone.create_index(
            index_name = index_name
        )
    pc_index = pinecone.Index(index_name)
    job_post_data = get_structured_data(
        llm = llm,
        input_text = job_text,
        schema = company_job_schema
    )

    applicant_data = get_structured_data(
        llm = llm,
        input_text = applicant_text,
        schema = applicant_schema
    )

    ## push everything into pinecone
    job_post_data["type"] = "job_post"
    applicant_data["type"] = "resume"

    # pinecone.upsert(upload_chunk)




# print (output)



# i need job responsibilites, job skills, and benifits, also summary on company, company goals ????



###### Next stage: Get Data From User File#####


###### Next Step: Write a Cover letter
'''
from langchain.schema import HumanMessage, SystemMessage, AIMessage

chat = "ChatOpenAI(temperature=0.7)" ###llm definition
chat(
    [
        SystemMessage(content="You are a Job Application writing bot that understands job requirements and skills requirements\
            then takes Work Experience and skills information of the applicant and writes a job cover letter.\
            You should not add new skills or experience that applicant does not have."
        )
    ]
)'''