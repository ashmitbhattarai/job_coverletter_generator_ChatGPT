#Modules for Prompt Design
from kor import create_extraction_chain
from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI

# Standard Helper Libraries
import tiktoken
import pandas as pd
import os

# Internal Libraries
from query_schema import company_job_schema
from langchain.callbacks import get_openai_callback
import pinecone

# env variables
from api_keys import open_api_key,hugging_face_api_key
from api_keys import pinecone_api_key,pinecone_environment
os.environ["HUGGINGFACEHUB_API_TOKEN"] = hugging_face_api_key
os.environ["OPENAI_API_KEY"] = open_api_key



def get_structured_job_data(input_text:str)-> object:
    """_summary_

    Args:
        input_text (str): Job Description as User Input

    Returns:
        object: JSON object Job Data
    """
    ### Define a LLM here
    llm = ChatOpenAI(
        model_name='gpt-3.5-turbo',
        # model_name='gpt-4',
        temperature=0.9,
        max_tokens=2000
    )

    chain = create_extraction_chain(
        llm,
        company_job_schema,
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

input_text = """Lead brainstorming sessions to develop potential solutions for business needs or problems
Provide specifications according to which the solution is defined, managed, and delivered
Identify opportunities for process improvements
Define features, development phases, and solution requirements.
Supervised, Unsupervised and reinforcement learning Using Python
Set-up, maintenance, and ongoing development of continuous build/ integration infrastructure (CI/CD)
Experience with different NoSQL and SQL, graph databases


Engage with AI vendors to evaluate off-the-shelf solutions and identify potential applications within the organization.
Collaborate with cross-functional teams to assess the feasibility, effectiveness, and potential impact of AI solutions on business processes and outcomes.
Provide guidance and support in the integration and adoption of AI technologi1es within the organization.
Assist in the development of AI-related strategies, roadmaps, and initiatives
"""





# print (output)



# i need job responsibilites, job skills, and benifits, also summary on company, company goals ????



###### Next stage: Get Data From User File#####


###### Next Step: Write a Cover letter
'''
from langchain.schema import HumanMessage, SystemMessage, AIMessage

chat = "ChatOpenAI(temperature=0.7)" ###llm definition

chat(
    [
        SystemMessage(content="You are a Job Application writing bot that understands job requirements and skills requirements then takes Work Experience and skills information of the applicant and writes a job cover letter. You should not add new skills or experience that applicant does not have."
        )
    ]
)'''