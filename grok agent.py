import asyncio
import nest_asyncio
from uagents import Agent, Context, Model
import os
from groq import Groq

sample_prompt = "List of 2 best phones with following minimum specs: ram - 4GB , rom - 64 GB , front camera - 8 MP,back camera - 64 MP,screen size - big , medium, small, operating system - Android, IOS,processor - Snapdragon 8 Gen 2, connectivity - 5G , Dual Support under price 15,000 INR. Output results in json with phone name being primary key and specs being nested key: value pair. Make sure to include price in INR"
# Allow running async functions in Colab
nest_asyncio.apply()

async def run_agent():
    # Set the Groq API key
    groq_api_key = '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'

    # Define the request and response models
    class QueryRequest(Model):
        query: str

    class QueryResponse(Model):
        response: str

    # Initialize the Groq client
    client = Groq(api_key=groq_api_key)

    # Initialize the agent
    agent = Agent(name="fetch_groq_agent")

    # Define the prompt
    #prompt = "List of 5 best phones with following minimum specs: ram - 6GB , rom - 128 GB , front camera - 16 MP,back camera - 64 MP,screen size - big , medium, small, operating system - Android, IOS,processor - Snapdragon 8 Gen 2, connectivity - 5G , Dual Support under price 25,000 INR. Output results in json with phone name being primary key and specs being nested key: value pair. Make sure to include price in INR"

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

        print("Response:", response_data)  # Print the output

        #await ctx.send(message=QueryResponse(response=response_data))

   # Simulate input data
    

    # Create a QueryRequest object with the sample prompt
    query_request = QueryRequest(query=sample_prompt)

    # Call the handler function directly with the sample prompt
    await handle_query(None, query_request)

# Call the async function directly
asyncio.run(run_agent())
