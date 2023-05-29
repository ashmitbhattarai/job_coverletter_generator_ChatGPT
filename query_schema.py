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
    temperature=0.9
)

# Kerr Schemata

## Prompt Schemata

skills_schema = Object(
    id="skill",
    description= "Technical Skills Enlisted in a Job Description",
    attributes = [
        Text(
            id = "technologies",
            description="Technologies Mentioned in Job Description"
        ),
        Text(
            id="responsibilities",
            description="Roles and Responsibilites in the Job Description"
        ),
        Text(
            id="experience",
            description="Experience of work in certain industry domain"
        )
    ],
    examples = [
        (
            "Are fluent with Python and experienced with Jupyter notebooks",
            [{"technologies":"Python"},{"technologies":"Jupyter notebook"}]
        ),
        (
            "Have experience in at least one of the following: neuroscience, BCI experimentation and neural signal processing",
            [{"experience":"neuroscience"},{"experience":"BCI experimentation"},{"experience":"neural signal processing"}]
        ),
        (
            "You will come up with technical solutions and process improvements for business needs",
            [{"reponsibilities":"technical solutions"},{"responsibilites":"process improvement"}]
        ),
        (
            "You will set up and help with the maintenance of the ongoing infrastructure.",
            [{"reponsibilities":"maintenance of infrastructure"}]
        )
    ]
)

chain = create_extraction_chain(llm,skills_schema)

input_text = """Lead brainstorming sessions to develop potential solutions for business needs or problems
Provide specifications according to which the solution is defined, managed, and delivered
Identify opportunities for process improvements
Define features, development phases, and solution requirements.
Supervised, Unsupervised and reinforcement learning Using Python
Set-up, maintenance, and ongoing development of continuous build/ integration infrastructure (CI/CD)
Experience with different NoSQL and SQL, graph databases"""

output = chain.predict_and_parse(text=(input_text))["data"]
print (output)

# i need job responsibilites, job skills, and benifits, also summary on company, company goals ????
