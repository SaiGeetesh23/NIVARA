from enum import Enum
from langgraph.prebuilt import create_react_agent
from langchain.tools import tool
import yfinance as yf
import json
import pandas as pd


# ---------------------------------------------------------------------------
# Enums for typed tool arguments
# ---------------------------------------------------------------------------

class FinancialType(str, Enum):
    income_stmt = "income_stmt"
    quarterly_income_stmt = "quarterly_income_stmt"
    balance_sheet = "balance_sheet"
    quarterly_balance_sheet = "quarterly_balance_sheet"
    cashflow = "cashflow"
    quarterly_cashflow = "quarterly_cashflow"


class HolderType(str, Enum):
    major_holders = "major_holders"
    institutional_holders = "institutional_holders"
    mutualfund_holders = "mutualfund_holders"
    insider_transactions = "insider_transactions"
    insider_purchases = "insider_purchases"
    insider_roster_holders = "insider_roster_holders"


class RecommendationType(str, Enum):
    recommendations = "recommendations"
    upgrades_downgrades = "upgrades_downgrades"


# ---------------------------------------------------------------------------
# Module-level Yahoo Finance tools
# These are pure functions with no agent state, so they live at module level.
# ---------------------------------------------------------------------------

@tool
def get_stock_info(ticker: str) -> str:
    """Get stock information for a given ticker symbol. Use National Stock Exchange Ticker."""
    company = yf.Ticker(ticker)
    try:
        if company.isin is None:
            return f"Company ticker {ticker} not found."
    except Exception as e:
        return f"Error getting stock information for {ticker}: {e}"
    return json.dumps(company.info)


@tool
def get_historical_stock_prices(ticker: str, period: str = "1mo", interval: str = "1d") -> str:
    """Get historical stock prices for a given ticker symbol.

    Args:
        ticker: The ticker symbol, e.g. 'AAPL' or 'RELIANCE.NS'.
        period: Valid periods: 1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max. Default '1mo'.
        interval: Valid intervals: 1m, 2m, 5m, 15m, 30m, 60m, 90m, 1h, 1d, 5d, 1wk, 1mo, 3mo. Default '1d'.
    """
    company = yf.Ticker(ticker)
    try:
        if company.isin is None:
            return f"Company ticker {ticker} not found."
    except Exception as e:
        return f"Error getting historical stock prices for {ticker}: {e}"
    hist_data = company.history(period=period, interval=interval)
    hist_data = hist_data.reset_index(names="Date")
    return hist_data.to_json(orient="records", date_format="iso")


@tool
def get_yahoo_finance_news(ticker: str) -> str:
    """Get latest news articles for a given ticker symbol.

    Args:
        ticker: The ticker symbol, e.g. 'AAPL' or 'INFY.NS'.
    """
    company = yf.Ticker(ticker)
    try:
        if company.isin is None:
            return f"Company ticker {ticker} not found."
    except Exception as e:
        return f"Error getting news for {ticker}: {e}"

    news_list = []
    for item in company.news:
        if item.get("content", {}).get("contentType", "") == "STORY":
            title = item.get("content", {}).get("title", "")
            summary = item.get("content", {}).get("summary", "")
            description = item.get("content", {}).get("description", "")
            url = item.get("content", {}).get("canonicalUrl", {}).get("url", "")
            news_list.append(
                f"Title: {title}\nSummary: {summary}\nDescription: {description}\nURL: {url}"
            )
    if not news_list:
        return f"No news found for ticker {ticker}."
    return "\n\n".join(news_list)


@tool
def get_stock_actions(ticker: str) -> str:
    """Get stock dividends and stock splits for a given ticker symbol."""
    try:
        company = yf.Ticker(ticker)
    except Exception as e:
        return f"Error getting stock actions for {ticker}: {e}"
    actions_df = company.actions.reset_index(names="Date")
    return actions_df.to_json(orient="records", date_format="iso")


@tool
def get_financial_statement(ticker: str, financial_type: str) -> str:
    """Get a financial statement for a given ticker symbol.

    Args:
        ticker: Ticker symbol.
        financial_type: One of income_stmt, quarterly_income_stmt, balance_sheet,
                        quarterly_balance_sheet, cashflow, quarterly_cashflow.
    """
    company = yf.Ticker(ticker)
    try:
        if company.isin is None:
            return f"Company ticker {ticker} not found."
    except Exception as e:
        return f"Error getting financial statement for {ticker}: {e}"

    statement_map = {
        FinancialType.income_stmt: company.income_stmt,
        FinancialType.quarterly_income_stmt: company.quarterly_income_stmt,
        FinancialType.balance_sheet: company.balance_sheet,
        FinancialType.quarterly_balance_sheet: company.quarterly_balance_sheet,
        FinancialType.cashflow: company.cashflow,
        FinancialType.quarterly_cashflow: company.quarterly_cashflow,
    }
    financial_statement = statement_map.get(financial_type)
    if financial_statement is None:
        valid = ", ".join([e.value for e in FinancialType])
        return f"Invalid financial_type '{financial_type}'. Valid options: {valid}."

    result = []
    for column in financial_statement.columns:
        date_str = column.strftime("%Y-%m-%d") if isinstance(column, pd.Timestamp) else str(column)
        date_obj = {"date": date_str}
        for index, value in financial_statement[column].items():
            date_obj[index] = None if pd.isna(value) else value
        result.append(date_obj)
    return json.dumps(result)


