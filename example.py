#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Generate example images for testing the image converter.

I created this script to make test images for my converter.
It's a quick way to generate sample images in different formats.
"""

from PIL import Image, ImageDraw, ImageFont
import os

def create_test_image(filename="test_image.png", width=800, height=600):
    """Create a simple test image with some shapes and text."""
    # Create a new image with a blue background
    img = Image.new('RGB', (width, height), color=(73, 109, 137))
    
    # Create a drawing object
    d = ImageDraw.Draw(img)
    
    # Draw a white rectangle with red outline
    d.rectangle([(width//4, height//4), (width*3//4, height*3//4)], 
                fill=(255, 255, 255), outline=(255, 0, 0), width=5)
    
    # Draw a green circle with blue outline
    d.ellipse([(width//3, height//3), (width*2//3, height*2//3)], 
              fill=(0, 255, 0), outline=(0, 0, 255), width=5)
    
    # Add some text
    try:
        # Try to load a font, use default if not available
        font = ImageFont.truetype("arial.ttf", 36)
    except IOError:
        font = ImageFont.load_default()
    
    d.text((width//2, height//5), "ImageConverter Test Image", 
           fill=(255, 255, 0), font=font, anchor="mm")
    
    # Save the image
    img.save(filename)
    print(f"Test image created: {filename}")
    
    return filename

def create_test_images_folder(folder_name="test_images", count=5):
    """Create a folder with test images in different formats."""
    # Create the folder if it doesn't exist
    os.makedirs(folder_name, exist_ok=True)
    
    # Create a subfolder for recursive testing
    subfolder = os.path.join(folder_name, "subfolder")
    os.makedirs(subfolder, exist_ok=True)
    
    # Image formats to create
    formats = [
        ("jpg", "JPEG"),
        ("png", "PNG"),
        ("webp", "WEBP"),
        ("bmp", "BMP"),
        ("tiff", "TIFF")
    ]
    
    created_files = []
    
    # Create images in the main folder
    for i in range(count):
        for ext, format_name in formats:
            filename = os.path.join(folder_name, f"test_image_{i+1}.{ext}")
            img = Image.new('RGB', (400, 300), color=(73, 109, 137))
            d = ImageDraw.Draw(img)
            d.text((200, 150), f"Test Image {i+1} - {format_name}", 
                   fill=(255, 255, 0), anchor="mm")
            img.save(filename, format=format_name)
            created_files.append(filename)
    
    # Create images in the subfolder
    for i in range(2):
        for ext, format_name in formats[:2]:  # Only JPG and PNG in subfolder
            filename = os.path.join(subfolder, f"subtest_image_{i+1}.{ext}")
            img = Image.new('RGB', (400, 300), color=(137, 73, 109))
            d = ImageDraw.Draw(img)
            d.text((200, 150), f"Subfolder Test {i+1} - {format_name}", 
                   fill=(0, 255, 255), anchor="mm")
            img.save(filename, format=format_name)
            created_files.append(filename)
    
    print(f"Created {len(created_files)} test images in '{folder_name}' folder.")
    return created_files

if __name__ == "__main__":
    # Create a single test image
    create_test_image()
    
    # Create a folder of test images
    create_test_images_folder() 