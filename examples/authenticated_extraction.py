"""Authenticated extraction — supply your own session file and Kaalka key."""

from webweavex import extract_web

if __name__ == "__main__":
    result = extract_web(
        "https://example.com/app",
        authenticated=True,
        session_path="./session.enc",
        encryption_key="replace-with-your-key",
        semantic_runtime=True,
    )
    print("authenticated:", result.get("authenticated"))
    print("bounded:", result.get("bounded"))
