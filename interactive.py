"""
Interactive mode module for the Educational RAG System.

This module provides an interactive command-line interface for
continuously querying the RAG system.
"""

import os
import argparse
from rag_query import rag_query


def interactive_mode(model="llama3:8b", top_k=5, db_path="./chroma_db"):
    """
    Run the RAG system in interactive mode.
    
    Args:
        model (str): The Ollama model to use
        top_k (int): Number of documents to retrieve
        db_path (str): Path to the ChromaDB directory
    """
    print("\n=== Educational RAG System Interactive Mode ===")
    print(f"Using model: {model}")
    print(f"Database: {db_path}")
    print('Type "exit" to quit\n')
    
    while True:
        query = input("\nQuestion: ")
        if query.lower() in ["exit", "quit", "q"]:
            break
        
        print("\nThinking...")
        result = rag_query(query, model, top_k)
        
        print("\nAnswer:")
        print(result["answer"])
        print("\nSources:")
        for i, source in enumerate(result["sources"]):
            print(f"[{i+1}] {os.path.basename(source)}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Interactive Educational RAG System')
    parser.add_argument('--model', default='llama3:8b', help='Ollama model to use')
    parser.add_argument('--top-k', type=int, default=5, help='Number of chunks to retrieve')
    parser.add_argument('--db-path', default='./chroma_db', help='ChromaDB storage path')
    
    args = parser.parse_args()
    
    # Check if database exists
    if not os.path.isdir(args.db_path):
        print(f"Error: Vector database at {args.db_path} does not exist. Process documents first.")
        exit(1)
    
    interactive_mode(args.model, args.top_k, args.db_path)