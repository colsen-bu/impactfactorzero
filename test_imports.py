#!/usr/bin/env python3
"""
Test script to verify imports work correctly
"""

# Test imports
try:
    import frontmatter
    print("✅ frontmatter imported successfully")
except ImportError as e:
    print(f"❌ frontmatter import failed: {e}")

try:
    import markdown
    print("✅ markdown imported successfully")
except ImportError as e:
    print(f"❌ markdown import failed: {e}")

try:
    from pathlib import Path
    print("✅ pathlib imported successfully")
except ImportError as e:
    print(f"❌ pathlib import failed: {e}")

# Test basic functionality
try:
    # Test frontmatter
    test_content = """---
title: Test Post
date: 2025-06-26
---
# Test content
This is a test."""
    
    post = frontmatter.loads(test_content)
    print(f"✅ frontmatter parsing works: {post.metadata['title']}")
    
    # Test markdown
    md = markdown.Markdown()
    html = md.convert(post.content)
    print(f"✅ markdown conversion works: {len(html)} characters")
    
except Exception as e:
    print(f"❌ Functionality test failed: {e}")

print("\n🎉 All tests completed!")
