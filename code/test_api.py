import requests

# API key'i test et
api_key = ""
url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"

headers = {
    "Content-Type": "application/json",
    "X-Google-API-Key": api_key
}

payload = {
    "contents": [
        {
            "parts": [
                {"text": "Merhaba, nasılsın?"}
            ]
        }
    ]
}

try:
    response = requests.post(url, headers=headers, json=payload)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.text}")
    
    if response.status_code == 200:
        result = response.json()
        print(f"AI Response: {result['candidates'][0]['content']['parts'][0]['text']}")
    else:
        print("API key geçersiz veya hata var!")
        
except Exception as e:
    print(f"Hata: {e}") 