# from fastapi import FastAPI
# from pydantic import BaseModel
# from transformers import BertTokenizerFast, BertForSequenceClassification
# import torch
# import joblib
# import os

# # ---------------------------------------------------
# # Setup paths safely (avoids "spaces in path" errors)
# # ---------------------------------------------------
# BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# MODEL_DIR = os.path.join(BASE_DIR, "crime_model")        # local model folder
# ENCODER_PATH = os.path.join(BASE_DIR, "label_encoder.pkl")  # local label encoder

# # ---------------------------------------------------
# # Load Model, Tokenizer, and Label Encoder
# # ---------------------------------------------------
# tokenizer = BertTokenizerFast.from_pretrained(MODEL_DIR)
# model = BertForSequenceClassification.from_pretrained(MODEL_DIR)
# label_encoder = joblib.load(ENCODER_PATH)

# # ---------------------------------------------------
# # IPC Mapping Dictionary
# # ---------------------------------------------------
# IPC_CODES = {
#     "Fraud":"IPC 323",
#     "Theft": "IPC 378",
#     "Murder": "IPC 302",
#     "Accident (Causing Death by Negligence)": "IPC 304A",
#     "Rape": "IPC 376",
#     "Cheating": "IPC 420",
#     "Kidnapping": "IPC 363",
#     "Robbery": "IPC 392",
#     "Dacoity": "IPC 395",
#     "Criminal Breach of Trust": "IPC 406",
#     "Extortion": "IPC 384",
#     "Defamation": "IPC 499",
#     "Dowry Death": "IPC 304B",
#     "Attempt to Murder": "IPC 307",
#     "Grievous Hurt": "IPC 325",
#     "House Trespass": "IPC 448",
#     "Forgery": "IPC 465",
#     "Rioting": "IPC 147",
#     "Unlawful Assembly": "IPC 141",
#     "Acid Attack": "IPC 326A",
#     "Cybercrime (Hacking)": "IPC 66 IT Act + IPC 379/420"
# }

# # ---------------------------------------------------
# # Create FastAPI app
# # ---------------------------------------------------
# app = FastAPI(title="🚔 Police Crime Classification API")

# # Input schema
# class TextInput(BaseModel):
#     text: str

# # ---------------------------------------------------
# # Prediction endpoint
# # ---------------------------------------------------
# @app.post("/predict")
# def predict(input_data: TextInput):
#     text = input_data.text
    
#     # Tokenize input
#     inputs = tokenizer(text, return_tensors="pt", padding=True, truncation=True, max_length=512)
    
#     # Run model
#     with torch.no_grad():
#         outputs = model(**inputs)
#         predictions = torch.argmax(outputs.logits, dim=-1).item()
    
#     # Decode label
#     predicted_label = label_encoder.inverse_transform([predictions])[0]
    
#     # Find IPC code for crime type
#     ipc_section = IPC_CODES.get(predicted_label, "Unknown IPC")

#     return {
#         "text": text,
#         "crime_type": predicted_label,
#         "ipc_section": ipc_section
#     }

# # ---------------------------------------------------
# # Health check endpoint
# # ---------------------------------------------------
# @app.get("/")
# def root():
#     return {"message": "🚨 Police Crime Classification API is running!"}







# from fastapi import FastAPI
# from pydantic import BaseModel
# from transformers import BertTokenizerFast, BertForSequenceClassification
# import torch
# import joblib
# import os

# # ---------------------------------------------------
# # Setup paths
# # ---------------------------------------------------
# BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# MODEL_DIR = os.path.join(BASE_DIR, "crime_model")        # local model folder
# ENCODER_PATH = os.path.join(BASE_DIR, "label_encoder.pkl")

# # ---------------------------------------------------
# # Load Model, Tokenizer, and Label Encoder
# # ---------------------------------------------------
# tokenizer = BertTokenizerFast.from_pretrained(MODEL_DIR)
# model = BertForSequenceClassification.from_pretrained(MODEL_DIR)
# label_encoder = joblib.load(ENCODER_PATH)

# # IPC mapping for ML labels
# ipc_mapping = {
#     "Murder": "302",
#     "Theft": "378",
#     "Robbery": "392",
#     "Assault": "351",
#     "House Trespass": "442",
#     "Fraud":"IPC 323",
#     "Theft": "IPC 378",
#     "Murder": "IPC 302",
#     "Accident (Causing Death by Negligence)": "IPC 304A",
#     "Rape": "IPC 376",
#     "Cheating": "IPC 420",
#     "Kidnapping": "IPC 363",
#     "Robbery": "IPC 392",
#     "Dacoity": "IPC 395",
#     "Criminal Breach of Trust": "IPC 406",
#     "Extortion": "IPC 384",
#     "Defamation": "IPC 499",
#     "Dowry Death": "IPC 304B",
#     "Attempt to Murder": "IPC 307",
#     "Grievous Hurt": "IPC 325",
#     "House Trespass": "IPC 448",
#     "Forgery": "IPC 465",
#     "Rioting": "IPC 147",
#     "Unlawful Assembly": "IPC 141",
#     "Acid Attack": "IPC 326A",
#     "Cybercrime (Hacking)": "IPC 66 IT Act + IPC 379/420"
# }

# # Keyword-based dictionary
# keyword_map = {
#     "murder": {"label": "Murder", "ipc": "302"},
#     "kill": {"label": "Murder", "ipc": "302"},
#     "killed": {"label": "Murder", "ipc": "302"},
#     "homicide": {"label": "Murder", "ipc": "302"},
#     "theft": {"label": "Theft", "ipc": "378"},
#     "steal": {"label": "Theft", "ipc": "378"},
#     "stole": {"label": "Theft", "ipc": "378"},
#     "robbery": {"label": "Robbery", "ipc": "392"},
#     "robbed": {"label": "Robbery", "ipc": "392"},
#     "assault": {"label": "Assault", "ipc": "351"},
#     "attack": {"label": "Assault", "ipc": "351"},
#     "trespass": {"label": "House Trespass", "ipc": "442"},
#     "trespassed": {"label": "House Trespass", "ipc": "442"},
#     "break-in": {"label": "House Trespass", "ipc": "442"}
# }

# # ---------------------------------------------------
# # Create FastAPI app
# # ---------------------------------------------------
# app = FastAPI()

# # Input schema
# class TextInput(BaseModel):
#     text: str

# # ---------------------------------------------------
# # Prediction endpoint
# # ---------------------------------------------------
# @app.post("/predict")
# def predict(input_data: TextInput):
#     text = input_data.text.lower()

#     # --- ML Model prediction ---
#     inputs = tokenizer(text, return_tensors="pt", padding=True, truncation=True, max_length=512)
#     with torch.no_grad():
#         outputs = model(**inputs)
#         predictions = torch.argmax(outputs.logits, dim=-1).item()

#     primary_label = label_encoder.inverse_transform([predictions])[0]
#     primary_ipc = ipc_mapping.get(primary_label, "IPC Not Found")

#     # --- Keyword-based prediction ---
#     additional = []
#     for word, info in keyword_map.items():
#         if word in text:
#             additional.append({"crime": info["label"], "ipc": info["ipc"]})

#     # remove duplicate entries
#     additional = [dict(t) for t in {tuple(d.items()) for d in additional}]

#     return {
#         "text": input_data.text,
#         "primary_prediction": f"{primary_label} (IPC {primary_ipc})",
#         "additional_predictions": additional
#     }



# from fastapi import FastAPI
# from pydantic import BaseModel
# from transformers import BertTokenizerFast, BertForSequenceClassification
# import torch
# import joblib
# import os
# import mysql.connector
# from datetime import datetime

# # ---------------------------------------------------
# # Database connection setup
# # ---------------------------------------------------
# db = mysql.connector.connect(
#     host="localhost",
#     user="root",
#     password="koye20@%",   # 🔹 change to your MySQL password
#     database="crime_system"
# )
# cursor = db.cursor()

# # ---------------------------------------------------
# # Path setup for model + encoder
# # ---------------------------------------------------
# BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# MODEL_DIR = os.path.join(BASE_DIR, "crime_model")
# ENCODER_PATH = os.path.join(BASE_DIR, "label_encoder.pkl")

# # ---------------------------------------------------
# # Load Model and Label Encoder
# # ---------------------------------------------------
# tokenizer = BertTokenizerFast.from_pretrained(MODEL_DIR)
# model = BertForSequenceClassification.from_pretrained(MODEL_DIR)
# label_encoder = joblib.load(ENCODER_PATH)

# # ---------------------------------------------------
# # IPC mapping for ML labels
# # ---------------------------------------------------
# ipc_mapping = {
#     "Murder": "IPC 302",
#     "Theft": "IPC 378",
#     "Robbery": "IPC 392",
#     "Assault": "IPC 351",
#     "House Trespass": "IPC 442",
#     "Fraud": "IPC 323",
#     "Accident (Causing Death by Negligence)": "IPC 304A",
#     "Rape": "IPC 376",
#     "Cheating": "IPC 420",
#     "Kidnapping": "IPC 363",
#     "Dacoity": "IPC 395",
#     "Criminal Breach of Trust": "IPC 406",
#     "Extortion": "IPC 384",
#     "Defamation": "IPC 499",
#     "Dowry Death": "IPC 304B",
#     "Attempt to Murder": "IPC 307",
#     "Grievous Hurt": "IPC 325",
#     "House Trespass": "IPC 448",
#     "Forgery": "IPC 465",
#     "Rioting": "IPC 147",
#     "Unlawful Assembly": "IPC 141",
#     "Acid Attack": "IPC 326A",
#     "Cybercrime (Hacking)": "IPC 66 IT Act + IPC 379/420"
# }

