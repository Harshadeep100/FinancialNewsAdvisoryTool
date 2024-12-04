import os
import streamlit as st
import pickle
import time
from langchain.chains import RetrievalQAWithSourcesChain
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.document_loaders import UnstructuredURLLoader
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEndpoint

from dotenv import load_dotenv
load_dotenv()  # take environment variables from .env (especially huggingface api key)

st.title("CryptoCool: News Research Tool")

# Input for News Article URLs
st.header("Provide the URLs of the News Articles to be Analyzed")
urls = []
for i in range(3):
    url = st.text_input(f"URL {i+1}")
    urls.append(url)

process_url_clicked = st.button("Analyze URLs")
file_path = "faiss_store_huggingface.pkl"

main_placeholder = st.empty()

# Set up the Hugging Face LLM (replace with your model and token)
repo_id = "mistralai/Mistral-7B-Instruct-v0.2"  # Replace with your Hugging Face model repo ID
api_token = os.getenv("HUGGINGFACEHUB_API_TOKEN")  # Make sure this is set in your .env file
llm = HuggingFaceEndpoint(
    repo_id=repo_id,
    temperature=0.9,
    model_kwargs={"max_length": 500},
    token=api_token
)

if process_url_clicked:
    # load data
    loader = UnstructuredURLLoader(urls=urls)
    main_placeholder.text("Data Loading...Started...\u2705\u2705\u2705")
    data = loader.load()
    # split data
    text_splitter = RecursiveCharacterTextSplitter(
        separators=['\n\n', '\n', '.', ','],
        chunk_size=1000
    )
    main_placeholder.text("Text Splitter...Started...\u2705\u2705\u2705")
    docs = text_splitter.split_documents(data)
    # create embeddings and save it to FAISS index
    embeddings = HuggingFaceEmbeddings()  # Using Hugging Face for embeddings
    vectorstore_huggingface = FAISS.from_documents(docs, embeddings)
    main_placeholder.text("Embedding Vector Started Building...\u2705\u2705\u2705")
    time.sleep(2)

    # Save the FAISS index to a pickle file
    with open(file_path, "wb") as f:
        pickle.dump(vectorstore_huggingface, f)

query = main_placeholder.text_input("Query: ")
if query:
    if os.path.exists(file_path):
        with open(file_path, "rb") as f:
            vectorstore = pickle.load(f)
            chain = RetrievalQAWithSourcesChain.from_llm(llm=llm, retriever=vectorstore.as_retriever())
            result = chain({"question": query}, return_only_outputs=True)
            # result will be a dictionary of this format --> {"answer": "", "sources": [] }
            st.header("Answer")
            st.write(result["answer"])

            # Display sources, if available
            sources = result.get("sources", "")
            if sources:
                st.subheader("Sources:")
                sources_list = sources.split("\n")  # Split the sources by newline
                for source in sources_list:
                    st.write(source)
