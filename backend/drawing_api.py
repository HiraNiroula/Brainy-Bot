from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
import os
import PyPDF2
import matplotlib.pyplot as plt

app = FastAPI()
UPLOAD_FOLDER = 'uploads/'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.post("/upload/")
async def upload_pdf(file: UploadFile = File(...)):
    if not file.filename.endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Invalid file type. Only PDF files are allowed.")
    
    file_location = os.path.join(UPLOAD_FOLDER, file.filename)
    with open(file_location, "wb") as f:
        f.write(await file.read())
    
    return {"message": "File uploaded successfully"}

@app.get("/visualize/{filename}")
async def visualize_pdf(filename: str):
    pdf_path = os.path.join(UPLOAD_FOLDER, filename)
    if not os.path.exists(pdf_path):
        raise HTTPException(status_code=404, detail="File not found")

    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        num_pages = len(reader.pages)

    plt.bar(['Pages'], [num_pages])
    plt.title(f'Number of Pages in {filename}')
    plt.ylabel('Count')
    plt.savefig('visualization.png')
    plt.close()

    return FileResponse('visualization.png', media_type='image/png', filename='visualization.png')

@app.post("/draw/")
async def save_drawing(drawing_data: dict):
    if 'drawing_data' not in drawing_data:
        raise HTTPException(status_code=400, detail="Drawing data is required")
    
    # Save drawing data logic here (e.g., to a database or file)
    return {"message": "Drawing data received", "data": drawing_data['drawing_data']}