import joblib
import json
import numpy as np
from langgraph.prebuilt import create_react_agent
from langchain.tools import tool


class PlannerAgent:
    """
    Encapsulates the PlannerAgent, which creates personalised investment plans
    for new Indian investors using a pre-trained ML model and a fixed playbook
    of product suggestions (Nifty 50 Index Fund, PPF, Sovereign Gold Bonds).
    """

    PROMPT = """
        You are PlannerAgent, an AI assistant that creates personalized investment plans for new Indian investors.

        **Your Mission:**
        1.  Your primary tool is `get_investment_plan`, which takes a user's age and risk tolerance to generate a precise asset allocation using a trained model.
        2.  Once you have the allocation percentages (equity, debt, gold), your job is to translate these numbers into a clear, actionable plan.
        3.  Present the final, comprehensive plan to the user in a simple, encouraging format.

        **Investment Playbook (How to suggest products):**
        - For the `equity` portion: Always suggest a "Nifty 50 Index Fund".
        - For the `debt` portion: Always suggest the "Public Provident Fund (PPF)" and mention its safety and tax benefits.
        - For the `gold` portion: Always suggest "Sovereign Gold Bonds (SGBs)" and mention they are a tax-efficient digital option.

        **Behavior Rules:**
        - **Strictly follow the playbook.** Do not suggest individual stocks or any other products.
        - Your final response to the user should be the complete, formatted plan. Do not just output the raw numbers.
        - You are a planner, not a conversationalist. Be direct and focused on creating the plan.
        """

    def __init__(self, llm, model_path: str = "./Agents/investment_portfolio_model.joblib"):
        """
        Initialises the PlannerAgent by loading the ML model.

        Args:
            llm: The language model instance to use for the agent.
            model_path: Path to the serialised scikit-learn model (.joblib).
        """
        self.llm = llm
        self.model = joblib.load(model_path)

    def create(self):
        """
        Builds and returns the compiled LangGraph ReAct agent.
        The investment plan tool is defined as a closure here so it can access
        the loaded model without using module-level globals.
        """
        model = self.model

        @tool
        def get_investment_plan(age: int, risk_tolerance: int) -> str:
            """
            Predicts the optimal investment portfolio allocation (equity %, gold %, debt %)
            for a user based on their age and risk tolerance using a pre-trained ML model.
            Returns the allocation as a JSON string.

            Args:
                age: The user's age in years.
                risk_tolerance: Risk comfort level on a scale of 1 (very cautious) to 5 (very aggressive).
            """
            print("--- PlannerAgent: PREDICTING ALLOCATION ---")
            try:
                params = np.array([[age, risk_tolerance]])
                response = model.predict(params)
                result = {
                    "equity_pct": float(response[0][0]),
                    "gold_pct": float(response[0][1]),
                    "debt_pct": float(response[0][2]),
                }
                return json.dumps(result)
            except Exception as e:
                return json.dumps({"error": f"Prediction failed: {str(e)}"})

        return create_react_agent(
            model=self.llm,
            tools=[get_investment_plan],
            prompt=self.PROMPT,
            name="planner_agent",
        )