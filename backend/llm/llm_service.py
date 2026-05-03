from openai import OpenAI
import os
from dotenv import load_dotenv

# Specify the path to the .env file
load_dotenv(dotenv_path="config/.env")


class LLMService:

    def __init__(self):

        self.client = OpenAI(
            base_url="https://integrate.api.nvidia.com/v1",
            api_key=os.getenv("NVIDIA_API_KEY")
        )

        self.model = "meta/llama-3.3-70b-instruct"

    def generate_response(self, context):

        prompt = f"""
You are an AI assistant helping users start businesses in India.

User Query:
{context['user_query']}

Business:
{context['business']}

Required Licenses:
{context['licenses']}

Available Schemes:
{context['schemes']}

Additional Knowledge:
{context['knowledge']}

Create a workflow plan.

Return ONLY valid JSON in this format:

{{
 "goal": "...",
 "workflow":[
   {{"step":1,"action":"...","authority":"..."}},
   {{"step":2,"action":"...","authority":"..."}}
 ]
}}
"""

        completion = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2,
            top_p=0.7,
            max_tokens=512,
        )

        return completion.choices[0].message.content