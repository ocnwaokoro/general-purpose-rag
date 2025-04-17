# General Purpose RAG System

A versatile Retrieval-Augmented Generation (RAG) system that lets you query your documents using natural language, built to run entirely locally on macOS with Apple Silicon.

![MIT License](https://img.shields.io/badge/License-MIT-green.svg)
![Python 3.8+](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Platform](https://img.shields.io/badge/Platform-macOS%20(Apple%20Silicon)-lightgrey)

## 📚 Overview

This system allows you to:
- Process various document types into searchable chunks
- Store those chunks with vector embeddings in ChromaDB
- Query your documents using natural language
- Get AI-generated answers based on the relevant context from your documents

**All processing runs locally** - no cloud services, API keys, or internet connection required after setup.

## 📄 Supported File Types

Currently, the system supports:
- PDF documents (`.pdf`)
- Text files (`.txt`)

More file types can be added by extending the document processor. See the "Adding Support for More File Types" section for details on how to support additional formats like:
- Word documents (`.docx`)
- Markdown files (`.md`)
- HTML files (`.html`)
- PowerPoint presentations (`.pptx`)
- And more!

## 🚀 Quick Start

1. **Clone this repository**
```bash
git clone https://github.com/yourusername/general-purpose-rag.git
cd general-purpose-rag
```

2. **Set up the environment**
```bash
# Create and activate virtual environment
python -m venv rag_env
source rag_env/bin/activate

# Install required packages
pip install -r requirements.txt
```

3. **Install Ollama**
```bash
# Install Ollama
brew install ollama

# Pull a model
ollama pull llama3:8b
```

4. **Start Ollama server** (in a separate terminal)
```bash
ollama serve
```

5. **Process your documents**
```bash
python main.py process /path/to/your/documents
```

6. **Query the system**
```bash
python main.py query "Who created Python?"
```

7. **Or use interactive mode**
```bash
python interactive.py
```

## 📋 Prerequisites

- macOS with Apple Silicon (M1/M2/M3)
- Python 3.8+
- Homebrew

## 🔧 System Architecture

The system consists of four main components:

1. **Document Processor** (`document_processor.py`): 
   - Loads supported file types from a directory
   - Splits documents into manageable chunks
   - Adds metadata to track source files

2. **Embedding Storage** (`embedding_storage.py`):
   - Generates vector embeddings using HuggingFace's `all-MiniLM-L6-v2` model
   - Stores document chunks and embeddings in ChromaDB
   - Handles similarity search for retrieval

3. **RAG Query System** (`rag_query.py`):
   - Retrieves relevant document chunks based on user queries
   - Formats context for the language model
   - Queries Ollama's local language model
   - Returns answers with source citations

4. **Interface** (`main.py` and `interactive.py`):
   - Command-line tools for processing documents and querying the system
   - Interactive mode for continuous querying

## 🛠️ Usage

### Processing Documents

```bash
python main.py process /path/to/your/documents

# With custom parameters
python main.py process /path/to/your/documents --chunk-size 800 --chunk-overlap 150 --db-path ./custom_db
```

Options:
- `--chunk-size`: Size of text chunks (default: 1000)
- `--chunk-overlap`: Overlap between chunks (default: 200)
- `--db-path`: ChromaDB storage path (default: ./chroma_db)

### Querying

```bash
python main.py query "How does transformer architecture work?"

# With custom parameters
python main.py query "Compare GPT vs. BERT architectures" --model mistral:7b --top-k 8
```

Options:
- `--model`: Ollama model to use (default: llama3:8b)
- `--top-k`: Number of chunks to retrieve (default: 5)
- `--db-path`: ChromaDB storage path (default: ./chroma_db)

### Interactive Mode

```bash
python interactive.py

# With custom parameters
python interactive.py --model phi3:mini --top-k 3 --db-path ./ai_papers_db
```

## 🔄 Customization Options

### Model Alternatives

You can use different Ollama models:
- `llama3:8b` - Good all-around model
- `mistral:7b` - Excellent reasoning capabilities
- `phi3:mini` - Efficient on Apple Silicon

```bash
# Pull a different model
ollama pull mistral:7b

# Use it in your query
python main.py query "Explain AI alignment" --model mistral:7b
```

### Adjusting Retrieval

For more accurate but slower retrieval:
```bash
python main.py query "What are LLM hallucinations?" --top-k 10
```

For faster but potentially less comprehensive answers:
```bash
python main.py query "Define prompt engineering" --top-k 3
```

### Adding Support for More File Types

Edit `document_processor.py` to add support for more file types:

```python
# Example: Add support for DOCX files
from langchain_community.document_loaders import Docx2txtLoader

# Add in the load_documents function
docx_loader = DirectoryLoader(directory_path, glob="**/*.docx", loader_cls=Docx2txtLoader)
documents.extend(docx_loader.load())
```

Popular document formats you might want to add:
- Word documents: `Docx2txtLoader`
- Markdown: `UnstructuredMarkdownLoader`
- HTML: `BSHTMLLoader`
- CSV: `CSVLoader`
- Excel: `UnstructuredExcelLoader`
- PowerPoint: `UnstructuredPowerPointLoader`
- JSON: `JSONLoader`
- Email: `UnstructuredEmailLoader`

## 📂 Project Structure

```
general-purpose-rag/
├── document_processor.py - Processes files into chunks
├── embedding_storage.py - Handles vector embeddings and ChromaDB storage
├── rag_query.py - Implements the RAG query system
├── main.py - CLI for processing documents and querying the system
├── interactive.py - Interactive CLI interface
├── requirements.txt - Required packages
├── rag_env/ - Virtual environment (created during setup)
└── chroma_db/ - ChromaDB storage (created after processing documents)
```
## 🔍 Advanced Use Cases

### Topic-Specific Databases

For different document collections, create separate ChromaDB databases:

```bash
# Process legal documents
python main.py process ~/Documents/Legal --db-path ./legal_db

# Process technical documentation
python main.py process ~/Documents/Technical --db-path ./technical_db

# Query AI ethics documents
python main.py query "Summarize AI safety concerns" --db-path ./legal_db

# Cross-database querying (using multiple RAG systems together)
python main.py query "How do LLMs impact software development?" --db-path ./combined_db
```

### Custom Document Processing

Adjust chunk size and overlap based on your content:

- **Long, complex documents**: Larger chunks, more overlap
  ```bash
  python main.py process /path/to/docs --chunk-size 1500 --chunk-overlap 300
  ```

- **Short, focused documents**: Smaller chunks, less overlap
  ```bash
  python main.py process /path/to/docs --chunk-size 500 --chunk-overlap 100
  ```

## ❓ Troubleshooting

- **Ollama connection errors**: Make sure Ollama is running with `ollama serve`
- **Model not found**: Ensure you've pulled the model with `ollama pull <model>`
- **ChromaDB errors**: Check that the persist directory exists and has write permissions
- **PDF parsing errors**: Some PDFs may be encrypted or in a format not readable by PyPDF. Try converting them to text first using tools like `pdftotext`

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📜 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- [LangChain](https://github.com/langchain-ai/langchain) - For document processing and RAG framework
- [ChromaDB](https://github.com/chroma-core/chroma) - For vector storage
- [Ollama](https://github.com/ollama/ollama) - For local LLM inference
- [HuggingFace](https://huggingface.co/) - For the embedding model