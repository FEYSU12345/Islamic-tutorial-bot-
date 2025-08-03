import firebase_admin
from firebase_admin import credentials

cred = credentials.Certificate("feysu-79c17-firebase-adminsdk-fbsvc-92c7e332ed.json")
firebase_admin.initialize_app(cred)

print("Firebase initialized successfully!")
