import hashlib

def generate_hash(paswd: str) -> str:
    return hashlib.sha256(paswd.encode('utf-8')).hexdigest()
