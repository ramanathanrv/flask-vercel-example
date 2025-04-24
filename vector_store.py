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
from langchain_community.document_loaders import JSONLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
import google.generativeai as genai  # Import Google Gemini API

class VectorStore:
    def __init__(self):
        self.index = None
        self.card_mapping = {}
        self.retriever = None

