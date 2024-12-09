# FinancialNews-Advisory-Tool

# Features:  
1. Import URLs or upload text documents that include URLs to retrieve article content. 

2. Utilize LangChain's UnstructuredURL Loader to process the article content.  

3. Create an embedding vector using OpenAI's embeddings and make use of FAISS, a robust similarity search tool, to facilitate quick and efficient retrieval of pertinent information.  

4. Engage with the LLM (Chatgpt) by submitting inquiries and obtaining responses along with their corresponding source URLs.

# Installation:
1. Clone this repository to your local machine

2. Navigate to the project directory

3. Install the required dependencies using pip: - pip install -r requirements.txt

4. Set up your OpenAI API key or HuggingFace API key by creating a .env file in the project root and adding your API

5. HuggingFaceHub_API_KEY=your_api_key_here (This has to be in your .env file)

# Usage
1. You can Run the Streamlit app by executing "streamlit run main.py"
   
2. The web application will launch in your browser.

3. In the headerbar, you can directly enter URLs.

4. Start the data loading and processing by clicking on "Analyze URLs"

5. Watch the system as it conducts text splitting, creates embedding vectors, and indexes them efficiently using FAISS.

6. The embeddings will be stored and indexed with FAISS, improving retrieval speed.

7. The FAISS index will be saved in a local file path in pickle format for future reference.

8. You can now pose a question and receive an answer based on those news articles.

# Project Structure
1. main.py: This is the main Streamlit application script.

2. requirements.txt: A list of Python packages that is required for the project.

3. faiss_store_openai.pkl: FAISS index is stored in the pickle file.

4. .env: Configuration file for storing OpenAI/HuggingFace API key.
