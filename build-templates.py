#!/usr/bin/env python3
"""
Simple template builder for Design Archive
Generates HTML files from templates/layout-base.html
"""

import os
import re
from pathlib import Path

def read_file(filepath):
    """Read file content"""
    with open(filepath, 'r', encoding='utf-8') as f:
        return f.read()

def write_file(filepath, content):
    """Write content to file"""
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

def extract_content_from_html(html_content):
    """Extract content between <div id="main"> and </div> (the main content area)"""
    # Look for content between the main div tags
    pattern = r'<div id="main">\s*<div class="inner">(.*?)</div>\s*</div>'
    match = re.search(pattern, html_content, re.DOTALL)
    if match:
        return match.group(1).strip()
    return ""

def extract_title_from_html(html_content):
    """Extract title from existing HTML"""
    pattern = r'<title>(.*?)</title>'
    match = re.search(pattern, html_content)
    if match:
        title = match.group(1)
        # Remove the suffix if it exists
        title = title.replace(' - James Sukanto Design Archive', '')
        title = title.replace('James Sukanto Design Archive', '')
        title = title.strip()
        if not title:
            return "James Sukanto Design Archive"
        return title
    return "James Sukanto Design Archive"

def extract_additional_head_from_html(html_content):
    """Extract any additional head content (like custom styles)"""
    # Look for style tags in head
    pattern = r'<style>(.*?)</style>'
    matches = re.findall(pattern, html_content, re.DOTALL)
    if matches:
        return '\n'.join([f'<style>{match}</style>' for match in matches])
    return ""

def build_page(template_content, title, content, additional_head=""):
    """Build a page from template with given content"""
    result = template_content
    result = result.replace('{{TITLE}}', title)
    result = result.replace('{{CONTENT}}', content)
    result = result.replace('{{ADDITIONAL_HEAD}}', additional_head)
    return result

def main():
    """Main build function"""
    print("🔨 Building HTML files from template...")
    
    # Read template
    template_path = 'templates/layout-base.html'
    if not os.path.exists(template_path):
        print(f"❌ Template not found: {template_path}")
        return
    
    template_content = read_file(template_path)
    print(f"✅ Loaded template: {template_path}")
    
    # Find all HTML files that need to be rebuilt
    html_files = [
        'index.html',
        'about.html',
        'proj_aisg.html',
        'proj_boots.html', 
        'proj_changi_ar.html',
        'proj_changi_emer.html',
        'proj_perx.html',
        'proj_vr_click.html',
        'proj_vr_peri.html',
        'proj_wine.html'
    ]
    
    rebuilt_count = 0
    
    for html_file in html_files:
        if os.path.exists(html_file):
            print(f"🔄 Processing: {html_file}")
            
            # Read existing file
            existing_content = read_file(html_file)
            
            # Extract components
            title = extract_title_from_html(existing_content)
            content = extract_content_from_html(existing_content)
            additional_head = extract_additional_head_from_html(existing_content)
            
            # Build new page
            new_content = build_page(template_content, title, content, additional_head)
            
            # Write to file
            write_file(html_file, new_content)
            print(f"✅ Rebuilt: {html_file}")
            rebuilt_count += 1
        else:
            print(f"⚠️  File not found: {html_file}")
    
    print(f"\n🎉 Build complete! Rebuilt {rebuilt_count} files.")
    print("📧 All pages now include the footer with email contact.")

if __name__ == "__main__":
    main() 