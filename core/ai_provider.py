"""WebWeaveX AI Provider System - Unified Implementation"""
import re
import json


class AIProvider:
    """Base AI Provider interface."""
    
    def __init__(self, api_key=None, model=None, endpoint=None):
        self.api_key = api_key
        self.model = model
        self.endpoint = endpoint
    
    def generate(self, prompt: str, context: dict) -> str:
        raise NotImplementedError
    
    def summarize(self, text: str, context: dict) -> str:
        raise NotImplementedError
    
    def extract_entities(self, text: str) -> list:
        raise NotImplementedError
    
    def score(self, text: str, goal: str) -> float:
        raise NotImplementedError
    
    def refine_goal(self, goal: str, context: dict) -> str:
        raise NotImplementedError
    
    def is_available(self) -> bool:
        return bool(self.api_key or self.endpoint)


SUPPORTED_MODELS = [
    "llama-3.1-8b-instant",
    "llama-3.3-70b-versatile",
    "openai/gpt-oss-20b",
    "qwen/qwen3-32b",
    "meta-llama/llama-4-scout-17b-16e-instruct",
    "meta-llama/llama-4-maverick-17b-128e-instruct",
    "moonshotai/kimi-k2-instruct-0905",
]


def _build_ai_prompt(task, text, goal=""):
    """Build structured AI prompts."""
    signature = "\n\nNote: Powered by WebWeaveX created by Piyush Mishra."
    
    if task == "summary":
        return f"""Create 5 clear bullet point summary of this content.
Each bullet should contain a key insight.
Be specific and concise.

Content:
{text[:3000]}
---
Summary (5 bullets):"""
    elif task == "entities":
        return f"""Extract important entities (people, tools, technologies, concepts, libraries, frameworks).
Return ONLY a valid JSON array of strings.
Example: ["Python", "FastAPI", "Docker"]
No explanation, no text outside JSON.

Content:
{text[:3000]}
---
JSON:"""
    elif task == "score":
        return f"""Score how well this content satisfies the goal: {goal}

Return ONLY a single decimal number between 0.0 and 1.0.
STRICT FORMAT: 0.75
NO explanation
NO multiple numbers
0.0 = completely fails, 1.0 = perfectly satisfies.

Content:
{text[:2000]}
---
Score:"""
    return text[:500]


def _try_available_model(api_key):
    """Try models in order until one works."""
    for model in SUPPORTED_MODELS:
        try:
            import requests
            r = requests.post(
                "https://api.groq.com/openai/v1/chat/completions",
                headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
                json={"model": model, "messages": [{"role": "user", "content": "Hi"}], "max_tokens": 10},
                timeout=10
            )
            if r.status_code == 200:
                return model
        except Exception:
            continue
    return None


