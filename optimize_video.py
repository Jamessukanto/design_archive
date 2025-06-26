#!/usr/bin/env python3
"""
Video Optimization Script for changiemV.mp4

This script creates a compressed version of the large video file using different methods:
1. First tries ffmpeg if available
2. Falls back to creating a poster image and suggesting alternative solutions
"""

import os
import subprocess
import shutil
from pathlib import Path
from PIL import Image
import logging

def setup_logging():
    """Setup logging configuration"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )

def check_ffmpeg():
    """Check if ffmpeg is available"""
    try:
        result = subprocess.run(['ffmpeg', '-version'], capture_output=True, text=True)
        return result.returncode == 0
    except FileNotFoundError:
        return False

def optimize_video_with_ffmpeg(input_path, output_path):
    """Optimize video using ffmpeg"""
    try:
        original_size = os.path.getsize(input_path)
        logging.info(f"Optimizing {input_path} with ffmpeg (Original: {original_size / (1024*1024):.1f}MB)")
        
        cmd = [
            'ffmpeg', '-i', input_path,
            '-c:v', 'libx264',
            '-crf', '28',
            '-preset', 'medium',
            '-c:a', 'aac',
            '-b:a', '128k',
            '-movflags', '+faststart',
            '-vf', 'scale=1280:720',  # Reduce resolution
            '-y',
            output_path
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode == 0:
            new_size = os.path.getsize(output_path)
            reduction = ((original_size - new_size) / original_size) * 100
            logging.info(f"Video optimized: {new_size / (1024*1024):.1f}MB ({reduction:.1f}% reduction)")
            return True
        else:
            logging.error(f"FFmpeg error: {result.stderr}")
            return False
    except Exception as e:
        logging.error(f"Error: {str(e)}")
        return False

def create_alternative_solutions():
    """Create alternative solutions for the video"""
    video_path = Path('images/changiemV.mp4')
    
    logging.info("Creating alternative solutions for video optimization:")
    
    # Option 1: Convert to WebM format (smaller but requires ffmpeg)
    webm_script = '''
# Alternative Video Optimization Commands
# Run these commands if you have ffmpeg installed:

# Option 1: Convert to WebM (much smaller file size)
ffmpeg -i images/changiemV.mp4 -c:v libvpx-vp9 -crf 30 -b:v 0 -b:a 128k -c:a libopus images/changiemV.webm

# Option 2: Heavily compress MP4
ffmpeg -i images/changiemV.mp4 -c:v libx264 -crf 28 -preset medium -vf scale=1280:720 -c:a aac -b:a 128k -movflags +faststart images/changiemV_compressed.mp4

# Option 3: Create a very small preview version
ffmpeg -i images/changiemV.mp4 -c:v libx264 -crf 35 -preset medium -vf scale=640:360 -c:a aac -b:a 64k -movflags +faststart images/changiemV_preview.mp4
'''
    
    with open('video_optimization_commands.txt', 'w') as f:
        f.write(webm_script)
    
    logging.info("Created video_optimization_commands.txt with ffmpeg commands")
    
    # Option 2: Suggest replacing with poster image
    poster_html = '''
<!-- Alternative: Replace video with poster image and link -->
<div class="video-placeholder" onclick="window.open('path/to/video', '_blank')">
    <img src="images/changiemV_poster.jpg" alt="Video Preview" />
    <div class="play-button">▶️ Click to watch video</div>
</div>

<style>
.video-placeholder {
    position: relative;
    cursor: pointer;
    display: inline-block;
}
.play-button {
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    background: rgba(0,0,0,0.7);
    color: white;
    padding: 10px 20px;
    border-radius: 5px;
    font-size: 18px;
}
</style>
'''
    
    with open('video_poster_alternative.html', 'w') as f:
        f.write(poster_html)
    
    logging.info("Created video_poster_alternative.html with poster image suggestion")

def main():
    setup_logging()
    
    video_path = Path('images/changiemV.mp4')
    if not video_path.exists():
        logging.error("Video file not found!")
        return
    
    # Check current size
    current_size = os.path.getsize(video_path)
    logging.info(f"Current video size: {current_size / (1024*1024):.1f}MB")
    
    if check_ffmpeg():
        logging.info("FFmpeg found! Attempting video optimization...")
        compressed_path = 'images/changiemV_compressed.mp4'
        
        if optimize_video_with_ffmpeg(str(video_path), compressed_path):
            # Replace original with compressed version
            shutil.move(compressed_path, str(video_path))
            logging.info("Video successfully optimized and replaced!")
        else:
            logging.error("FFmpeg optimization failed")
            create_alternative_solutions()
    else:
        logging.warning("FFmpeg not found. Creating alternative solutions...")
        create_alternative_solutions()
        
        logging.info("""
RECOMMENDATIONS FOR VIDEO OPTIMIZATION:

1. Install ffmpeg and run the commands in video_optimization_commands.txt
2. Use an online video compressor like:
   - https://www.videosmaller.com/
   - https://compress-video-online.com/
   - https://www.media.io/video-compressor.html

3. Consider replacing the video with a poster image (see video_poster_alternative.html)

Target: Reduce the 47MB video to under 5MB for better web performance.
""")

if __name__ == "__main__":
    main() 