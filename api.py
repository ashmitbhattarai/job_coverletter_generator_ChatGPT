# Modules for Prompt Design
from kor import create_extraction_chain
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain import Prompt, OpenAI
from langchain.chat_models import ChatOpenAI
from langchain.vectorstores import Pinecone
from langchain.callbacks import get_openai_callback
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate

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
from utils import get_structured_data
from utils import generate_cover_letter
import pinecone

# env variables
from api_keys import open_api_key, hugging_face_api_key
from api_keys import pinecone_api_key,pinecone_environment
os.environ["HUGGINGFACEHUB_API_TOKEN"] = hugging_face_api_key





def get_parsed_llm(job_title,job_text,applicant_text):
    all_data = {}
    ## LLM Models
    llm = ChatOpenAI(
        model='gpt-3.5-turbo',
        openai_api_key=open_api_key,
        # model_name='gpt-4',
        temperature=0.5,
    )# type: ignore
    
    llm_summary = OpenAI(
        openai_api_key=open_api_key,
        temperature = 0
    )# type: ignore

    ## Embeddings Model
    embed =  OpenAIEmbeddings(
        model="text-embeddings-ada-002",
        openai_api_key=open_api_key
    )# type: ignore

    ## Pinecone initialization
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
    ## generate summary
    prompt_template = "Write a concise summary of the following Job Vacancy Posting:\n\n{job_text}\n\n CONCISE SUMMARY:"
    summary_prompt = PromptTemplate(template = prompt_template, input_variables=["job_text"] )
    chain = LLMChain(
        llm=llm_summary,
        prompt=summary_prompt
    )
    summary = chain.run(job_text=job_title+"\n\n"+job_text)

    embedding = embed.embed_query(job_text)
    # FLATTEN THE POST DATA
    meta_data = {}
    ids =  [str(uuid4())]

    ## meta data cannot be NULL

    meta_data, cover_letter_prompt = generate_cover_letter(job_post_data,summary,applicant_data)
    meta_data["text"] = job_text
    meta_data["job_post"] = job_title
    # meta_data["job_json"] = job_post_data
    meta_data["summary"] = summary
    upload_chunk = zip(ids,[embedding],[meta_data])
    try:
        pc_index.upsert(vectors= upload_chunk)
    except Exception as e:
        print ("Error!!",e)
    

    # return "["+str(json.dumps(applicant_data,indent=3)) +\
    #       ",\n"+ str(json.dumps(job_post_data,indent=3)) + "]" + "\n\n"+\
    #       str(summary)
    all_data["job_meta"] = job_post_data
    all_data["job_summary"] = summary
    all_data["applicant_meta"] = applicant_data
    all_data["job_text"] = job_text
    all_data["job_title"] = job_title
    all_data["applicant_text"] = applicant_text
    all_data["job_embeddings"] = embedding

    json.dump(
        fp=open(ids[0]+".json","w+"),
        obj=all_data,
        indent=3
    )
    cover_letter = llm.predict(cover_letter_prompt)
    return cover_letter
    ## push everything into pinecone
###### Next Step: Write a Cover letter


# chat = "ChatOpenAI(temperature=0.7)" ###llm definition


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


    


