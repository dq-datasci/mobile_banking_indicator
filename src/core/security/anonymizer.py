import hashlib
from typing import Optional

class PIIAnonymizer:
    """
    Utility class for anonymizing Personally Identifiable Information (PII)
    such as user names, IP addresses, etc. using SHA-256 hashing.
    """

    @staticmethod
    def hash_sha256(value: Optional[str]) -> Optional[str]:
        """
        Takes a string and returns its SHA-256 hash representation.
        If the input is None or empty, returns the original value.
        
        Args:
            value (Optional[str]): The string to hash.
            
        Returns:
            Optional[str]: The hex digest of the hashed string or original if empty/None.
        """
        if not value:
            return value
        
        # Encode the string and compute SHA-256 hash
        hash_object = hashlib.sha256(value.encode('utf-8'))
        return hash_object.hexdigest()
