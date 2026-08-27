import os
import google.generativeai as genai

# Google Gemini API की सेटिंग्स (Render या आपके लोकल एनवायरनमेंट से GEMINI_API_KEY उठाएगा)
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))

def insightify_ai_bot(message):
    try:
        # सिस्टम प्रॉम्प्ट और यूजर मैसेज को मिलाकर Gemini के लिए तैयार करना
        system_instruction = (
            "You are a professional and helpful AI assistant for Insightify Tech Innovations Private Limited, "
            "an IT services and software development firm based in Hathras, Uttar Pradesh. "
            "Help clients with web development, SEO audits, and technical queries. "
            "कृपया आवश्यकतानुसार हिंदी भाषा में भी सहायता करें।"
        )
        
        # सही और लेटेस्ट Gemini मॉडल सेट करना
        model = genai.GenerativeModel(
            model_name="gemini-1.5-flash",
            system_instruction=system_instruction
        )
        
        # मैसेज भेजकर जवाब जनरेट करना
        response = model.generate_content(message)
        
        # एआई का असली जवाब रिटर्न करना
        return response.text.strip()
        
    except Exception as e:
        print(f"Gemini API Error: {e}")
        return "माफ़ कीजिए, अभी हमारे एआई सर्वर से संपर्क नहीं हो पा रहा है। कृपया कुछ देर बाद प्रयास करें।"