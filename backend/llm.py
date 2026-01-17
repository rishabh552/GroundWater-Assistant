"""
LLM integration using HuggingFace Transformers with IBM Granite 3.0 8B
(Fallback when llama.cpp/ctransformers fail)
"""
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

from backend.config import (
    LLM_MODEL_ID,
    LLM_CONTEXT_LENGTH,
    LLM_TEMPERATURE,
    LLM_MAX_TOKENS,
)

# Model ID from config (can be overridden via environment variable)
MODEL_ID = LLM_MODEL_ID

# Global model instance (loaded once)
_llm_instance = None
_tokenizer = None


def load_model():
    """
    Load the Granite model using HuggingFace Transformers.
    Downloads the model on first run.
    Uses GPU if available for faster inference.
    """
    global _llm_instance, _tokenizer
    
    if _llm_instance is not None:
        return _llm_instance, _tokenizer
    
    # Check for GPU
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"Loading model: {MODEL_ID}")
    print(f"Using device: {device}")
    if device == "cuda":
        print(f"GPU: {torch.cuda.get_device_name(0)}")
    
    _tokenizer = AutoTokenizer.from_pretrained(MODEL_ID)
    _llm_instance = AutoModelForCausalLM.from_pretrained(
        MODEL_ID,
        torch_dtype=torch.float16 if device == "cuda" else torch.float32,
        device_map=device
    )
    
    print("Model loaded successfully!")
    return _llm_instance, _tokenizer


def generate_response(model_tuple, prompt: str, system_prompt: str = None) -> str:
    """
    Generate a response from the Granite model.
    
    Args:
        model_tuple: Tuple of (model, tokenizer)
        prompt: User query with context
        system_prompt: Optional system instructions
        
    Returns:
        Generated text response
    """
    model, tokenizer = model_tuple
    
    # Format messages for chat template
    messages = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    messages.append({"role": "user", "content": prompt})
    
    # Apply chat template
    input_text = tokenizer.apply_chat_template(
        messages,
        tokenize=False,
        add_generation_prompt=True
    )
    
    # Tokenize
    inputs = tokenizer(input_text, return_tensors="pt")
    
    # Move inputs to the same device as the model
    inputs = {k: v.to(model.device) for k, v in inputs.items()}
    
    # Generate
    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_new_tokens=LLM_MAX_TOKENS,
            temperature=LLM_TEMPERATURE if LLM_TEMPERATURE > 0 else 0.1,
            do_sample=True,
            pad_token_id=tokenizer.eos_token_id
        )
    
    # Decode only the new tokens
    response = tokenizer.decode(
        outputs[0][inputs['input_ids'].shape[1]:],
        skip_special_tokens=True
    )
    
    return response.strip()


# Test the model when run directly
if __name__ == "__main__":
    print("Testing Granite model loading...")
    model_tuple = load_model()
    
    test_prompt = "What is groundwater and why is it important?"
    print(f"\nTest prompt: {test_prompt}")
    
    response = generate_response(model_tuple, test_prompt)
    print(f"\nResponse: {response}")
