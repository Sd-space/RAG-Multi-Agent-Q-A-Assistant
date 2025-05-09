from tools import use_calculator, use_dictionary
from rag_pipeline import retrieve_top_chunks, generate_answer

def route_query(query, vector_store):
    decision_log = ""

    if any(kw in query.lower() for kw in ["calculate", "sum", "add", "multiply", "divide"]):
        decision_log = "Routed to Calculator Tool"
        return use_calculator(query), decision_log

    elif any(kw in query.lower() for kw in ["define", "what is", "meaning of"]):
        decision_log = "Routed to Dictionary Tool"
        return use_dictionary(query), decision_log

    else:
        decision_log = "Routed to RAG Pipeline"
        chunks = retrieve_top_chunks(query, vector_store)
        answer = generate_answer(query, chunks)
        return answer, decision_log, chunks
