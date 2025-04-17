"""
Document processor module for the Educational RAG System.

This module handles loading documents from a directory and splitting them into chunks.
It supports PDF and text files.
"""

import os
from langchain_community.document_loaders import PyPDFLoader, TextLoader, DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter


def load_documents(directory_path):
    """
    Load documents from a directory with various file types.
    
    Args:
        directory_path (str): Path to the directory containing documents
        
    Returns:
        list: List of loaded Document objects
    """
    # Create loaders for different file types
    pdf_loader = DirectoryLoader(directory_path, glob="**/*.pdf", loader_cls=PyPDFLoader)
    text_loader = DirectoryLoader(directory_path, glob="**/*.txt", loader_cls=TextLoader)
    
    documents = []
    # Load documents using appropriate loaders
    try:
        documents.extend(pdf_loader.load())
        print(f"Loaded PDF documents")
    except Exception as e:
        print(f"Error loading PDF files: {e}")
    
    try:
        documents.extend(text_loader.load())
        print(f"Loaded text documents")
    except Exception as e:
        print(f"Error loading text files: {e}")
    
    return documents


def split_documents(documents, chunk_size=1000, chunk_overlap=200):
    """
    Split documents into chunks for processing.
    
    Args:
        documents (list): List of Document objects
        chunk_size (int): Size of each chunk in characters
        chunk_overlap (int): Overlap between chunks in characters
        
    Returns:
        list: List of chunked Document objects with metadata
    """
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["\n\n", "\n", ".", " ", ""]
    )
    
    chunks = text_splitter.split_documents(documents)
    
    # Add metadata about which document and chunk this is
    for i, chunk in enumerate(chunks):
        if "source" in chunk.metadata:
            file_name = os.path.basename(chunk.metadata["source"])
            chunk.metadata["file_name"] = file_name
        chunk.metadata["chunk_id"] = i
    
    return chunks


def process_directory(directory_path, chunk_size=1000, chunk_overlap=200):
    """
    Process all documents in a directory.
    
    Args:
        directory_path (str): Path to the directory containing documents
        chunk_size (int): Size of each chunk in characters
        chunk_overlap (int): Overlap between chunks in characters
        
    Returns:
        list: List of processed document chunks
    """
    print(f"Processing documents in {directory_path}...")
    documents = load_documents(directory_path)
    print(f"Loaded {len(documents)} documents")
    
    chunks = split_documents(documents, chunk_size, chunk_overlap)
    print(f"Created {len(chunks)} chunks")
    
    return chunks