
# **Jazon - World’s First Downloadable AI SDR**

##### Jazon is built on Lyzr Automata, a multi-agent automation framework that allows anyone to build reliable enterprise-grade meta-agents. Jazon performs all functions of an SDR. You can build any meta-agent similar to Jazon using the Lyzr Automata framework.
#

[![Video Title](https://raw.githubusercontent.com/LyzrCore/lyzr-automata/main/agent-templates/jazon/assets/intro_demo_thumbnail.png)](https://www.lyzr.ai/wp-content/uploads/2024/04/LYZR-VIDEO-7.mp4)

### **Why did we build Jazon?**

##### It all started with a tweet from Jason Lemkin of SaaStr. We took this as a challenge to build a meta-agent on Lyzr Automata. We ended up building a base version in just four days. 

#
![Jason's tweet](https://raw.githubusercontent.com/LyzrCore/lyzr-automata/main/agent-templates/jazon/assets/jason_tweet.png)

#

##### Below is the architecture we designed to solve the above problem statement from Jason Lemkin.

![architecture](https://raw.githubusercontent.com/LyzrCore/lyzr-automata/main/agent-templates/jazon/assets/arch.png)

##### And here is how Jazon works with a placeholder UI built by our team.

[![Video Title](https://raw.githubusercontent.com/LyzrCore/lyzr-automata/main/agent-templates/jazon/assets/demo_video_thumbnail.png)](https://www.lyzr.ai/wp-content/uploads/2024/04/WALKTHROUGH.mp4)

## Features
1. **Goal Oriented** - Jazon AI SDR is 100% focused on the goal, which is to book meetings for you. The workflow is designed in a manner where the AI agent does not rest until a meeting is booked or until the customer says no or unsubscribes. You can define the number of outreaches (5 or 7 or more) to the Email Composer agent.
2. **100% Data Privacy** - Jazon AI SDR, built on Lyzr Automata, is available as a downloadable docker file. You can now run your AI SDR locally on your cloud ensuring 100% data privacy and security. Jazon AI SDR is a great locally deployable and customizable alternate to https://11x.ai/.
3. **Customizable** - Jazon AI SDR is completely customizable. You can customize the prompts, data supplied through RAG, workflows, and response handling.
4. **Scalable** - The docker file can be deployed in a manner that allows for scale with 100% availability and load handling.
5. **Enterprise Ready** - While the open-source version is good to go in production, Lyzr offers an enterprise version of Jazon AI SDR. You get white-glove onboarding support with professional services help to customize the agent as per your need. You also get additional features like agent performance monitoring, agent toxicity controller, user query analytics and more. You also get 24*7 enterprise support for your production workloads.
6. **Expandable** - Take the Jazon AI SDR template and expand it to a larger use case. Add voice calling, social media messaging and more features to the meta-agent.
7. **Integrations** - Jazon AI SDR integrates with all LLMs (OpenAI GPT4, Claude3, Google Gemini, Llama3, Mistral), all leading vector databases, and runs on any cloud natively as Jazon AI runs as a container.

## Running Jazon

Jazon reads its configuration from environment variables, so copy the sample file and
fill it in before starting the server:

```bash
cp .env.example .env
```

### With Docker

```bash
docker build -t jazon .
docker run --rm -p 8005:8005 --env-file .env jazon
```

The container runs as the unprivileged `jazon` user, not as root.

### Without Docker

```bash
pip install -r requirements.txt
uvicorn app.server:app --host 0.0.0.0 --port 8005
```

The API is then available on http://localhost:8005.


### Book Demo

#### Interested in deploying Jazon AI SDR or a similar meta-agent for your organization? Speak to us.

[Book Demo](https://www.lyzr.ai/book-demo/)
