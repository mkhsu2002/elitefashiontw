import os
from datetime import datetime
import xml.etree.ElementTree as ET
from xml.dom import minidom

def generate_sitemap():
    base_url = "https://tw.elitefasion.com/"
    root_dir = "."
    sitemap_file = "sitemap.xml"
    
    # Files to exclude
    exclude_files = ["404.html", "sitemap.xml", "google", "yandex", "bing"]
    
    urlset = ET.Element("urlset", xmlns="http://www.sitemaps.org/schemas/sitemap/0.9")
    
    # Walk through the directory
    for root, dirs, files in os.walk(root_dir):
        # Exclude hidden directories and .agent
        dirs[:] = [d for d in dirs if not d.startswith('.') and d != '.agent']
        
        for file in files:
            if file.endswith(".html"):
                if any(exclude in file for exclude in exclude_files):
                    continue
                
                # Get relative path
                rel_path = os.path.relpath(os.path.join(root, file), root_dir)
                if rel_path == ".":
                    continue
                
                # Normalize path for URL
                url_path = rel_path.replace(os.sep, '/')
                if url_path == "index.html":
                    url_path = ""
                
                full_url = base_url + url_path
                
                # Create URL entry
                url_elem = ET.SubElement(urlset, "url")
                ET.SubElement(url_elem, "loc").text = full_url
                
                # Set lastmod
                mtime = os.path.getmtime(os.path.join(root, file))
                lastmod = datetime.fromtimestamp(mtime).strftime('%Y-%m-%d')
                ET.SubElement(url_elem, "lastmod").text = lastmod
                
                # Set priority and changefreq
                priority = "0.6"
                changefreq = "monthly"
                
                if url_path == "":
                    priority = "1.0"
                    changefreq = "weekly"
                elif "/" not in url_path: # Top level pages
                    priority = "0.8"
                    changefreq = "weekly"
                
                ET.SubElement(url_elem, "changefreq").text = changefreq
                ET.SubElement(url_elem, "priority").text = priority

    # Prettify XML
    xml_str = ET.tostring(urlset, encoding="utf-8")
    reparsed = minidom.parseString(xml_str)
    pretty_xml = reparsed.toprettyxml(indent="  ")
    
    with open(sitemap_file, "w", encoding="utf-8") as f:
        f.write(pretty_xml)
    
    print(f"Sitemap generated: {os.path.abspath(sitemap_file)}")

if __name__ == "__main__":
    generate_sitemap()
