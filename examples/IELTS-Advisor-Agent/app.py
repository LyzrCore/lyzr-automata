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
    page_title="Lyzr IELTS Coaching Agent",
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
st.title("Lyzr IELTS Coaching Agent ")
st.markdown("### Welcome to the Lyzr IELTS Coaching Agent!")
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
ielts_agent = Agent(
    role="Ielts expert",
    prompt_persona=f"As an examiner of IELTS system, you can suggest an answer about {topic} with more than 250 words and below 300 words regading to 7.5."
)

ielts_task  =  Task(
			name="get Ielts study",
			model=open_ai_text_completion_model,
			agent=ielts_agent,
			instructions="Give Answer for IELTS",
	)

output = LinearSyncPipeline(
    name="Ielts details",
		# completion message after pipeline completes
    completion_message="pipeline completed",
    tasks=[
				# tasks are instance of Task class
         ielts_task # Task C
    ],
).run()

print(output[0]['task_output'])
st.markdown(output[0]['task_output'])