# # ---------------------------------------------------
# # Keyword-based crime mapping
# # ---------------------------------------------------
# keyword_map = {
#     "murder": {"label": "Murder", "ipc": "IPC 302"},
#     "kill": {"label": "Murder", "ipc": "IPC 302"},
#     "killed": {"label": "Murder", "ipc": "IPC 302"},
#     "homicide": {"label": "Murder", "ipc": "IPC 302"},
#     "theft": {"label": "Theft", "ipc": "IPC 378"},
#     "steal": {"label": "Theft", "ipc": "IPC 378"},
#     "stole": {"label": "Theft", "ipc": "IPC 378"},
#     "robbery": {"label": "Robbery", "ipc": "IPC 392"},
#     "robbed": {"label": "Robbery", "ipc": "IPC 392"},
#     "assault": {"label": "Assault", "ipc": "IPC 351"},
#     "attack": {"label": "Assault", "ipc": "IPC 351"},
#     "trespass": {"label": "House Trespass", "ipc": "IPC 442"},
#     "trespassed": {"label": "House Trespass", "ipc": "IPC 442"},
#     "break-in": {"label": "House Trespass", "ipc": "IPC 442"},
# }

# # ---------------------------------------------------
# # FastAPI setup
# # ---------------------------------------------------
# app = FastAPI()

# # Input model for reports
# class ReportInput(BaseModel):
#     officer_id: int
#     place: str
#     location: str
#     city: str
#     country: str
#     description: str

# # ---------------------------------------------------
# # Helper: Keyword Detection
# # ---------------------------------------------------
# def detect_from_keywords(text: str):
#     text_lower = text.lower()
#     for word, info in keyword_map.items():
#         if word in text_lower:
#             return info["label"], info["ipc"]
#     return None, None

# # ---------------------------------------------------
# # Prediction and Storage Endpoint
# # ---------------------------------------------------
# @app.post("/predict")
# def predict_and_store(data: ReportInput):
#     # Try keyword-based detection first
#     keyword_label, keyword_ipc = detect_from_keywords(data.description)

#     if keyword_label:
#         predicted_label = keyword_label
#         ipc_code = keyword_ipc
#         detection_source = "keyword"
#     else:
#         # Fall back to ML model
#         inputs = tokenizer(data.description, return_tensors="pt", padding=True, truncation=True, max_length=512)
#         with torch.no_grad():
#             outputs = model(**inputs)
#             pred = torch.argmax(outputs.logits, dim=-1).item()
#         predicted_label = label_encoder.inverse_transform([pred])[0]
#         ipc_code = ipc_mapping.get(predicted_label, "Unknown")
#         detection_source = "ml_model"

#     # Insert prediction into MySQL
#     try:
#         query = """
#         INSERT INTO crime_reports 
#         (officer_id, date_time, place, location, city, country, description, crime_type, ipc_section)
#         VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
#         """
#         values = (
#             data.officer_id,
#             datetime.now(),
#             data.place,
#             data.location,
#             data.city,
#             data.country,
#             data.description,
#             predicted_label,
#             ipc_code
#         )
#         cursor.execute(query, values)
#         db.commit()
#     except Exception as e:
#         db.rollback()
#         return {"error": f"Database insertion failed: {e}"}

#     return {
#         "crime_type": predicted_label,
#         "ipc_section": ipc_code,
#         "detection_method": detection_source,
#         "message": "✅ Report classified and stored successfully!"
#     }

# @app.get("/")
# def root():
#     return {"message": "🚨 Crime Classification Hybrid API connected to MySQL!"}



# from fastapi import FastAPI
# from pydantic import BaseModel
# from transformers import BertTokenizerFast, BertForSequenceClassification
# import torch
# import joblib
# import os
# import mysql.connector
# from datetime import datetime

# # ---------------------------------------------------
# # Database connection setup
# # ---------------------------------------------------
# db = mysql.connector.connect(
#     host="localhost",
#     user="root",
#     password="koye20@%",   # 🔹 change to your MySQL password
#     database="crime_system"
# )
# cursor = db.cursor()

# # ---------------------------------------------------
# # Path setup for model + encoder
# # ---------------------------------------------------
# BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# MODEL_DIR = os.path.join(BASE_DIR, "crime_model")
# ENCODER_PATH = os.path.join(BASE_DIR, "label_encoder.pkl")

# # ---------------------------------------------------
# # Load Model and Label Encoder
# # ---------------------------------------------------
# tokenizer = BertTokenizerFast.from_pretrained(MODEL_DIR)
# model = BertForSequenceClassification.from_pretrained(MODEL_DIR)
# label_encoder = joblib.load(ENCODER_PATH)

# # ---------------------------------------------------
# # IPC mapping for ML labels
# # ---------------------------------------------------
# ipc_mapping = {
#     "Murder": "IPC 302",
#     "Theft": "IPC 378",
#     "Robbery": "IPC 392",
#     "Assault": "IPC 351",
#     "House Trespass": "IPC 442",
#     "Fraud": "IPC 323",
#     "Accident (Causing Death by Negligence)": "IPC 304A",
#     "Rape": "IPC 376",
#     "Cheating": "IPC 420",
#     "Kidnapping": "IPC 363",
#     "Dacoity": "IPC 395",
#     "Criminal Breach of Trust": "IPC 406",
#     "Extortion": "IPC 384",
#     "Defamation": "IPC 499",
#     "Dowry Death": "IPC 304B",
#     "Attempt to Murder": "IPC 307",
#     "Grievous Hurt": "IPC 325",
#     "House Trespass": "IPC 448",
#     "Forgery": "IPC 465",
#     "Rioting": "IPC 147",
#     "Unlawful Assembly": "IPC 141",
#     "Acid Attack": "IPC 326A",
#     "Cybercrime (Hacking)": "IPC 66 IT Act + IPC 379/420"
# }

# # ---------------------------------------------------
# # Keyword-based crime mapping
# # ---------------------------------------------------
# keyword_map = {
#     "murder": {"label": "Murder", "ipc": "IPC 302"},
#     "kill": {"label": "Murder", "ipc": "IPC 302"},
#     "killed": {"label": "Murder", "ipc": "IPC 302"},
#     "homicide": {"label": "Murder", "ipc": "IPC 302"},
#     "theft": {"label": "Theft", "ipc": "IPC 378"},
#     "steal": {"label": "Theft", "ipc": "IPC 378"},
#     "stole": {"label": "Theft", "ipc": "IPC 378"},
#     "robbery": {"label": "Robbery", "ipc": "IPC 392"},
#     "robbed": {"label": "Robbery", "ipc": "IPC 392"},
#     "assault": {"label": "Assault", "ipc": "IPC 351"},
#     "attack": {"label": "Assault", "ipc": "IPC 351"},
#     "trespass": {"label": "House Trespass", "ipc": "IPC 442"},
#     "trespassed": {"label": "House Trespass", "ipc": "IPC 442"},
#     "break-in": {"label": "House Trespass", "ipc": "IPC 442"},
# }

# # ---------------------------------------------------
# # FastAPI setup
# # ---------------------------------------------------
# app = FastAPI()

# # Input model for reports
# class ReportInput(BaseModel):
#     officer_id: int
#     place: str
#     location: str
#     city: str
#     country: str
#     description: str

# # ---------------------------------------------------
# # Helper: Keyword Detection
# # ---------------------------------------------------
# def detect_from_keywords(text: str):
#     text_lower = text.lower()
#     for word, info in keyword_map.items():
#         if word in text_lower:
#             return info["label"], info["ipc"]
#     return None, None

# # ---------------------------------------------------
# # Prediction and Storage Endpoint
# # ---------------------------------------------------
# @app.post("/predict")
# def predict_and_store(data: ReportInput):
#     # Try keyword-based detection first
#     keyword_label, keyword_ipc = detect_from_keywords(data.description)

#     if keyword_label:
#         predicted_label = keyword_label
#         ipc_code = keyword_ipc
#         detection_source = "keyword"
#     else:
#         # Fall back to ML model
#         inputs = tokenizer(data.description, return_tensors="pt", padding=True, truncation=True, max_length=512)
#         with torch.no_grad():
#             outputs = model(**inputs)
#             pred = torch.argmax(outputs.logits, dim=-1).item()
#         predicted_label = label_encoder.inverse_transform([pred])[0]
#         ipc_code = ipc_mapping.get(predicted_label, "Unknown")
#         detection_source = "ml_model"

#     # Insert prediction into MySQL
#     try:
#         query = """
#         INSERT INTO crime_reports 
#         (officer_id, date_time, place, location, city, country, description, crime_type, ipc_section)
#         VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
#         """
#         values = (
#             data.officer_id,
#             datetime.now(),
#             data.place,
#             data.location,
#             data.city,
#             data.country,
#             data.description,
#             predicted_label,
#             ipc_code
#         )
#         cursor.execute(query, values)
#         db.commit()
#     except Exception as e:
#         db.rollback()
#         return {"error": f"Database insertion failed: {e}"}

