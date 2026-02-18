import os
from PIL import Image, ImageDraw

def create_icon(size, filename):
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Blue Circle
    draw.ellipse([0, 0, size, size], fill=(59, 130, 246))
    
    # White Text/Shape (Simplified for visibility)
    padding = size // 4
    draw.rectangle([padding, padding, size-padding, size-padding], fill=(255, 255, 255))

    img.save(filename)
    print(f"Generated {filename}")

# Generate icons
create_icon(16, "icon16.png")
create_icon(48, "icon48.png")
create_icon(128, "icon128.png")
print("✅ Icons created successfully!")