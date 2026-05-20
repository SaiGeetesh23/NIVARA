# from langchain_milvus import Milvus
# from langchain_classic.retrievers.multi_query import MultiQueryRetriever
# from langchain.tools import tool
# from langgraph.prebuilt import create_react_agent
# from langchain_core.output_parsers import StrOutputParser


# class RAGAgent:
#     """
#     Encapsulates the RAG (Retrieval-Augmented Generation) agent for answering
#     finance-related questions from the Zilliz/Milvus vector knowledge base.
#     """

#     PROMPT = """
#         You are RAG_agent, an AI assistant specialized in answering questions about Finance. 
#         You are powered by a Retrieval-Augmented Generation (RAG) system that uses a Milvus/Zilliz Cloud vector database.

#         Your role:
#         1. Retrieve semantically similar document excerpts from the Finance knowledge base using the `retrieve_financial_documents` tool.
#            - This knowledge base contains financial guides, investment strategies, regulations, policies, FAQs, and domain-specific resources.
#            - Each retrieval returns the top-k most relevant document chunks that best match the user's query.
#         2. Use ONLY the retrieved document excerpts to construct your answers.
#         3. If the retrieved context does not provide enough information, explicitly respond with:
#            "The provided document excerpts do not contain sufficient information to answer this question."
#         4. If the user asks about something unrelated to Finance or outside the scope of the retrieved documents, respond with:
#            "I can only answer questions based on the provided financial document excerpts."

#         Behavior rules:
#         - Do NOT use external knowledge, personal opinions, or assumptions.
#         - Do NOT generate content beyond what is present in the retrieved context.
#         - Keep answers concise, factual, and strictly grounded in the retrieved text.
#         - If information is ambiguous, acknowledge the limitation rather than guessing.

#         In short:
#         You are not a general chatbot. You are a Finance-focused retrieval agent that acts as a factual interface to the financial knowledge base.
#         """

#     def __init__(self, llm, embedding, zilliz_uri, zilliz_username, zilliz_password, zilliz_api_key=None):
#         """
#         Initialises the RAGAgent.

#         Args:
#             llm: The language model instance to use for the agent and multi-query retriever.
#             embedding: The embedding model used to vectorise queries against Milvus.
#             zilliz_uri: Connection URI for the Zilliz/Milvus cluster.
#             zilliz_username: Milvus username.
#             zilliz_password: Milvus password.
#             zilliz_api_key: Optional API key (for serverless Zilliz clusters).
#         """
#         self.llm = llm
#         self.vector_store = Milvus(
#             embedding_function=embedding,
#             connection_args={
#                 "uri": zilliz_uri,
#                 "user": zilliz_username,
#                 "password": zilliz_password,
#                 # "token": zilliz_api_key,  # Uncomment for serverless clusters
#                 "secure": True,
#                 "collection_name": "LangChainCollection",
#             },
#         )

#     def create(self):
#         """
#         Builds and returns the compiled LangGraph ReAct agent.
#         The retriever tool is defined here as a closure so it captures
#         the initialised vector_store and llm without needing globals.
#         """
#         llm = self.llm
#         vector_store = self.vector_store

#         @tool
#         def retrieve_financial_documents(question: str) -> str:
#             """
#             Tool to retrieve semantically similar document excerpts from the
#             Finance knowledge base. Returns the concatenated text of the top
#             retrieved documents.
#             """
#             print("--- RAGAgent: RETRIEVING DOCUMENTS ---")
#             retriever = MultiQueryRetriever.from_llm(
#                 retriever=vector_store.as_retriever(search_kwargs={"k": 4}),
#                 llm=llm,
#             )
#             retrieved_docs = retriever.invoke(question)
#             if not retrieved_docs:
#                 return "No relevant documents were found to answer this question."
#             return "\n\n---\n\n".join([doc.page_content for doc in retrieved_docs])

#         agent = create_react_agent(
#             model=self.llm,
#             tools=[retrieve_financial_documents],
#             prompt=self.PROMPT,
#             name="RAG_agent",
#         )
#         return agent

# from pymilvus import connections, Collection, utility
# from langchain_classic.retrievers.multi_query import MultiQueryRetriever
# from langchain_core.documents import Document
# from langchain_core.retrievers import BaseRetriever
# from langchain.tools import tool
# from langgraph.prebuilt import create_react_agent
# from pydantic import ConfigDict


# class MilvusRetriever(BaseRetriever):
#     model_config = ConfigDict(arbitrary_types_allowed=True)

#     collection: Collection
#     embedding: object
#     text_field: str = "text"
#     output_fields: list[str] = ["text"]
#     k: int = 4

