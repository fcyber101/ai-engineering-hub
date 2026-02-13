
### Answer generation





def create_generate_answer(state, llm):
    """generate the answer"""
    question = state["question"]
    documents = state.get("documents", [])
    feedback = state.get("grade_feedback", "")
    
    # Combine documents
    context = "\n\n".join([doc.page_content for doc in documents]) if documents else ""
    
    # Prompt
    prompt = f"""Answer this question:

    QUESTION: {question}

    FEEDBACK ON PREVIOUS ATTEMPT if provided: {feedback}

    AVAILABLE DATA: {context}

    Your answer:"""
    
    answer = llm.invoke(prompt)  
    return {"answer": answer.content}


