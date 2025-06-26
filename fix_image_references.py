#!/usr/bin/env python3
"""
Fix Image References Script

This script fixes HTML references to images that were converted from PNG to JPG
but the HTML still references the old PNG extension.
"""

import os
import re
from pathlib import Path

def fix_image_references():
    """Fix all broken image references in HTML files"""
    
    # List of images that were converted from PNG to JPG
    converted_images = [
        'aisg14', 'boots3', 'changiar1', 'changiar2', 'changiem1', 'changiem6',
        'changiem7', 'changiem8', 'changiem10', 'changiem11', 'changiem12', 
        'changiem13', 'changiem14', 'perx1', 'vrclick1', 'vrclick2', 'vrperi2',
        'wine2', 'wine3', 't_boots', 't_changi_ar', 't_changi_emer', 't_perx',
        't_vr_click', 't_vr_saber', 't_wine'
    ]
    
    # Get all HTML files
    html_files = list(Path('.').glob('*.html'))
    
    for html_file in html_files:
        print(f"Checking {html_file}...")
        
        try:
            with open(html_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            original_content = content
            
            # Fix each converted image reference
            for image_name in converted_images:
                # Pattern to match the image reference
                pattern = f'images/{image_name}\.png'
                replacement = f'images/{image_name}.jpg'
                
                if pattern in content:
                    content = content.replace(pattern, replacement)
                    print(f"  ✅ Fixed: {pattern} → {replacement}")
            
            # Write back if changes were made
            if content != original_content:
                with open(html_file, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f"  📝 Updated {html_file}")
            else:
                print(f"  ✓ No changes needed for {html_file}")
                
        except Exception as e:
            print(f"  ❌ Error processing {html_file}: {str(e)}")

def verify_images():
    """Verify that all referenced images actually exist"""
    print("\n" + "="*50)
    print("VERIFYING IMAGE REFERENCES")
    print("="*50)
    
    html_files = list(Path('.').glob('*.html'))
    missing_images = []
    
    for html_file in html_files:
        try:
            with open(html_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Find all image references
            image_refs = re.findall(r'images/([^"\'>\s]+)', content)
            
            for image_ref in image_refs:
                image_path = Path('images') / image_ref
                if not image_path.exists():
                    missing_images.append((str(html_file), image_ref))
                    
        except Exception as e:
            print(f"Error checking {html_file}: {str(e)}")
    
    if missing_images:
        print("❌ MISSING IMAGES FOUND:")
        for html_file, image_ref in missing_images:
            print(f"  {html_file}: images/{image_ref}")
    else:
        print("✅ All image references are valid!")
    
    return len(missing_images) == 0

def main():
    print("🔧 FIXING IMAGE REFERENCES")
    print("="*50)
    
    # Fix HTML references
    fix_image_references()
    
    # Verify all images exist
    all_good = verify_images()
    
    print("\n" + "="*50)
    if all_good:
        print("✅ SUCCESS: All image references fixed!")
        print("Your website should now display all images correctly.")
    else:
        print("⚠️  Some images are still missing. Check the list above.")
    print("="*50)

if __name__ == "__main__":
    main() 