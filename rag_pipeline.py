from openrouter_chat import HuggingFaceChat
from langchain.schema import HumanMessage


from dotenv import load_dotenv
load_dotenv()


llm = HuggingFaceChat()

def retrieve_top_chunks(query, vector_store, k=3):
    return vector_store.similarity_search(query, k=k)

def generate_answer(query, context_chunks):
    # Join the context chunks into a single string
    context = "\n\n".join([doc.page_content for doc in context_chunks])

    # Format the prompt according to LLaMA 3 Instruct style
    prompt = f"""<s>[INST] <<SYS>>
You are a helpful, respectful, and honest assistant. Always provide concise, context-aware answers.
<</SYS>>

Context:
{context}

Question: {query}

Answer: Please answer based only on the above context and summarize it clearly.
[/INST]
"""

    # Optional: print the prompt for debugging
    print(prompt)

    # Generate the output using your LLaMA model
    return llm._generate(prompt)

