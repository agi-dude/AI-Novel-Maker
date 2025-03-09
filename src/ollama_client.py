import json
import logging
import requests
from typing import Dict, List, Optional, Any
import re

from config import OLLAMA_API_HOST

logger = logging.getLogger(__name__)

class OllamaClient:
    def __init__(self, model: str, api_host: str = OLLAMA_API_HOST):
        self.model = model
        self.api_host = api_host
        logger.info(f"Initialized Ollama client with model: {model}")
    
    def generate(self, prompt: str, system: Optional[str] = None, temperature: float = 0.7) -> str:
        """Generate text using Ollama API"""
        url = f"{self.api_host}/api/generate"
        
        payload = {
            "model": self.model,
            "prompt": prompt,
            "temperature": temperature,
            "stream": False
        }
        
        if system:
            payload["system"] = system
        
        try:
            logger.debug(f"Sending request to Ollama API: {url}")
            response = requests.post(url, json=payload)
            response.raise_for_status()
            
            result = response.json()
            generated_text = result.get("response", "")
            logger.debug(f"Generated {len(generated_text)} characters")
            
            return re.sub(r'\s*<think>[\s\S]*?</think>\s*', generated_text, '')
        
        except requests.exceptions.RequestException as e:
            logger.error(f"Error calling Ollama API: {e}")
            raise
    
    def chat(self, messages: List[Dict[str, str]], system: Optional[str] = None, temperature: float = 0.7) -> str:
        """Chat using Ollama API"""
        url = f"{self.api_host}/api/chat"
        
        payload = {
            "model": self.model,
            "messages": messages,
            "temperature": temperature,
            "stream": False
        }
        
        if system:
            payload["system"] = system
        
        try:
            logger.debug(f"Sending chat request to Ollama API: {url}")
            response = requests.post(url, json=payload)
            response.raise_for_status()
            
            result = response.json()
            message = result.get("message", {})
            content = message.get("content", "")
            logger.debug(f"Generated {len(content)} characters")
            
            return re.sub(r'\s*<think>[\s\S]*?</think>\s*', content, '')
        
        except requests.exceptions.RequestException as e:
            logger.error(f"Error calling Ollama API: {e}")
            raise