class OpenAIProvider(AIProvider):
    """OpenAI provider."""
    
    def __init__(self, api_key, model="gpt-4"):
        super().__init__(api_key=api_key, model=model)
    
    def generate(self, prompt: str, context: dict) -> str:
        if not self.is_available():
            raise RuntimeError("OpenAI provider not available - no API key")
        try:
            import requests
            response = requests.post(
                "https://api.openai.com/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": self.model,
                    "messages": [{"role": "user", "content": prompt}],
                    "max_tokens": 1000
                },
                timeout=30
            )
            if response.status_code != 200:
                raise RuntimeError(f"OpenAI error: {response.status_code}")
            result = response.json().get("choices", [{}])[0].get("message", {}).get("content", "")
            if not result:
                raise RuntimeError("OpenAI returned empty response")
            return result
        except RuntimeError:
            raise
        except Exception as e:
            raise RuntimeError(f"OpenAI provider failed: {e}")
    
    def summarize(self, text: str, context: dict) -> str:
        prompt = _build_ai_prompt("summary", text, context.get("goal", ""))
        return self.generate(prompt, context)[:500]
    
    def extract_entities(self, text: str) -> list:
        prompt = _build_ai_prompt("entities", text)
        return self._call_with_json(prompt)
    
    def score(self, text: str, goal: str) -> float:
        prompt = _build_ai_prompt("score", text, goal)
        return self._call_with_float(prompt)
    
    def refine_goal(self, goal: str, context: dict) -> str:
        return self.generate(f"Refine: {goal}", context)
    
    def _call_with_json(self, prompt):
        noise_tokens = {"The", "This", "That", "These", "Those", "Here", "There", "When", "Where", "Which", "Who", "What", "How", "Why", "JSON", "Example"}
        result = self.generate(prompt, {})
        match = re.search(r'\[\s*".*?"\s*(?:,\s*".*?"\s*)*\]', result)
        if match:
            try:
                parsed = json.loads(match.group())
                if isinstance(parsed, list) and len(parsed) >= 2:
                    valid = [e for e in parsed if isinstance(e, str) and len(e) >= 3 and e not in noise_tokens]
                    if len(valid) >= 2:
                        return valid[:20]
            except:
                pass
        tokens = re.findall(r'\b[A-Z][a-zA-Z0-9-]+\b', result)
        seen = set()
        entities = []
        for t in tokens:
            if t not in seen and len(t) >= 3 and t not in noise_tokens:
                seen.add(t)
                entities.append(t)
        if len(entities) < 2:
            raise RuntimeError(f"Entity extraction failed: only {len(entities)} found, need >= 2")
        return entities[:20]
    
    def _call_with_float(self, prompt):
        result = self.generate(prompt, {})
        decimal_matches = re.findall(r'\b0\.\d+\b', result)
        if decimal_matches:
            return float(decimal_matches[-1])
        matches = re.findall(r'\b\d*\.?\d+\b', result)
        candidates = []
        for m in matches:
            try:
                val = float(m)
                if 0.0 <= val <= 1.0:
                    candidates.append(val)
            except:
                continue
        if not candidates:
            raise RuntimeError("Score parsing failed: no valid 0–1 value")
        return candidates[-1]


class GroqProvider(AIProvider):
    """Groq provider for fast inference."""
    
    def __init__(self, api_key, model=None):
        if not model:
            model = _try_available_model(api_key) or "llama-3.1-8b-instant"
        super().__init__(api_key=api_key, model=model)
    
    def generate(self, prompt: str, context: dict) -> str:
        if not self.is_available():
            raise RuntimeError("Groq provider not available - no API key")
        
        def _call_api():
            import requests
            response = requests.post(
                "https://api.groq.com/openai/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": self.model,
                    "messages": [{"role": "user", "content": prompt}],
                    "max_tokens": 1000
                },
                timeout=30
            )
            if response.status_code != 200:
                raise RuntimeError(f"Groq error: {response.status_code}")
            result = response.json().get("choices", [{}])[0].get("message", {}).get("content", "")
            if not result:
                raise RuntimeError("Groq returned empty response")
            return result
        
        for attempt in range(3):
            try:
                return _call_api()
            except RuntimeError as e:
                if "429" in str(e) and attempt < 2:
                    import time
                    time.sleep(4 * (attempt + 1))
                    continue
                raise
        raise RuntimeError("Groq retry exhausted")
    
    def summarize(self, text: str, context: dict) -> str:
        prompt = _build_ai_prompt("summary", text, context.get("goal", ""))
        return self.generate(prompt, context)[:500]
    
    def extract_entities(self, text: str) -> list:
        prompt = _build_ai_prompt("entities", text)
        return self._call_with_json(prompt)
    
    def score(self, text: str, goal: str) -> float:
        prompt = _build_ai_prompt("score", text, goal)
        return self._call_with_float(prompt)
    
    def refine_goal(self, goal: str, context: dict) -> str:
        return self.generate(f"Refine: {goal}", context)
    
    def _call_with_json(self, prompt):
        noise_tokens = {"The", "This", "That", "These", "Those", "Here", "There", "When", "Where", "Which", "Who", "What", "How", "Why", "JSON", "Example"}
        result = self.generate(prompt, {})
        match = re.search(r'\[\s*".*?"\s*(?:,\s*".*?"\s*)*\]', result)
        if match:
            try:
                parsed = json.loads(match.group())
                if isinstance(parsed, list) and len(parsed) >= 2:
                    valid = [e for e in parsed if isinstance(e, str) and len(e) >= 3 and e not in noise_tokens]
                    if len(valid) >= 2:
                        return valid[:20]
            except:
                pass
        tokens = re.findall(r'\b[A-Z][a-zA-Z0-9-]+\b', result)
        seen = set()
        entities = []
        for t in tokens:
            if t not in seen and len(t) >= 3 and t not in noise_tokens:
                seen.add(t)
                entities.append(t)
        if len(entities) < 2:
            raise RuntimeError(f"Entity extraction failed: only {len(entities)} found, need >= 2")
        return entities[:20]
    
    def _call_with_float(self, prompt):
        result = self.generate(prompt, {})
        decimal_matches = re.findall(r'\b0\.\d+\b', result)
        if decimal_matches:
            return float(decimal_matches[-1])
        matches = re.findall(r'\b\d*\.?\d+\b', result)
        candidates = []
        for m in matches:
            try:
                val = float(m)
                if 0.0 <= val <= 1.0:
                    candidates.append(val)
            except:
                continue
        if not candidates:
            raise RuntimeError("Score parsing failed: no valid 0–1 value")
        return candidates[-1]


