"""
Translation module for multilingual support (Tamil, Hindi, English)
Uses Google Translate API for language detection and translation
"""
from googletrans import Translator

# Supported languages
SUPPORTED_LANGUAGES = {
    'en': 'English',
    'ta': 'Tamil',
    'hi': 'Hindi'
}

# Global translator instance
_translator = None


def get_translator():
    """Get or create translator instance."""
    global _translator
    if _translator is None:
        _translator = Translator()
    return _translator


def detect_language(text: str) -> str:
    """
    Detect the language of input text.
    
    Args:
        text: Input text
        
    Returns:
        Language code (e.g., 'ta', 'en', 'hi')
    """
    try:
        translator = get_translator()
        detection = translator.detect(text)
        return detection.lang
    except Exception as e:
        print(f"Language detection failed: {e}")
        return 'en'  # Default to English


def translate_to_english(text: str, source_lang: str = None) -> tuple:
    """
    Translate text to English for LLM processing.
    
    Args:
        text: Input text in any language
        source_lang: Optional source language code
        
    Returns:
        Tuple of (translated_text, detected_language)
    """
    try:
        # Quick check: if text is purely ASCII, it's likely English - skip detection
        # This avoids false positives from the translation API
        if text.isascii():
            return text, 'en'
        
        translator = get_translator()
        
        # Detect language if not provided (only for non-ASCII text)
        if source_lang is None:
            source_lang = detect_language(text)
        
        # If already English, return as-is
        if source_lang == 'en':
            return text, 'en'
        
        # Translate to English
        result = translator.translate(text, src=source_lang, dest='en')
        return result.text, source_lang
        
    except Exception as e:
        print(f"Translation to English failed: {e}")
        return text, 'en'


def translate_response(text: str, target_lang: str) -> str:
    """
    Translate LLM response back to user's language.
    
    Args:
        text: English response from LLM
        target_lang: Target language code
        
    Returns:
        Translated response
    """
    try:
        # If target is English, return as-is
        if target_lang == 'en':
            return text
        
        translator = get_translator()
        result = translator.translate(text, src='en', dest=target_lang)
        return result.text
        
    except Exception as e:
        print(f"Translation to {target_lang} failed: {e}")
        return text  # Return original if translation fails


def get_language_name(lang_code: str) -> str:
    """Get human-readable language name."""
    return SUPPORTED_LANGUAGES.get(lang_code, lang_code.upper())


# Test translation when run directly
if __name__ == "__main__":
    print("Testing translation module...")
    
    # Test Tamil
    tamil_text = "சேலம் மாவட்டத்தின் நிலத்தடி நீர் நிலை என்ன?"
    english, lang = translate_to_english(tamil_text)
    print(f"\nTamil input: {tamil_text}")
    print(f"Detected language: {lang}")
    print(f"English translation: {english}")
    
    # Test response translation
    response = "Salem district has moderate groundwater levels."
    tamil_response = translate_response(response, 'ta')
    print(f"\nEnglish response: {response}")
    print(f"Tamil translation: {tamil_response}")
