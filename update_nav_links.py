
import os
import re

directory = r'G:\My Drive\git\gpsworkshop-1'
files = [f for f in os.listdir(directory) if f.endswith('.html')]

# Navigation Menu Update
gallery_li = '<li><a href="gallery.html">Memories</a></li>'

for filename in files:
    filepath = os.path.join(directory, filename)
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    
    # 1. Add Gallery/Memories to Navbar if missing
    if 'gallery.html' not in content:
        # Regex to find the last <li> inside <ul class="nav-menu">
        # This is a simple approach, looking for the closing </ul> of the menu
        # We assume standard formatting like the index.html we saw
        nav_pattern = re.compile(r'(<ul class="nav-menu">.*?)(</ul>)', re.DOTALL)
        
        def add_nav_item(match):
            ul_content = match.group(1)
            closing_tag = match.group(2)
            # Append inside
            return f'{ul_content}\n                {gallery_li}\n            {closing_tag}'
            
        new_content = nav_pattern.sub(add_nav_item, content)
    else:
        new_content = content

    # 2. Fix Quiz Page Specifics
    if filename == 'quiz.html':
        # Fix the corrupted arrows
        # Previous fix might have left "&larr;’" or "â†"
        # We saw "&larr;  " and "Back to Home &larr;’"
        new_content = new_content.replace("&larr;’", "&rarr;") # Fix broken right arrow
        new_content = new_content.replace("&larr;  ", "&larr; ") # Fix extra space if any
        new_content = new_content.replace("â†", "&larr;") 
        new_content = new_content.replace("â†’", "&rarr;")
        
        # Replace "Back to Home" with "Memories"
        # Only target the specific link at the bottom
        # <a href="index.html" class="nav-btn next">Back to Home &rarr;</a>
        # Regex to capture the href and text
        quiz_next_pattern = re.compile(r'<a href="index\.html" class="nav-btn next">[^<]+</a>')
        new_content = quiz_next_pattern.sub(r'<a href="gallery.html" class="nav-btn next">Memories &rarr;</a>', new_content)

    if new_content != content:
        print(f"Updating {filename}...")
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
    else:
        print(f"No changes for {filename}")

print("Done.")
