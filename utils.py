# Modules for Prompt Design
from kor import create_extraction_chain
from langchain.callbacks import get_openai_callback
from langchain.schema import HumanMessage, SystemMessage, AIMessage
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.chat_models import ChatOpenAI


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
    #     SystemMessage(content="
    #                   "
    #     )
    # ]
    #)
    responsibilities = ""
    experiences = ""
    personal_skills = ""
    # summary = "This is a summary"
    # applicant_dict,job_dict = json.load(open("system_output.json","r+"))
    job_role_name = job_dict["job_data"].get("job_title","Data Scientist")
    for_work= job_dict["job_data"].get("work_done","Data Science")
    
    skill_data = job_dict["job_data"]["skills"]
    if "responsibilites" in skill_data and len(skill_data["responsibilites"]) > 0:
        responsibilities = "\n".join(skill_data["responsibilites"])
    if "experiences" in skill_data and len(skill_data["experiences"]) > 0:
        experiences = "\n".join(skill_data["experiences"])
    if "personal_skills" in skill_data and len(skill_data["personal_skills"]) > 0:
        personal_skills = "\n".join(skill_data["personal_skills"])
    job_input_text = summary +"\n"+"Requirements:\n" + experiences + "\n" + responsibilities + "\n" + personal_skills

    applicant_name = applicant_dict["applicant_data"]["applicant_name"]
    applicant_experience = applicant_dict["applicant_data"]["years_of_experience"]

    worked_at = ":\n Worked at:\n"
    for work_dict in applicant_dict["applicant_data"]["companies_worked_at"]:
        worked_at += work_dict["company"]
        worked_at += "\nPerformed Following Duties:"
        tasks = "\n-".join(work_dict["tasks"])
        worked_at += tasks
        worked_at += "\nWorked at:\n"

    
    applicant_tools = applicant_dict["applicant_data"]["technologies"]
    applicant_tools = ", ".join(applicant_tools)

    from templates import cover_letter_prompt
    cover_letter_template = PromptTemplate(
        template = cover_letter_prompt, 
        input_variables=[
            "job_role_name",
            "job_input_text",
            "worked_at",
            "applicant_tools",
            "applicant_name",
            "years_of_experience"
        ]
    )
    final_prompt = cover_letter_template.format(
            job_role_name = job_role_name,
            job_input_text = job_input_text,
            worked_at = worked_at,
            applicant_tools = applicant_tools,
            applicant_name = applicant_name,
            years_of_experience = applicant_experience
    )
    # llm = ChatOpenAI(
    #     model_name='gpt-4',
    #     temperature=0.7
    # )# type: ignore
    # chain_cover = LLMChain(
    #     llm=llm,
    #     prompt=cover_letter_template
    # )
    print (final_prompt)
    meta_data={}
    return meta_data,final_prompt


# generate_cover_letter({},"",{})