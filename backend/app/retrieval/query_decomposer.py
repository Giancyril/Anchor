import json
from typing import List
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI
from app.config import settings

class QueryDecomposer:
    """
    Decomposes complex multi-intent questions into sub-queries and generates query variations.
    """
    def __init__(self, model_name: str = "gpt-4o-mini"):
        self.model_name = model_name

    async def decompose(self, query: str) -> List[str]:
        """Decompose a query into 1-3 distinct atomic search queries."""
        if not settings.OPENAI_API_KEY:
            # Fallback for offline / unit test mode
            if " and " in query.lower() or " or " in query.lower():
                parts = [p.strip() for p in query.replace("?", "").split(" and ")]
                return [query] + [p for p in parts if len(p) > 5]
            return [query]

        llm = ChatOpenAI(
            model=self.model_name,
            temperature=0.0,
            openai_api_key=settings.OPENAI_API_KEY,
        )

        prompt = ChatPromptTemplate.from_messages([
            ("system", "You are an AI search query optimizer. Given a user support query, generate 1 to 3 distinct, specific search queries that will retrieve the relevant knowledge base documentation. Output ONLY a valid JSON array of strings, e.g. [\"query 1\", \"query 2\"]."),
            ("human", "User Query: {query}"),
        ])

        chain = prompt | llm | StrOutputParser()
        try:
            raw = await chain.ainvoke({"query": query})
            parsed = json.loads(raw.strip())
            if isinstance(parsed, list) and all(isinstance(x, str) for x in parsed):
                return parsed if query in parsed else [query] + parsed
        except Exception:
            pass

        return [query]

query_decomposer = QueryDecomposer()