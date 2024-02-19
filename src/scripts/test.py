import hashlib

def encript_string(hash_string:str) -> str:
    """
    https://medium.com/@dwernychukjosh/sha256-encryption-with-python-bf216db497f9
    """
    sha_signature = hashlib.sha256(
        hash_string.encode()
    ).hexdigest()
    return sha_signature

hash_string = 'confidential data'
sha_signature = encript_string(hash_string)

print(sha_signature)
