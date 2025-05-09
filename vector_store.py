from langchain.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.document_loaders import TextLoader

def build_vector_store():
    docs = []
    for file in ["data/faq.txt", "data/specs.txt", "data/guide.txt"]:
        raw = TextLoader(file).load()
        splitter = RecursiveCharacterTextSplitter(chunk_size=300, chunk_overlap=50)
        docs.extend(splitter.split_documents(raw))
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2",model_kwargs={"device": "cpu"})
    return FAISS.from_documents(docs, embeddings)
