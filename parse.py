import spacy
import re
from langchain_ollama import OllamaLLM

# Initialize Mistral Model (Make sure you have the proper setup to run Mistral)
llm = OllamaLLM(model="mistral")

def parse_with_ollama(dom_content, query):
    """Parses the given DOM content based on user instructions using Mistral."""
    try:
        if isinstance(dom_content, list):
            print("⚠️ Warning: dom_content is a list. Converting to string.")
            dom_content = "\n".join(dom_content)  # Convert list to string

        if not isinstance(dom_content, str):
            return "❌ Error: Expected a string but received something else."

        if not dom_content.strip():
            return "⚠️ No content available for extraction."

        print("🔍 DEBUG: Sending content to AI model...")
        prompt = f"Extract information based on the following query: {query}\nContent: {dom_content}"
        response = llm.invoke(prompt)

        if not response:
            return "⚠️ No relevant content extracted."

        response = response.strip()

        print("✅ DEBUG: AI Extraction Successful!")
        return response

    except Exception as e:
        print(f"❌ [ERROR] Parsing failed: {e}")
        return "Error extracting content. Please try again."

def summarize_with_mistral(dom_content):
    """Generates a summary of the given DOM content using Mistral."""
    try:
        if isinstance(dom_content, list):
            print("⚠️ Warning: dom_content is a list. Converting to string.")
            dom_content = "\n".join(dom_content)  # Convert list to string

        if not isinstance(dom_content, str):
            return "❌ Error: Expected a string but received something else."

        if not dom_content.strip():
            return "⚠️ No content to summarize."

        print("🔍 DEBUG: Sending content to AI model for summarization...")
        prompt = f"Summarize: {dom_content}"
        response = llm.invoke(prompt)

        if not response:
            return "⚠️ No summary generated."

        print("✅ DEBUG: AI Summary Successful!")
        return response.strip()

    except Exception as e:
        print(f"❌ [ERROR] Summarization failed: {e}")
        return "Error generating summary. Please try again."
