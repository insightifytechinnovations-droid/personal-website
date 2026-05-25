import os
import openai

# API Key को सुरक्षित तरीके से लोड करें
openai.api_key = os.environ.get("OPENAI_API_KEY")

def generate_code_for_client(client_demand):
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "आप एक एक्सपर्ट सॉफ्टवेयर इंजीनियर हैं। क्लाइंट की जरूरत के हिसाब से प्रोफेशनल कोड लिखें।"},
            {"role": "user", "content": f"क्लाइंट की डिमांड: {client_demand}"}
        ]
    )
    return response.choices[0].message.content

def generate_product_ad(product_name, image_description):
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "आप एक एक्सपर्ट डिजिटल मार्केटर हैं। प्रोडक्ट की फोटो देखकर उसका विज्ञापन और खासियतें लिखें जिससे लोग उसे तुरंत खरीदें।"},
            {"role": "user", "content": f"प्रोडक्ट: {product_name}, विवरण: {image_description}। इसका एक आकर्षक विज्ञापन और 5 खासियतें लिखें।"}
        ]
    )
    return response.choices[0].message.content