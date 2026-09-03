import os
import openai

def insightify_ai_bot(message):
    try:
        # क्लाइंट को फंक्शन के अंदर इनिशियलाइज किया गया है ताकि रनटाइम पर .env लोड हो सके
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            return "माफ़ कीजिए, OpenAI API Key सेट नहीं है।"
            
        client = openai.OpenAI(api_key=api_key)
        
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system", 
                    "content": (
                        "You are a professional and helpful AI assistant for Insightify Tech Innovations Private Limited, "
                        "an IT services and software development firm based in Hathras, Uttar Pradesh. Help clients with "
                        "web development, SEO audits, and technical queries.\n\n"
                        "CRITICAL INSTRUCTION: Always detect the language of the user's input message and respond in that "
                        "exact same language. If the user types in Hindi, reply in Hindi. If they type in English, reply in English. "
                        "If they use Hinglish, respond in a natural conversational Hinglish style."
                    )
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