# Kor imports
from kor import create_extraction_chain
from kor.nodes import Object, Text, Number

#Langchain imports
from langchain.chat_models import ChatOpenAI
from langchain.llms import OpenAI
from langchain.llms import HuggingFaceHub
# Standard Helper Libraries
import pandas as pd
import os

# env variables
from api_keys import open_api_key,hugging_face_api_key


os.environ["HUGGINGFACEHUB_API_TOKEN"] = hugging_face_api_key
os.environ["OPENAI_API_KEY"] = open_api_key


# define a LLM here
# llm = HuggingFaceHub(
#     repo_id='google/flan-t5-xl',
#     model_kwargs={
#         'temperature':0.5,
#         "max_length":128
#     }
# )

llm = OpenAI(
    model_name='gpt-3.5-turbo',
    # model_name='gpt-4',
    temperature=0.9,
    max_tokens=2000
)

# Kerr Schemata

## Prompt Schemata

skills_schema = Object(
    id="skills",
    description= "All roles and responsibilities, experiences and technical skills and enlisted in a Job Description",
    attributes = [
        Text(
            id = "technologies",
            description="Technologies Mentioned in Job Description eg: AWS Sagemaker, CI/CD, etc"
        ),
        Text(
            id="responsibilities",
            description="Roles and Responsibilites in the Job Description"
        ),
        Text(
            id="experience",
            description="Experience of work in a certain industry or a tool. Can include years of experience."
        ),
        Text(
            id="personal_skills",
            description = "Personal traits companies look for"
        )
    ],
    examples = [
        (
            "Are fluent with Python 5+ years and experienced with Jupyter notebooks",
            [{"technologies":"Python","experience":"5+ years"},{"technologies":"Jupyter notebook"}]
        ),
        (
            "Have experience in at least one of the following: Computer Vision, neuroscience, BCI experimentation and neural signal processing",
            [{"experience":"neuroscience"},{"experience":"BCI experimentation"},{"experience":"neural signal processing"}, {"experience":"Computer Vision"}]
        ),
        (
            "You will come up with technical solutions and process improvements for business needs",
            [{"reponsibilities":"technical solutions"},{"responsibilites":"process improvement"}]
        ),
        (
            "Reporting to the Lead Data Scientist, you will work alongside our talented team to develop and implement machine learning solutions that solve complex problems.",
            [{"reponsibilities":"report to Lead Data Scientist"},{"responsibilities":"implement machine learning solutions"}]
        ),
        (
            "Collaborate with cross-functional teams to assess the feasibility, effectiveness, and potential impact of AI solutions on business processes and outcomes",
            [{"reponsibilities":"Collaborate with cross-functional teams"}]
        ),
        (
            "We are committed to attracting and retaining people who have the right mix of skills, knowledge, leadership, and motivation",
            [{"personal_skills":"right mix of skills"},{"personal_skills":"knowledge"},{"personal_skills":"leadership"},{"personal_skills":"motivation"}]
        )
    ],
    many=True
)

company_job_schema = Object(
    id="job_data",
    description="Includes Job Title or Role, information about hiring company, job requirements, job responsibilities and tools and technologies used.",
    attributes = [
        Text(
            id="job_title",
            description="Job title or role in Job Description",
            examples=[("We are seeking a talented Data Scientist to join our passionate team.","Data Scientist")]
            many=False
        ),
        Text(
            id="company_name",
            description="Name of the company",
            examples=[("About the Company: Roy Hill represents the next generation of integrated iron ore mine, rail and port operations in the Pilbara region of Western Australia.",'Roy Hill')]
            many=False
        ),
        skills_schema
        
    ]
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
