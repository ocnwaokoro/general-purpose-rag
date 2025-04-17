"""
Main module for the Educational RAG System.

This module provides the command-line interface for processing documents
and querying the system.
"""

import argparse
import os
from document_processor import process_directory
from embedding_storage import store_documents
from rag_query import rag_query


def main():
    """
    Main function that handles command-line arguments and runs the system.
    """
    parser = argparse.ArgumentParser(description='Educational RAG System')
    subparsers = parser.add_subparsers(dest='command', help='Command to run')
    
    # Process documents command
    process_parser = subparsers.add_parser('process', help='Process documents')
    process_parser.add_argument('directory', help='Directory containing documents')
    process_parser.add_argument('--chunk-size', type=int, default=1000, help='Chunk size')
    process_parser.add_argument('--chunk-overlap', type=int, default=200, help='Chunk overlap')
    process_parser.add_argument('--db-path', default='./chroma_db', help='ChromaDB storage path')
    
    # Query command
    query_parser = subparsers.add_parser('query', help='Query the RAG system')
    query_parser.add_argument('query', help='Question to ask')
    query_parser.add_argument('--model', default='llama3:8b', help='Ollama model to use')
    query_parser.add_argument('--top-k', type=int, default=5, help='Number of chunks to retrieve')
    query_parser.add_argument('--db-path', default='./chroma_db', help='ChromaDB storage path')
    
    args = parser.parse_args()
    
    if args.command == 'process':
        # Make sure the directory exists
        if not os.path.isdir(args.directory):
            print(f"Error: Directory {args.directory} does not exist")
            return
        
        # Process documents
        chunks = process_directory(args.directory, args.chunk_size, args.chunk_overlap)
        if chunks:
            store_documents(chunks, args.db_path)
        else:
            print("No documents were processed.")
    
    elif args.command == 'query':
        # Make sure the database exists
        if not os.path.isdir(args.db_path):
            print(f"Error: Vector database at {args.db_path} does not exist. Process documents first.")
            return
        
        # Query the system
        result = rag_query(args.query, args.model, args.top_k)
        print("\nAnswer:")
        print(result["answer"])
        print("\nSources:")
        for i, source in enumerate(result["sources"]):
            print(f"[{i+1}] {os.path.basename(source)}")
    else:
        parser.print_help()


if __name__ == "__main__":
    main()