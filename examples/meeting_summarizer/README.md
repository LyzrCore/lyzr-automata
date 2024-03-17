# Meeting Summarizer

**Author** - Rasswanth S  
**Email** - rasswanth@lyzr.ai

A workflow using Lyzr-Automata designed to summarize meetings and send email reports. The app's goal is to retrieve meeting transcript and attendees list from Microsoft Graph API and send summary of the meeting to all attendees. 

## Flow Diagram
![Architecture Flow Diagram](<Summarizer Diagram.jpg>)

## Steps
1. Fetch **Transcript** and **List of Attendees** of a meeting through Microsoft Graph API
2. Summarize the transcript by creating a Task for it
3. Email the summary to list of attendees by creating another Task for it with the help of Send Email Tool

## Links

**Medium** - https://medium.com/@rasswanthshankar/meeting-minutes-made-easy-summarize-key-points-and-send-emails-using-lyzr-automata-b0ff9d9eca41

**Video Walkthrough** - https://www.loom.com/share/f298c64641ff4d888a0ce3a0c6221ff5?sid=436f4caa-8622-4844-8eb8-7822c8f35df1