#!/usr/bin/env python3
"""
Image Optimization Script for Design Archive Website

This script optimizes images for web performance by:
1. Resizing large images to appropriate web dimensions
2. Converting PNGs with transparent backgrounds to JPGs with matching background color
3. Compressing images to reduce file sizes
4. Updating all HTML references to the optimized images
"""

import os
import re
import shutil
from pathlib import Path
from PIL import Image, ImageOps
import subprocess
import logging

# Configuration
BACKGROUND_COLOR = '#131313'  # Website background color from CSS
MAX_WIDTH = 1920  # Maximum width for images
MAX_HEIGHT = 1080  # Maximum height for images
THUMBNAIL_MAX_WIDTH = 800  # Max width for thumbnail images (t_*.png)
JPEG_QUALITY = 85  # JPEG compression quality
PNG_COMPRESS_LEVEL = 6  # PNG compression level (0-9)

# File size thresholds (in bytes)
LARGE_FILE_THRESHOLD = 500 * 1024  # 500KB
VERY_LARGE_FILE_THRESHOLD = 1024 * 1024  # 1MB

def setup_logging():
    """Setup logging configuration"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('image_optimization.log'),
            logging.StreamHandler()
        ]
    )

def hex_to_rgb(hex_color):
    """Convert hex color to RGB tuple"""
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

def should_convert_to_jpg(image_path, file_size):
    """Determine if a PNG should be converted to JPG"""
    if not image_path.lower().endswith('.png'):
        return False
    
    # Convert large PNGs to JPG, but preserve small transparent PNGs
    if file_size > LARGE_FILE_THRESHOLD:
        # Check if image has transparency
        try:
            with Image.open(image_path) as img:
                return img.mode in ('RGBA', 'LA') or 'transparency' in img.info
        except Exception:
            return False
    return False

def optimize_image(input_path, output_path, is_thumbnail=False):
    """Optimize a single image"""
    try:
        original_size = os.path.getsize(input_path)
        logging.info(f"Processing {input_path} (Original size: {original_size / 1024:.1f}KB)")
        
        with Image.open(input_path) as img:
            # Convert to RGB if necessary and handle transparency
            if img.mode in ('RGBA', 'LA'):
                # Create background with website color
                background = Image.new('RGB', img.size, hex_to_rgb(BACKGROUND_COLOR))
                if img.mode == 'LA':
                    img = img.convert('RGBA')
                background.paste(img, mask=img.split()[-1])  # Use alpha channel as mask
                img = background
            elif img.mode == 'P':
                img = img.convert('RGB')
            
            # Resize image if needed
            max_w = THUMBNAIL_MAX_WIDTH if is_thumbnail else MAX_WIDTH
            max_h = int(max_w * 0.75)  # Maintain aspect ratio
            
            if img.width > max_w or img.height > max_h:
                img.thumbnail((max_w, max_h), Image.Resampling.LANCZOS)
                logging.info(f"Resized to {img.width}x{img.height}")
            
            # Determine output format
            output_ext = os.path.splitext(output_path)[1].lower()
            should_convert = should_convert_to_jpg(input_path, original_size)
            
            if should_convert and output_ext == '.png':
                # Convert to JPG
                output_path = output_path.replace('.png', '.jpg')
                img.save(output_path, 'JPEG', quality=JPEG_QUALITY, optimize=True)
                logging.info(f"Converted PNG to JPG")
            elif output_ext in ['.jpg', '.jpeg']:
                img.save(output_path, 'JPEG', quality=JPEG_QUALITY, optimize=True)
            else:
                img.save(output_path, 'PNG', optimize=True, compress_level=PNG_COMPRESS_LEVEL)
        
        new_size = os.path.getsize(output_path)
        reduction = ((original_size - new_size) / original_size) * 100
        logging.info(f"Optimized: {new_size / 1024:.1f}KB ({reduction:.1f}% reduction)")
        
        return output_path, original_size, new_size
        
    except Exception as e:
        logging.error(f"Error processing {input_path}: {str(e)}")
        return None, 0, 0

def check_ffmpeg():
    """Check if ffmpeg is available"""
    try:
        result = subprocess.run(['ffmpeg', '-version'], capture_output=True, text=True)
        return result.returncode == 0
    except FileNotFoundError:
        return False

def optimize_video(input_path, output_path):
    """Optimize video file using ffmpeg"""
    if not check_ffmpeg():
        logging.warning(f"FFmpeg not found. Skipping video optimization for {input_path}")
        logging.info("To install ffmpeg: brew install ffmpeg (on macOS) or apt install ffmpeg (on Ubuntu)")
        # Just copy the file without optimization
        shutil.copy2(input_path, output_path)
        original_size = os.path.getsize(input_path)
        return output_path, original_size, original_size
    
    try:
        original_size = os.path.getsize(input_path)
        logging.info(f"Processing video {input_path} (Original size: {original_size / (1024*1024):.1f}MB)")
        
        # Use ffmpeg to compress video
        cmd = [
            'ffmpeg', '-i', input_path,
            '-c:v', 'libx264',  # Use H.264 codec
            '-crf', '28',  # Constant Rate Factor (lower = better quality)
            '-preset', 'medium',  # Encoding speed/compression ratio
            '-c:a', 'aac',  # Audio codec
            '-b:a', '128k',  # Audio bitrate
            '-movflags', '+faststart',  # Optimize for web streaming
            '-y',  # Overwrite output file
            output_path
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode == 0:
            new_size = os.path.getsize(output_path)
            reduction = ((original_size - new_size) / original_size) * 100
            logging.info(f"Video optimized: {new_size / (1024*1024):.1f}MB ({reduction:.1f}% reduction)")
            return output_path, original_size, new_size
        else:
            logging.error(f"FFmpeg error: {result.stderr}")
            return None, 0, 0
            
    except Exception as e:
        logging.error(f"Error processing video {input_path}: {str(e)}")
        return None, 0, 0

def update_html_references(old_path, new_path):
    """Update all HTML files to reference the new optimized image"""
    html_files = list(Path('.').glob('*.html'))
    old_filename = os.path.basename(old_path)
    new_filename = os.path.basename(new_path)
    
    if old_filename == new_filename:
        return  # No change needed
    
    for html_file in html_files:
        try:
            with open(html_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Replace image references
            patterns = [
                f'images/{old_filename}',
                f'images\\{old_filename}',
                old_filename
            ]
            
            updated = False
            for pattern in patterns:
                if pattern in content:
                    replacement = pattern.replace(old_filename, new_filename)
                    content = content.replace(pattern, replacement)
                    updated = True
            
            if updated:
                with open(html_file, 'w', encoding='utf-8') as f:
                    f.write(content)
                logging.info(f"Updated references in {html_file}")
                
        except Exception as e:
            logging.error(f"Error updating {html_file}: {str(e)}")

def create_backup():
    """Create a backup of the original images"""
    backup_dir = Path('images_backup')
    images_dir = Path('images')
    
    if backup_dir.exists():
        logging.info("Backup already exists, skipping backup creation")
        return True
    
    try:
        logging.info("Creating backup of original images...")
        shutil.copytree(images_dir, backup_dir)
        logging.info(f"Backup created at {backup_dir}")
        return True
    except Exception as e:
        logging.error(f"Failed to create backup: {str(e)}")
        return False

def main():
    """Main optimization function"""
    setup_logging()
    
    # Create backup first
    if not create_backup():
        logging.error("Failed to create backup. Exiting for safety.")
        return
    
    # Create optimized images directory
    optimized_dir = Path('images_optimized')
    optimized_dir.mkdir(exist_ok=True)
    
    images_dir = Path('images')
    if not images_dir.exists():
        logging.error("Images directory not found!")
        return
    
    total_original_size = 0
    total_optimized_size = 0
    optimized_files = []
    
    # Get all image and video files
    image_extensions = ['.png', '.jpg', '.jpeg', '.gif']
    video_extensions = ['.mp4', '.mov', '.avi']
    
    all_files = []
    for ext in image_extensions + video_extensions:
        all_files.extend(images_dir.glob(f'*{ext}'))
        all_files.extend(images_dir.glob(f'*{ext.upper()}'))
    
    logging.info(f"Found {len(all_files)} files to process")
    
    for file_path in all_files:
        if file_path.is_file():
            output_path = optimized_dir / file_path.name
            is_thumbnail = file_path.name.startswith('t_')
            
            if file_path.suffix.lower() in video_extensions:
                result_path, orig_size, new_size = optimize_video(str(file_path), str(output_path))
            else:
                result_path, orig_size, new_size = optimize_image(str(file_path), str(output_path), is_thumbnail)
            
            if result_path:
                total_original_size += orig_size
                total_optimized_size += new_size
                optimized_files.append((str(file_path), result_path))
    
    # Replace original files with optimized versions
    logging.info("Replacing original files with optimized versions...")
    for original_path, optimized_path in optimized_files:
        try:
            # Update HTML references if filename changed
            update_html_references(original_path, optimized_path)
            
            # Replace original file
            shutil.move(optimized_path, original_path)
            logging.info(f"Replaced {original_path}")
            
        except Exception as e:
            logging.error(f"Error replacing {original_path}: {str(e)}")
    
    # Remove temporary directory
    try:
        optimized_dir.rmdir()
    except:
        pass
    
    # Summary
    total_reduction = ((total_original_size - total_optimized_size) / total_original_size) * 100 if total_original_size > 0 else 0
    logging.info("\n" + "="*50)
    logging.info("OPTIMIZATION SUMMARY")
    logging.info("="*50)
    logging.info(f"Files processed: {len(optimized_files)}")
    logging.info(f"Original total size: {total_original_size / (1024*1024):.1f}MB")
    logging.info(f"Optimized total size: {total_optimized_size / (1024*1024):.1f}MB")
    logging.info(f"Total reduction: {total_reduction:.1f}%")
    logging.info(f"Space saved: {(total_original_size - total_optimized_size) / (1024*1024):.1f}MB")

if __name__ == "__main__":
    main() 