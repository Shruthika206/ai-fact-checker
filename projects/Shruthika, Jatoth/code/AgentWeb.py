import streamlit as st
import asyncio
import os
from dotenv import load_dotenv

from agent_framework import Agent
from agent_framework.foundry import FoundryChatClient
from azure.identity import DefaultAzureCredential

# Load env
load_dotenv()

PROJECT_ENDPOINT = os.getenv("FOUNDRY_PROJECT_ENDPOINT")
MODEL_DEPLOYMENT = os.getenv("FOUNDRY_MODEL")

# Streamlit UI config
st.set_page_config(page_title="AI Fact Checker", page_icon="🤖")

st.title("🤖 AI Fact Checker Agent")
st.write("Ask anything. I will verify facts using AI reasoning.")

# Store chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display old messages
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])


# Async function for agent
async def get_response(user_input):
    credential = DefaultAzureCredential()

    client = FoundryChatClient(
        project_endpoint=PROJECT_ENDPOINT,
        credential=credential,
        model=MODEL_DEPLOYMENT
    )

    async with Agent(
        client=client,
        instructions="""
You are a FACT-CHECKING AI AGENT.

Rules:
- Verify claims logically
- Respond with TRUE / FALSE / PARTIAL
- Explain briefly
"""
    ) as agent:

        result = await agent.run(user_input)
        return result.text


# Handle input
user_input = st.chat_input("Ask your question...")

if user_input:
    # Show user message
    st.chat_message("user").write(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})

    # Get AI response
    with st.spinner("Thinking..."):
        response = asyncio.run(get_response(user_input))

    # Show AI response
    st.chat_message("assistant").write(response)
    st.session_state.messages.append({"role": "assistant", "content": response})