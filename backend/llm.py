"""
LLM integration with support for multiple providers (Local/Granite vs Cloud/Gemini)
"""
import torch
import google.genai as genai
from transformers import AutoModelForCausalLM, AutoTokenizer
import os

from backend.config import (
    LLM_MODEL_ID,
    LLM_CONTEXT_LENGTH,
    LLM_TEMPERATURE,
    LLM_MAX_TOKENS,
    LLM_PROVIDER,
    GEMINI_API_KEY,
    GEMINI_MODEL_ID
)

# Global instances
_llm_instance = None
_tokenizer = None
_gemini_client = None


def load_model():
    """
    Load the appropriate model based on configuration.
    Returns:
        - For Local: (model, tokenizer) tuple
        - For Gemini: None (client is stateless/configured globally)
    """
    global _llm_instance, _tokenizer, _gemini_client
    
    print(f"Initializing LLM Provider: {LLM_PROVIDER.upper()}")
    
    if LLM_PROVIDER == "gemini":
        if not GEMINI_API_KEY:
            raise ValueError("GEMINI_API_KEY is missing in environment variables!")
        
        if _gemini_client is None:
            # Initialize the new Client
            _gemini_client = genai.Client(api_key=GEMINI_API_KEY)
            print("Gemini API Client configured successfully.")
        return None
        
    else:
        # Default to Local Granite
        if _llm_instance is not None:
            return _llm_instance, _tokenizer
        
        device = "cuda" if torch.cuda.is_available() else "cpu"
        print(f"Loading local model: {LLM_MODEL_ID}")
        print(f"Using device: {device}")
        
        _tokenizer = AutoTokenizer.from_pretrained(LLM_MODEL_ID)
        _llm_instance = AutoModelForCausalLM.from_pretrained(
            LLM_MODEL_ID,
            torch_dtype=torch.float16 if device == "cuda" else torch.float32,
            device_map=device
        )
        print("Local model loaded successfully!")
        return _llm_instance, _tokenizer


def generate_response(model_tuple, prompt: str, system_prompt: str = None) -> str:
    """
    Generate response using the configured provider.
    
    Args:
        model_tuple: Output from load_model() (can be None for Gemini)
        prompt: User query
        system_prompt: Optional system instructions
    """
    if LLM_PROVIDER == "gemini":
        return _generate_gemini(prompt, system_prompt)
    else:
        return _generate_local(model_tuple, prompt, system_prompt)


def _generate_gemini(prompt: str, system_prompt: str = None) -> str:
    """Generate using Google Gemini API (New SDK)"""
    global _gemini_client
    try:
        if _gemini_client is None:
             _gemini_client = genai.Client(api_key=GEMINI_API_KEY)

        # Call the new API: client.models.generate_content
        
        # GEMMA FIX: Some models (like Gemma 3) do not support 'system_instruction' 
        # in the config. We detect if it's a Gemma model and move system prompt to the main content.
        is_gemma = "gemma" in GEMINI_MODEL_ID.lower()
        
        if is_gemma and system_prompt:
            # Format as a single sequence for Gemma
            gen_contents = f"System: {system_prompt}\n\nUser: {prompt}"
            gen_config = {
                'temperature': LLM_TEMPERATURE,
                'max_output_tokens': LLM_MAX_TOKENS,
            }
        else:
            # Standard Gemini approach
            gen_contents = prompt
            gen_config = {
                'system_instruction': system_prompt,
                'temperature': LLM_TEMPERATURE,
                'max_output_tokens': LLM_MAX_TOKENS,
            }

        response = _gemini_client.models.generate_content(
            model=GEMINI_MODEL_ID,
            contents=gen_contents,
            config=gen_config
        )
        
        return response.text
    except Exception as e:
        print(f"Gemini API Error: {e}")
        return f"Error connecting to AI service. Please try again. (Details: {str(e)})"


def _generate_local(model_tuple, prompt: str, system_prompt: str = None) -> str:
    """Generate using local HuggingFace model"""
    model, tokenizer = model_tuple
    
    messages = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    messages.append({"role": "user", "content": prompt})
    
    input_text = tokenizer.apply_chat_template(
        messages,
        tokenize=False,
        add_generation_prompt=True
    )
    
    inputs = tokenizer(input_text, return_tensors="pt")
    inputs = {k: v.to(model.device) for k, v in inputs.items()}
    
    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_new_tokens=LLM_MAX_TOKENS,
            temperature=LLM_TEMPERATURE if LLM_TEMPERATURE > 0 else 0.1,
            do_sample=True,
            pad_token_id=tokenizer.eos_token_id
        )
    
    response = tokenizer.decode(
        outputs[0][inputs['input_ids'].shape[1]:],
        skip_special_tokens=True
    )
    
    return response.strip()


if __name__ == "__main__":
    # Test script
    print("Testing LLM generation...")
    try:
        model_input = load_model()
        test_response = generate_response(
            model_input, 
            "Hello, are you online?", 
            system_prompt="You are a helpful assistant."
        )
        print(f"\nResponse: {test_response}")
    except Exception as e:
        print(f"\nTest failed: {e}")