#     def _get_relevant_documents(self, query: str):
#         query_vector = self.embedding.embed_query(query)

#         results = self.collection.search(
#             data=[query_vector],
#             anns_field="vector",
#             param={"metric_type": "COSINE", "params": {"nprobe": 10}},
#             limit=self.k,
#             output_fields=self.output_fields,
#         )

#         docs = []
#         for hit in results[0]:
#             entity = hit.entity
#             text = entity.get(self.text_field, "")
#             docs.append(Document(page_content=text, metadata={"score": hit.score}))
#         return docs


# class RAGAgent:
#     PROMPT = """
#         You are RAG_agent, an AI assistant specialized in answering questions about Finance.
#         You are powered by a Retrieval-Augmented Generation (RAG) system that uses a Milvus/Zilliz Cloud vector database.

#         Your role:
#         1. Retrieve semantically similar document excerpts from the Finance knowledge base using the `retrieve_financial_documents` tool.
#         2. Use ONLY the retrieved document excerpts to construct your answers.
#         3. If the retrieved context does not provide enough information, explicitly respond with:
#            "The provided document excerpts do not contain sufficient information to answer this question."
#         4. If the user asks about something unrelated to Finance or outside the scope of the retrieved documents, respond with:
#            "I can only answer questions based on the provided financial document excerpts."

#         Behavior rules:
#         - Do NOT use external knowledge, personal opinions, or assumptions.
#         - Do NOT generate content beyond what is present in the retrieved context.
#         - Keep answers concise, factual, and strictly grounded in the retrieved text.
#         - If information is ambiguous, acknowledge the limitation rather than guessing.
#     """

#     def __init__(self, llm, embedding, zilliz_uri, zilliz_username, zilliz_password, zilliz_api_key=None):
#         self.llm = llm
#         self.embedding = embedding

#         alias = "default"

#         try:
#             connections.disconnect(alias=alias)
#         except Exception:
#             pass

#         connect_kwargs = {
#             "alias": alias,
#             "uri": zilliz_uri,
#             "secure": True,
#         }

#         if zilliz_api_key:
#             connect_kwargs["token"] = zilliz_api_key
#         else:
#             connect_kwargs["user"] = zilliz_username
#             connect_kwargs["password"] = zilliz_password

#         connections.connect(**connect_kwargs)

#         if not utility.has_collection("LangChainCollection", using=alias):
#             raise ValueError("Collection 'LangChainCollection' does not exist in Milvus.")

#         self.collection = Collection("LangChainCollection", using=alias)
#         self.collection.load()

#         self.retriever = MilvusRetriever(
#             collection=self.collection,
#             embedding=self.embedding,
#             text_field="text",
#             output_fields=["text"],
#             k=4,
#         )

#     def create(self):
#         llm = self.llm
#         retriever = self.retriever

#         @tool
#         def retrieve_financial_documents(question: str) -> str:
#             """
#             Retrieve the most relevant financial document excerpts from the Milvus knowledge base
#             for a given user question and return them as plain text.
#             """
#             print("--- RAGAgent: RETRIEVING DOCUMENTS ---")
#             multi_query_retriever = MultiQueryRetriever.from_llm(
#                 retriever=retriever,
#                 llm=llm,
#             )
#             retrieved_docs = multi_query_retriever.invoke(question)

#             if not retrieved_docs:
#                 return "No relevant documents were found to answer this question."

#             return "\n\n---\n\n".join(doc.page_content for doc in retrieved_docs)

#         agent = create_react_agent(
#             model=self.llm,
#             tools=[retrieve_financial_documents],
#             prompt=self.PROMPT,
#             name="RAG_agent",
#         )
#         return agent



from pymilvus import connections, Collection, utility
from langchain_classic.retrievers.multi_query import MultiQueryRetriever
from langchain_core.documents import Document
from langchain_core.retrievers import BaseRetriever
from langchain.tools import tool
from langgraph.prebuilt import create_react_agent
from pydantic import ConfigDict
import numpy as np  # For vector normalization if needed

class MilvusRetriever(BaseRetriever):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    collection: Collection
    embedding: object
    text_field: str = "text"
    vector_field: str = "vector"
    output_fields: list[str] = ["text"]
    k: int = 4
    metric_type: str = "L2"  # Default L2; set "COSINE" after index recreation

    def _get_relevant_documents(self, query: str):
        query_vector = self.embedding.embed_query(query)
        
        # Normalize only for COSINE
        if self.metric_type == "COSINE":
            norm = np.linalg.norm(query_vector)
            if norm != 0:
                query_vector = query_vector / norm
        
        search_params = {
            "metric_type": self.metric_type,
            "params": {"nprobe": 10}
        }

        results = self.collection.search(
            data=[query_vector],
            anns_field=self.vector_field,
            param=search_params,
            limit=self.k,
            output_fields=self.output_fields,
        )

        docs = []
        for hit in results[0]:
            entity = hit.entity
            text = entity.get(self.text_field, "")
            docs.append(Document(page_content=text, metadata={"score": float(hit.score)}))
        return docs

