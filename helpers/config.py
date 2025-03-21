import os

class Config:
    JWT_SECRET_KEY = "jwt_secret_key"
    FRONTEND_URL = "http://localhost:5000"
    MONGO_URI = "mongodb+srv://<username>:<password>@cluster0.tvycbjn.mongodb.net/?retryWrites=true&w=majority"
    DB_NAME = "estate_db"
    AUTH_COLLECTION = "users"
    GATEPASS_COLLECTION = "visitor_tokens"
