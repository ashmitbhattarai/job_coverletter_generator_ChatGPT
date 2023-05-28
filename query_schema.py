# Kor imports
from kor import create_extraction_chain
from kor.nodes import Object, Text, Number

#Langchain imports
from langchain.chat_models import ChatOpenAI
from langchain.llms import OpenAI

# Standard Helper Libraries
import pandas as pd
import os

# env variables
from api_keys import open_api_key


# define a LLM here
llm = ""


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
        )
    ],
    examples = [
        (
            "Are fluent with Python and experienced with Jupyter notebooks",
            [{"technologies":"Python"},{"technologies":"Jupyter"}]
        ),
        (
            "Have experience in at least one of the following: neuroscience, BCI experimentation and neural signal processing",
            [{"technologies":"neuroscience"},{"technologies":"BCI experimentation"},{"technologies":"neural signal processing"}]
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

input_text = ""

output = chain.predict_and_parse(text=(input_text))["data"]

# i need job responsibilites, job skills, and benifits, also summary on company, company goals ????
