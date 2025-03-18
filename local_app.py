import streamlit as st
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, Settings
from llama_index.llms.ollama import Ollama
# import Ollama
from llama_index.embeddings.ollama import OllamaEmbedding
import os
import tempfile

# Configure Streamlit page
st.set_page_config(
    page_title="Document Chat Local",
    page_icon="🔍",
    layout="centered"
)

# Initialize Ollama components
@st.cache_resource
def configure_llamaindex():
    llm = Ollama(
        model="deepseek-r1",
        base_url="http://localhost:11434",
        temperature=0.2,
        request_timeout=300
    )
    # embed_model = set_global_tokenizer(llm.tokenizer)
    embed_model = OllamaEmbedding(
        model_name="nomic-embed-text",
        base_url="http://localhost:11434"
    )
    Settings.llm = llm
    Settings.embed_model = embed_model
    return llm, embed_model

llm, embed_model = configure_llamaindex()

# Streamlit UI Components
st.title("Multi Document RAG with LlamaIndex and Deepseek-r1")
st.markdown("""
    Upload multiple documents and query them using Deepseek-r1 locally!
    Supported formats: PDF, TXT, DOCX, CSV
""")

# File upload and processing
def process_files(uploaded_files):
    with tempfile.TemporaryDirectory() as temp_dir:
        for file in uploaded_files:
            temp_path = os.path.join(temp_dir, file.name)
            with open(temp_path, "wb") as f:
                f.write(file.getbuffer())
        
        loader = SimpleDirectoryReader(
            temp_dir,
            recursive=True,
            required_exts=[".pdf", ".txt", ".docx", ".csv"]
        )
        try:
            documents = loader.load_data()
            index = VectorStoreIndex.from_documents(documents)
            return index
        except Exception as e:
            st.error(f"Error processing files: {str(e)}")
            return None

# Session state management
if "index" not in st.session_state:
    st.session_state.index = None
if "processed_files" not in st.session_state:
    st.session_state.processed_files = []
  


# Query interface
if st.session_state.index:
    query = st.chat_input("Ask about your documents...")
    if query:
        with st.spinner("Consulting Deepseek-r1..."):
            try:
                chat_engine = st.session_state.index.as_chat_engine(
                    chat_mode="context",
                    verbose=True
                )
                response = chat_engine.chat(query)
                
                with st.chat_message("user"):
                    st.write(query)
                
                with st.chat_message("assistant"):
                    st.write(response.response)
                    
                    # Show context sources
                    with st.expander("Document References"):
                        for source in response.source_nodes:
                            st.write(f"**Document:** {source.metadata.get('file_name', 'Unknown')}")
                            st.write(f"**Page:** {source.metadata.get('page_label', 'N/A')}")
                            st.write(f"**Confidence:** {source.score:.2f}")
                            st.markdown(f"```\n{source.text}\n```")
            except Exception as e:
                st.error(f"Error generating response: {str(e)}")
else:
    st.info("Upload and process documents on the sidebar to begin querying")

# Sidebar with model information
with st.sidebar:
    st.header("Configuration")
    st.markdown(f"""
        **LLM Model:** `deepseek-r1`  
        **Temperature:** `{llm.temperature}`  
    """)
    
    st.divider()
    st.markdown("""
        **Instructions:**
        1. Upload documents
        2. Click 'Process Documents'
        3. Ask questions in natural language
    """)
    st.divider()
    st.header("📁 Document Management")
    # File upload section
    uploaded_files = st.file_uploader(
        "Upload documents",
        type=["pdf", "txt", "docx", "csv"],
        accept_multiple_files=True,
        help="Upload multiple documents for RAG processing"
    )

    # Process files button
    if uploaded_files and st.button("Process Documents"):
        with st.status("Analyzing documents...", expanded=True) as status:
            st.write("Validating file formats...")
            valid_files = [f for f in uploaded_files if f.name.split(".")[-1] in ["pdf", "txt", "docx", "csv"]]
            
            st.write("Processing documents...")
            new_index = process_files(valid_files)
            
            if new_index:
                st.session_state.index = new_index
                st.session_state.processed_files = [f.name for f in valid_files]
                status.update(label="Processing complete!", state="complete", expanded=False)
                st.success(f"Processed {len(valid_files)} documents successfully!")

        # Clear chat button
    if st.button("🧹 Clear Chat History"):
        st.session_state.messages = [
            {"role": "assistant", "content": "Ask me anything about the research papers!"}
        ]
        st.rerun()

# Display processed files
if st.session_state.processed_files:
    with st.expander("📁 Processed Documents"):
        st.write("\n".join([f"- {f}" for f in st.session_state.processed_files]))
