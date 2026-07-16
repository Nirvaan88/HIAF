#models.py
import os
from pymongo import MongoClient
from werkzeug.security import generate_password_hash

client = MongoClient(os.getenv("MONGO_URI"))

db = client['employee_management']

employees_collection = db['employees']

def ensure_admin_exists():
    admin = employees_collection.find_one({'role': 'admin'})
    if not admin:
        # Fetch secure credentials from the .env file instead of hardcoding them
        admin_phone = os.getenv('ADMIN_PHONE', '0000000000') # Still keeps a fallback if .env is missing
        admin_pass = os.getenv('ADMIN_PASSWORD', 'admin123')
        
        employees_collection.insert_one({
            'employee_id': '0000000000',
            'name': 'admin',
            'phone': admin_phone,
            'role': 'admin',
            'password': generate_password_hash(admin_pass),
            'details_completed': True
        })
    else:
        if admin.get('employee_id') != '0000000000':
            employees_collection.update_one({'_id': admin['_id']}, {'$set': {'employee_id': '0000000000'}})