class RAGAgent:
    PROMPT = """
        You are RAG_agent, an AI assistant specialized in answering questions about Finance.
        You are powered by a Retrieval-Augmented Generation (RAG) system that uses a Milvus/Zilliz Cloud vector database.

        Your role:
        1. Retrieve semantically similar document excerpts from the Finance knowledge base using the `retrieve_financial_documents` tool.
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
    """

    def __init__(self, llm, embedding, zilliz_uri, zilliz_username, zilliz_password, zilliz_api_key=None, timeout=60):
        self.llm = llm
        self.embedding = embedding
        self.timeout = timeout

        alias = "default"

        try:
            connections.disconnect(alias=alias)
        except Exception:
            pass

        connect_kwargs = {
            "alias": alias,
            "uri": zilliz_uri,
            "secure": True,
            "timeout": self.timeout,  # Increased timeout for Zilliz
        }

        if zilliz_api_key:
            connect_kwargs["token"] = zilliz_api_key
        else:
            connect_kwargs["user"] = zilliz_username
            connect_kwargs["password"] = zilliz_password

        # Connect with retry logic
        max_retries = 3
        for attempt in range(max_retries):
            try:
                connections.connect(**connect_kwargs)
                print(f"Zilliz connected successfully (attempt {attempt + 1})")
                break
            except Exception as e:
                print(f"Connection attempt {attempt + 1} failed: {e}")
                if attempt == max_retries - 1:
                    raise
                import time
                time.sleep(2 ** attempt)  # Exponential backoff

        if not utility.has_collection("LangChainCollection", using=alias):
            raise ValueError("Collection 'LangChainCollection' does not exist in Milvus.")

        self.collection = Collection("LangChainCollection", using=alias)
        
        # Safe index diagnostic (pymilvus v2.4+ compatible)
        try:
            indexes = self.collection.indexes
            if indexes:
                idx = indexes[0]
                metric_type = idx.params.get('metric_type', 'Unknown') if idx.params else 'No params'
                index_type = getattr(idx, 'index_type', 'Unknown') or getattr(idx, 'index_name', 'No index_type')
                print(f"Collection index: metric_type={metric_type}, type={index_type}")
            else:
                print("WARNING: No index on 'vector' field. Call create_index_if_needed().")
        except Exception as e:
            print(f"Index check failed (ignore if no index): {e}")
        
        self.collection.load()
        print("Collection loaded.")

        # Start with L2; change to "COSINE" after recreating index
        self.retriever = MilvusRetriever(
            collection=self.collection,
            embedding=self.embedding,
            text_field="text",
            output_fields=["text"],
            k=4,
            metric_type="L2",
        )

    def create_index_if_needed(self, embedding_dim: int = 1536):
        """Recreate index as COSINE HNSW (best for RAG). Backup data first!"""
        if self.collection.has_index():
            print("Dropping existing index...")
            self.collection.drop_index()
        
        index_params = {
            "metric_type": "COSINE",
            "index_type": "HNSW",
            "params": {"M": 16, "efConstruction": 200}
        }
        self.collection.create_index(field_name="vector", index_params=index_params)
        self.collection.load()
        print("COSINE HNSW index created/updated.")
        # Update retriever after index change
        self.retriever.metric_type = "COSINE"
        return True

    def create(self):
        llm = self.llm
        retriever = self.retriever

        @tool
        def retrieve_financial_documents(question: str) -> str:
            """
            Retrieve the most relevant financial document excerpts from the Milvus knowledge base
            for a given user question and return them as plain text.
            """
            print("--- RAGAgent: RETRIEVING DOCUMENTS ---")
            multi_query_retriever = MultiQueryRetriever.from_llm(
                retriever=retriever,
                llm=llm,
            )
            retrieved_docs = multi_query_retriever.invoke(question)

            if not retrieved_docs:
                return "No relevant documents were found to answer this question."

            return "\n\n---\n\n".join(doc.page_content for doc in retrieved_docs)

        agent = create_react_agent(
            model=self.llm,
            tools=[retrieve_financial_documents],
            prompt=self.PROMPT,
            name="RAG_agent",
        )
        return agent