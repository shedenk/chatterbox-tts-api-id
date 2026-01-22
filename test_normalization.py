import sys
import os

# Add app to path
sys.path.append(os.getcwd())

from app.core.text_processing import normalize_text

test_cases = [
    ("Indonesian text with “smart quotes” and – dashes.", 'Indonesian text with "smart quotes" and - dashes.'),
    ("Ellipsis… and weird glottal stopʼ marks", "Ellipsis... and weird glottal stop' marks"),
    ("Accents: éèêë áàâä íìîï", "Accents: eeee aaaa iiii"),
    ("Control characters \x00\x01\x02 test", "Control characters  test"),
    ("Mix: Peléʼs “quote”—test…", "Pele's \"quote\"-test...")
]

print("🔍 Starting Text Normalization Verification...")
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
    print("\n✨ All normalization tests passed!")
else:
    print("\n⚠️ Some normalization tests failed.")
    sys.exit(1)