@tool
def get_holder_info(ticker: str, holder_type: str) -> str:
    """Get holder information for a given ticker symbol.

    Args:
        ticker: Ticker symbol.
        holder_type: One of major_holders, institutional_holders, mutualfund_holders,
                     insider_transactions, insider_purchases, insider_roster_holders.
    """
    company = yf.Ticker(ticker)
    try:
        if company.isin is None:
            return f"Company ticker {ticker} not found."
    except Exception as e:
        return f"Error getting holder info for {ticker}: {e}"

    holder_map = {
        HolderType.major_holders: lambda: company.major_holders.reset_index(names="metric").to_json(orient="records"),
        HolderType.institutional_holders: lambda: company.institutional_holders.to_json(orient="records"),
        HolderType.mutualfund_holders: lambda: company.mutualfund_holders.to_json(orient="records", date_format="iso"),
        HolderType.insider_transactions: lambda: company.insider_transactions.to_json(orient="records", date_format="iso"),
        HolderType.insider_purchases: lambda: company.insider_purchases.to_json(orient="records", date_format="iso"),
        HolderType.insider_roster_holders: lambda: company.insider_roster_holders.to_json(orient="records", date_format="iso"),
    }
    handler = holder_map.get(holder_type)
    if handler is None:
        valid = ", ".join([e.value for e in HolderType])
        return f"Invalid holder_type '{holder_type}'. Valid options: {valid}."
    return handler()


@tool
def get_option_expiration_dates(ticker: str) -> str:
    """Fetch the available options expiration dates for a given ticker symbol."""
    company = yf.Ticker(ticker)
    try:
        if company.isin is None:
            return f"Company ticker {ticker} not found."
    except Exception as e:
        return f"Error getting option expiration dates for {ticker}: {e}"
    return json.dumps(company.options)


@tool
def get_option_chain(ticker: str, expiration_date: str, option_type: str) -> str:
    """Fetch the option chain for a given ticker symbol, expiration date, and option type.

    Args:
        ticker: Ticker symbol.
        expiration_date: Expiration date in 'YYYY-MM-DD' format.
        option_type: 'calls' or 'puts'.
    """
    company = yf.Ticker(ticker)
    try:
        if company.isin is None:
            return f"Company ticker {ticker} not found."
    except Exception as e:
        return f"Error getting option chain for {ticker}: {e}"

    if expiration_date not in company.options:
        return (
            f"No options available for {expiration_date}. "
            "Use `get_option_expiration_dates` to list valid dates."
        )
    if option_type not in ("calls", "puts"):
        return "Invalid option_type. Use 'calls' or 'puts'."

    chain = company.option_chain(expiration_date)
    data = chain.calls if option_type == "calls" else chain.puts
    return data.to_json(orient="records", date_format="iso")


@tool
def get_recommendations(ticker: str, recommendation_type: str, months_back: int = 12) -> str:
    """Get analyst recommendations or upgrades/downgrades for a given ticker symbol.

    Args:
        ticker: Ticker symbol.
        recommendation_type: 'recommendations' or 'upgrades_downgrades'.
        months_back: How many months back to look for upgrades/downgrades (default 12).
    """
    company = yf.Ticker(ticker)
    try:
        if company.isin is None:
            return f"Company ticker {ticker} not found."
    except Exception as e:
        return f"Error getting recommendations for {ticker}: {e}"

    try:
        if recommendation_type == RecommendationType.recommendations:
            return company.recommendations.to_json(orient="records")
        elif recommendation_type == RecommendationType.upgrades_downgrades:
            df = company.upgrades_downgrades.reset_index()
            cutoff = pd.Timestamp.now() - pd.DateOffset(months=months_back)
            df = df[df["GradeDate"] >= cutoff].sort_values("GradeDate", ascending=False)
            return df.drop_duplicates(subset=["Firm"]).to_json(orient="records", date_format="iso")
        else:
            return f"Invalid recommendation_type '{recommendation_type}'. Use 'recommendations' or 'upgrades_downgrades'."
    except Exception as e:
        return f"Error getting recommendations for {ticker}: {e}"


# ---------------------------------------------------------------------------
# MarketAgent class
# ---------------------------------------------------------------------------

_ALL_TOOLS = [
    get_stock_info,
    get_historical_stock_prices,
    get_yahoo_finance_news,
    get_stock_actions,
    get_financial_statement,
    get_holder_info,
    get_option_expiration_dates,
    get_option_chain,
    get_recommendations,
]


class MarketAgent:
    """
    Encapsulates the MarketAgent, which uses Yahoo Finance tools to answer
    factual queries about stocks, financials, holders, news, and options.
    """

    PROMPT = """
        You are MarketAgent, an AI assistant specialized in providing financial information about stocks
        listed on global exchanges, with a primary focus on the Indian market.

        Your role:
        1. Use the provided tools to fetch real-time and historical stock data from Yahoo Finance.
        2. Answer user queries strictly based on the available tools. Do not make assumptions or use external knowledge.
        3. Tools available: get_stock_info, get_financial_statement, get_holder_info, get_recommendations,
           get_stock_actions, get_yahoo_finance_news, get_historical_stock_prices,
           get_option_expiration_dates, get_option_chain.

        Behavior rules:
        - Always respond factually and concisely.
        - Use only the data retrieved from the tools.
        - If the requested information is unavailable, respond with:
          "The requested data is not available for this ticker or period."
        - Do not provide investment advice, predictions, or opinions.
        - If the user asks unrelated questions, respond:
          "I can only answer questions related to stocks, financial statements, holders, recommendations, options, and news."

        You are a finance-focused retrieval agent acting as a factual interface to Yahoo Finance data.
        """

    def __init__(self, llm):
        """
        Initialises the MarketAgent.

        Args:
            llm: The language model instance to use for the agent.
        """
        self.llm = llm

    def create(self):
        """Builds and returns the compiled LangGraph ReAct agent."""
        return create_react_agent(
            model=self.llm,
            tools=_ALL_TOOLS,
            prompt=self.PROMPT,
            name="market_agent",
        )