#     return {
#         "crime_type": predicted_label,
#         "ipc_section": ipc_code,
#         "detection_method": detection_source,
#         "message": "✅ Report classified and stored successfully!"
#     }

# @app.get("/")
# def root():
#     return {"message": "🚨 Crime Classification Hybrid API connected to MySQL!"}


 #1
# from fastapi import FastAPI
# from fastapi.middleware.cors import CORSMiddleware
# from pydantic import BaseModel
# from transformers import BertTokenizerFast, BertForSequenceClassification
# import torch
# import joblib
# import os
# import mysql.connector
# from datetime import datetime

# # ---------------------------------------------------
# # Database connection setup
# # ---------------------------------------------------
# db = mysql.connector.connect(
#     host="localhost",
#     user="root",
#     password="koye20@%",   # 🔹 change to your MySQL password
#     database="crime_system"
# )
# cursor = db.cursor()

# # ---------------------------------------------------
# # Path setup for model + encoder
# # ---------------------------------------------------
# BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# MODEL_DIR = os.path.join(BASE_DIR, "crime_model")
# ENCODER_PATH = os.path.join(BASE_DIR, "label_encoder.pkl")

# # ---------------------------------------------------
# # Load Model and Label Encoder
# # ---------------------------------------------------
# tokenizer = BertTokenizerFast.from_pretrained(MODEL_DIR)
# model = BertForSequenceClassification.from_pretrained(MODEL_DIR)
# label_encoder = joblib.load(ENCODER_PATH)

# # ---------------------------------------------------
# # IPC mapping for ML labels
# # ---------------------------------------------------
# ipc_mapping = {
#     "Murder": "IPC 302",
#     "Theft": "IPC 378",
#     "Robbery": "IPC 392",
#     "Assault": "IPC 351",
#     "House Trespass": "IPC 442",
#     "Fraud": "IPC 323",
#     "Accident (Causing Death by Negligence)": "IPC 304A",
#     "Rape": "IPC 376",
#     "Cheating": "IPC 420",
#     "Kidnapping": "IPC 363",
#     "Dacoity": "IPC 395",
#     "Criminal Breach of Trust": "IPC 406",
#     "Extortion": "IPC 384",
#     "Defamation": "IPC 499",
#     "Dowry Death": "IPC 304B",
#     "Attempt to Murder": "IPC 307",
#     "Grievous Hurt": "IPC 325",
#     "House Trespass": "IPC 448",
#     "Forgery": "IPC 465",
#     "Rioting": "IPC 147",
#     "Unlawful Assembly": "IPC 141",
#     "Acid Attack": "IPC 326A",
#     "Cybercrime (Hacking)": "IPC 66 IT Act + IPC 379/420"
# }

# # ---------------------------------------------------
# # Keyword-based crime mapping
# # ---------------------------------------------------
# keyword_map = {
#     "murder": {"label": "Murder", "ipc": "IPC 302"},
#     "kill": {"label": "Murder", "ipc": "IPC 302"},
#     "killed": {"label": "Murder", "ipc": "IPC 302"},
#     "homicide": {"label": "Murder", "ipc": "IPC 302"},
#     "theft": {"label": "Theft", "ipc": "IPC 378"},
#     "steal": {"label": "Theft", "ipc": "IPC 378"},
#     "stole": {"label": "Theft", "ipc": "IPC 378"},
#     "robbery": {"label": "Robbery", "ipc": "IPC 392"},
#     "robbed": {"label": "Robbery", "ipc": "IPC 392"},
#     "assault": {"label": "Assault", "ipc": "IPC 351"},
#     "attack": {"label": "Assault", "ipc": "IPC 351"},
#     "trespass": {"label": "House Trespass", "ipc": "IPC 442"},
#     "trespassed": {"label": "House Trespass", "ipc": "IPC 442"},
#     "break-in": {"label": "House Trespass", "ipc": "IPC 442"},
# }

# # ---------------------------------------------------
# # FastAPI setup + CORS fix
# # ---------------------------------------------------
# app = FastAPI()

# # ✅ Allow frontend + Node.js backend + local live server access
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],  # For development — you can restrict later
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# # ---------------------------------------------------
# # Input model for reports
# # ---------------------------------------------------
# class ReportInput(BaseModel):
#     officer_id: int
#     place: str
#     location: str
#     city: str
#     country: str
#     description: str

# # ---------------------------------------------------
# # Helper: Keyword Detection
# # ---------------------------------------------------
# def detect_from_keywords(text: str):
#     text_lower = text.lower()
#     for word, info in keyword_map.items():
#         if word in text_lower:
#             return info["label"], info["ipc"]
#     return None, None

# # ---------------------------------------------------
# # Prediction and Storage Endpoint
# # ---------------------------------------------------
# @app.post("/predict")
# def predict_and_store(data: ReportInput):
#     # Try keyword-based detection first
#     keyword_label, keyword_ipc = detect_from_keywords(data.description)

#     if keyword_label:
#         predicted_label = keyword_label
#         ipc_code = keyword_ipc
#         detection_source = "keyword"
#     else:
#         # Fall back to ML model
#         inputs = tokenizer(data.description, return_tensors="pt", padding=True, truncation=True, max_length=512)
#         with torch.no_grad():
#             outputs = model(**inputs)
#             pred = torch.argmax(outputs.logits, dim=-1).item()
#         predicted_label = label_encoder.inverse_transform([pred])[0]
#         ipc_code = ipc_mapping.get(predicted_label, "Unknown")
#         detection_source = "ml_model"

#     # Insert prediction into MySQL
#     try:
#         query = """
#         INSERT INTO crime_reports 
#         (officer_id, date_time, place, location, city, country, description, crime_type, ipc_section)
#         VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
#         """
#         values = (
#             data.officer_id,
#             datetime.now(),
#             data.place,
#             data.location,
#             data.city,
#             data.country,
#             data.description,
#             predicted_label,
#             ipc_code
#         )
#         cursor.execute(query, values)
#         db.commit()
#     except Exception as e:
#         db.rollback()
#         return {"error": f"Database insertion failed: {e}"}

#     return {
#         "crime_type": predicted_label,
#         "ipc_section": ipc_code,
#         "detection_method": detection_source,
#         "message": "✅ Report classified and stored successfully!"
#     }

# # ---------------------------------------------------
# # Health Check Endpoint
# # ---------------------------------------------------
# @app.get("/")
# def root():
#     return {"message": "🚨 Crime Classification Hybrid API connected to MySQL and ready!"}




# from fastapi import FastAPI
# from fastapi.middleware.cors import CORSMiddleware
# from pydantic import BaseModel
# from transformers import BertTokenizerFast, BertForSequenceClassification
# import torch
# import joblib
# import os
# import mysql.connector
# from datetime import datetime
# from contextlib import asynccontextmanager

# # ---------------------------------------------------
# # Database connection setup (will be initialized in lifespan)
# # ---------------------------------------------------
# db = None
# cursor = None

# # ---------------------------------------------------
# # Path setup for model + encoder
# # ---------------------------------------------------
# BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# MODEL_DIR = os.path.join(BASE_DIR, "crime_model")
# ENCODER_PATH = os.path.join(BASE_DIR, "label_encoder.pkl")

# # ---------------------------------------------------
# # Load Model and Label Encoder
# # ---------------------------------------------------
# tokenizer = BertTokenizerFast.from_pretrained(MODEL_DIR)
# model = BertForSequenceClassification.from_pretrained(MODEL_DIR)
# label_encoder = joblib.load(ENCODER_PATH)

# # ---------------------------------------------------
# # IPC mapping for ML labels
# # ---------------------------------------------------
# ipc_mapping = {
#     "Murder": "IPC 302",
#     "Theft": "IPC 378",
#     "Robbery": "IPC 392",
#     "Assault": "IPC 351",
#     "House Trespass": "IPC 442",
#     "Fraud": "IPC 323",
#     "Accident (Causing Death by Negligence)": "IPC 304A",
#     "Rape": "IPC 376",
#     "Cheating": "IPC 420",
#     "Kidnapping": "IPC 363",
#     "Dacoity": "IPC 395",
#     "Criminal Breach of Trust": "IPC 406",
#     "Extortion": "IPC 384",
#     "Defamation": "IPC 499",
#     "Dowry Death": "IPC 304B",
#     "Attempt to Murder": "IPC 307",
#     "Grievous Hurt": "IPC 325",
#     "Forgery": "IPC 465",
#     "Rioting": "IPC 147",
#     "Unlawful Assembly": "IPC 141",
#     "Acid Attack": "IPC 326A",
#     "Cybercrime (Hacking)": "IPC 66 IT Act + IPC 379/420"
# }

