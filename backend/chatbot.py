import PyPDF2
import json
from pymongo import MongoClient, errors
from transformers import pipeline
from config.config import MONGO_URI, DB_NAME, COLLECTION_NAME, USER_QUESTIONS_COLLECTION

summarizer = pipeline("summarization", model="facebook/bart-base")

def connect_to_mongo():
    try:
        client = MongoClient(MONGO_URI)
        db = client[DB_NAME]
        collection = db[COLLECTION_NAME]
        summary_collection = db[USER_QUESTIONS_COLLECTION]
        print("Connected to MongoDB successfully.")
        return collection, summary_collection
    except errors.ConnectionError as e:
        print(f"Could not connect to MongoDB: {e}")
        return None, None

def extract_text_from_pdf(pdf_path):
    units = []
    try:
        with open(pdf_path, "rb") as file:
            pdf_reader = PyPDF2.PdfReader(file)
            for page in pdf_reader.pages:
                text = page.extract_text()
                if text:
                    # Here, we split by double newlines as an example
                    units.extend(text.split("\n\n"))  # Adjust this based on your PDF structure
        print("PDF text extracted successfully.")
    except FileNotFoundError:
        print(f"Error: The file {pdf_path} was not found.")
        return None
    except PyPDF2.PdfReaderError as e:
        print(f"Error reading PDF file: {e}")
        return None
    return units

def save_units_to_json(units, json_file_path):
    try:
        with open(json_file_path, 'w') as json_file:
            json.dump(units, json_file, indent=4)
        print(f"Units saved to {json_file_path} successfully.")
    except Exception as e:
        print(f"Error saving to JSON file: {e}")

def load_units_from_json(json_file_path):
    try:
        with open(json_file_path, 'r') as json_file:
            units = json.load(json_file)
        print(f"Units loaded from {json_file_path} successfully.")
        return units
    except Exception as e:
        print(f"Error loading JSON file: {e}")
        return []

def store_pdf_content(collection, units):
    if collection is not None:
        try:
            for unit in units:
                collection.insert_one({"content": unit})
            print("PDF content stored in MongoDB successfully.")
        except errors.PyMongoError as e:
            print(f"Error storing PDF content in MongoDB: {e}")

def summarize_text(text, chunk_size=512):
    summaries = []
    # Split the text into chunks
    for i in range(0, len(text), chunk_size):
        chunk = text[i:i + chunk_size]
        try:
            summary = summarizer(chunk, max_length=15, do_sample=False)
            summaries.append(summary[0]['summary_text'])
        except Exception as e:
            print(f"Error summarizing text: {e}")
            summaries.append("I'm sorry, I couldn't summarize this part at the moment.")
    return " ".join(summaries)

pdf_path = r"D:\Hacakthon\english.pdf"  
json_file_path = r"D:\Hacakthon\units.json"

# Step 1: Extract text from PDF and save to JSON
units = extract_text_from_pdf(pdf_path)
if units:
    save_units_to_json(units, json_file_path)

# Step 2: Load units from JSON and store in MongoDB
collection, summary_collection = connect_to_mongo()
if collection is not None:  # Corrected this line
    loaded_units = load_units_from_json(json_file_path)
    store_pdf_content(collection, loaded_units)

if __name__ == "__main__":
    print("Welcome to the AI-powered learning assistant chatbot!")
    print("Type 'exit' or 'quit' to end the chat.")
    
    while True:
        user_input = input("You: ")
        if user_input.lower() in ["exit", "quit"]:
            print("Goodbye!")
            break
        
        documents = collection.find()
        matched_content = []
        for doc in documents:
            if 'content' in doc:  
                if user_input.lower() in doc['content'].lower(): 
                    matched_content.append(doc['content'])

        if matched_content:
            relevant_content = " ".join(matched_content)
            summary = summarize_text(relevant_content)
            
            if summary_collection is not None:
                try:
                    summary_collection.insert_one({"user_input": user_input, "summary": summary})
                    print("Summary stored in MongoDB successfully.")
                except errors.PyMongoError as e:
                    print(f"Error storing summary in MongoDB: {e}")
            else:
                print("Summary collection is not available.")
        else:
            print("No relevant content found for your query.")