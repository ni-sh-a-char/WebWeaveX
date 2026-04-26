import requests


class AIProvider:
    def generate(self, prompt):
        raise NotImplementedError


class GenericAPIProvider(AIProvider):
    def __init__(self, endpoint, api_key):
        self.endpoint = endpoint
        self.api_key = api_key

    def generate(self, prompt):
        try:
            headers = {"Authorization": f"Bearer {self.api_key}"}
            response = requests.post(
                self.endpoint,
                json={"prompt": prompt},
                headers=headers,
                timeout=30
            )
            try:
                data = response.json()
            except Exception:
                data = {}
            return {
                "text": data.get("text") or data.get("response") or "",
                "raw": data
            }
        except Exception:
            return {"text": "", "raw": {}}