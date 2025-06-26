# 🚀 Quick Video Compression Solutions (No Installation Required)

## Option A: Online Compressors (Fastest - 2-5 minutes)

### 1. **VideoSmaller.com** (Recommended)
- Go to: https://www.videosmaller.com/
- Upload `changiemV.mp4` (47MB)
- Set compression to "Low Compression" (keeps good quality)
- Expected result: 3-8MB file
- **Download and replace the original file**

### 2. **Compress-Video-Online.com**
- Go to: https://compress-video-online.com/
- Upload your video
- Choose "Medium" compression
- Expected result: 4-10MB file

### 3. **CloudConvert.com**
- Go to: https://cloudconvert.com/mp4-converter
- Upload video → Convert to MP4
- Set quality to 720p, bitrate to 1000-2000 kbps
- Expected result: 2-6MB file

## Option B: Quick Python Script (If you want to try without ffmpeg)

Create a simple script that creates a poster image from the video and suggests replacement:

```python
# Run this if you want to replace video with poster temporarily
import os
from PIL import Image

# Create a placeholder poster image
def create_video_poster():
    # Create a simple poster image
    poster = Image.new('RGB', (1280, 720), '#131313')
    poster.save('images/changiemV_poster.jpg', 'JPEG', quality=85)
    print("Created poster image: images/changiemV_poster.jpg")

create_video_poster()
```

## Option C: Immediate HTML Fix (Removes autoplay)

Replace the video tag in `proj_changi_emer.html` line 59:

**From:**
```html
<video 
  src="images/changiemV.mp4" 
  style="width: 100%;" 
  controls 
  autoplay 
  muted 
  loop>
</video>
```

**To:**
```html
<video 
  src="images/changiemV.mp4" 
  style="width: 100%;" 
  controls 
  preload="metadata"
  poster="images/changiemV_poster.jpg">
</video>
```

This stops autoplay and only loads when user clicks play!

## 🎯 **RECOMMENDED: Option A + Option C**

1. **Use VideoSmaller.com** to compress the video (5 minutes)
2. **Remove autoplay** from the HTML (1 minute)
3. **Test the page** - should load instantly now!

## Target Results:
- **Current**: 47MB autoplay video (6+ minutes loading on mobile)
- **After**: 3-8MB click-to-play video (3-5 seconds loading)
- **Performance gain**: 85-95% improvement! 