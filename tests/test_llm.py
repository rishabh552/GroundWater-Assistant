"""Convenience wrapper to load and test the Granite model."""
from backend.llm import generate_response, load_model


def main():
    print("Testing Granite model loading...")
    model_tuple = load_model()

    test_prompt = "What is groundwater and why is it important?"
    print(f"\nTest prompt: {test_prompt}")

    response = generate_response(model_tuple, test_prompt)
    print(f"\nResponse: {response}")


if __name__ == "__main__":
    main()
