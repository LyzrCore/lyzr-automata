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
    page_title="Lyzr Test Cases Generator",
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
st.sidebar.image(image, width=150)

# App title and introduction
st.sidebar.title("Lyzr Test Cases Generator")
st.sidebar.markdown("### Welcome to the Lyzr Test Cases Generator!")
st.sidebar.markdown("Upload Your Code and get Your Test Cases.")


open_ai_text_completion_model = OpenAIModel(
    api_key=api,
    parameters={
        "model": "gpt-4-turbo-preview",
        "temperature": 0.2,
        "max_tokens": 1500,
    },
)

code = st.sidebar.text_area("Enter Your Code: ",height=200)
description = st.sidebar.text_input("Enter Code Description: ")


def test_cases(code,description):
    test_agent = Agent(
        role="Test Case expert",
        prompt_persona=f"You are a helpful assistant capable of generating software test cases from code."
    )

    task1 = Task(
        name="Generate Test Cases",
        model=open_ai_text_completion_model,
        agent=test_agent,
        instructions=f"You have to create test cases for given {code} and {description}. "
                     f"Generate positive and negative test cases both."
                     f"[!important] Only give test cases nothing else.",
    )

    output = LinearSyncPipeline(
        name="Test Case Details",
        completion_message="Test Cases Generated",
        tasks=[
            task1
        ],
    ).run()

    return output[0]['task_output']


if st.sidebar.button("Generate"):
    tc = test_cases(code, description)
    st.markdown(tc)







