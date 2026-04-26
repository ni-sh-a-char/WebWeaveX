"""
AI Adapter System for WebWeaveX
Provides abstraction layer for AI processing
"""


class BaseAIAdapter:
    def process(self, content):
        return None
    
    def get_mode(self):
        return "base"


class LocalAIAdapter(BaseAIAdapter):
    def process(self, content):
        return {"mode": "local", "result": None}
    
    def get_mode(self):
        return "local"


class CloudAIAdapter(BaseAIAdapter):
    def process(self, content):
        return {"mode": "cloud", "result": None}
    
    def get_mode(self):
        return "cloud"


class NoAIAdapter(BaseAIAdapter):
    def process(self, content):
        return {"mode": "off", "result": None}
    
    def get_mode(self):
        return "off"


def get_ai_adapter(mode):
    mode = mode or "off"
    if mode == "local":
        return LocalAIAdapter()
    elif mode == "cloud":
        return CloudAIAdapter()
    return NoAIAdapter()


__all__ = ["BaseAIAdapter", "LocalAIAdapter", "CloudAIAdapter", "NoAIAdapter", "get_ai_adapter"]