from parse import summarize_with_mistral

test_content = "Amazon is an online marketplace where users can buy and sell products."
print("🔍 Testing Mistral Summarization...")
summary = summarize_with_mistral(test_content)
print(f"🛠 Raw Summary Output: {summary}")