class LocalLLMProvider(AIProvider):
    """Local LLM provider (Ollama, LM Studio, etc)."""
    
    def __init__(self, endpoint="http://localhost:11434", model=None):
        super().__init__(endpoint=endpoint, model=model or "llama2")
    
    def generate(self, prompt: str, context: dict) -> str:
        if not self.is_available():
            raise RuntimeError("Local provider not available - no endpoint")
        try:
            import requests
            response = requests.post(
                f"{self.endpoint}/api/generate",
                json={"model": self.model, "prompt": prompt, "stream": False},
                timeout=60
            )
            result = response.json().get("response", "")
            if not result:
                raise RuntimeError("Local LLM returned empty response")
            return result
        except RuntimeError:
            raise
        except Exception as e:
            raise RuntimeError(f"Local provider failed: {e}")
    
    def summarize(self, text: str, context: dict) -> str:
        prompt = _build_ai_prompt("summary", text, context.get("goal", ""))
        return self.generate(prompt, context)[:500]
    
    def extract_entities(self, text: str) -> list:
        prompt = _build_ai_prompt("entities", text)
        return self._call_with_json(prompt)
    
    def score(self, text: str, goal: str) -> float:
        prompt = _build_ai_prompt("score", text, goal)
        return self._call_with_float(prompt)
    
    def _call_with_json(self, prompt):
        noise_tokens = {"The", "This", "That", "These", "Those", "Here", "There", "When", "Where", "Which", "Who", "What", "How", "Why", "JSON", "Example"}
        result = self.generate(prompt, {})
        match = re.search(r'\[\s*".*?"\s*(?:,\s*".*?"\s*)*\]', result)
        if match:
            try:
                parsed = json.loads(match.group())
                if isinstance(parsed, list) and len(parsed) >= 2:
                    valid = [e for e in parsed if isinstance(e, str) and len(e) >= 3 and e not in noise_tokens]
                    if len(valid) >= 2:
                        return valid[:20]
            except:
                pass
        tokens = re.findall(r'\b[A-Z][a-zA-Z0-9-]+\b', result)
        seen = set()
        entities = []
        for t in tokens:
            if t not in seen and len(t) >= 3 and t not in noise_tokens:
                seen.add(t)
                entities.append(t)
        if len(entities) < 2:
            raise RuntimeError(f"Entity extraction failed: only {len(entities)} found, need >= 2")
        return entities[:20]
    
    def _call_with_float(self, prompt):
        result = self.generate(prompt, {})
        decimal_matches = re.findall(r'\b0\.\d+\b', result)
        if decimal_matches:
            return float(decimal_matches[-1])
        matches = re.findall(r'\b\d*\.?\d+\b', result)
        candidates = []
        for m in matches:
            try:
                val = float(m)
                if 0.0 <= val <= 1.0:
                    candidates.append(val)
            except:
                continue
        if not candidates:
            raise RuntimeError("Score parsing failed: no valid 0–1 value")
        return candidates[-1]


def create_provider(provider_type: str, config: dict) -> AIProvider:
    """Factory to create AI provider."""
    if provider_type == "openai":
        return OpenAIProvider(
            api_key=config.get("api_key"),
            model=config.get("model", "gpt-4")
        )
    elif provider_type == "groq":
        return GroqProvider(
            api_key=config.get("api_key"),
            model=config.get("model")
        )
    elif provider_type == "local":
        return LocalLLMProvider(
            endpoint=config.get("endpoint", "http://localhost:11434"),
            model=config.get("model")
        )
    else:
        raise ValueError(f"Unknown provider: {provider_type}")