# # ---------------------------------------------------
# # Keyword-based crime mapping
# # ---------------------------------------------------
# keyword_map = {
#     "murder": {"label": "Murder", "ipc": "IPC 302"},
#     "kill": {"label": "Murder", "ipc": "IPC 302"},
#     "killed": {"label": "Murder", "ipc": "IPC 302"},
#     "homicide": {"label": "Murder", "ipc": "IPC 302"},
#     "theft": {"label": "Theft", "ipc": "IPC 378"},
#     "steal": {"label": "Theft", "ipc": "IPC 378"},
#     "stole": {"label": "Theft", "ipc": "IPC 378"},
#     "robbery": {"label": "Robbery", "ipc": "IPC 392"},
#     "robbed": {"label": "Robbery", "ipc": "IPC 392"},
#     "assault": {"label": "Assault", "ipc": "IPC 351"},
#     "attack": {"label": "Assault", "ipc": "IPC 351"},
#     "trespass": {"label": "House Trespass", "ipc": "IPC 442"},
#     "trespassed": {"label": "House Trespass", "ipc": "IPC 442"},
#     "break-in": {"label": "House Trespass", "ipc": "IPC 442"},
# }

# # ---------------------------------------------------
# # Lifespan Event Handler (Modern approach)
# # ---------------------------------------------------
# @asynccontextmanager
# async def lifespan(app: FastAPI):
#     """
#     Lifespan event handler for startup and shutdown.
#     Replaces deprecated @app.on_event() decorators.
#     """
#     # Startup
#     global db, cursor
    
#     print("=" * 60)
#     print("🚨 Crime Classification ML API Starting...")
#     print("=" * 60)
    
#     # Initialize database connection
#     try:
#         db = mysql.connector.connect(
#             host="localhost",
#             user="root",
#             password="koye20@%",
#             database="crime_system"
#         )
#         cursor = db.cursor()
#         print(f"✅ Database connected: {db.is_connected()}")
#     except Exception as e:
#         print(f"⚠️  Database connection failed: {e}")
#         print("   Continuing without database (predict endpoint will still work)")
    
#     print(f"✅ Model loaded from: {MODEL_DIR}")
#     print(f"✅ Label encoder loaded from: {ENCODER_PATH}")
#     print(f"✅ Total crime types supported: {len(ipc_mapping)}")
#     print(f"✅ Total keywords mapped: {len(keyword_map)}")
#     print("=" * 60)
#     print("📡 API Endpoints:")
#     print("   - POST /predict              : Simple crime prediction")
#     print("   - POST /predict_and_store    : Predict + save to DB")
#     print("   - POST /batch_predict        : Batch predictions")
#     print("   - GET  /                     : Service info")
#     print("   - GET  /health               : Health check")
#     print("   - GET  /stats                : Crime statistics")
#     print("   - GET  /ipc_codes            : List all IPC codes")
#     print("=" * 60)
#     print("🚀 Server ready at http://127.0.0.1:8000")
#     print("📚 API docs at http://127.0.0.1:8000/docs")
#     print("=" * 60)
    
#     yield  # Application runs here
    
#     # Shutdown
#     print("\n" + "=" * 60)
#     print("🛑 Shutting down Crime Classification ML API...")
#     if db and db.is_connected():
#         cursor.close()
#         db.close()
#         print("✅ Database connection closed")
#     print("=" * 60)

# # ---------------------------------------------------
# # FastAPI setup with CORS and Lifespan
# # ---------------------------------------------------
# app = FastAPI(
#     title="Crime Classification ML API",
#     description="AI-powered crime classification system with IPC code mapping",
#     version="2.0.0",
#     lifespan=lifespan
# )

# # ✅ CRITICAL: Add CORS middleware to allow cross-origin requests
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],  # Allow all origins (restrict in production)
#     allow_credentials=True,
#     allow_methods=["*"],  # Allow all HTTP methods (GET, POST, OPTIONS, etc.)
#     allow_headers=["*"],  # Allow all headers
# )

# # ---------------------------------------------------
# # Input models
# # ---------------------------------------------------
# class PredictionInput(BaseModel):
#     description: str

# class ReportInput(BaseModel):
#     officer_id: int
#     place: str
#     location: str
#     city: str
#     country: str
#     description: str

# # ---------------------------------------------------
# # Helper: Keyword Detection
# # ---------------------------------------------------
# def detect_from_keywords(text: str):
#     text_lower = text.lower()
#     for word, info in keyword_map.items():
#         if word in text_lower:
#             return info["label"], info["ipc"]
#     return None, None

# # ---------------------------------------------------
# # Health Check Endpoint
# # ---------------------------------------------------
# @app.get("/")
# def root():
#     return {
#         "message": "🚨 Crime Classification ML API is running!",
#         "status": "online",
#         "endpoints": ["/predict", "/predict_and_store"]
#     }

# # ---------------------------------------------------
# # Simple Prediction Endpoint (no DB storage)
# # ---------------------------------------------------
# @app.post("/predict")
# def predict(data: PredictionInput):
#     """
#     Simple prediction endpoint that only returns crime classification.
#     Used by Node.js backend.
#     """
#     try:
#         # Try keyword-based detection first
#         keyword_label, keyword_ipc = detect_from_keywords(data.description)

#         if keyword_label:
#             predicted_label = keyword_label
#             ipc_code = keyword_ipc
#             detection_source = "keyword"
#         else:
#             # Fall back to ML model
#             inputs = tokenizer(
#                 data.description, 
#                 return_tensors="pt", 
#                 padding=True, 
#                 truncation=True, 
#                 max_length=512
#             )
#             with torch.no_grad():
#                 outputs = model(**inputs)
#                 pred = torch.argmax(outputs.logits, dim=-1).item()
            
#             predicted_label = label_encoder.inverse_transform([pred])[0]
#             ipc_code = ipc_mapping.get(predicted_label, "Unknown")
#             detection_source = "ml_model"

#         return {
#             "crime_type": predicted_label,
#             "ipc_section": ipc_code,
#             "detection_method": detection_source,
#             "success": True
#         }

#     except Exception as e:
#         return {
#             "error": str(e),
#             "crime_type": "Unknown",
#             "ipc_section": "Unknown",
#             "success": False
#         }

# # ---------------------------------------------------
# # Prediction and Storage Endpoint (direct DB access)
# # ---------------------------------------------------
# @app.post("/predict_and_store")
# def predict_and_store(data: ReportInput):
#     """
#     Alternative endpoint that handles both prediction and database storage.
#     Can be used if bypassing Node.js backend.
#     """
#     if not db or not db.is_connected():
#         return {
#             "success": False,
#             "error": "Database not connected. Use /predict endpoint for prediction only."
#         }
    
#     try:
#         # Try keyword-based detection first
#         keyword_label, keyword_ipc = detect_from_keywords(data.description)

#         if keyword_label:
#             predicted_label = keyword_label
#             ipc_code = keyword_ipc
#             detection_source = "keyword"
#         else:
#             # Fall back to ML model
#             inputs = tokenizer(
#                 data.description, 
#                 return_tensors="pt", 
#                 padding=True, 
#                 truncation=True, 
#                 max_length=512
#             )
#             with torch.no_grad():
#                 outputs = model(**inputs)
#                 pred = torch.argmax(outputs.logits, dim=-1).item()
            
#             predicted_label = label_encoder.inverse_transform([pred])[0]
#             ipc_code = ipc_mapping.get(predicted_label, "Unknown")
#             detection_source = "ml_model"

#         # Insert prediction into MySQL
#         query = """
#         INSERT INTO crime_reports 
#         (officer_id, date_time, place, location, city, country, description, crime_type, ipc_section)
#         VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
#         """
#         values = (
#             data.officer_id,
#             datetime.now(),
#             data.place,
#             data.location,
#             data.city,
#             data.country,
#             data.description,
#             predicted_label,
#             ipc_code
#         )
#         cursor.execute(query, values)
#         db.commit()

#         return {
#             "crime_type": predicted_label,
#             "ipc_section": ipc_code,
#             "detection_method": detection_source,
#             "message": "✅ Report classified and stored successfully!",
#             "success": True
#         }

#     except Exception as e:
#         db.rollback()
#         return {
#             "error": f"Database insertion failed: {e}",
#             "success": False
#         }

# # ===============================
# #  Additional Utility Endpoints
# # ===============================

# @app.get("/health")
# def health_check():
#     """Health check endpoint for monitoring"""
#     db_status = "not_connected"
    
#     try:
#         if db and db.is_connected():
#             cursor.execute("SELECT 1")
#             db_status = "connected"
#     except Exception as e:
#         db_status = f"error: {str(e)}"
    
#     return {
#         "status": "online",
#         "service": "Crime Classification ML API",
#         "database": db_status,
#         "model_loaded": model is not None,
#         "endpoints": {
#             "predict": "/predict",
#             "predict_and_store": "/predict_and_store",
#             "health": "/health",
#             "stats": "/stats"
#         }
#     }

# @app.get("/stats")
# def get_ml_stats():
#     """Get statistics about crime classifications"""
#     if not db or not db.is_connected():
#         return {
#             "success": False,
#             "error": "Database not connected"
#         }
    
#     try:
#         query = """
#         SELECT 
#             crime_type, 
#             COUNT(*) as count,
#             DATE(date_time) as date
#         FROM crime_reports 
#         WHERE date_time >= DATE_SUB(NOW(), INTERVAL 30 DAY)
#         GROUP BY crime_type, DATE(date_time)
#         ORDER BY date DESC, count DESC
#         """
#         cursor.execute(query)
#         results = cursor.fetchall()
        
