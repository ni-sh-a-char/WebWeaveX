from kaalka import Kaalka


def _get_kaalka():
    """Create fresh Kaalka instance."""
    return Kaalka()


def secure_store(context, key, value):
    """Store encrypted value in context."""
    if value is None:
        return
    k = _get_kaalka()
    encrypted = k.encrypt(str(value))
    context.setdefault("secure", {})
    context["secure"][key] = encrypted


def secure_get(context, key, default=None):
    """Retrieve decrypted value from context."""
    encrypted = context.get("secure", {}).get(key)
    if not encrypted:
        return default
    k = _get_kaalka()
    try:
        return k.decrypt(encrypted)
    except Exception:
        return default


def secure_store_api_key(context, provider, api_key):
    """Store API key encrypted."""
    secure_store(context, f"api_key_{provider}", api_key)


def secure_get_api_key(context, provider):
    """Retrieve API key."""
    return secure_get(context, f"api_key_{provider}")


def is_encrypted(value) -> bool:
    """Check if value appears to be Kaalka encrypted."""
    if not isinstance(value, str):
        return False
    return len(value) > 10 and not ("<" in value or "{" in value)


def validate_ai_config(ai_config):
    """Validate AI config and return (is_valid, error)."""
    if not ai_config:
        return False, "No config"
    
    provider = ai_config.get("provider")
    
    if provider in ("openai", "groq"):
        api_key = ai_config.get("api_key")
        if not api_key:
            return False, f"Missing api_key for {provider}"
        return True, None
    
    if provider == "local":
        endpoint = ai_config.get("endpoint")
        if not endpoint:
            return False, "Missing endpoint for local"
        return True, None
    
    return False, f"Unknown provider: {provider}"


def encrypt_dict(data: dict, context, prefix: str = "") -> dict:
    """Encrypt all sensitive string values in dict."""
    result = {}
    sensitive_keys = ("api_key", "key", "token", "secret", "password", "credential")
    
    for k, v in data.items():
        key_name = f"{prefix}{k}" if prefix else k
        if isinstance(v, str) and any(s in k.lower() for s in sensitive_keys):
            secure_store(context, key_name, v)
            result[k] = f"__encrypted:{key_name}__"
        elif isinstance(v, dict):
            result[k] = encrypt_dict(v, context, f"{key_name}.")
        else:
            result[k] = v
    
    return result


def decrypt_dict(data: dict, context) -> dict:
    """Decrypt encrypted values in dict."""
    result = {}
    
    for k, v in data.items():
        if isinstance(v, str) and v.startswith("__encrypted:") and v.endswith("__"):
            key = v[12:-2]
            result[k] = secure_get(context, key)
        elif isinstance(v, dict):
            result[k] = decrypt_dict(v, context)
        else:
            result[k] = v
    
    return result