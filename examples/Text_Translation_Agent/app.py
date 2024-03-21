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
    page_title="Lyzr Text Translation Agent",
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
st.title("Lyzr Text Translation Agent")
st.markdown("### Welcome to the Lyzr Text Translation Agent!")

sentence = st.text_input("Enter a sentence:")
language = st.text_input("Enter Language:")

open_ai_text_completion_model = OpenAIModel(
    api_key=api,
    parameters={
        "model": "gpt-4-turbo-preview",
        "temperature": 0.2,
        "max_tokens": 1500,
    },
)

def text_translator(topic,language):
    translator_prompt = "You are an Expert LINGUIST and TRANSLATOR. Your task is to PROVIDE GUIDANCE on how to EFFECTIVELY translate texts between languages."
    mcq_agent = Agent(
        role="Translation expert",
        prompt_persona=translator_prompt
    )

    mcq_task  =  Task(
        name="Text Translation",
        model=open_ai_text_completion_model,
        agent=mcq_agent,
        instructions=f"your task is to translate {topic} in {language} and only give translated text",
    )

    output = LinearSyncPipeline(
        name="Translation Details",
        completion_message="pipeline completed",
        tasks=[
             mcq_task
        ],
    ).run()

    return output[0]['task_output']

if st.button("Translate"):
    translation = text_translator(sentence,language)
    st.markdown(translation)
