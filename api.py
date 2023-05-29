#Modules for Prompt Design
from kor import create_extraction_chain
from langchain.llms import OpenAI

# Standard Helper Libraries
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


### Define a LLM here
llm = OpenAI(
    model_name='gpt-3.5-turbo',
    # model_name='gpt-4',
    temperature=0.9,
    max_tokens=2000
)


chain = create_extraction_chain(llm,company_job_schema)

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



# output = chain.predict_and_parse(text=(input_text))["data"]
# print (output)

# i need job responsibilites, job skills, and benifits, also summary on company, company goals ????

with get_openai_callback() as cb:
    print (f"Total Tokens:{cb.total_tokens}")
    print (f"Prompt Tokens:{cb.prompt_tokens}")
    print (f"Completion Tokens:{cb.completion_tokens}")
    print (f"Number of Requests:{cb.successful_requests }")
    print (f"Total Cost:{cb.total_cost}")

