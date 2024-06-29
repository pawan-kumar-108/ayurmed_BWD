import chainlit as cl
from haystack.document_stores import InMemoryDocumentStore
from haystack.nodes import PromptNode, PromptTemplate, BM25Retriever
from haystack.pipelines import Pipeline
from transformers import GenerationConfig
from dotenv import load_dotenv
import os
from PyPDF2 import PdfReader
import docx

load_dotenv()

# Function to read PDF files
def read_pdf(file_path):
    text = ""
    try:
        with open(file_path, "rb") as file:
            pdf_reader = PdfReader(file)
            for page_num in range(len(pdf_reader.pages)):
                text += pdf_reader.pages[page_num].extract_text()
        return text
    except Exception as e:
        return f"Error reading PDF file: {e}"

# Function to read Word files
def read_word(file_path):
    try:
        doc = docx.Document(file_path)
        text = ""
        for paragraph in doc.paragraphs:
            text += paragraph.text + "\n"
        return text
    except Exception as e:
        return f"Error reading Word file: {e}"

# Function to read Text files
def read_txt(file_path):
    try:
        with open(file_path, "r") as file:
            text = file.read()
        return text
    except Exception as e:
        return f"Error reading text file: {e}"

# Function to read all files in a directory
def read_directory(directory):
    combined_text = ""
    for file_name in os.listdir(directory):
        file_path = os.path.join(directory, file_name)
        if file_name.endswith(".pdf"):
            combined_text += read_pdf(file_path)
        elif file_name.endswith(".docx"):
            combined_text += read_word(file_path)
        elif file_name.endswith(".txt"):
            combined_text += read_txt(file_path)
    return combined_text

# Chunking strategy to split text into smaller chunks
def chunk_text(text, chunk_size=1000, overlap=100):
    words = text.split()
    chunks = []
    for i in range(0, len(words), chunk_size - overlap):
        chunk = ' '.join(words[i:i + chunk_size])
        chunks.append(chunk)
    return chunks

# Load the environment variable
HF_TOKEN = os.getenv("HF_TOKEN")
if not HF_TOKEN:
    raise ValueError("HF_TOKEN environment variable is not set")

# Placeholder for dataset content (modify the path as needed)
dataset_content = read_directory("document_")
print("Dataset Content Loaded")

# To just validate the content
print(dataset_content[:2000])

# Initialize Document Store
document_store = InMemoryDocumentStore(use_bm25=True)
print("Document Store Initialized")

# Populate the document store with chunks
docs = [{'content': chunk} for chunk in chunk_text(dataset_content)]
document_store.write_documents(docs)
print(f"{len(docs)} Documents Written to Document Store")

# Initialize BM25 Retriever
retriever = BM25Retriever(document_store=document_store)
print("BM25 Retriever Initialized")

# Refined Prompt Template
prompt_template = PromptTemplate("You are an Ayurvedic Health Expert who is focussed on traeting their patient on chat. You have to listen to the query as disease symptom and answer based on knowledge base. Make sure that you use the knowledge base So, based on the given context, please provide the answers in a friendly way to soothe the patients queries: {query}")

# Initialize Prompt Node
prompt_node = PromptNode(
    model_name_or_path="mistralai/Mistral-7B-Instruct-v0.3",
    api_key=HF_TOKEN,
    default_prompt_template=prompt_template,
    max_length=500,
    model_kwargs={"generation_kwargs": GenerationConfig(do_sample=True, top_p=0.3, temperature=0.1)}
)
print("Prompt Node Initialized")

# Create the pipeline
generative_pipeline = Pipeline()
generative_pipeline.add_node(component=retriever, name="retriever", inputs=["Query"])
generative_pipeline.add_node(component=prompt_node, name="prompt_node", inputs=["retriever"])
print("Pipeline Created")

@cl.on_message
async def main(message: cl.Message):
    print("Received Message:", message.content)
    
    # Run the pipeline
    response = generative_pipeline.run(query=message.content)
    print("Pipeline Response:", response)

    # Ensure response is in the expected format
    if 'results' in response:
        answers = response['results']
        
        if isinstance(answers, list):
            formatted_response = "".join(answers)
        else:
            print("Expected 'results' to be a list, but got:", type(answers))
            formatted_response = "I'm sorry, I couldn't find an answer to your question."
    else:
        print("Response did not contain 'results':", response)
        formatted_response = "I'm sorry, I couldn't find an answer to your question."

    await cl.Message(content=formatted_response).send()