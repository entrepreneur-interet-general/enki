import os

def reset_csv(csv_path: str):
    if os.path.exists(csv_path):
        os.remove(csv_path)
    os.makedirs(os.path.dirname(csv_path), exist_ok=True)