# Storyboard Generator

**Author** - Rasswanth S  
**Email** - rasswanth@lyzr.ai

A storyboard generator and screenplay writer using Lyzr-Automata. Using a small description of a scene, the app writes a screenplay and generates a storyboard for it using approprate LLM Models.

## Flow Diagram
![Architecture Flow Diagram](<Flow Diagram.jpg>)

## Steps
1. Create a Text-to-Text Model (GPT-4) and Text-to-Image Model (DALLE 3) using OpenAIModel
2. Create an Agent with instructions and persona to write screenplay
3. Create a Task to make use of the Model and Agent to write the screenplay
4. Create a Task to generate storyboard using DALLE 3 model
5. Run tasks in LinearSyncPipeline

## Links

**Medium** - https://medium.com/@rasswanthshankar/boost-your-filmmaking-workflow-create-storyboards-and-write-scenes-using-lyzr-automata-aa9c18394b4c

**Video Walkthrough** - https://tella.video/storyboard-generator-8fpi