# Kor imports
from kor.nodes import Object, Text, Selection, Option,Number

# KOR Objects
## Skills Schemata

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
            "We are committed to attracting and retaining people who have the right mix of skills, knowledge, leadership, and self-motivation",
            [{"personal_skills":"skillfull"},{"personal_skills":"knowledgeable"},{"personal_skills":"leadership"},{"personal_skills":"motivated"}]
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
            examples=[("We are seeking a talented Data Scientist to join our passionate team.","Data Scientist")],
            many=False
        ),
        Text(
            id="company_name",
            description="Name of the company",
            examples=[("About the Company: Roy Hill represents the next generation of integrated iron ore mine, rail and port operations in the Pilbara region of Western Australia.",'Roy Hill')],
            many=False
        ),
        Text(
            id="work_done",
            description="What does the company uses AI services for?"
        ),
        Selection(
            id="job_type",
            description="Is the Job Full Time, Part-Time, Contract or Freelance",
            options = [
                Option(id="full_time", description="Full-time basis"),
                Option(id="part_time", description="Part-time basis"),
                Option(id="contract", description="Casual basis"),
                Option(id="freelance", description="None of Above"),
            ]
        ),
        skills_schema    
    ]
)

date_range = Object(
    id="date_range",
    description="""
        The range of date that person has worked in the company for
    """,
    attributes=[
        Number(
            id="start_date",
            description="The start date of the person in company"
        ),
        Number(
            id="end_date",
            description="The last date of work for person in company"
        )
    ],
    examples=[
        (
            "Perceptyx Inc. (Pyx)12/2017 - 01/2023",
            [
                {"start_date": 2017, "end_date": 2023},
            ]
        )
    ],
    many=True
)

applicant_schema = Object(
    id = "applicant_data",
    description = "Includes applicant's name, Skills, Companies Worked for, experiences in those companies, Certifications, Personal Projects, Education",
    attributes=[
        Text(
            id="applicant_name",
            description = "Name of the Person or applicant this CV or Resume is of",
            many=False
        ),
        Text(
            id="company",
            description="Name of the company applicant has worked for",
            examples = [
                ("Work Experience Senior Data Scientist Perceptyx Inc. (Pyx): Perceptyx combines Employee Surveys","Perceptyx Inc.")
            ],
            many=True
        ),
        date_range,
        Text(
            id="technologies",
            description = "technologies the applicant has worked on",
            many=True
        ),
        Text(
            id="tasks",
            description = "achievements and task the applicant has worked on the company",
            many=True
        ),
        Number(
            id = "years_of_experience",
            description = "Number of years the applicant has worked for ",
            examples = [
                ("Around 6 years of experience as Python Developer and Data Scientist.",6)
            ],
            many=True
        )
    ],

    examples = [
        (
            "ChaptGPT for Job Application Cover Letter Generation using LangChain, KOR and PineCone v2",
            [
                {"technologies":"ChatGPT"},
                {"technologies":"LangChain"},
                {"technologies":"KOR"},
                {"technologies":"PineCone"}
            ]
        ),
        (
            "MLOps AWS Athena PySpark RESTful APIs OpenAI ChatGPT",
            [
                {"technologies":"MLOps"},
                {"technologies":"AWS Athena"},
                {"technologies":"PySpark"},
                {"technologies":"RESTful API"},
                {"technologies":"OpenAI"},
                {"technologies":"ChatGPT"}
            ]

        ),
        (
            """ShopGrok
                09/2018 - 05/2022,
                ShopGrok is a provider of consumer insights and data analytics to the retail and consumer sector
                Sydney,Australia

                Achievements/Tasks:

                Design, develop, modify, document, test, implement, and maintain ShopGrok Data Mining and Ingestion
                Pipeline for SaaS platform. Scaled up the infrastructure to collect 1+ Million data points daily.""",
            [
                {"tasks":"Design, develop, modify, document, test, implement, and maintain ShopGrok Data Mining and Ingestion Pipeline","company":"ShopGrok","date_range":{"start_date":2018,"end_date":2021}},
                {"tasks":"Scaled up the infrastructure to collect 1+ Million data points daily.","company":"ShopGrok","date_range":{"start_date":2018,"end_date":2021}}
            ]
        )
    ]
)