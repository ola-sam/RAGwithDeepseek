# 🔍 LocalRAG: Enterprise-Grade Document Intelligence on Your Laptop

**A fully local RAG system powered by Ollama (Deepseek-r1) and LlamaIndex - No API keys required!**

## 🌟 Features
- **100% Local Execution** - All processing happens on your machine
- **Multi-Document Support** - PDF, TXT, DOCX, CSV formats
- **Auditable Responses** - Source tracing with confidence scores
- **Privacy-First Architecture** - Zero data leaves your environment
- **Modern UI** - Streamlit-powered chat interface
- **Advanced Retrieval** - Hybrid search with Nomic embeddings

## 🛠️ Technologies Used
- **LLM:** `deepseek-r1` via Ollama
- **Embeddings:** `nomic-embed-text`
- **Framework:** LlamaIndex
- **UI:** Streamlit
- **Processing:** PyPDF, python-docx, transformers

## 🚀 Quick Start

### Prerequisites
- Python 3.9+
- [Ollama](https://ollama.ai/) installed and running
- 8GB+ RAM recommended


### Usage
```bash
streamlit run rag_app.py
```
1. **Process Documents**:
   - Upload files via UI
   - Click "Process Documents"
   
2. **Query Documents**:
   - Ask natural language questions
   - Review sources in expandable sections

## ⚙️ Configuration
Modify `configure_llamaindex()` in `local_app.py` to adjust:
- Temperature (0-1)
- Request timeout
- Chunk sizes
- Search parameters

## 📚 Supported File Types
| Format | Processor | Limitations |
|--------|-----------|-------------|
| PDF    | PyPDF     | Text-based PDFs only |
| DOCX   | python-docx | No images |
| TXT    | Native    | UTF-8 encoding |
| CSV    | pandas    | <1MB recommended |


## 🤝 Contributing
PRs welcome! Please follow:
1. Fork repository
2. Create feature branch (`feat/your-feature`)
3. Submit PR with detailed description


---

**Maintainer:** Sam Elegure 
**Special Thanks:** 
[@Ollama](https://github.com/ollama/ollama) team, 
[LlamaIndex](https://github.com/run-llama/llama_index) contributors

