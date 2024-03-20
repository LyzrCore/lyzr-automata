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
    page_title="Lyzr MCQ Generator",
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
st.title("Lyzr MCQ Generator")
st.markdown("### Welcome to the Lyzr MCQ Generator!")
st.markdown("Upload Your Topic and get Perfect Answers.")

open_ai_text_completion_model = OpenAIModel(
    api_key=api,
    parameters={
        "model": "gpt-4-turbo-preview",
        "temperature": 0.2,
        "max_tokens": 1500,
    },
)

topic = st.chat_input("Enter Topic")
mcq_agent = Agent(
    role="MCQ expert",
    prompt_persona=f"Your task is to DEVELOP a 10 MULTIPLE-CHOICE QUESTION (MCQ) about {topic} and also give its answers"
)

mcq_task  =  Task(
    name="get MCQ study",
    model=open_ai_text_completion_model,
    agent=mcq_agent,
    instructions="Give 10 MCQ Questions with answers",
)

if topic:
    output = LinearSyncPipeline(
        name="MCQ details",
        completion_message="pipeline completed",
        tasks=[
             mcq_task
        ],
    ).run()

    print(output[0]['task_output'])
    st.markdown(output[0]['task_output'])
