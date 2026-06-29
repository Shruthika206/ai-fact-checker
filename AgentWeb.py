import os
import streamlit as st
from dotenv import load_dotenv
from azure.identity import DefaultAzureCredential
from agent_framework import Agent
from agent_framework.foundry import FoundryChatClient

load_dotenv()

PROJECT_ENDPOINT = os.getenv("FOUNDRY_PROJECT_ENDPOINT")
MODEL_DEPLOYMENT = os.getenv("FOUNDRY_MODEL")

st.set_page_config(page_title="AI Fact Checker", page_icon="🤖")

st.title("🤖 AI Fact Checker Agent")
st.write("Ask anything. I will verify facts using AI reasoning.")

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])


async def get_response(user_input):
    credential = DefaultAzureCredential()

    client = FoundryChatClient(
        endpoint=PROJECT_ENDPOINT,
        credential=credential,
        deployment_name=MODEL_DEPLOYMENT,
    )

    instructions = """
You are a FACT-CHECKING AI AGENT.

Rules:
- Verify claims logically.
- Respond with TRUE, FALSE, or PARTIAL.
- Explain briefly.
- If you are unsure, say what information is missing.
"""

    async with Agent(
        chat_client=client,
        instructions=instructions,
    ) as agent:
        result = await agent.run(user_input)
        return str(result)


user_input = st.chat_input("Ask your question...")

if user_input:
    st.chat_message("user").write(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})

    with st.spinner("Checking..."):
        import asyncio
        response = asyncio.run(get_response(user_input))

    st.chat_message("assistant").write(response)
    st.session_state.messages.append({"role": "assistant", "content": response})