#         # Process results
#         stats = {}
#         for row in results:
#             crime_type = row[0]
#             count = row[1]
#             date = str(row[2])
            
#             if crime_type not in stats:
#                 stats[crime_type] = {"total": 0, "by_date": {}}
            
#             stats[crime_type]["total"] += count
#             stats[crime_type]["by_date"][date] = count
        
#         return {
#             "success": True,
#             "period": "Last 30 days",
#             "statistics": stats
#         }
    
#     except Exception as e:
#         return {
#             "success": False,
#             "error": str(e)
#         }

# @app.post("/batch_predict")
# def batch_predict(descriptions: list[str]):
#     """
#     Predict crime types for multiple descriptions at once.
#     Useful for bulk processing or testing.
#     """
#     try:
#         results = []
        
#         for description in descriptions:
#             # Try keyword detection first
#             keyword_label, keyword_ipc = detect_from_keywords(description)
            
#             if keyword_label:
#                 results.append({
#                     "description": description[:50] + "..." if len(description) > 50 else description,
#                     "crime_type": keyword_label,
#                     "ipc_section": keyword_ipc,
#                     "detection_method": "keyword"
#                 })
#             else:
#                 # Use ML model
#                 inputs = tokenizer(
#                     description, 
#                     return_tensors="pt", 
#                     padding=True, 
#                     truncation=True, 
#                     max_length=512
#                 )
#                 with torch.no_grad():
#                     outputs = model(**inputs)
#                     pred = torch.argmax(outputs.logits, dim=-1).item()
                
#                 predicted_label = label_encoder.inverse_transform([pred])[0]
#                 ipc_code = ipc_mapping.get(predicted_label, "Unknown")
                
#                 results.append({
#                     "description": description[:50] + "..." if len(description) > 50 else description,
#                     "crime_type": predicted_label,
#                     "ipc_section": ipc_code,
#                     "detection_method": "ml_model"
#                 })
        
#         return {
#             "success": True,
#             "total_processed": len(results),
#             "predictions": results
#         }
    
#     except Exception as e:
#         return {
#             "success": False,
#             "error": str(e)
#         }

# @app.get("/ipc_codes")
# def get_ipc_codes():
#     """Return all supported IPC codes and their crime types"""
#     return {
#         "success": True,
#         "ipc_mapping": ipc_mapping,
#         "keyword_map": {k: v for k, v in keyword_map.items()},
#         "total_crime_types": len(ipc_mapping)
#     }

# # ===============================
# #  Error Handlers
# # ===============================

# @app.exception_handler(Exception)
# async def global_exception_handler(request, exc):
#     """Global exception handler for unhandled errors"""
#     return {
#         "success": False,
#         "error": "Internal server error",
#         "details": str(exc),
#         "path": str(request.url)
#     }

# # ===============================
# #  Startup Event
# # ===============================

# @app.on_event("startup")
# async def startup_event():
#     """Run on application startup"""
#     print("=" * 60)
#     print("🚨 Crime Classification ML API Starting...")
#     print("=" * 60)
#     print(f"✅ Model loaded from: {MODEL_DIR}")
#     print(f"✅ Label encoder loaded from: {ENCODER_PATH}")
#     print(f"✅ Database connected: {db.is_connected()}")
#     print(f"✅ Total crime types supported: {len(ipc_mapping)}")
#     print(f"✅ Total keywords mapped: {len(keyword_map)}")
#     print("=" * 60)
#     print("📡 API Endpoints:")
#     print("   - POST /predict              : Simple crime prediction")
#     print("   - POST /predict_and_store    : Predict + save to DB")
#     print("   - POST /batch_predict        : Batch predictions")
#     print("   - GET  /                     : Service info")
#     print("   - GET  /health               : Health check")
#     print("   - GET  /stats                : Crime statistics")
#     print("   - GET  /ipc_codes            : List all IPC codes")
#     print("=" * 60)
#     print("🚀 Server ready at http://127.0.0.1:8000")
#     print("📚 API docs at http://127.0.0.1:8000/docs")
#     print("=" * 60)

# @app.on_event("shutdown")
# async def shutdown_event():
#     """Run on application shutdown"""
#     print("🛑 Shutting down Crime Classification ML API...")
#     if db.is_connected():
#         cursor.close()
#         db.close()
#         print("✅ Database connection closed")

# # ===============================
# #  Run Instructions
# # ===============================
# # To run this application:
# # 1. Ensure all dependencies are installed:
# #    pip install fastapi uvicorn transformers torch mysql-connector-python joblib
# #
# # 2. Make sure MySQL is running and crime_system database exists
# #
# # 3. Start the server:
# #    uvicorn app:app --reload --port 8000 --host 0.0.0.0
# #
# # 4. Access API documentation:
# #    http://127.0.0.1:8000/docs
# #
# # 5. Test the API:
# #    curl -X POST http://127.0.0.1:8000/predict \
# #      -H "Content-Type: application/json" \
# #      -d '{"description": "A theft occurred at the store"}'
# # ===============================



# from fastapi import FastAPI
# from fastapi.middleware.cors import CORSMiddleware
# from pydantic import BaseModel
# from transformers import BertTokenizerFast, BertForSequenceClassification
# import torch
# import joblib
# import os
# import mysql.connector
# from datetime import datetime
# from contextlib import asynccontextmanager

# # ---------------------------------------------------
# # Database connection setup (will be initialized in lifespan)
# # ---------------------------------------------------
# db = None
# cursor = None

# # ---------------------------------------------------
# # Path setup for model + encoder
# # ---------------------------------------------------
# BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# MODEL_DIR = os.path.join(BASE_DIR, "crime_model")
# ENCODER_PATH = os.path.join(BASE_DIR, "label_encoder.pkl")

# # ---------------------------------------------------
# # Load Model and Label Encoder
# # ---------------------------------------------------
# tokenizer = BertTokenizerFast.from_pretrained(MODEL_DIR)
# model = BertForSequenceClassification.from_pretrained(MODEL_DIR)
# label_encoder = joblib.load(ENCODER_PATH)

# # ---------------------------------------------------
# # IPC mapping for ML labels
# # ---------------------------------------------------
# ipc_mapping = {
#     "Murder": "IPC 302",
#     "Theft": "IPC 378",
#     "Robbery": "IPC 392",
#     "Assault": "IPC 351",
#     "House Trespass": "IPC 442",
#     "Fraud": "IPC 323",
#     "Accident (Causing Death by Negligence)": "IPC 304A",
#     "Rape": "IPC 376",
#     "Cheating": "IPC 420",
#     "Kidnapping": "IPC 363",
#     "Dacoity": "IPC 395",
#     "Criminal Breach of Trust": "IPC 406",
#     "Extortion": "IPC 384",
#     "Defamation": "IPC 499",
#     "Dowry Death": "IPC 304B",
#     "Attempt to Murder": "IPC 307",
#     "Grievous Hurt": "IPC 325",
#     "Forgery": "IPC 465",
#     "Rioting": "IPC 147",
#     "Unlawful Assembly": "IPC 141",
#     "Acid Attack": "IPC 326A",
#     "Cybercrime (Hacking)": "IPC 66 IT Act + IPC 379/420"
# }

# # ---------------------------------------------------
# # Keyword-based crime mapping
# # ---------------------------------------------------
# keyword_map = {
#     "murder": {"label": "Murder", "ipc": "IPC 302"},
#     "kill": {"label": "Murder", "ipc": "IPC 302"},
#     "killed": {"label": "Murder", "ipc": "IPC 302"},
#     "homicide": {"label": "Murder", "ipc": "IPC 302"},
#     "theft": {"label": "Theft", "ipc": "IPC 378"},
#     "steal": {"label": "Theft", "ipc": "IPC 378"},
#     "stole": {"label": "Theft", "ipc": "IPC 378"},
#     "robbery": {"label": "Robbery", "ipc": "IPC 392"},
#     "robbed": {"label": "Robbery", "ipc": "IPC 392"},
#     "acid": {"label": "Acid Attack", "ipc": "IPC 326A"},
#     "assault": {"label": "Assault", "ipc": "IPC 351"},
#     "attack": {"label": "Assault", "ipc": "IPC 351"},
#     "trespass": {"label": "House Trespass", "ipc": "IPC 442"},
#     "trespassed": {"label": "House Trespass", "ipc": "IPC 442"},
#     "break-in": {"label": "House Trespass", "ipc": "IPC 442"},
# }

# # ---------------------------------------------------
# # Lifespan Event Handler (Modern approach)
# # ---------------------------------------------------
# @asynccontextmanager
# async def lifespan(app: FastAPI):
#     """
#     Lifespan event handler for startup and shutdown.
#     Replaces deprecated @app.on_event() decorators.
#     """
#     # Startup
#     global db, cursor
    
#     print("=" * 60)
#     print("🚨 Crime Classification ML API Starting...")
#     print("=" * 60)
    
#     # Initialize database connection
#     try:
#         db = mysql.connector.connect(
#             host="localhost",
#             user="root",
#             password="koye20@%",
#             database="crime_system"
#         )
#         cursor = db.cursor()
#         print(f"✅ Database connected: {db.is_connected()}")
#     except Exception as e:
#         print(f"⚠️  Database connection failed: {e}")
#         print("   Continuing without database (predict endpoint will still work)")
    
