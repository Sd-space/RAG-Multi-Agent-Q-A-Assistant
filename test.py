from openai import OpenAI

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key="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",  # Replace with your actual OpenRouter API key
)

try:
    response = client.chat.completions.create(
        model="openai/gpt-3.5-turbo-0613",
        messages=[{"role": "user", "content": "Hello!"}],
        extra_headers={
            "HTTP-Referer": "https://your-site.com",  # Optional
            "X-Title": "Test Script",                # Optional
        },
        extra_body={},
    )
    print("✅ API Key is working. Response:")
    print(response.choices[0].message.content)

except Exception as e:
    print("❌ API Key might be invalid or request failed:")
    print(e)
