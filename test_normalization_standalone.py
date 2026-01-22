import unicodedata

def normalize_text(text: str) -> str:
    """ Normalize text to remove or replace non-standard characters that might trip up the model """
    if not text:
        return ""
    
    # Use standard NFC normalization first
    text = unicodedata.normalize('NFC', text)
    
    # Replace common "smart" characters and symbols that are often problematic
    replacements = {
        # Smart quotes
        '“': '"', '”': '"', '‘': "'", '’': "'",
        # Various dashes and hyphens
        '–': '-', '—': '-', '−': '-', '‐': '-',
        # Ellipses
        '…': '...',
        # Accented characters (Indonesian sometimes uses these in names or loanwords)
        'é': 'e', 'è': 'e', 'ê': 'e', 'ë': 'e',
        'á': 'a', 'à': 'a', 'â': 'a', 'ä': 'a',
        'í': 'i', 'ì': 'i', 'î': 'i', 'ï': 'i',
        'ó': 'o', 'ò': 'o', 'ô': 'o', 'ö': 'o',
        'ú': 'u', 'ù': 'u', 'û': 'u', 'ü': 'u',
        'ñ': 'n', 'ç': 'c',
        # glottal stop / hamzah marks sometimes copy-pasted in Indonesian
        'ʿ': "'", 'ʾ': "'", 'ʻ': "'", 'ʼ': "'", 'ʽ': "'"
    }
    
    for char, replacement in replacements.items():
        if char in text:
            text = text.replace(char, replacement)
            
    # Remove other control characters and problematic non-printable chars
    text = "".join(ch for ch in text if unicodedata.category(ch)[0] != "C" or ch in "\n\r\t")
            
    return text.strip()

test_cases = [
    ("Indonesian text with “smart quotes” and – dashes.", 'Indonesian text with "smart quotes" and - dashes.'),
    ("Ellipsis… and weird glottal stopʼ marks", "Ellipsis... and weird glottal stop' marks"),
    ("Accents: éèêë áàâä íìîï", "Accents: eeee aaaa iiii"),
    ("Control characters \x00\x01\x02 test", "Control characters  test"),
    ("Mix: Peléʼs “quote”—test…", "Mix: Pele's \"quote\"-test...")
]

print("🔍 Starting Standalone Normalization Verification...")
success = True

for original, expected in test_cases:
    result = normalize_text(original)
    if result == expected:
        print(f"✅ PASS: [{original}] -> [{result}]")
    else:
        print(f"❌ FAIL: [{original}]")
        print(f"   Expected: [{expected}]")
        print(f"   Got:      [{result}]")
        success = False

if success:
    print("\n✨ All stabilization tests passed!")
else:
    import sys
    sys.exit(1)
