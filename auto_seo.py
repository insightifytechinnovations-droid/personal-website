import time
import os

def update_sitemap():
    # यह कोड आपके सभी 45 पेजों की एक लिस्ट बनाएगा और XML फाइल अपडेट करेगा
    pages = ["index", "services", "web-design", "seo", "app-dev"] # और भी जोड़ें
    with open("templates/sitemap.xml", "w") as f:
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n')
        for page in pages:
            f.write(f'  <url><loc>https://yourwebsite.com/{page}</loc></url>\n')
        f.write('</urlset>')
    print("Sitemap Updated Successfully!")

# हर 24 घंटे में चलने के लिए लूप
while True:
    update_sitemap()
    time.sleep(86400) # 24 घंटे का समय