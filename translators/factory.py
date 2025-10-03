import json
import os
from typing import Dict, Any, List
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


def load_language_config() -> Dict[str, Any]:
    """
    Load language configuration from config.json

    Returns:
        Dict[str, Any]: Language configuration including available languages and default language

    Raises:
        FileNotFoundError: If config.json file is not found
        json.JSONDecodeError: If config.json contains invalid JSON
    """
    # Read config.json
    config_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'config.json')
    with open(config_path, 'r') as f:
        config = json.load(f)

    # Extract language configuration
    languages = config.get('languages', [])
    default_language = config.get('default_language', '')

    # If no languages configured, use fallback languages
    if not languages:
        languages = [
            {"name": "Chinese", "code": "zh", "default": True},
            {"name": "English", "code": "en"},
            {"name": "Russian", "code": "ru"},
            {"name": "Japanese", "code": "ja"},
            {"name": "Korean", "code": "ko"},
            {"name": "French", "code": "fr"}
        ]
        default_language = "Chinese"
    elif not default_language:
        # Find default language or use first language
        for lang in languages:
            if lang.get('default', False):
                default_language = lang['name']
                break
        else:
            default_language = languages[0]['name']

    return {
        'languages': languages,
        'default_language': default_language
    }


def validate_language_config(config: Dict[str, Any]) -> bool:
    """
    Validate language configuration

    Args:
        config (Dict[str, Any]): Language configuration dictionary

    Returns:
        bool: True if configuration is valid, False otherwise
    """
    languages = config.get('languages', [])
    default_language = config.get('default_language', '')

    # Check if languages is a non-empty list
    if not isinstance(languages, list) or len(languages) == 0:
        return False

    # Check if each language has a name
    for lang in languages:
        if not isinstance(lang, dict) or 'name' not in lang:
            return False

    # Check if default_language exists in languages
    if default_language:
        language_names = [lang['name'] for lang in languages]
        if default_language not in language_names:
            return False

    return True