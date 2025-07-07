import requests
import os
import openai

openai.api_key = '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'

response = openai.Completion.create(
    model = "text-davinci-002",
    prompt = "In the current world, Artificial Intelligence is gaining more and more traction. However, while it has its advantages, the world should also be careful of its pitfalls. In this article, we will elaborate.",
    temperature = 0.7,
    max_tokens = 700,
    top_p=1,
    frequency_penalty = 0,
    presence_penalty = 0
)

text_string = "sample text"

model_id = "text-embedding-ada-002"

embedding = openai.Embedding.create(input=text_string, model=model_id)['data'][0]['embedding']
response

