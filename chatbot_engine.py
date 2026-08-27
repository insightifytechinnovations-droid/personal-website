import os
import openai

# OpenAI API की सेटिंग्स (Render या आपके लोकल एनवायरनमेंट से की उठाएगा)
openai.api_key = os.environ.get("OPENAI_API_KEY")

def insightify_ai_bot(message):
    try:
        # OpenAI मॉडल को कॉल करके सही जवाब जनरेट करना
        response = openai.chat.completions.create(
            model="gpt-4o-mini",  # आप चाहें तो gpt-3.5-turbo भी रख सकते हैं
            messages=[
                {
                    "role": "system", 
                    "content": "You are a professional and helpful AI assistant for Insightify Tech Innovations Private Limited, an IT services and software development firm based in Hathras, Uttar Pradesh. Help clients with web development, SEO audits, and technical queries."
                },
                {
                    "role": "user", 
                    "content": message
                }
            ],
            max_tokens=500,
            temperature=0.7
        )
        
        # एआई का असली जवाब रिटर्न करना
        return response.choices[0].message.content.strip()
        
    except Exception as e:
        print(f"OpenAI API Error: {e}")
        return "माफ़ कीजिए, अभी हमारे एआई सर्वर से संपर्क नहीं हो पा रहा है। कृपया कुछ देर बाद प्रयास करें।"