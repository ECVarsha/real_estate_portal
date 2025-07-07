import json
from django.contrib.auth.hashers import make_password

def transform_user_data():
    with open('data_backups/20250416_010907/user.json') as f:
        users = json.load(f)
    
    transformed = []
    for user in users:
        new_user = {
            "model": "auth.user",
            "pk": user["pk"],
            "fields": {
                "password": user["fields"]["password"],
                "last_login": user["fields"]["last_login"],
                "is_superuser": user["fields"]["is_superuser"],
                "username": user["fields"]["username"],
                "first_name": "",
                "last_name": "",
                "email": user["fields"].get("email", ""),
                "is_staff": user["fields"].get("is_staff", False),
                "is_active": True,
                "date_joined": "2025-04-16T00:00:00Z"
            }
        }
        transformed.append(new_user)
    
    with open('transformed_users.json', 'w') as f:
        json.dump(transformed, f, indent=2)