#     print(f"✅ Model loaded from: {MODEL_DIR}")
#     print(f"✅ Label encoder loaded from: {ENCODER_PATH}")
#     print(f"✅ Total crime types supported: {len(ipc_mapping)}")
#     print(f"✅ Total keywords mapped: {len(keyword_map)}")
#     print("=" * 60)
#     print("📡 API Endpoints:")
#     print("   - POST /predict              : Simple crime prediction")
#     print("   - POST /predict_and_store    : Predict + save to DB")
#     print("   - POST /batch_predict        : Batch predictions")
#     print("   - GET  /                     : Service info")
#     print("   - GET  /health               : Health check")
#     print("   - GET  /stats                : Crime statistics")
#     print("   - GET  /ipc_codes            : List all IPC codes")
#     print("=" * 60)
#     print("🚀 Server ready at http://127.0.0.1:8000")
#     print("📚 API docs at http://127.0.0.1:8000/docs")
#     print("=" * 60)
    
#     yield  # Application runs here
    
#     # Shutdown
#     print("\n" + "=" * 60)
#     print("🛑 Shutting down Crime Classification ML API...")
#     if db and db.is_connected():
#         cursor.close()
#         db.close()
#         print("✅ Database connection closed")
#     print("=" * 60)

# # ---------------------------------------------------
# # FastAPI setup with CORS and Lifespan
# # ---------------------------------------------------
# app = FastAPI(
#     title="Crime Classification ML API",
#     description="AI-powered crime classification system with IPC code mapping",
#     version="2.0.0",
#     lifespan=lifespan
# )

# # ✅ CRITICAL: Add CORS middleware to allow cross-origin requests
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],  # Allow all origins (restrict in production)
#     allow_credentials=True,
#     allow_methods=["*"],  # Allow all HTTP methods (GET, POST, OPTIONS, etc.)
#     allow_headers=["*"],  # Allow all headers
# )

# # ---------------------------------------------------
# # Input models
# # ---------------------------------------------------
# class PredictionInput(BaseModel):
#     description: str

# class ReportInput(BaseModel):
#     officer_id: int
#     place: str
#     location: str
#     city: str
#     country: str
#     description: str

# # ---------------------------------------------------
# # Helper: Multiple Crime Detection from Keywords
# # ---------------------------------------------------
# def detect_from_keywords(text: str):
#     """
#     Detect ALL matching crimes from keywords in the text.
#     Returns tuple of (list of labels, list of IPC codes) or (None, None) if no matches.
#     """
#     text_lower = text.lower()
#     detected_crimes = {}  # Use dict to avoid duplicates
    
#     for word, info in keyword_map.items():
#         if word in text_lower:
#             crime_label = info["label"]
#             # Avoid duplicate crime types (e.g., "murder" and "killed" both map to Murder)
#             if crime_label not in detected_crimes:
#                 detected_crimes[crime_label] = info["ipc"]
    
#     if detected_crimes:
#         labels = list(detected_crimes.keys())
#         ipcs = list(detected_crimes.values())
#         return labels, ipcs
    
#     return None, None

# # ---------------------------------------------------
# # Health Check Endpoint
# # ---------------------------------------------------
# @app.get("/")
# def root():
#     return {
#         "message": "🚨 Crime Classification ML API is running!",
#         "status": "online",
#         "endpoints": ["/predict", "/predict_and_store"],
#         "features": ["Multi-crime detection", "Keyword + ML hybrid", "IPC code mapping"]
#     }

# # ---------------------------------------------------
# # Simple Prediction Endpoint (no DB storage)
# # ---------------------------------------------------
# @app.post("/predict")
# def predict(data: PredictionInput):
#     """
#     Simple prediction endpoint that only returns crime classification.
#     Supports multiple crime detection from keywords.
#     Used by Node.js backend.
#     """
#     try:
#         # Try keyword-based detection first (now returns multiple matches)
#         keyword_labels, keyword_ipcs = detect_from_keywords(data.description)

#         if keyword_labels:
#             # Multiple crimes detected via keywords
#             predicted_label = ", ".join(keyword_labels)
#             ipc_code = ", ".join(keyword_ipcs)
#             detection_source = "keyword"
#             crime_count = len(keyword_labels)
#         else:
#             # Fall back to ML model (single prediction)
#             inputs = tokenizer(
#                 data.description, 
#                 return_tensors="pt", 
#                 padding=True, 
#                 truncation=True, 
#                 max_length=512
#             )
#             with torch.no_grad():
#                 outputs = model(**inputs)
#                 pred = torch.argmax(outputs.logits, dim=-1).item()
            
#             predicted_label = label_encoder.inverse_transform([pred])[0]
#             ipc_code = ipc_mapping.get(predicted_label, "Unknown")
#             detection_source = "ml_model"
#             crime_count = 1

#         return {
#             "crime_type": predicted_label,
#             "ipc_section": ipc_code,
#             "detection_method": detection_source,
#             "crime_count": crime_count,
#             "success": True
#         }

#     except Exception as e:
#         return {
#             "error": str(e),
#             "crime_type": "Unknown",
#             "ipc_section": "Unknown",
#             "success": False
#         }

# # ---------------------------------------------------
# # Prediction and Storage Endpoint (direct DB access)
# # ---------------------------------------------------
# @app.post("/predict_and_store")
# def predict_and_store(data: ReportInput):
#     """
#     Alternative endpoint that handles both prediction and database storage.
#     Supports multiple crime detection and stores them as comma-separated values.
#     Can be used if bypassing Node.js backend.
#     """
#     if not db or not db.is_connected():
#         return {
#             "success": False,
#             "error": "Database not connected. Use /predict endpoint for prediction only."
#         }
    
#     try:
#         # Try keyword-based detection first (now returns multiple matches)
#         keyword_labels, keyword_ipcs = detect_from_keywords(data.description)

#         if keyword_labels:
#             # Multiple crimes detected via keywords
#             predicted_label = ", ".join(keyword_labels)
#             ipc_code = ", ".join(keyword_ipcs)
#             detection_source = "keyword"
#             crime_count = len(keyword_labels)
#         else:
#             # Fall back to ML model (single prediction)
#             inputs = tokenizer(
#                 data.description, 
#                 return_tensors="pt", 
#                 padding=True, 
#                 truncation=True, 
#                 max_length=512
#             )
#             with torch.no_grad():
#                 outputs = model(**inputs)
#                 pred = torch.argmax(outputs.logits, dim=-1).item()
            
#             predicted_label = label_encoder.inverse_transform([pred])[0]
#             ipc_code = ipc_mapping.get(predicted_label, "Unknown")
#             detection_source = "ml_model"
#             crime_count = 1

#         # Insert prediction into MySQL (comma-separated for multiple crimes)
#         query = """
#         INSERT INTO crime_reports 
#         (officer_id, date_time, place, location, city, country, description, crime_type, ipc_section)
#         VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
#         """
#         values = (
#             data.officer_id,
#             datetime.now(),
#             data.place,
#             data.location,
#             data.city,
#             data.country,
#             data.description,
#             predicted_label,  # Comma-separated if multiple
#             ipc_code          # Comma-separated if multiple
#         )
#         cursor.execute(query, values)
#         db.commit()

#         return {
#             "crime_type": predicted_label,
#             "ipc_section": ipc_code,
#             "detection_method": detection_source,
#             "crime_count": crime_count,
#             "message": "✅ Report classified and stored successfully!",
#             "success": True
#         }

#     except Exception as e:
#         db.rollback()
#         return {
#             "error": f"Database insertion failed: {e}",
#             "success": False
#         }

# # ===============================
# #  Additional Utility Endpoints
# # ===============================

# @app.get("/health")
# def health_check():
#     """Health check endpoint for monitoring"""
#     db_status = "not_connected"
    
#     try:
#         if db and db.is_connected():
#             cursor.execute("SELECT 1")
#             db_status = "connected"
#     except Exception as e:
#         db_status = f"error: {str(e)}"
    
#     return {
#         "status": "online",
#         "service": "Crime Classification ML API",
#         "database": db_status,
#         "model_loaded": model is not None,
#         "features": {
#             "multi_crime_detection": True,
#             "keyword_detection": True,
#             "ml_fallback": True
#         },
#         "endpoints": {
#             "predict": "/predict",
#             "predict_and_store": "/predict_and_store",
#             "health": "/health",
#             "stats": "/stats"
#         }
#     }

# @app.get("/stats")
# def get_ml_stats():
#     """Get statistics about crime classifications"""
#     if not db or not db.is_connected():
#         return {
#             "success": False,
#             "error": "Database not connected"
#         }
    
#     try:
#         query = """
#         SELECT 
#             crime_type, 
#             COUNT(*) as count,
#             DATE(date_time) as date
#         FROM crime_reports 
#         WHERE date_time >= DATE_SUB(NOW(), INTERVAL 30 DAY)
#         GROUP BY crime_type, DATE(date_time)
#         ORDER BY date DESC, count DESC
#         """
#         cursor.execute(query)
#         results = cursor.fetchall()
        
