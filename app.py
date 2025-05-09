import streamlit as st
from vector_store import build_vector_store
from agent import route_query

st.title("📚 RAG Multi-Agent Q&A Assistant")

query = st.text_input("Ask a question:")

if 'vs' not in st.session_state:
    st.session_state.vs = build_vector_store()

if query:
    result = route_query(query, st.session_state.vs)
    if len(result) == 2:
        answer, log = result
        st.markdown(f"**Decision:** {log}")
        st.markdown(f"**Answer:** {answer}")
    else:
        answer, log, context = result
        print(type(answer))
        st.markdown(f"**Decision:** {log}")
        st.markdown(f"**Answer:** {answer}")
        st.markdown("**Retrieved Context:**")
        for i, chunk in enumerate(context, 1):
            st.text(f"{i}. {chunk.page_content[:300]}")
