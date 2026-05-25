# इस फाइल को चलाएं और ये अपने आप sitemap.xml बना देगी
xml_content = """<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url>
    <loc>https://insightifytech.in/</loc>
    <changefreq>daily</changefreq>
  </url>
</urlset>"""

with open("sitemap.xml", "w") as f:
    f.write(xml_content)

print("सफलता! आपके रूट फोल्डर में sitemap.xml बन गई है।")