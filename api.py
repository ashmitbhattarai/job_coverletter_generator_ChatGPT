# Modules for Prompt Design
from kor import create_extraction_chain
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI
from langchain.vectorstores import Pinecone
from langchain.callbacks import get_openai_callback

# Interface and Parsing
import streamlit as st

# Standard Helper Libraries
from uuid import uuid4
import tiktoken
import pandas as pd
import json
import os

# Internal Libraries
from query_schema import company_job_schema,applicant_schema
import pinecone

# env variables
from api_keys import open_api_key, hugging_face_api_key
from api_keys import pinecone_api_key,pinecone_environment
os.environ["HUGGINGFACEHUB_API_TOKEN"] = hugging_face_api_key




def get_structured_data(
        llm : object,
        input_text: str,
        schema: object
    ) -> dict:
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
    ) # type: ignore
    prompt_text = chain.prompt.format_prompt("[user_input]").to_string()

    # p50k_base for davinci2 and 3, cl100k_base for gpt4,3.5 turbo, embeddings
    encoding  = tiktoken.get_encoding('cl100k_base')
    # print (prompt_text)
    # print("")
    print (len(encoding.encode(prompt_text)),"tokens just in prompt\n\n")
    output={}
    with get_openai_callback() as cb:
        output = chain.predict_and_parse(text=(input_text))["data"]
        # print (output)
        print (f"Total Tokens:{cb.total_tokens}")
        print (f"Prompt Tokens:{cb.prompt_tokens}")
        print (f"Completion Tokens:{cb.completion_tokens}")
        print (f"Number of Requests:{cb.successful_requests }")
        print (f"Total Cost:{cb.total_cost}")
    return output

def get_parsed_llm(job_title,job_text,applicant_text):

    ## LLM Model
    llm = ChatOpenAI(
        model_name='gpt-3.5-turbo',
        openai_api_key=open_api_key,
        # model_name='gpt-4',
        temperature=0.9,
        max_tokens=2000
    )# type: ignore
    
    ## Embeddings Model
    embed =  OpenAIEmbeddings(
        model="text-embeddings-ada-002",
        openai_api_key=open_api_key
    )

    ### Pinecone model
    pinecone.init(
        api_key=pinecone_api_key,
        environment=pinecone_environment
    )
    index_name = "job-search"

    if index_name not in pinecone.list_indexes():
        pinecone.create_index(
            name = index_name,
            dimension=1536
        ) #type: ignore
    
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

    embedding = embed.embed_query(job_text)
    # FLATTEN THE POST DATA
    meta_data = {}
    ids =  [str(uuid4())]
    meta_data["text"] = job_text
    meta_data["job_post"] = job_title
    meta_data["job_post"] = job_post_data
    upload_chunk = zip(ids,[embedding],[meta_data])
    try:
        pc_index.upsert(vectors=zip(upload_chunk))
    except:
        print ("Error!!")
    return str(json.dumps(applicant_data,indent=3)) +\
          "\n"+ str(json.dumps(job_post_data,indent=3))
    ## push everything into pinecone
###### Next Step: Write a Cover letter
# '''
# from langchain.schema import HumanMessage, SystemMessage, AIMessage

# chat = "ChatOpenAI(temperature=0.7)" ###llm definition
# chat(
#     [
#         SystemMessage(content="You are a Job Application writing bot that understands job requirements and skills requirements\
#             then takes Work Experience and skills information of the applicant and writes a job cover letter.\
#             You should not add new skills or experience that applicant does not have."
#         )
#     ]
# )'''

###### Next stage: Streamlit -- Get Data From User #####
st.title("Job Cover Letter Generator")

refresh_form = st.form(key="Refresh")
refresh = refresh_form.form_submit_button("Refresh")
if refresh:
    st.experimental_rerun()

with st.form(key='job_form') as input_form:
    job_post_title = st.text_input("Paste the Job Post Title here..")
    job_post_body = st.text_area("Paste the Job Description here..")
    cv_body = st.text_area("Copy Paste your CV as text here ..")
    submitted = st.form_submit_button("Submit")
    call_api = True
    if submitted:
        if job_post_title.strip() == "":
            st.write("Please Write Something on Job Title")
            call_api = False
        if job_post_body.strip() == "":
            st.write("Please Write Something on Job Description Body")
            call_api = False
        if cv_body.strip() == "":
            st.write("Please Write on CV Body")
            call_api = False
        if call_api:
            cover_letter = get_parsed_llm(
                job_title=job_post_title,
                job_text=job_post_body,
                applicant_text=cv_body
            )
            st.code("COVER LETTER:\n\n"+cover_letter)


    


