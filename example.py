"""
Example script demonstrating how to use the OpenAI API function.
"""
import os
from main import run_llm
from data import format_prompt, parse_response

def main():
    # Make sure you have set your OpenAI API key in the environment
    if "OPENAI_API_KEY" not in os.environ:
        print("Please set your OPENAI_API_KEY environment variable.")
        print("You can do this by running: export OPENAI_API_KEY='your-api-key'")
        return
    
    # Example 1: Simple prompt
    print("Example 1: Simple prompt")
    response = run_llm("What is machine learning?")
    print(f"Response: {response}\n")
    
    # Example 2: Using a template prompt
    print("Example 2: Using a template prompt")
    topic = "artificial intelligence in healthcare"
    formatted_prompt = format_prompt("generate_ideas", topic=topic)
    print(f"Formatted prompt: {formatted_prompt}")
    
    response = run_llm(formatted_prompt)
    print(f"Raw response: {response}\n")
    
    # Example 3: Parsing the response
    print("Example 3: Parsing the response")
    parsed = parse_response(response)
    
    if parsed["type"] == "list":
        print("Parsed items:")
        for i, item in enumerate(parsed["items"], 1):
            print(f"{i}. {item}")
    else:
        print(f"Parsed content: {parsed['content']}")

if __name__ == "__main__":
    main()