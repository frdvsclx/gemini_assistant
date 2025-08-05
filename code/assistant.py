import os
import requests #http istekleri icin

# API key'i doğrudan tanımla
api_key = "api_key"

url ="https://genyerativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"

headers = {"Content-Type": "application/json",  #json formatinda gonder
           "X-Google-API-Key": api_key } #yetkilndirme icin 

def get_gemini_response(promt: str) -> str: #gemini ana fonksiyon
    payload = {
        "contents": [
            { "parts": 
                [
                { "text": promt} #kullanici sorusu
                ]
            }
        ]
    }
        
    #geminiye api istegi gonder
    response = requests.post(url, headers=headers,json=payload)
        
    #istek basarili(http 200) ise cevabi dondur
    if response.status_code == 200:
        try:
            result = response.json() #json formatindaki yaniti dic cevir
            return result["candidates"][0]["content"]["parts"][0]["text"]
        except Exception as exp:
            return f"Hata: {exp}"
    else:
        return f"api hatasi: {response.status_code}: {response.text}"

if __name__ == "__main__":
    user_input = input("soru: ") #terminalden soru alma
    response = get_gemini_response(user_input) #geminiden alinan yanit return edilir
    print("gemini: ", response) 

