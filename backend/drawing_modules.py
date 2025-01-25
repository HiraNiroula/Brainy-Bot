import cv2
import numpy as np
import pymongo
import PyPDF2
from io import BytesIO
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neighbors import NearestNeighbors
from config.config import MONGO_URI, DB_NAME, COLLECTION_NAME
from pymongo import MongoClient

client = MongoClient(MONGO_URI)
database = client[DB_NAME]
collection = database[COLLECTION_NAME] 

def extract_text_from_pdf(pdf_id):
    pdf_document = collection.find_one({"_id": pdf_id})  
    if pdf_document and "pdf_file" in pdf_document:
        pdf_file = pdf_document["pdf_file"]  
        reader = PyPDF2.PdfReader(BytesIO(pdf_file))
        text = ""
        for page in reader.pages:
            text += page.extract_text() + "\n"
        return text
    return ""

canvas = np.zeros((500, 900, 3), dtype="uint8")
drawing = False
last_point = None
brush_color = (255, 0, 0)  
brush_size = 5
history = []  
redo_stack = []  

def draw(event, x, y, flags, param):
    global drawing, last_point, canvas, history, redo_stack

    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        last_point = (x, y)
        history.append(canvas.copy())
        redo_stack.clear()  

    elif event == cv2.EVENT_MOUSEMOVE:
        if drawing:
            cv2.line(canvas, last_point, (x, y), brush_color, brush_size)
            last_point = (x, y)

    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False
        last_point = None

def change_color(new_color):
    global brush_color
    brush_color = new_color

def change_brush_size(new_size):
    global brush_size
    brush_size = new_size

def undo():
    global canvas, history, redo_stack
    if history:
        redo_stack.append(canvas.copy())  
        canvas = history.pop()  


def redo():
    global canvas, redo_stack
    if redo_stack:
        history.append(canvas.copy())  
        canvas = redo_stack.pop()  
def visualize_pdf_content(pdf_id):
    text = extract_text_from_pdf(pdf_id)
    y0, dy = 50, 30  
    for i, line in enumerate(text.split('\n')):
        if y0 + i * dy < canvas.shape[0]:  
            cv2.putText(canvas, line, (10, y0 + i * dy), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1, cv2.LINE_AA)
    return text

def extract_features_from_drawing():
    gray_canvas = cv2.cvtColor(canvas, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray_canvas, 127, 255, cv2.THRESH_BINARY_INV)
    features = thresh.flatten()
    return features

def suggest_content(drawing_features, pdf_text):
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform([pdf_text])
    
    knn = NearestNeighbors(n_neighbors=1)
    knn.fit(tfidf_matrix)
    
    drawing_text = " ".join([str(int(x)) for x in drawing_features])  # Convert features to string
    drawing_tfidf = vectorizer.transform([drawing_text])
    
    distances, indices = knn.kneighbors(drawing_tfidf)
    return pdf_text  
cv2.namedWindow("Canvas")
cv2.setMouseCallback("Canvas", draw)

pdf_id = "your_pdf_id"  
pdf_text = visualize_pdf_content(pdf_id)

while True:
    cv2.imshow("Canvas", canvas)
    
    key = cv2.waitKey(1) & 0xFF
    if key == 27:
        break
    elif key == ord('u'):  
        undo()
    elif key == ord('r'):  
        redo()
    elif key == ord('c'):  
        change_color((0, 0, 255))  
    elif key == ord('s'):  
        drawing_features = extract_features_from_drawing()
        suggested_content = suggest_content(drawing_features, pdf_text)
        print("Suggested Content:\n", suggested_content) 

cv2.destroyAllWindows()  