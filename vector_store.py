# import s2
from data_utils import DataUtils  # Importing the DataUtils class
from genai_utils import count_tokens  # Importing the count_tokens function
from constants import DATA_FILE  # Import DATA_FILE from constants
from constants import ALG  # Import DATA_FILE from constants
from constants import FAISS_INDEX_PATH  # Import DATA_FILE from constants
import os
import time
import json
import pickle
from langchain.schema import Document
from langchain.document_loaders import JSONLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
import google.generativeai as genai  # Import Google Gemini API
# from card_recommender import CardRecommender

class VectorStore:
    def __init__(self):
        self.index = None
        self.card_mapping = {}
        self.retriever = None

    def build_index(self):
        db = None
        if os.path.exists(FAISS_INDEX_PATH):
            print("Loading existing FAISS vector store...")
            db = FAISS.load_local(FAISS_INDEX_PATH, GoogleGenerativeAIEmbeddings(model="models/embedding-001"), allow_dangerous_deserialization=True)
            print("Done Loading vector store")
            self.index = db
        else:             
            print("🔁 Building FAISS vector index...")
            data = DataUtils.load_crawled_data(DATA_FILE)
            documents = []

            for entry in data:
                card = entry["card"]
                content = ". ".join(entry["benefits"])
                documents.append({"page_content": card + "\n" + content, "metadata": {"card": entry["card"]}})

            # Convert to LangChain documents
            docs = [Document(page_content=d["page_content"], metadata=d["metadata"]) for d in documents]

            # Split text
            splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
            split_docs = splitter.split_documents(docs)

            # Embed documents
            embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")  # Use Gemini embeddings
            db = FAISS.from_documents(split_docs, embeddings)
            db.save_local(FAISS_INDEX_PATH)

            # Build card mapping (index -> card name)
            card_mapping = {}
            for i, doc in enumerate(split_docs):
                card_mapping[i] = doc.metadata["card"]

            print("✅ Vector index built")
            # Assigning to the instance variables
            self.index = db
            self.card_mapping = card_mapping
        
        # continue
        self.retriever = db.as_retriever(search_type="similarity", search_kwargs={"k": 5})

    # def r2(self, cards, prompt):
    #     # Assuming you already have a `retriever` (local store or vector store) and model (e.g., ALG) initialized
    #     card_rec = CardRecommender(retriever=self.retriever, model=ALG)
    #     cards_str = ", ".join(cards)
    #     # User query
    #     query = f"I have these cards with me: {cards_str}. My query: {prompt}"

    #     # Get the recommendation
    #     response = card_rec.get_card_recommendation(query)

    #     # Print or use the response
    #     print("LLM Response:", response)
    #     return response

