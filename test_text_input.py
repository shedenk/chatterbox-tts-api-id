#!/usr/bin/env python3
"""Test script to analyze the Pelé text and identify potential issues"""

# The problematic text from the user
test_text = """bukan hanya legenda Brasil, tapi ikon sepak bola dunia. Ia memenangkan tiga Piala Dunia dan menunjukkan bahwa sepak bola bisa menjadi bahasa universal. Gaya bermainnya penuh kreativitas, insting tajam, dan kemampuan mencetak gol dari berbagai situasi. Di masanya, Pelé membuat dunia jatuh cinta pada sepak bola dan mengangkat olahraga ini ke level global."""

print("=" * 80)
print("TEXT ANALYSIS")
print("=" * 80)
print(f"\nOriginal Text Length: {len(test_text)} characters")
print(f"\nOriginal Text:\n{test_text}")

# Analyze character composition
print("\n" + "=" * 80)
print("CHARACTER ANALYSIS")
print("=" * 80)

# Check for non-ASCII characters
non_ascii_chars = []
for i, char in enumerate(test_text):
    if ord(char) > 127:
        non_ascii_chars.append((i, char, ord(char), hex(ord(char))))

if non_ascii_chars:
    print(f"\nFound {len(non_ascii_chars)} non-ASCII characters:")
    for pos, char, code, hexcode in non_ascii_chars:
        print(f"  Position {pos}: '{char}' (U+{hexcode[2:].upper().zfill(4)}, decimal {code})")
else:
    print("\n✓ All characters are standard ASCII")

# Check for control characters
import unicodedata
control_chars = []
for i, char in enumerate(test_text):
    if unicodedata.category(char)[0] == "C" and char not in "\n\r\t":
        control_chars.append((i, char, ord(char)))

if control_chars:
    print(f"\n⚠️  Found {len(control_chars)} control characters:")
    for pos, char, code in control_chars:
        print(f"  Position {pos}: {repr(char)} (code {code})")
else:
    print("\n✓ No problematic control characters")

# Test basic normalization
print("\n" + "=" * 80)
print("NORMALIZATION TEST")
print("=" * 80)

import unicodedata

# Simple normalization
normalized_text = unicodedata.normalize('NFC', test_text)
print(f"\nNFC Normalized Length: {len(normalized_text)} characters")

if normalized_text != test_text:
    print("⚠️  Text changed after normalization")
    print(f"Difference: {len(test_text) - len(normalized_text)} characters")
else:
    print("✓ Text unchanged after NFC normalization")

# Check encoding
print("\n" + "=" * 80)
print("ENCODING TEST")
print("=" * 80)

try:
    utf8_encoded = test_text.encode('utf-8')
    print(f"✓ UTF-8 encoding successful: {len(utf8_encoded)} bytes")
    
    # Try decoding back
    decoded = utf8_encoded.decode('utf-8')
    if decoded == test_text:
        print("✓ Round-trip encoding/decoding successful")
    else:
        print("⚠️  Text changed after encoding/decoding round-trip")
except Exception as e:
    print(f"❌ Encoding error: {e}")

# Check sentence splitting
print("\n" + "=" * 80)
print("SENTENCE SPLITTING TEST")
print("=" * 80)

sentences = []
temp_text = test_text
sentence_endings = ['. ', '! ', '? ', '.\n', '!\n', '?\n']

while temp_text:
    best_split = len(temp_text)
    for ending in sentence_endings:
        pos = temp_text.find(ending)
        if pos != -1 and pos < best_split:
            best_split = pos + len(ending)
    
    if best_split == len(temp_text):
        sentences.append(temp_text)
        break
    else:
        sentences.append(temp_text[:best_split])
        temp_text = temp_text[best_split:]

print(f"Found {len(sentences)} sentences:")
for i, sentence in enumerate(sentences, 1):
    print(f"  {i}. ({len(sentence)} chars) {sentence[:60]}{'...' if len(sentence) > 60 else ''}")

print("\n" + "=" * 80)
print("SUMMARY")
print("=" * 80)
print(f"""
Text appears to be: {"CLEAN ✓" if not non_ascii_chars and not control_chars else "HAS SPECIAL CHARACTERS ⚠️"}
Suitable for processing: {"YES ✓" if len(test_text) > 0 else "NO ❌"}
Recommended action: {"Process directly" if not non_ascii_chars else "Apply normalization first"}
""")
