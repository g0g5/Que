import json
import os
from typing import Dict, Any
from translators.base import TranslatorProvider
from translators.gemini import GeminiProvider
from translators.openai import OpenAIProvider


def load_translator() -> TranslatorProvider:
    """
    Load translator based on configuration in config.json
    
    Returns:
        TranslatorProvider: Instance of the configured translator provider
        
    Raises:
        ValueError: If provider configuration is invalid or provider is not supported
        FileNotFoundError: If config.json file is not found
    """
    # Read config.json
    config_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'config.json')
    with open(config_path, 'r') as f:
        config = json.load(f)
    
    # Get the selected provider name
    provider_name = config.get('provider')
    if not provider_name:
        raise ValueError("No provider specified in config.json")
    
    # Find provider configuration
    provider_configs = config.get('providers', [])
    provider_config = None
    for p in provider_configs:
        if p.get('provider_name') == provider_name:
            provider_config = p
            break
    
    if not provider_config:
        raise ValueError(f"Configuration for provider '{provider_name}' not found")
    
    # Get provider type
    provider_type = provider_config.get('provider_type')
    if not provider_type:
        raise ValueError(f"Provider type not specified for provider '{provider_name}'")
    
    # Create provider instance based on provider_type
    if provider_type == 'GeminiAPI':
        api_key = provider_config.get('api_key', '')
        model = provider_config.get('model', 'gemini-2.5-flash')
        return GeminiProvider(api_key, model)
    elif provider_type == 'OpenAICompatible':
        base_url = provider_config.get('base_url', 'https://api.openai.com/v1')
        api_key = provider_config.get('api_key', '')
        model = provider_config.get('model', 'gpt-3.5-turbo')
        return OpenAIProvider(base_url, api_key, model)
    else:
        raise ValueError(f"Unsupported provider type: {provider_type}")