#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
ImageConverter - A simple tool for converting images

I created this script to easily convert images between different formats
and do some basic image manipulation like resizing and changing color modes.
"""

import os
import sys
import argparse
import time
from pathlib import Path
from typing import List, Tuple, Optional, Dict, Union

try:
    from PIL import Image
    from tqdm import tqdm
    from colorama import init, Fore, Style
except ImportError:
    print("Missing dependencies. Please install required packages:")
    print("pip install -r requirements.txt")
    sys.exit(1)

# Initialize colorama
init(autoreset=True)

# Supported formats
SUPPORTED_FORMATS = {
    'jpg': 'JPEG',
    'jpeg': 'JPEG',
    'png': 'PNG',
    'webp': 'WEBP',
    'bmp': 'BMP',
    'tiff': 'TIFF',
    'gif': 'GIF'
}

def print_banner():
    """Display the program banner."""
    banner = f"""
{Fore.CYAN}╔══════════════════════════════════════════════════════════╗
{Fore.CYAN}║ {Fore.YELLOW}██╗███╗   ███╗ █████╗  ██████╗ ███████╗{Fore.CYAN}                ║
{Fore.CYAN}║ {Fore.YELLOW}██║████╗ ████║██╔══██╗██╔════╝ ██╔════╝{Fore.CYAN}                ║
{Fore.CYAN}║ {Fore.YELLOW}██║██╔████╔██║███████║██║  ███╗█████╗{Fore.CYAN}                  ║
{Fore.CYAN}║ {Fore.YELLOW}██║██║╚██╔╝██║██╔══██║██║   ██║██╔══╝{Fore.CYAN}                  ║
{Fore.CYAN}║ {Fore.YELLOW}██║██║ ╚═╝ ██║██║  ██║╚██████╔╝███████╗{Fore.CYAN}                ║
{Fore.CYAN}║ {Fore.YELLOW}╚═╝╚═╝     ╚═╝╚═╝  ╚═╝ ╚═════╝ ╚══════╝{Fore.CYAN}                ║
{Fore.CYAN}║ {Fore.GREEN} ██████╗ ██████╗ ███╗   ██╗██╗   ██╗███████╗██████╗ ████████╗{Fore.CYAN}███████╗██████╗  ║
{Fore.CYAN}║ {Fore.GREEN}██╔════╝██╔═══██╗████╗  ██║██║   ██║██╔════╝██╔══██╗╚══██╔══╝{Fore.CYAN}██╔════╝██╔══██╗ ║
{Fore.CYAN}║ {Fore.GREEN}██║     ██║   ██║██╔██╗ ██║██║   ██║█████╗  ██████╔╝   ██║   {Fore.CYAN}█████╗  ██████╔╝ ║
{Fore.CYAN}║ {Fore.GREEN}██║     ██║   ██║██║╚██╗██║╚██╗ ██╔╝██╔══╝  ██╔══██╗   ██║   {Fore.CYAN}██╔══╝  ██╔══██╗ ║
{Fore.CYAN}║ {Fore.GREEN}╚██████╗╚██████╔╝██║ ╚████║ ╚████╔╝ ███████╗██║  ██║   ██║   {Fore.CYAN}███████╗██║  ██║ ║
{Fore.CYAN}║ {Fore.GREEN} ╚═════╝ ╚═════╝ ╚═╝  ╚═══╝  ╚═══╝  ╚══════╝╚═╝  ╚═╝   ╚═╝   {Fore.CYAN}╚══════╝╚═╝  ╚═╝ ║
{Fore.CYAN}╚══════════════════════════════════════════════════════════╝
    """
    print(banner)
    print(f"{Fore.CYAN}Version: {Fore.WHITE}1.0.0")
    print(f"{Fore.CYAN}Created by: {Fore.WHITE}Ati")
    print(f"{Fore.CYAN}License: {Fore.WHITE}MIT")
    print()

def parse_arguments() -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="A tool for converting images between different formats",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    input_group = parser.add_mutually_exclusive_group(required=True)
    input_group.add_argument('-i', '--input', type=str, help='Input image file')
    input_group.add_argument('-d', '--directory', type=str, help='Input directory')
    
    parser.add_argument('-o', '--output', type=str, required=True, 
                        help='Output file or directory')
    parser.add_argument('-t', '--type', type=str, choices=list(SUPPORTED_FORMATS.keys()),
                        help='Output format')
    parser.add_argument('-q', '--quality', type=int, choices=range(1, 101), default=90,
                        help='Image quality (1-100, only for JPG and WebP)')
    parser.add_argument('-w', '--width', type=int, help='Output width')
    parser.add_argument('-h', '--height', type=int, help='Output height')
    parser.add_argument('-r', '--recursive', action='store_true', 
                        help='Search recursively in subdirectories')
    parser.add_argument('-g', '--grayscale', action='store_true',
                        help='Convert to grayscale')
    
    return parser.parse_args()

def get_output_format(output_path: str, specified_type: Optional[str] = None) -> str:
    """Determine the output format based on filename or specified type."""
    if specified_type:
        return SUPPORTED_FORMATS[specified_type.lower()]
    
    ext = os.path.splitext(output_path)[1].lower().replace('.', '')
    if ext in SUPPORTED_FORMATS:
        return SUPPORTED_FORMATS[ext]
    
    # Default format if not recognized
    return 'JPEG'

def process_image(
    input_path: str, 
    output_path: str, 
    output_format: str, 
    quality: int = 90, 
    width: Optional[int] = None, 
    height: Optional[int] = None, 
    grayscale: bool = False
) -> bool:
    """
    Process an image with the given parameters.
    
    Args:
        input_path: Path to the input image
        output_path: Path to save the output image
        output_format: Output format (PIL format name)
        quality: Image quality (1-100)
        width: Output width (optional)
        height: Output height (optional)
        grayscale: Convert to grayscale
        
    Returns:
        bool: Whether the conversion was successful
    """
    try:
        # Load the image
        img = Image.open(input_path)
        
        # Color mode conversion if needed
        if grayscale:
            img = img.convert('L')
        elif img.mode == 'RGBA' and output_format == 'JPEG':
            # JPEG doesn't support transparency, convert to RGB
            img = img.convert('RGB')
        
        # Resize if needed
        if width or height:
            # If only one dimension is specified, calculate the other proportionally
            if width and not height:
                wpercent = width / float(img.size[0])
                height = int(float(img.size[1]) * float(wpercent))
            elif height and not width:
                hpercent = height / float(img.size[1])
                width = int(float(img.size[0]) * float(hpercent))
            
            img = img.resize((width, height), Image.LANCZOS)
        
        # Create output directory if it doesn't exist
        os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
        
        # Save the image
        save_kwargs = {}
        if output_format in ['JPEG', 'WEBP']:
            save_kwargs['quality'] = quality
        if output_format == 'PNG':
            save_kwargs['optimize'] = True
        
        img.save(output_path, format=output_format, **save_kwargs)
        return True
    
    except Exception as e:
        print(f"{Fore.RED}Error processing image ({input_path}): {e}")
        return False

def find_image_files(directory: str, recursive: bool = False) -> List[str]:
    """
    Find all image files in the given directory.
    
    Args:
        directory: The directory to search
        recursive: Search recursively in subdirectories
        
    Returns:
        List[str]: List of found image files
    """
    image_files = []
    valid_extensions = tuple(f".{ext}" for ext in SUPPORTED_FORMATS.keys())
    
    if recursive:
        for root, _, files in os.walk(directory):
            for file in files:
                if file.lower().endswith(valid_extensions):
                    image_files.append(os.path.join(root, file))
    else:
        for file in os.listdir(directory):
            if file.lower().endswith(valid_extensions):
                image_files.append(os.path.join(directory, file))
    
    return image_files

def process_directory(
    input_dir: str, 
    output_dir: str, 
    output_format: str, 
    quality: int = 90, 
    width: Optional[int] = None, 
    height: Optional[int] = None, 
    recursive: bool = False, 
    grayscale: bool = False
) -> Tuple[int, int]:
    """
    Process a directory with the given parameters.
    
    Args:
        input_dir: Input directory
        output_dir: Output directory
        output_format: Output format
        quality: Image quality
        width: Output width
        height: Output height
        recursive: Search recursively in subdirectories
        grayscale: Convert to grayscale
        
    Returns:
        Tuple[int, int]: (number of successful conversions, total number of files)
    """
    # Find image files
    image_files = find_image_files(input_dir, recursive)
    
    if not image_files:
        print(f"{Fore.YELLOW}No image files found in the specified directory.")
        return 0, 0
    
    # Create output directory
    os.makedirs(output_dir, exist_ok=True)
    
    # Format extension
    ext = next((k for k, v in SUPPORTED_FORMATS.items() if v == output_format), 'jpg')
    
    # Processing
    success_count = 0
    
    print(f"{Fore.CYAN}Processing images...")
    for input_path in tqdm(image_files, unit="image"):
        # Calculate relative path for output file
        if recursive:
            rel_path = os.path.relpath(input_path, input_dir)
            rel_dir = os.path.dirname(rel_path)
            filename = os.path.splitext(os.path.basename(input_path))[0]
            
            # Create output directory if in recursive mode
            if rel_dir:
                os.makedirs(os.path.join(output_dir, rel_dir), exist_ok=True)
                output_path = os.path.join(output_dir, rel_dir, f"{filename}.{ext}")
            else:
                output_path = os.path.join(output_dir, f"{filename}.{ext}")
        else:
            filename = os.path.splitext(os.path.basename(input_path))[0]
            output_path = os.path.join(output_dir, f"{filename}.{ext}")
        
        # Process image
        if process_image(input_path, output_path, output_format, quality, width, height, grayscale):
            success_count += 1
    
    return success_count, len(image_files)

def main():
    """Main program."""
    # Display banner
    print_banner()
    
    # Parse arguments
    args = parse_arguments()
    
    start_time = time.time()
    
    # Process single image or directory
    if args.input:
        # Process single image
        if not os.path.isfile(args.input):
            print(f"{Fore.RED}Error: The specified input file does not exist.")
            return
        
        output_format = get_output_format(args.output, args.type)
        
        print(f"{Fore.CYAN}Processing image: {Fore.WHITE}{args.input}")
        print(f"{Fore.CYAN}Output format: {Fore.WHITE}{output_format}")
        
        if process_image(
            args.input, 
            args.output, 
            output_format, 
            args.quality, 
            args.width, 
            args.height, 
            args.grayscale
        ):
            print(f"{Fore.GREEN}Image successfully converted: {Fore.WHITE}{args.output}")
        else:
            print(f"{Fore.RED}An error occurred while converting the image.")
    
    else:
        # Process directory
        if not os.path.isdir(args.directory):
            print(f"{Fore.RED}Error: The specified input directory does not exist.")
            return
        
        if not args.type:
            print(f"{Fore.RED}Error: Output format must be specified (-t/--type) when processing a directory.")
            return
        
        output_format = SUPPORTED_FORMATS[args.type.lower()]
        
        print(f"{Fore.CYAN}Processing directory: {Fore.WHITE}{args.directory}")
        print(f"{Fore.CYAN}Output directory: {Fore.WHITE}{args.output}")
        print(f"{Fore.CYAN}Output format: {Fore.WHITE}{output_format}")
        print(f"{Fore.CYAN}Recursive mode: {Fore.WHITE}{'Yes' if args.recursive else 'No'}")
        
        success_count, total_count = process_directory(
            args.directory, 
            args.output, 
            output_format, 
            args.quality, 
            args.width, 
            args.height, 
            args.recursive, 
            args.grayscale
        )
        
        if total_count == 0:
            print(f"{Fore.YELLOW}No image files found in the specified directory.")
        else:
            print(f"{Fore.GREEN}Processing completed: {Fore.WHITE}{success_count}/{total_count} images successfully converted.")
    
    elapsed_time = time.time() - start_time
    print(f"{Fore.CYAN}Processing time: {Fore.WHITE}{elapsed_time:.2f} seconds")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}Processing interrupted by user.")
        sys.exit(0)
    except Exception as e:
        print(f"{Fore.RED}Unexpected error: {e}")
        sys.exit(1) 