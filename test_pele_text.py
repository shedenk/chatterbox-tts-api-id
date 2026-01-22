#!/usr/bin/env python3
"""
Test script for Pelé text processing
Tests normalization, chunking, and validation for the specific Indonesian text
"""

import sys
import os

# Add app to path
sys.path.append(os.getcwd())

from app.core.text_processing import (
    normalize_text,
    split_text_for_long_generation,
    split_text_into_chunks
)

# The exact text from the user that's causing issues
PELE_TEXT = """bukan hanya legenda Brasil, tapi ikon sepak bola dunia. Ia memenangkan tiga Piala Dunia dan menunjukkan bahwa sepak bola bisa menjadi bahasa universal. Gaya bermainnya penuh kreativitas, insting tajam, dan kemampuan mencetak gol dari berbagai situasi. Di masanya, Pelé membuat dunia jatuh cinta pada sepak bola dan mengangkat olahraga ini ke level global."""

def test_normalization():
    """Test text normalization"""
    print("=" * 80)
    print("TEST 1: TEXT NORMALIZATION")
    print("=" * 80)
    
    print(f"\nOriginal text ({len(PELE_TEXT)} chars):")
    print(f"  {PELE_TEXT[:100]}...")
    
    normalized = normalize_text(PELE_TEXT)
    
    print(f"\nNormalized text ({len(normalized)} chars):")
    print(f"  {normalized[:100]}...")
    
    # Check for the é character
    if 'é' in PELE_TEXT:
        print(f"\n✅ Original contains 'é': {PELE_TEXT.count('é')} occurrence(s)")
    
    if 'é' in normalized:
        print(f"❌ FAIL: Normalized text still contains 'é'")
        return False
    else:
        print(f"✅ PASS: 'é' was successfully normalized to 'e'")
    
    # Check for any high-unicode characters
    high_unicode = [ch for ch in normalized if ord(ch) > 127]
    if high_unicode:
        print(f"⚠️  Warning: {len(high_unicode)} high-unicode characters remain: {set(high_unicode)}")
        return False
    else:
        print(f"✅ PASS: No high-unicode characters in normalized text")
    
    return True

def test_chunking():
    """Test text chunking"""
    print("\n" + "=" * 80)
    print("TEST 2: TEXT CHUNKING (Regular)")
    print("=" * 80)
    
    normalized = normalize_text(PELE_TEXT)
    chunks = split_text_into_chunks(normalized, max_length=150)
    
    print(f"\nSplit into {len(chunks)} chunks:")
    for i, chunk in enumerate(chunks, 1):
        print(f"  Chunk {i} ({len(chunk)} chars): {chunk[:60]}...")
        
        # Verify each chunk has no problematic characters
        high_unicode = [ch for ch in chunk if ord(ch) > 127]
        if high_unicode:
            print(f"    ❌ FAIL: Chunk has high-unicode: {set(high_unicode)}")
            return False
        else:
            print(f"    ✅ Clean")
    
    print(f"\n✅ PASS: All chunks are properly normalized")
    return True

def test_long_text_chunking():
    """Test long text chunking (for background processing)"""
    print("\n" + "=" * 80)
    print("TEST 3: LONG TEXT CHUNKING")
    print("=" * 80)
    
    # For testing, we'll repeat the text to make it "long"
    long_text = (PELE_TEXT + " ") * 10  # Make it about 3500 chars
    
    print(f"\nLong text length: {len(long_text)} chars")
    
    chunks = split_text_for_long_generation(long_text, max_chunk_size=1000)
    
    print(f"Split into {len(chunks)} chunks:")
    for i, chunk_obj in enumerate(chunks, 1):
        chunk_text = chunk_obj.text
        print(f"  Chunk {i} ({chunk_obj.character_count} chars): {chunk_text[:60]}...")
        
        # Verify each chunk has no problematic characters
        high_unicode = [ch for ch in chunk_text if ord(ch) > 127]
        if high_unicode:
            print(f"    ❌ FAIL: Chunk has high-unicode: {set(high_unicode)}")
            return False
        else:
            print(f"    ✅ Clean")
    
    print(f"\n✅ PASS: All long-text chunks are properly normalized")
    return True

def test_utf8_encoding():
    """Test UTF-8 encoding/decoding"""
    print("\n" + "=" * 80)
    print("TEST 4: UTF-8 ENCODING")
    print("=" * 80)
    
    normalized = normalize_text(PELE_TEXT)
    
    try:
        # Encode to UTF-8
        encoded = normalized.encode('utf-8')
        print(f"✅ UTF-8 encoding successful: {len(encoded)} bytes")
        
        # Decode back
        decoded = encoded.decode('utf-8')
        if decoded == normalized:
            print(f"✅ Round-trip encoding/decoding successful")
            return True
        else:
            print(f"❌ FAIL: Text changed after round-trip")
            return False
    except Exception as e:
        print(f"❌ FAIL: Encoding error: {e}")
        return False

def main():
    """Run all tests"""
    print("\n" + "🧪 " * 20)
    print("PELÉ TEXT PROCESSING TEST SUITE")
    print("🧪 " * 20 + "\n")
    
    tests = [
        ("Normalization", test_normalization),
        ("Chunking", test_chunking),
        ("Long Text Chunking", test_long_text_chunking),
        ("UTF-8 Encoding", test_utf8_encoding),
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"\n❌ {test_name} CRASHED: {e}")
            import traceback
            traceback.print_exc()
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 80)
    print("TEST SUMMARY")
    print("=" * 80)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status}: {test_name}")
    
    print(f"\n{'✨ ALL TESTS PASSED' if passed == total else '⚠️  SOME TESTS FAILED'}")
    print(f"Results: {passed}/{total} tests passed\n")
    
    return 0 if passed == total else 1

if __name__ == "__main__":
    sys.exit(main())
