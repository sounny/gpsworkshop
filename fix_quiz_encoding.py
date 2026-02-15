
import os

file_path = 'G:\\My Drive\\git\\gpsworkshop-1\\quiz.html'

with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
    content = f.read()

# We need to detect the "mojibake" or just replace the string if it was saved that way.
# The tool might have returned "â†" but the file might actually be valid UTF-8 that the tool displayed as latin1.
# HOWEVER, the User says "on the quiz page there is still an issue... â†". 
# This implies the BROWSER sees it as "â†", which means the file is likely UTF-8 but the browser is forcing a different encoding 
# OR the file was double-encoded.
# If the file has `<meta charset="UTF-8">`, it should be fine if it IS UTF-8.
# If it shows as "â†" in a UTF-8 aware viewer, it means the bytes in the file ARE "â†" (0xC3 0xA2 0xE2 0x80 ... wait).
# "â" is 0xE2 in Latin-1. "†" is 0x2020 which is not a single byte in Latin-1.
# 0xE2 0x86 0x90 is UTF-8 for ←.
# If viewed as cp1252:
# 0xE2 -> â
# 0x86 -> †
# 0x90 -> (undefined/control) or sometimes displayed as space?

# If the user sees "â†", it means the file contains 0xE2 0x86 0x90 but is being interpreted as cp1252 (or similar).
# But the file *says* <meta charset="UTF-8">.
# So if the browser obeys that, and *still* shows "â†", it means the file *actually contains* the UTF-8 bytes for "â†" (i.e. double encoding):
# "â" (UTF-8: 0xC3 0xA2) + "†" (UTF-8: 0xE2 0x80 0xA0) etc.

# BUT, the `view_file` output showed "â†". The agent environment likely reads as UTF-8.
# If `view_file` (which reads as UTF-8) shows "â†", then the file *actually* has the characters "â†" in it (so it's double encoded or just wrong chars).
# So I should simple replace "â†" with "&larr;" and "â†’" with "&rarr;".

new_content = content.replace("â†", "&larr;").replace("â†’", "&rarr;")
# For the heart: "â ¤ï¸ "
new_content = new_content.replace("â ¤ï¸", "❤️")

if new_content != content:
    print("Replaced content.")
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
else:
    print("No replacement made. Trying fallback patterns.")
    # Fallback: maybe the space is different or "ï¸" is special
    # Try simpler replace
    new_content = content.replace("Field Testing</a>", "&larr; Field Testing</a>")
    new_content = new_content.replace(">Back to Home", ">Back to Home &rarr;")
    new_content = new_content.replace("Made with", "Made with ❤️")
    
    # This is destructive if I'm not careful, but "Field Testing</a>" is unique in that line?
    # Actually "nav-btn prev">â† Field Testing</a>"
    # Let's try replacing the corrupted string with the entities by context
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
