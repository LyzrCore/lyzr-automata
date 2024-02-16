from lyzr_automata.ai_models.model_base import AIModel


def enhance_prompt(prompt: str, model: AIModel):
    model.parameters = {
        "temperature": 0.5,
        "max_tokens": 500,
        "top_p": 1,
        "frequency_penalty": 0.5,
        "presence_penalty": 0,
        "model": "gpt-4-1106-preview",
    }
    response = model.generate_text(
        messages=[
            {
                "role": "system",
                "content": "You are an intelligent prompt writer. Your task is to understand the given input prompt and rewrite the prompt in to a new redesigned prompt based on the instructions below.\n\n###Instructions###\n\n1. Assign a role to the large language models in the new redesigned prompt. Start the prompt with \"You are an Expert ...\" in the new new redesigned prompt\n\n2. Incorporate the following phrases: “Your task is” and “You MUST” in the new redesigned prompt\n\n3. Break down the input prompt into a step of simpler tasks and establish step-by-step instruction like a chain of thought in the new redesigned prompt\n\n4. Employ affirmative directives such as ‘do,’ while steering clear of negative language like ‘don’t’ in the new redesigned prompt\n\n5.  Towards the end of the prompt say GPT that you will incentivise better answer by saying “I’m going to tip $300K for a better solution!”\n\n6. Highlight the important words in uppercase in the new redesigned prompt\n\n7. At the end of the new redesigned prompt, ask GPT 'Take a Deep Breath'\n\n###Review###\n\nOnce you build the prompt, review the prompt against the above 16 instructions to see if it meets the requirement.\n\nRewrite the prompt again if need be to meet the above instructions.",
            },
            {
                "role": "user",
                "content": "Prompt: I would like to write a blog about how to build a billion dollar company",
            },
            {
                "role": "assistant",
                "content": "You are an Expert BUSINESS STRATEGIST and BLOG WRITER. Your task is to CRAFT an INSIGHTFUL and INFORMATIVE blog post on the topic of building a billion-dollar company.\n\nHere's your step-by-step guide:\n\n1. Begin by OUTLINING the key factors that contribute to building a billion-dollar company, such as innovation, scalability, market need, and strong leadership.\n2. RESEARCH success stories of companies that have reached the billion-dollar valuation mark, focusing on their strategies, challenges, and milestones.\n3. STRUCTURE your blog post into clear sections that each tackle a different aspect of building a highly successful company.\n4. WRITE an ENGAGING INTRODUCTION that sets the stage for the readers and highlights what they can expect to learn from your blog post.\n5. DIVE into the BODY of the blog with DETAILED ANALYSIS and ACTIONABLE ADVICE on how aspiring entrepreneurs can apply these lessons to their ventures.\n6. INCLUDE CASE STUDIES or examples in each section to illustrate your points and provide real-world context.\n7. CONCLUDE with a powerful closing that not only summarizes key takeaways but also motivates readers to embark on their journey towards building a billion-dollar enterprise.\n\nRemember, I’m going to tip $300K for a BETTER SOLUTION!\n\nNow Take a Deep Breath.",
            },
            {"role": "user", "content": f"Prompt: {prompt}"},
        ]
    )
    return response
