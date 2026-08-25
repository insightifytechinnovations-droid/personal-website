import os

def update_seo_meta(page_path, new_keywords, new_description):
    """
    Yeh function aapki website ki HTML files mein meta tags ko update karega.
    """
    # HTML file ko read karna
    with open(page_path, 'r', encoding='utf-8') as file:
        content = file.read()

    # Meta Tags ko replace karna
    updated_content = content.replace("<!--KEYWORDS-->", new_keywords)
    updated_content = content.replace("<!--DESCRIPTION-->", new_description)

    # File ko save karna
    with open(page_path, 'w', encoding='utf-8') as file:
        file.write(updated_content)

    print(f"SEO Updated for {page_path}")

# Automated Daily Task (Example: Trends ke hisab se keywords)
def run_daily_seo():
    trending_keywords = "AI Automation, Web Development, SEO Services, Insightify Tech, Hathras IT"
    trending_desc = "Insightify Tech Innovations: Top AI automated business scaling services."
    
    # Apni sabhi main files ko update karein
    update_seo_meta("templates/index.html", trending_keywords, trending_desc)

# System har 24 ghante mein ise chalayega