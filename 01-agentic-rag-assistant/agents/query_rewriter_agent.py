
### Query Rewriter



from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser


def create_query_rewriter(llm):
    """
    Creates a query rewriter optimized for dense vector retrieval.
    Returns a callable that takes a question → returns improved query string.
    """
    system_prompt = """You are an expert query re-writer whose only goal is to convert a user's natural-language question 
    into the 'single best version' for semantic vector similarity search (dense retrieval).

    Rules – follow strictly:
    1. Preserve the original semantic intent — do NOT add new assumptions or facts
    2. Make the query clearer, more precise, and keyword-rich when helpful
    3. Use natural but search-optimized language (important entities, synonyms if natural)
    4. Remove chit-chat, greetings, politeness phrases
    5. Turn vague/underspecified questions into more concrete versions
    6. For multi-part questions → focus on the 'core information need'
    7. Keep the rewritten query concise (ideally 8–25 words)
    8. Output **only** the improved question — no explanations, no quotes, no prefixes.
    Now rewrite the following question:"""

    # prompt template

    reasoning_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system_prompt + "\n\nFirst think step-by-step about the user's intent, then output only the final rewritten question."),
            (
                "human",
                "Here is the initial question: \n\n {question} \n Fomulate an improved question"
            )
        ]
    )


    reasoning_rewriter = reasoning_prompt | llm | StrOutputParser()

    return reasoning_rewriter
