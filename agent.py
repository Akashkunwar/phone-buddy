import asyncio
from uagents import Agent, Context, Model
from groq import Groq
import os
import streamlit as st

class QueryRequest(Model):
    query: str

class QueryResponse(Model):
    response: str

def get_groq_api_key():
    return os.getenv('groq_api_key')

async def run_agent(prompt, groq_api_key):
    client = Groq(api_key=groq_api_key)
    agent = Agent(name="fetch_groq_agent")

    @agent.on_message(model=QueryRequest)
    async def handle_query(ctx: Context, query_request: QueryRequest):
        completion = client.chat.completions.create(
            model="gemma-7b-it",
            messages=[
                {
                    "role": "user",
                    "content": query_request.query
                }
            ],
            temperature=1,
            max_tokens=1024,
            top_p=1,
            stream=True,
            stop=None,
        )
        response_data = ""
        for chunk in completion:
            response_data += chunk.choices[0].delta.content or ""
        st.session_state['groq_response'] = response_data

    query_request = QueryRequest(query=prompt)
    await handle_query(None, query_request)