#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Fix encoding issues in quiz.html"""

import os

file_path = r'g:\My Drive\git\gpsworkshop\quiz.html'

# Read the file with explicit UTF-8 encoding
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Create a dictionary of replacements for double-encoded UTF-8 chars
replacements = {
    'ðŸ"¡': '📡',
    'ðŸŽ¯': '🎯',
    'ðŸ§ ': '🧠',
    'âœ…': '✅',
    'âŒ': '❌',
    'â†': '←',
    'â†'': '→',
    'â€¢': '•',
    'â¤ï¸': '❤️',
    'Â°': '°',
}

# Apply replacements
for old, new in replacements.items():
    content = content.replace(old, new)

# Write back with UTF-8 encoding
with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print('Done - encoding fixed!')
