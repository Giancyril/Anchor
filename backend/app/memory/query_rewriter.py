from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI
from app.config import settings

class QueryRewriter:
    """
    Reformulates ambiguous or contextual follow-up user questions into
    self-contained, standalone search queries using conversational context.
    """
    def __init__(self, model_name: str = "gpt-4o-mini"):
        self.model_name = model_name

    async def rewrite(self, query: str, conversation_context: str) -> str:
        if not conversation_context.strip() or not settings.OPENAI_API_KEY:
            return query

        llm = ChatOpenAI(
            model=self.model_name,
            temperature=0.0,
            openai_api_key=settings.OPENAI_API_KEY,
        )

        prompt = ChatPromptTemplate.from_messages([
            ("system", "You are an AI conversational query rewriter. Given the conversation history between a customer and a support assistant, reformulate the customer's latest question into a clear, standalone search query that can be understood without the chat history. Do NOT answer the question. Output ONLY the rewritten question."),
            ("human", "Conversation History:\n{history}\n\nLatest Customer Question: {query}\n\nStandalone Search Query:"),
        ])

        chain = prompt | llm | StrOutputParser()
        try:
            rewritten = await chain.ainvoke({"history": conversation_context, "query": query})
            return rewritten.strip().strip('"')
        except Exception:
            return query

query_rewriter = QueryRewriter()