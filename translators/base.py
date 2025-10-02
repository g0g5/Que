from abc import ABC, abstractmethod


class TranslatorProvider(ABC):
    """Abstract class for translation providers"""
    
    @abstractmethod
    def translate(self, lang: str, content: str) -> str:
        """
        Translate content to the specified language
        
        Args:
            lang (str): Target language code
            content (str): Content to translate
            
        Returns:
            str: Translated content
        """
        pass