#!/usr/bin/env python3
"""
Standalone test for Pelé text normalization
No external dependencies needed - tests only the normalization logic
"""

import unicodedata

# The exact text from the user that's causing issues
PELE_TEXT = """bukan hanya legenda Brasil, tapi ikon sepak bola dunia. Ia memenangkan tiga Piala Dunia dan menunjukkan bahwa sepak bola bisa menjadi bahasa universal. Gaya bermainnya penuh kreativitas, insting tajam, dan kemampuan mencetak gol dari berbagai situasi. Di masanya, Pelé membuat dunia jatuh cinta pada sepak bola dan mengangkat olahraga ini ke level global."""

def normalize_text_standalone(text):
    """Standalone version of normalize_text for testing"""
    if not text:
        return ""
    
    # Validate UTF-8 encoding
    try:
        text = text.encode('utf-8', errors='ignore').decode('utf-8')
    except Exception as e:
        print(f"⚠️  UTF-8 validation warning: {e}")
    
    # Use standard NFC normalization first
    text = unicodedata.normalize('NFC', text)
    
    # Track replacements for logging
    replacements_made = []
    
    # Comprehensive character replacement map
    replacements = {
        # Smart quotes
        '"': '"', '"': '"', ''': "'", ''': "'",
        # Various dashes and hyphens
        '–': '-', '—': '-', '−': '-', '‐': '-',
        # Ellipses
        '…': '...',
        # Common Latin accents (lowercase)
        'é': 'e', 'è': 'e', 'ê': 'e', 'ë': 'e', 'ē': 'e', 'ė': 'e', 'ę': 'e',
        'á': 'a', 'à': 'a', 'â': 'a', 'ä': 'a', 'ā': 'a', 'ã': 'a', 'å': 'a',
        'í': 'i', 'ì': 'i', 'î': 'i', 'ï': 'i', 'ī': 'i', 'į': 'i',
        'ó': 'o', 'ò': 'o', 'ô': 'o', 'ö': 'o', 'ō': 'o', 'õ': 'o', 'ø': 'o',
        'ú': 'u', 'ù': 'u', 'û': 'u', 'ü': 'u', 'ū': 'u', 'ũ': 'u',
        'ñ': 'n', 'ç': 'c',
        # Uppercase accented characters
        'É': 'E', 'È': 'E', 'Ê': 'E', 'Ë': 'E',
        'Á': 'A', 'À': 'A', 'Â': 'A', 'Ä': 'A',
        'Í': 'I', 'Ì': 'I', 'Î': 'I', 'Ï': 'I',
        'Ó': 'O', 'Ò': 'O', 'Ô': 'O', 'Ö': 'O',
        'Ú': 'U', 'Ù': 'U', 'Û': 'U', 'Ü': 'U',
        'Ñ': 'N', 'Ç': 'C',
        # glottal stop / hamzah marks
        'ʿ': "'", 'ʾ': "'", 'ʻ': "'", 'ʼ': "'", 'ʽ': "'",
        # Other common problematic characters
        '‚': ',', '„': '"', '‹': '<', '›': '>', '«': '"', '»': '"',
    }
    
    # Apply replacements and track what was changed
    for char, replacement in replacements.items():
        if char in text:
            count = text.count(char)
            replacements_made.append(f"'{char}'→'{replacement}' ({count}x)")
            text = text.replace(char, replacement)
    
    # Log replacements if any were made
    if replacements_made:
        print(f"🔄 Text normalization: {', '.join(replacements_made)}")
    
    # Remove control characters
    original_len = len(text)
    text = "".join(ch for ch in text if unicodedata.category(ch)[0] != "C" or ch in "\n\r\t")
    
    if len(text) != original_len:
        removed_count = original_len - len(text)
        print(f"🧹 Removed {removed_count} control character(s)")
    
    # Final validation
    high_unicode_chars = [ch for ch in text if ord(ch) > 127 and ch not in "\n\r\t"]
    if high_unicode_chars:
        unique_chars = list(set(high_unicode_chars))
        print(f"⚠️  Warning: {len(high_unicode_chars)} high-unicode characters remain: {unique_chars[:10]}")
    
    return text.strip()

def main():
    print("=" * 80)
    print("PELÉ TEXT NORMALIZATION TEST")
    print("=" * 80)
    
    print(f"\n📝 Original Text ({len(PELE_TEXT)} chars):")
    print(f"{PELE_TEXT}\n")
    
    # Check for special characters in original
    print("🔍 Character Analysis:")
    special_chars = []
    for ch in PELE_TEXT:
        if ord(ch) > 127:
            special_chars.append((ch, ord(ch), hex(ord(ch))))
    
    if special_chars:
        print(f"Found {len(special_chars)} non-ASCII character(s):")
        for ch, code, hexcode in set(special_chars):
            count = PELE_TEXT.count(ch)
            print(f"  '{ch}' (U+{hexcode[2:].upper().zfill(4)}, decimal {code}) - {count}x")
    else:
        print("  All characters are standard ASCII")
    
    # Test normalization
    print(f"\n🔄 Applying normalization...")
    normalized = normalize_text_standalone(PELE_TEXT)
    
    print(f"\n✅ Normalized Text ({len(normalized)} chars):")
    print(f"{normalized}\n")
    
    # Verify results
    print("=" * 80)
    print("VERIFICATION")
    print("=" * 80)
    
    all_passed = True
    
    # Test 1: Check if 'é' was replaced
    if 'é' in PELE_TEXT:
        if 'é' in normalized:
            print("❌ FAIL: 'é' still present in normalized text")
            all_passed = False
        else:
            print("✅ PASS: 'é' successfully replaced with 'e'")
    
    # Test 2: Check for any remaining high-unicode
    high_unicode = [ch for ch in normalized if ord(ch) > 127]
    if high_unicode:
        print(f"❌ FAIL: {len(high_unicode)} high-unicode character(s) remain: {set(high_unicode)}")
        all_passed = False
    else:
        print("✅ PASS: No high-unicode characters in normalized text")
    
    # Test 3: UTF-8 encoding test
    try:
        encoded = normalized.encode('utf-8')
        decoded = encoded.decode('utf-8')
        if decoded == normalized:
            print("✅ PASS: UTF-8 encoding/decoding round-trip successful")
        else:
            print("❌ FAIL: Text changed after UTF-8 round-trip")
            all_passed = False
    except Exception as e:
        print(f"❌ FAIL: UTF-8 encoding error: {e}")
        all_passed = False
    
    # Test 4: Check if text is safe for ASCII
    try:
        _ = normalized.encode('ascii', errors='strict')
        print("✅ PASS: Text is pure ASCII")
    except UnicodeEncodeError:
        print("⚠️  WARNING: Text contains non-ASCII characters (but this is OK for UTF-8)")
    
    print("\n" + "=" * 80)
    if all_passed:
        print("✨ ALL TESTS PASSED - Text is ready for TTS processing")
        print("=" * 80)
        return 0
    else:
        print("⚠️  SOME TESTS FAILED - Review the output above")
        print("=" * 80)
        return 1

if __name__ == "__main__":
    import sys
    sys.exit(main())
