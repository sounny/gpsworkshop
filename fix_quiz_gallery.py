
import os
import re

# 1. Fix Quiz HTML Heart Emoji
quiz_path = 'G:\\My Drive\\git\\gpsworkshop-1\\quiz.html'
with open(quiz_path, 'r', encoding='utf-8', errors='ignore') as f:
    quiz_content = f.read()

# Use regex to find the footer love line and fix the heart
# Pattern: class="footer-love">Made with .*? by
quiz_pattern = re.compile(r'(class="footer-love">Made with )(.*?)( by)')
new_quiz_content = quiz_pattern.sub(r'\1❤️\3', quiz_content)

if new_quiz_content != quiz_content:
    print("Fixing quiz.html heart emoji...")
    with open(quiz_path, 'w', encoding='utf-8') as f:
        f.write(new_quiz_content)
else:
    print("No changes needed for quiz.html heart.")

# 2. Fix Gallery CSS for White Text
gallery_path = 'G:\\My Drive\\git\\gpsworkshop-1\\gallery.html'
with open(gallery_path, 'r', encoding='utf-8', errors='ignore') as f:
    gallery_content = f.read()

# Force white text on headers and captions
# We'll inject a style block at the end of the <head> to override previous styles
style_override = """
    <style>
        .gallery-header h1, .gallery-header p {
            color: white !important;
        }
        .gallery-overlay h3, .gallery-overlay p {
            color: white !important;
        }
        .story-caption h3, .story-caption p {
            color: white !important;
        }
        /* Ensure overlay is visible if desired, or at least readable when shown */
        .gallery-overlay {
            color: white !important;
            /* text-shadow: 0 1px 3px rgba(0,0,0,0.8); */
        }
    </style>
</head>
"""

if style_override.strip() not in gallery_content:
    # distinct marker to avoid double insertion
    marker = "/* gallery-white-text-fix */"
    if marker not in gallery_content:
        new_style = style_override.replace("</head>", f"    {marker}\n    </style>\n</head>")
        # Actually, let's just replace </head> with our block
        new_gallery_content = gallery_content.replace('</head>', f'{style_override}')
        
        print("Updating gallery.html styles...")
        with open(gallery_path, 'w', encoding='utf-8') as f:
            f.write(new_gallery_content)
    else:
         print("Gallery styles already fixed.")
else:
    print("Gallery styles already fixed.")