#         # Process results
#         stats = {}
#         for row in results:
#             crime_type = row[0]
#             count = row[1]
#             date = str(row[2])
            
#             if crime_type not in stats:
#                 stats[crime_type] = {"total": 0, "by_date": {}}
            
#             stats[crime_type]["total"] += count
#             stats[crime_type]["by_date"][date] = count
        
#         return {
#             "success": True,
#             "period": "Last 30 days",
#             "statistics": stats
#         }
    
#     except Exception as e:
#         return {
#             "success": False,
#             "error": str(e)
#         }

# @app.post("/batch_predict")
# def batch_predict(descriptions: list[str]):
#     """
#     Predict crime types for multiple descriptions at once.
#     Supports multiple crime detection per description.
#     Useful for bulk processing or testing.
#     """
#     try:
#         results = []
        
#         for description in descriptions:
#             # Try keyword detection first (now returns multiple matches)
#             keyword_labels, keyword_ipcs = detect_from_keywords(description)
            
#             if keyword_labels:
#                 results.append({
#                     "description": description[:50] + "..." if len(description) > 50 else description,
#                     "crime_type": ", ".join(keyword_labels),
#                     "ipc_section": ", ".join(keyword_ipcs),
#                     "detection_method": "keyword",
#                     "crime_count": len(keyword_labels)
#                 })
#             else:
#                 # Use ML model
#                 inputs = tokenizer(
#                     description, 
#                     return_tensors="pt", 
#                     padding=True, 
#                     truncation=True, 
#                     max_length=512
#                 )
#                 with torch.no_grad():
#                     outputs = model(**inputs)
#                     pred = torch.argmax(outputs.logits, dim=-1).item()
                
#                 predicted_label = label_encoder.inverse_transform([pred])[0]
#                 ipc_code = ipc_mapping.get(predicted_label, "Unknown")
                
#                 results.append({
#                     "description": description[:50] + "..." if len(description) > 50 else description,
#                     "crime_type": predicted_label,
#                     "ipc_section": ipc_code,
#                     "detection_method": "ml_model",
#                     "crime_count": 1
#                 })
        
#         return {
#             "success": True,
#             "total_processed": len(results),
#             "predictions": results
#         }
    
#     except Exception as e:
#         return {
#             "success": False,
#             "error": str(e)
#         }

# @app.get("/ipc_codes")
# def get_ipc_codes():
#     """Return all supported IPC codes and their crime types"""
#     return {
#         "success": True,
#         "ipc_mapping": ipc_mapping,
#         "keyword_map": {k: v for k, v in keyword_map.items()},
#         "total_crime_types": len(ipc_mapping)
#     }

# # ===============================
# #  Error Handlers
# # ===============================

# @app.exception_handler(Exception)
# async def global_exception_handler(request, exc):
#     """Global exception handler for unhandled errors"""
#     return {
#         "success": False,
#         "error": "Internal server error",
#         "details": str(exc),
#         "path": str(request.url)
#     }

# # ===============================
# #  Run Instructions
# # ===============================
# # To run this application:
# # 1. Ensure all dependencies are installed:
# #    pip install fastapi uvicorn transformers torch mysql-connector-python joblib
# #
# # 2. Make sure MySQL is running and crime_system database exists
# #
# # 3. Start the server:
# #    uvicorn app:app --reload --port 8000 --host 0.0.0.0
# #
# # 4. Access API documentation:
# #    http://127.0.0.1:8000/docs
# #
# # 5. Test multi-crime detection:
# #    curl -X POST http://127.0.0.1:8000/predict \
# #      -H "Content-Type: application/json" \
# #      -d '{"description": "There was a murder and theft at the bank"}'
# #
# #    Expected response:
# #    {
# #      "crime_type": "Murder, Theft",
# #      "ipc_section": "IPC 302, IPC 378",
# #      "detection_method": "keyword",
# #      "crime_count": 2,
# #      "success": true
# #    }
# # ===============================

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from transformers import BertTokenizerFast, BertForSequenceClassification
import torch
import joblib
import os
import mysql.connector
from datetime import datetime
from contextlib import asynccontextmanager

# ---------------------------------------------------
# Database connection setup (will be initialized in lifespan)
# ---------------------------------------------------
db = None
cursor = None

# ---------------------------------------------------
# Path setup for model + encoder
# ---------------------------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_DIR = os.path.join(BASE_DIR, "crime_model")
ENCODER_PATH = os.path.join(BASE_DIR, "label_encoder.pkl")

# ---------------------------------------------------
# Load Model and Label Encoder
# ---------------------------------------------------
tokenizer = BertTokenizerFast.from_pretrained(MODEL_DIR)
model = BertForSequenceClassification.from_pretrained(MODEL_DIR)
label_encoder = joblib.load(ENCODER_PATH)

# ---------------------------------------------------
# IPC mapping for ML labels
# ---------------------------------------------------
ipc_mapping = {
    "Murder": "IPC 302",
    "Theft": "IPC 378",
    "Robbery": "IPC 392",
    "Assault": "IPC 351",
    "House Trespass": "IPC 442",
    "Fraud": "IPC 323",
    "Accident (Causing Death by Negligence)": "IPC 304A",
    "Rape": "IPC 376",
    "Cheating": "IPC 420",
    "Kidnapping": "IPC 363",
    "Dacoity": "IPC 395",
    "Criminal Breach of Trust": "IPC 406",
    "Extortion": "IPC 384",
    "Defamation": "IPC 499",
    "Dowry Death": "IPC 304B",
    "Attempt to Murder": "IPC 307",
    "Grievous Hurt": "IPC 325",
    "Forgery": "IPC 465",
    "Rioting": "IPC 147",
    "Unlawful Assembly": "IPC 141",
    "Acid Attack": "IPC 326A",
    "Cybercrime (Hacking)": "IPC 66 IT Act + IPC 379/420"
}

