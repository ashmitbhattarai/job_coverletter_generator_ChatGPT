# Modules for Prompt Design
from kor import create_extraction_chain
from langchain.callbacks import get_openai_callback
from langchain.schema import HumanMessage, SystemMessage, AIMessage

# Standard Helper Libraries
import tiktoken
import json
import os


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

def generate_cover_letter(job_dict,summary,applicant_dict):
    # chat.temperature=0.7
    # chat(
    # [
    #     SystemMessage(content="You are a Job Application writing bot that understands job requirements and skills requirements.\
    #                   Next, you take Work Experience and skills information of the applicant and writes a job cover letter addressed to Lead Data Scientist.\
    #                   You should not add new skills or experience that applicant does not have.\
    #                   "
    #     )
    # ]
    #)
    responsibilities = []
    experiences = []
    personal_skills = []

    applicant_dict,job_dict = json.load(open("system_output.json","r+"))
    job_role_name = job_dict["job_data"].get("job_title","Data Scientist")
    for_work= job_dict["job_data"].get("work_done","Data Science")
    
    skill_data = job_dict["job_data"]["skills"]
    if "responsibilites" in skill_data and len(skill_data["responsibilites"]) > 0:
        responsibilities = "\n".join(responsibilities)
    if "experiences" in skill_data and len(skill_data["experiences"]) > 0:
        experiences = "\n".join(experiences)
    if "personal_skills" in skill_data and len(skill_data["personal_skills"]) > 0:
        personal_skills = "\n".join(personal_skills)
    
    applicant_name = applicant_dict["applicant_data"]["applicant_name"]
    applicant_experience = applicant_dict["applicant_data"]["years_of_experience"]

generate_cover_letter({},"",{})