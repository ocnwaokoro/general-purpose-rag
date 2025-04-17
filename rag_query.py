"""
RAG query module for the Educational RAG System.

This module implements the Retrieval-Augmented Generation query functionality
by retrieving relevant documents and querying the Ollama API.
"""

import requests
import os
from embedding_storage import retrieve_documents


def query_ollama(prompt, model="llama3:8b"):
    """
    Query the Ollama API with a prompt.
    
    Args:
        prompt (str): The prompt to send to the model
        model (str): The Ollama model to use
        
    Returns:
        str: The model's response
    """
    response = requests.post(
        'http://localhost:11434/api/generate',
        json={
            "model": model,
            "prompt": prompt,
            "stream": False
        }
    )
    
    if response.status_code == 200:
        return response.json()["response"]
    else:
        return f"Error: {response.text}"


def rag_query(user_query, model="llama3:8b", top_k=5):
    """
    Perform a RAG query using the retrieved documents and Ollama.
    
    Args:
        user_query (str): The user's question
        model (str): The Ollama model to use
        top_k (int): Number of documents to retrieve
        
    Returns:
        dict: Dictionary containing answer and sources
    """
    # Retrieve relevant documents
    relevant_docs = retrieve_documents(user_query, top_k)
    
    # Prepare context from retrieved documents
    context_parts = []
    sources = []
    
    for doc, score in relevant_docs:
        context_parts.append(f"Document: {doc.metadata.get('file_name', 'Unknown')}\nContent: {doc.page_content}")
        if "source" in doc.metadata:
            source = doc.metadata["source"]
            sources.append(source)
    
    context = "\n\n".join(context_parts)
    
    # Format sources for citation
    formatted_sources = []
    for i, source in enumerate(set(sources)):
        formatted_sources.append(f"[{i+1}] {os.path.basename(source)}")
    
    # Create prompt with context
    prompt = f"""You are an educational assistant that answers questions based on course materials.
Use the following context to answer the question, and cite your sources where possible.

CONTEXT:
{context}

SOURCES:
{', '.join(formatted_sources)}

QUESTION:
{user_query}

ANSWER:
"""
    
    # Query the LLM
    answer = query_ollama(prompt, model)
    
    return {
        "answer": answer,
        "sources": list(set(sources))
    }