# ---------------------------------------------------
# Keyword-based crime mapping
# ---------------------------------------------------
keyword_map = {
    "murder": {"label": "Murder", "ipc": "IPC 302"},
    "dowry": {"label": "Dowry Death", "ipc": "IPC 304B"},
    "kill": {"label": "Murder", "ipc": "IPC 302"},
    "killed": {"label": "Murder", "ipc": "IPC 302"},
    "homicide": {"label": "Murder", "ipc": "IPC 302"},
    "theft": {"label": "Theft", "ipc": "IPC 378"},
    "steal": {"label": "Theft", "ipc": "IPC 378"},
    "stole": {"label": "Theft", "ipc": "IPC 378"},
    "robbery": {"label": "Robbery", "ipc": "IPC 392"},
    "robbed": {"label": "Robbery", "ipc": "IPC 392"},
    # "acid": {"label": "Acid Attack", "ipc": "IPC 326A"},
    # "assault": {"label": "Assault", "ipc": "IPC 351"},
    "attack": {"label": "Assault", "ipc": "IPC 351"},
    "trespass": {"label": "House Trespass", "ipc": "IPC 442"},
    "trespassed": {"label": "House Trespass", "ipc": "IPC 442"},
    "break-in": {"label": "House Trespass", "ipc": "IPC 442"},
     "murder": {"label": "Murder", "ipc": "IPC 302"},
    "kill": {"label": "Murder", "ipc": "IPC 302"},
    "killed": {"label": "Murder", "ipc": "IPC 302"},
    "homicide": {"label": "Murder", "ipc": "IPC 302"},
    "stabbed": {"label": "Murder", "ipc": "IPC 302"},
    "strangled": {"label": "Murder", "ipc": "IPC 302"},
    "beheaded": {"label": "Murder", "ipc": "IPC 302"},

    # --- 💰 Theft / Robbery / Dacoity ---
    "theft": {"label": "Theft", "ipc": "IPC 378"},
    "steal": {"label": "Theft", "ipc": "IPC 378"},
    "stole": {"label": "Theft", "ipc": "IPC 378"},
    "robbery": {"label": "Robbery", "ipc": "IPC 392"},
    "robbed": {"label": "Robbery", "ipc": "IPC 392"},
    "snatched": {"label": "Robbery", "ipc": "IPC 392"},
    "dacoity": {"label": "Dacoity", "ipc": "IPC 395"},
    "gang robbery": {"label": "Dacoity", "ipc": "IPC 395"},

    # --- 🏠 Trespassing / Burglary ---
    "trespass": {"label": "House Trespass", "ipc": "IPC 442"},
    "break-in": {"label": "House Trespass", "ipc": "IPC 442"},
    "burglar": {"label": "House Trespass", "ipc": "IPC 442"},
    "intruder": {"label": "House Trespass", "ipc": "IPC 442"},

    # --- 🧨 Assault / Violence ---
    "assault": {"label": "Assault", "ipc": "IPC 351"},
    "attack": {"label": "Assault", "ipc": "IPC 351"},
    "beaten": {"label": "Assault", "ipc": "IPC 351"},
    "hit": {"label": "Assault", "ipc": "IPC 351"},
    "injured": {"label": "Assault", "ipc": "IPC 351"},
    "violence": {"label": "Assault", "ipc": "IPC 351"},
    "fight": {"label": "Assault", "ipc": "IPC 351"},

    # --- 💍 Dowry / Domestic Violence / Suicide ---
    "dowry": {"label": "Dowry Death", "ipc": "IPC 304B"},
    "harass": {"label": "Dowry Death", "ipc": "IPC 304B"},
    "harassed": {"label": "Dowry Death", "ipc": "IPC 304B"},
    "torture": {"label": "Dowry Death", "ipc": "IPC 304B"},
    "bride": {"label": "Dowry Death", "ipc": "IPC 304B"},
    "suicide": {"label": "Dowry Death", "ipc": "IPC 304B"},
    "in-laws": {"label": "Dowry Death", "ipc": "IPC 304B"},
    "domestic": {"label": "Dowry Death", "ipc": "IPC 304B"},
    "burnt": {"label": "Dowry Death", "ipc": "IPC 304B"},

    # --- 🧑‍🤝‍🧑 Kidnapping / Abduction ---
    "kidnap": {"label": "Kidnapping", "ipc": "IPC 363"},
    "abduct": {"label": "Kidnapping", "ipc": "IPC 363"},
    "missing": {"label": "Kidnapping", "ipc": "IPC 363"},

    # --- 🕵️ Fraud / Cheating / Forgery ---
    "fraud": {"label": "Fraud", "ipc": "IPC 420"},
    "cheat": {"label": "Cheating", "ipc": "IPC 420"},
    "scam": {"label": "Cheating", "ipc": "IPC 420"},
    "fake": {"label": "Forgery", "ipc": "IPC 465"},
    "forgery": {"label": "Forgery", "ipc": "IPC 465"},
    "duplicate": {"label": "Forgery", "ipc": "IPC 465"},

    # --- 🧑‍💻 Cyber Crime ---
    "hack": {"label": "Cybercrime (Hacking)", "ipc": "IPC 66 IT Act + IPC 379/420"},
    "hacked": {"label": "Cybercrime (Hacking)", "ipc": "IPC 66 IT Act + IPC 379/420"},
    "phishing": {"label": "Cybercrime (Hacking)", "ipc": "IPC 66 IT Act + IPC 420"},
    "virus": {"label": "Cybercrime (Hacking)", "ipc": "IPC 66 IT Act"},
    "cyber": {"label": "Cybercrime (Hacking)", "ipc": "IPC 66 IT Act"},

    # --- 👩 Sexual Offences ---
    "rape": {"label": "Rape", "ipc": "IPC 376"},
    "molest": {"label": "Assault", "ipc": "IPC 354"},
    "harassment": {"label": "Assault", "ipc": "IPC 354"},
    "sexual": {"label": "Rape", "ipc": "IPC 376"},
    "abuse": {"label": "Assault", "ipc": "IPC 354"},

    # --- 💣 Rioting / Unlawful Assembly ---
    "riot": {"label": "Rioting", "ipc": "IPC 147"},
    "mob": {"label": "Unlawful Assembly", "ipc": "IPC 141"},
    "protest": {"label": "Unlawful Assembly", "ipc": "IPC 141"},

    # --- 🧴 Acid Attack ---
    "acid": {"label": "Acid Attack", "ipc": "IPC 326A"},
    "threw acid": {"label": "Acid Attack", "ipc": "IPC 326A"},
    "acid burn": {"label": "Acid Attack", "ipc": "IPC 326A"},

    # --- 💣 Extortion / Blackmail ---
    "blackmail": {"label": "Extortion", "ipc": "IPC 384"},
    "threaten": {"label": "Extortion", "ipc": "IPC 384"},
    "extort": {"label": "Extortion", "ipc": "IPC 384"},

    # --- ⚙️ Miscellaneous ---
    "defame": {"label": "Defamation", "ipc": "IPC 499"},
    "rumor": {"label": "Defamation", "ipc": "IPC 499"},
    "accident": {"label": "Accident (Causing Death by Negligence)", "ipc": "IPC 304A"},
    "negligence": {"label": "Accident (Causing Death by Negligence)", "ipc": "IPC 304A"},

}

# ---------------------------------------------------
# Lifespan Event Handler (Startup + Shutdown)
# ---------------------------------------------------
@asynccontextmanager
async def lifespan(app: FastAPI):
    global db, cursor
    print("=" * 60)
    print("🚨 Crime Classification ML API Starting...")
    print("=" * 60)

    try:
        db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="koye20@%",
            database="crime_system"
        )
        cursor = db.cursor()
        print("✅ Database connected")
    except Exception as e:
        print(f"⚠️  Database connection failed: {e}")

    print(f"✅ Model loaded from: {MODEL_DIR}")
    print(f"✅ Label encoder loaded from: {ENCODER_PATH}")
    print(f"✅ Total crime types supported: {len(ipc_mapping)}")
    print("=" * 60)
    yield

    print("\n🛑 Shutting down...")
    if db and db.is_connected():
        cursor.close()
        db.close()
        print("✅ Database closed")

# ---------------------------------------------------
# FastAPI setup
# ---------------------------------------------------
app = FastAPI(
    title="Crime Classification ML API",
    version="2.0.0",
    description="AI-powered crime classification system (ML-first, keyword-second)",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------------------------------
# Input Models
# ---------------------------------------------------
class PredictionInput(BaseModel):
    description: str

class ReportInput(BaseModel):
    officer_id: int
    place: str
    location: str
    city: str
    country: str
    description: str

# ---------------------------------------------------
# Keyword Detection Function
# ---------------------------------------------------
def detect_from_keywords(text: str):
    text_lower = text.lower()
    detected = {}
    for word, info in keyword_map.items():
        if word in text_lower:
            if info["label"] not in detected:
                detected[info["label"]] = info["ipc"]
    if detected:
        return list(detected.keys()), list(detected.values())
    return None, None

# ---------------------------------------------------
# Root Endpoint
# ---------------------------------------------------
@app.get("/")
def root():
    return {"message": "🚨 Crime Classification ML API (ML-first mode) is running!"}

# ---------------------------------------------------
# Prediction Endpoint (ML first, then keyword)
# ---------------------------------------------------
@app.post("/predict")
def predict(data: PredictionInput):
    try:
        # Step 1: ML Model first
        inputs = tokenizer(data.description, return_tensors="pt", padding=True, truncation=True, max_length=512)
        with torch.no_grad():
            outputs = model(**inputs)
            pred = torch.argmax(outputs.logits, dim=-1).item()

        predicted_label = label_encoder.inverse_transform([pred])[0]
        ipc_code = ipc_mapping.get(predicted_label, "Unknown")

        # Step 2: Keyword matching (adds more crimes if found)
        keyword_labels, keyword_ipcs = detect_from_keywords(data.description)
        if keyword_labels:
            if predicted_label not in keyword_labels:
                keyword_labels.insert(0, predicted_label)
                keyword_ipcs.insert(0, ipc_code)
            predicted_label = ", ".join(keyword_labels)
            ipc_code = ", ".join(keyword_ipcs)
            detection_source = "ml_model + keyword"
        else:
            detection_source = "ml_model"

        return {
            "crime_type": predicted_label,
            "ipc_section": ipc_code,
            "detection_method": detection_source,
            "success": True
        }

    except Exception as e:
        return {"success": False, "error": str(e)}

# ---------------------------------------------------
# Prediction + Database Storage (ML first)
# ---------------------------------------------------
@app.post("/predict_and_store")
def predict_and_store(data: ReportInput):
    if not db or not db.is_connected():
        return {"success": False, "error": "Database not connected"}

    try:
        # Step 1: ML prediction first
        inputs = tokenizer(data.description, return_tensors="pt", padding=True, truncation=True, max_length=512)
        with torch.no_grad():
            outputs = model(**inputs)
            pred = torch.argmax(outputs.logits, dim=-1).item()

        predicted_label = label_encoder.inverse_transform([pred])[0]
        ipc_code = ipc_mapping.get(predicted_label, "Unknown")

        # Step 2: Keyword enhancement
        keyword_labels, keyword_ipcs = detect_from_keywords(data.description)
        if keyword_labels:
            if predicted_label not in keyword_labels:
                keyword_labels.insert(0, predicted_label)
                keyword_ipcs.insert(0, ipc_code)
            predicted_label = ", ".join(keyword_labels)
            ipc_code = ", ".join(keyword_ipcs)
            detection_source = "ml_model + keyword"
        else:
            detection_source = "ml_model"

        # Step 3: Save to DB
        query = """
        INSERT INTO crime_reports 
        (officer_id, date_time, place, location, city, country, description, crime_type, ipc_section)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        values = (
            data.officer_id,
            datetime.now(),
            data.place,
            data.location,
            data.city,
            data.country,
            data.description,
            predicted_label,
            ipc_code
        )
        cursor.execute(query, values)
        db.commit()

        return {
            "crime_type": predicted_label,
            "ipc_section": ipc_code,
            "detection_method": detection_source,
            "message": "✅ Report classified and stored successfully!",
            "success": True
        }

    except Exception as e:
        db.rollback()
        return {"success": False, "error": str(e)}

# ---------------------------------------------------
# Health Check
# ---------------------------------------------------
@app.get("/health")
def health_check():
    status = "connected" if db and db.is_connected() else "not_connected"
    return {"status": "online", "database": status, "model_loaded": model is not None}
