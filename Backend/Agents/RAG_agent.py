from langchain_community.vectorstores import Milvus
from langchain_milvus import Milvus
from langchain_core.prompts import PromptTemplate
from langchain.retrievers.multi_query import MultiQueryRetriever
from langchain.tools import tool
from langgraph.prebuilt import create_react_agent
from langchain_core.output_parsers import StrOutputParser

_RAG_llm = None
_embedding = None
_ZILLIZ_CLOUD_URI = None
_ZILLIZ_CLOUD_USERNAME = None
_ZILLIZ_CLOUD_PASSWORD = None
_ZILLIZ_CLOUD_API_KEY = None
_rag_agent_prompt = None
vector_store = None
_parser = None

def init_rag_agent(rag_llm, embedding, ZILLIZ_CLOUD_URI, ZILLIZ_CLOUD_USERNAME, ZILLIZ_CLOUD_PASSWORD, ZILLIZ_CLOUD_API_KEY):
    global _RAG_llm, _embedding, _ZILLIZ_CLOUD_URI, _ZILLIZ_CLOUD_USERNAME, _ZILLIZ_CLOUD_PASSWORD, _ZILLIZ_CLOUD_API_KEY, _rag_agent_prompt, vector_store, _parser
    _RAG_llm = rag_llm
    _embedding = embedding
    _ZILLIZ_CLOUD_URI = ZILLIZ_CLOUD_URI
    _ZILLIZ_CLOUD_USERNAME = ZILLIZ_CLOUD_USERNAME
    _ZILLIZ_CLOUD_PASSWORD = ZILLIZ_CLOUD_PASSWORD
    _ZILLIZ_CLOUD_API_KEY = ZILLIZ_CLOUD_API_KEY
    _rag_agent_prompt = """
        You are RAG_agent, an AI assistant specialized in answering questions about Finance. 
        You are powered by a Retrieval-Augmented Generation (RAG) system that uses a Milvus/Zilliz Cloud vector database.

        Your role:
        1. Retrieve semantically similar document excerpts from the Finance knowledge base using the `retriever_tool`.
        - This knowledge base contains financial guides, investment strategies, regulations, policies, FAQs, and domain-specific resources.
        - Each retrieval returns the top-k most relevant document chunks that best match the user’s query.
        2. Use ONLY the retrieved document excerpts to construct your answers.
        3. If the retrieved context does not provide enough information, explicitly respond with:
        "The provided document excerpts do not contain sufficient information to answer this question."
        4. If the user asks about something unrelated to Finance or outside the scope of the retrieved documents, respond with:
        "I can only answer questions based on the provided financial document excerpts."

        Behavior rules:
        - Do NOT use external knowledge, personal opinions, or assumptions.
        - Do NOT generate content beyond what is present in the retrieved context.
        - Keep answers concise, factual, and strictly grounded in the retrieved text.
        - If information is ambiguous, acknowledge the limitation rather than guessing.

        In short:
        You are not a general chatbot. You are a Finance-focused retrieval agent that acts as a factual interface to the financial knowledge base.
        """

    vector_store = Milvus(
        embedding_function=embedding,
        connection_args={
            "uri": ZILLIZ_CLOUD_URI,
            "user": ZILLIZ_CLOUD_USERNAME,
            "password": ZILLIZ_CLOUD_PASSWORD,
            # "token": ZILLIZ_CLOUD_API_KEY,  # API key, for serverless clusters which can be used as replacements for user and password
            "secure": True,
            "collection_name" : "LangChainCollection"
        },
    )
    _parser = StrOutputParser()

@tool
def retrieve_financial_documents(question: str) -> str:
    """
    Tool to retrieve semantically similar document excerpts from the Finance knowledge base.
    Returns the concatenated text of the retrieved documents.
    """
    print("--- RETRIEVING DOCUMENTS ---")
    if vector_store is None:
        return "Vector store is not initialized."

    # The multi-query retriever is still a great choice here
    retriever = MultiQueryRetriever.from_llm(
        retriever=vector_store.as_retriever(search_kwargs={'k': 4}),
        llm=_RAG_llm
    )
    
    retrieved_docs = retriever.invoke(question)

    if not retrieved_docs:
        return "No relevant documents were found to answer this question."
        
    # Combine the content of the retrieved documents into a single string
    context_text = "\n\n---\n\n".join([doc.page_content for doc in retrieved_docs])
    return context_text

def create_rag_agent():
    RAG_agent = create_react_agent(
        model = _RAG_llm,
        tools = [retrieve_financial_documents],
        prompt = _rag_agent_prompt,
        name = 'RAG_agent'
    )
    return RAG_agent


