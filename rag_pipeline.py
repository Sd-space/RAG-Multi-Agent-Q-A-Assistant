from openrouter_chat import OpenRouterChat
from langchain.schema import HumanMessage


from dotenv import load_dotenv
load_dotenv()


llm = OpenRouterChat()

def retrieve_top_chunks(query, vector_store, k=3):
    return vector_store.similarity_search(query, k=k)

def generate_answer(query, context_chunks):
    context = "\n\n".join([doc.page_content for doc in context_chunks])
    prompt = f"Context:\n{context}\n\nQuestion: {query}\nAnswer:Please Give answer based on context and summarize the answer"
    print(prompt)
    #message = HumanMessage(content=prompt)  # properly structured message
    # converted_message = llm._convert_message(message)
    
    return llm._generate(prompt)
