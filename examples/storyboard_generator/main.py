import streamlit as st
from lyzr_functions import storyboard_generator

input_scene = st.text_area("Enter Scene Description")

button=st.button('Submit')
if (button==True):
    # CALL FUNCTION TO GENERATE OUTPUT
    generated_output = storyboard_generator(input_scene)

    # DISPLAY OUTPUT
    text_output = generated_output[0]['task_output']
    st.write(text_output)
    image_file_name = generated_output[1]['task_output'].local_file_path
    st.image(image_file_name, caption='Storyboard')