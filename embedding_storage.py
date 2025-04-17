"""
Embedding storage module for the Educational RAG System.

This module handles creating and storing embeddings for document chunks
using HuggingFace embeddings and ChromaDB.
"""

from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

def get_embeddings():
    """
    Initialize the HuggingFace embedding model.
    
    Returns:
        HuggingFaceEmbeddings: Initialized embedding model
    """
    return HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")


def store_documents(chunks, persist_directory="./chroma_db"):
    """
    Store document chunks in a ChromaDB vector store.
    
    Args:
        chunks (list): List of document chunks to store
        persist_directory (str): Directory to persist the vector store
        
    Returns:
        Chroma: The created vector store
    """
    # Initialize embedding function
    embedding_function = get_embeddings()
    
    # Create a Chroma vector store
    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embedding_function,
        persist_directory=persist_directory
    )
    
    print(f"Stored {len(chunks)} chunks in ChromaDB at {persist_directory}")
    
    return vectorstore


def retrieve_documents(query, top_k=5, persist_directory="./chroma_db"):
    """
    Retrieve relevant documents for a query.
    
    Args:
        query (str): The query string
        top_k (int): Number of documents to retrieve
        persist_directory (str): Directory where the vector store is persisted
        
    Returns:
        list: List of (document, score) tuples
    """
    # Initialize embedding function
    embedding_function = get_embeddings()
    
    # Load existing vector store
    vectorstore = Chroma(
        persist_directory=persist_directory,
        embedding_function=embedding_function
    )
    
    # Retrieve relevant documents
    results = vectorstore.similarity_search_with_score(query, k=top_k)
    
    return results