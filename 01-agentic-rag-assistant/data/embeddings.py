
from memory.document_loaders import all_markdown_files
### Embeddings ###

from typing import List, Tuple
import os

from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.retrievers import BM25Retriever
from langchain_core.tools import StructuredTool
from langchain_core.documents import Document

# Global embeddings instance (loaded once)
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")


def make_hybrid_retriever_tool(
    file_list: List[str],
    db_dir: str = "./data/documents/company_faiss_df",
    name: str = "company_search",
    desc: str = "Search company info from documents (hybrid dense + sparse retrieval)"
) -> Tuple[StructuredTool, callable]:
    """
    Creates or loads a hybrid (dense + BM25) retriever tool.
    
    Returns:
        Tuple[StructuredTool, callable]: (tool, hybrid_retrieve_function)
    """
    os.makedirs(db_dir, exist_ok=True)
    index_path = os.path.join(db_dir, "index.faiss")
    docs_path = os.path.join(db_dir, "index.pkl")

    vectorstore = None
    chunks: List[Document] = []

    # Load existing FAISS index 
    if os.path.exists(index_path) and os.path.exists(docs_path):
        try:
            vectorstore = FAISS.load_local(
                folder_path=db_dir,
                embeddings=embeddings,
                allow_dangerous_deserialization=True
            )
            print(f"Loaded existing FAISS index from {db_dir}")
        except Exception as e:
            print(f"Failed to load FAISS index: {e}")
            print("→ Will rebuild the index...")

    # Build new index if missing 
    if vectorstore is None:
        print(f"Creating new FAISS index in {db_dir}")

        if not file_list:
            raise ValueError("file_list is empty — cannot create index")

        raw_docs: List[Document] = []
        for filepath in file_list:
            if not os.path.isfile(filepath):
                print(f"File not found, skipping: {filepath}")
                continue
            try:
                loader = TextLoader(filepath, encoding="utf-8")
                raw_docs.extend(loader.load())
            except Exception as e:
                print(f"Failed to load file {filepath}: {e}")

        if not raw_docs:
            raise ValueError("No documents could be loaded from the provided file_list")

        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,           
            separators=[
                "\n#{1,6} ",    
                "\n\n",         
                "\n",           
                " ",            
                ""
            ],
            keep_separator=True,
            add_start_index=True,
        )

        chunks = text_splitter.split_documents(raw_docs)

        if not chunks:
            raise ValueError("No chunks created after splitting — check document content")

        vectorstore = FAISS.from_documents(chunks, embeddings)
        vectorstore.save_local(db_dir)
        print(f"New FAISS index created and saved to {db_dir}")

    # Prepare retrievers 
    if not chunks:
        # fallback only if loaded but didn't re-split
        print("Warning: using docstore fallback (less reliable)")
        chunks = list(vectorstore.docstore._dict.values())

    # Sparse retriever — BM25
    sparse_retriever = BM25Retriever.from_documents(chunks)
    sparse_retriever.k = 5

    # Dense (semantic) retriever
    dense_retriever = vectorstore.as_retriever(search_kwargs={"k": 5})

    # Hybrid retrieval logic
    def hybrid_retrieve(query: str, top_k: int = 6) -> List[Document]:
        """Combine dense + sparse results with simple deduplication"""
        dense_docs = dense_retriever.invoke(query)
        sparse_docs = sparse_retriever.invoke(query)

        seen = set()
        combined = []

        for doc in dense_docs + sparse_docs:
            key = doc.page_content.strip()
            if key not in seen:
                seen.add(key)
                combined.append(doc)

        return combined[:top_k]

    # Tool function
    def tool_func(query: str) -> str:
        """Tool to search company documents using hybrid retrieval"""
        print(f"[TOOL] Using {name!r} for query: {query}")
        results = hybrid_retrieve(query)
        if not results:
            return "No relevant information found in company documents."
        return "\n\n".join(doc.page_content for doc in results)

    # Create the actual tool
    tool = StructuredTool.from_function(
        func=tool_func,
        name=name,
        description=desc,
    )

    return tool, hybrid_retrieve



_, hybrid_retrieve_func = make_hybrid_retriever_tool(all_markdown_files)
