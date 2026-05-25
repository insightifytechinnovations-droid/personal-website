import os

# 45 पेजों की लिस्ट
pages = [
    "about", "contact", "services", "web-design", "seo", "app-dev", "software", 
    "marketing", "hosting", "domain", "graphics", "video-edit", "content", 
    "branding", "crm", "erp", "cloud", "security", "ai-solutions", "data-analytics",
    "ecommerce", "maintenance", "social-media", "email-marketing", "pay-per-click",
    "affiliate", "blogging", "ui-ux", "testing", "devops", "iot", "blockchain",
    "cyber-security", "machine-learning", "network", "api-dev", "database",
    "server-setup", "training", "consulting", "strategy", "support", "faq",
    "terms", "privacy"
]

# templates फोल्डर का पाथ
folder = "templates"

# फाइलें बनाने का लूप
for page in pages:
    with open(f"{folder}/{page}.html", "w", encoding="utf-8") as f:
        f.write(f"{{% extends 'base.html' %}}\n")
        f.write(f"{{% block content %}}\n")
        f.write(f"    <h1 class='text-4xl font-bold text-center'>{page.replace('-', ' ').title()}</h1>\n")
        f.write(f"    <p class='text-center mt-4'>Insightify Tech की यह सेवा {page.replace('-', ' ')} पर आधारित है।</p>\n")
        f.write(f"{{% endblock %}}")

print("बधाई हो! आपके 45 पेज तैयार हो गए हैं।")