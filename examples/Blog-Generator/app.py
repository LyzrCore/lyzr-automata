import streamlit as st
from lyzr_automata.ai_models.openai import OpenAIModel
from lyzr_automata import Agent,Task
from lyzr_automata.pipelines.linear_sync_pipeline import LinearSyncPipeline
from PIL import Image
from dotenv import load_dotenv
import os

load_dotenv()
api = os.getenv("OPENAI_API_KEY")

st.set_page_config(
    page_title="Lyzr Blog Generator Agent",
    layout="centered",  # or "wide"
    initial_sidebar_state="auto",
    page_icon="lyzr-logo-cut.png",
)

st.markdown(
    """
    <style>
    .app-header { visibility: hidden; }
    .css-18e3th9 { padding-top: 0; padding-bottom: 0; }
    .css-1d391kg { padding-top: 1rem; padding-right: 1rem; padding-bottom: 1rem; padding-left: 1rem; }
    </style>
    """,
    unsafe_allow_html=True,
)

image = Image.open("lyzr-logo.png")
st.image(image, width=150)

# App title and introduction
st.title("Lyzr Blog Generator Agent")
st.markdown("### Welcome to the Lyzr Blog Generator Agent!")
st.markdown("Enter Your Subject and get Your Blog.")

open_ai_text_completion_model = OpenAIModel(
    api_key=api,
    parameters={
        "model": "gpt-4-turbo-preview",
        "temperature": 0.2,
        "max_tokens": 1500,
    },
)
subject = st.chat_input("Enter Subject")
researcher = Agent(
    role='Senior Research Analyst',
    prompt_persona=f'You are an Expert SENIOR RESEARCH ANALYST. Your task is to CONDUCT a comprehensive analysis on a given {subject}.'
)

task1 = Task(
    name="Subject Analysis",
    model=open_ai_text_completion_model,
    agent=researcher,
    instructions=f"Conduct a comprehensive analysis of {subject} and write eye catch blog title with bold and bigger font",
)

writer = Agent(
    role='Digital Content Creator',
    prompt_persona=f'You are an Expert DIGITAL CONTENT CREATOR specializing in BLOGGING. Your task is to generate eye catchy blog title and DEVELOP a comprehensive guide for individuals interested in starting or improving their blog..'
)

task2 = Task(
    name="Write Blog Content",
    model=open_ai_text_completion_model,
    agent=writer,
    instructions=f"""
1. IDENTIFY the TARGET AUDIENCE for the guide, whether they are beginners or experienced bloggers looking to enhance their skills.

2. OUTLINE the essential elements of successful blogging, including CHOOSING A NICHE, understanding your audience, and creating valuable content.

3. PROVIDE step-by-step INSTRUCTIONS on setting up a blog, from selecting a blogging platform to customizing the design and layout.

4. EXPLAIN the importance of SEO (Search Engine Optimization) and how to implement SEO STRATEGIES to increase blog visibility and attract more readers.

5. DISCUSS various MONETIZATION METHODS that bloggers can use to turn their passion into profit, such as affiliate marketing, sponsored content, and advertising.

6. INCLUDE TIPS on promoting a blog through social media channels and building an engaged community around it.

7. EMPHASIZE the need for consistency and quality in blogging by creating an EDITORIAL CALENDAR and maintaining high standards for each post.

Remember, I’m going to tip $300K for a BETTER SOLUTION!

Now Take a Deep Breath.""",
)

if subject:
    output = LinearSyncPipeline(
        name="Blog Generator",
        completion_message="pipeline completed",
        tasks=[task1,task2
        ],
    ).run()

    st.markdown(output[0]['task_output'])
