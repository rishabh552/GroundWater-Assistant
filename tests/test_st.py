import sys
import traceback

try:
    import sentence_transformers
    print(f"sentence_transformers version: {sentence_transformers.__version__}")
    import torch
    print(f"torch version: {torch.__version__}")
    print(f"CUDA available: {torch.cuda.is_available()}")
except Exception:
    traceback.print_exc()
