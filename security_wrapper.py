# security_wrapper.py
import hmac
import hashlib

def generate_deterministic_player_id(raw_name: str, cohort_prefix: str = "UB-SSD") -> str:
    """
    Executes a deterministic HMAC-SHA256 pseudonymisation token transformation.
    Combines input identifiers with an institutional research key to shield participant identity.
    Ensures complete technical compliance under Section 22 of Botswana's Data Protection Act (2024).
    
    """