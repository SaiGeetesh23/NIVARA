import joblib
from langgraph.prebuilt import create_react_agent
from langchain.tools import tool
import json
import numpy as np

_loaded_model = None
_planner_agent_llm = None
planner_agent_prompt = None

def init_planner_agent(planner_agent_llm):
    """Initializes the Planner Agent by loading the joblib model and setting the LLM."""
    global _loaded_model, _planner_agent_llm, planner_agent_prompt
    _loaded_model = joblib.load('./Agents/investment_portfolio_model.joblib')
    _planner_agent_llm = planner_agent_llm
    planner_agent_prompt = """
        You are PlannerAgent, an AI assistant that creates personalized investment plans for new Indian investors.

        **Your Mission:**
        1.  Your primary tool is `get_investment_plan`, which takes a user's age and risk tolerance to generate a precise asset allocation using a trained model.
        2.  Once you have the allocation percentages (equity, debt, gold), your job is to translate these numbers into a clear, actionable plan.
        3.  To make the plan credible, you MUST augment your suggestions with real-time data by calling the `MarketAgent`.
        4.  Present the final, comprehensive plan to the user in a simple, encouraging format.

        **Investment Playbook (How to suggest products):**
        - For the `equity` portion: Always suggest a "Nifty 50 Index Fund". Call the `MarketAgent`'s `get_historical_stock_prices` tool for the ticker "^NSEI" to fetch its recent performance.
        - For the `debt` portion: Always suggest the "Public Provident Fund (PPF)" and mention its safety and tax benefits.
        - For the `gold` portion: Always suggest "Sovereign Gold Bonds (SGBs)" and mention they are a tax-efficient digital option.

        **Behavior Rules:**
        - **Strictly follow the playbook.** Do not suggest individual stocks or any other products.
        - Your final response to the user should be the complete, formatted plan. Do not just output the raw numbers.
        - You are a planner, not a conversationalist. Be direct and focused on creating the plan.
        """

@tool
def get_investment_plan(age: int, risk_tolerance: int):
    """
    Predicts the optimal investment portfolio allocation (Equity, Gold, Debt) for a user based on their age and risk tolerance using a pre-trained machine learning model.
    Returns the allocation as a JSON string.
    """
    print("--- PLANNER AGENT: PREDICTING ALLOCATION ---")
    if _loaded_model is None:
        return json.dumps({"error": "Model not loaded."})
    try:
        params = np.array([[age, risk_tolerance]])
        response = _loaded_model.predict(params)

        equity_pct = response[0][0]
        gold_pct = response[0][1]
        debt_pct = response[0][2]

        result = {
            'equity_pct' : equity_pct,
            'gold_pct' : gold_pct,
            'debt_pct' : debt_pct
        }
        return json.dumps(result)
    except Exception as e:
        return json.dumps({"error": f"An error occurred during prediction: {str(e)}"})


def create_planner_agent():
    """Creates the LangGraph ReAct agent for financial planning."""
    planner_agent = create_react_agent(
        model = _planner_agent_llm,
        tools = [get_investment_plan],
        prompt = planner_agent_prompt,
        name = 'planner_agent'
    )
    return planner_agent