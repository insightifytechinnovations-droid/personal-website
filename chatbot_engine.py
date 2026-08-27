import os
import openai

# OpenAI API की सेटिंग्स (Render से OPENAI_API_KEY उठाएगा)
openai.api_key = os.environ.get("OPENAI_API_KEY")

def insightify_ai_bot(message):
    try:
        response = openai.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system", 
                    "content": "You are a professional and helpful AI assistant for Insightify Tech Innovations Private Limited, an IT services and software development firm based in Hathras, Uttar Pradesh. Help clients with web development, SEO audits, and technical queries. कृपया हिंदी में भी सहायता करें।"
                },
                {
                    "role": "user", 
                    "content": message
                }
            ],
            max_tokens=500,
            temperature=0.7
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"OpenAI API Error: {e}")
        return "माफ़ कीजिए, अभी हमारे एआई सर्वर से संपर्क नहीं हो पा रहा है। कृपया कुछ देर बाद प्रयास करें।"