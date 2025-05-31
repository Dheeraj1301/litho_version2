# agents/assistant.py

from langchain.agents import initialize_agent, Tool
from langchain.chat_models import ChatOpenAI
from langchain.agents.agent_types import AgentType
from agents.tools.mask_optimizer import optimize_mask
from agents.tools.log_parser import suggest_fix_from_logs
from agents.tools.yield_predictor import analyze_yield_trends
import os
from dotenv import load_dotenv

load_dotenv()

llm = ChatOpenAI(
    model="gpt-4",
    temperature=0.2,
    api_key=os.getenv("OPENAI_API_KEY")
)

tools = [
    Tool(name="OptimizeMask", func=optimize_mask, description="Suggest optimal mask parameters"),
    Tool(name="DebugLogs", func=suggest_fix_from_logs, description="Fix issues using litho debug logs"),
    Tool(name="YieldPredictor", func=analyze_yield_trends, description="Analyze trends from yield prediction")
]

assistant_agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True
)


def ask_assistant(query: str):
    return assistant_agent.run(query)
