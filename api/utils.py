import json
import os
from typing import Dict


def load_users():
    if os.path.exists('users.json'):
        with open('users.json', 'r', encoding='utf-8') as file:
            return json.load(file)
    else:
        return {}