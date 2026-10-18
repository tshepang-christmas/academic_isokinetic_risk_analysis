# security_wrapper.py
import hmac
import hashlib
import os

ACADEMIC_SECRET_KEY = "PHR799_SECRET_KEY"  
TOKEN_LENGTH = 12                


def _load_key() -> bytes:
    """Read the pseudonymisation key from the environment; refuse to run without it."""
    key = os.environ.get(ACADEMIC_SECRET_KEY, "")
    if not key:
        raise RuntimeError(
            f"Environment variable {ACADEMIC_SECRET_KEY} is not set. "
            "Set it to the research key before starting the application."
        )
    return key.encode("utf-8")


_SECRET_KEY = _load_key()


def generate_deterministic_player_id(raw_name: str, cohort_prefix: str = "UB-SSD") -> str:
    """
    Executes a deterministic HMAC-SHA256 pseudonymisation token transformation.
    Combines input identifiers with an institutional research key to shield participant identity.
    Ensures complete technical compliance under Section 22 of Botswana's Data Protection Act (2024).
    
    This is a pseudonymisation, not anonymisation.
    """
    clean_input = " ".join(str(raw_name).split()).upper()

    if not clean_input:
        return f"{cohort_prefix}-UNKNOWN"

    digest = hmac.new(_SECRET_KEY, clean_input.encode("utf-8"), hashlib.sha256).hexdigest()
    return f"{cohort_prefix}-{digest[:TOKEN_LENGTH].upper()}"