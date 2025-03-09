# 🖼️ ImageConverter

![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Status](https://img.shields.io/badge/status-active-brightgreen)

Hey there! This is my **ImageConverter** tool I built to help myself (and now you!) convert images between different formats. I was tired of using online converters with ads and size limits, so I made this simple command-line tool that supports JPG, PNG, WebP, BMP, TIFF, and GIF formats.

## ✨ What It Does

I built this tool to:
- Convert images between different formats (obviously!)
- Process entire folders of images in one go
- Search through subfolders if needed
- Resize images while converting
- Adjust quality settings for JPG and WebP
- Convert images to grayscale when I need that vintage look

## 🚀 Getting Started

```bash
# Clone my repo
git clone https://github.com/ati2025/imageconverter.git
cd imageconverter

# Set up a virtual environment (I recommend this)
python -m venv venv
source venv/bin/activate  # Linux/Mac
# OR
venv\Scripts\activate  # Windows

# Install the stuff you need
pip install -r requirements.txt
```

## 💻 How To Use It

### Basic Conversion

This is the simplest way to convert a single image:

```bash
python image_converter.py -i input.jpg -o output.png
```

### Converting a Whole Folder

Got a bunch of images? No problem:

```bash
python image_converter.py -d input_folder -o output_folder -t png
```

### Including Subfolders

If your images are organized in subfolders:

```bash
python image_converter.py -d input_folder -o output_folder -t webp -r
```

### Resizing Images

Need to make images smaller or larger?

```bash
python image_converter.py -i input.jpg -o output.jpg -w 800 -h 600
```

### Adjusting Quality

For JPG or WebP, you can control the compression:

```bash
python image_converter.py -i input.jpg -o output.webp -q 85
```

## 📋 Command Options

| Parameter | Short | What it does |
|-----------|-------|--------------|
| `--input` | `-i` | The image file you want to convert |
| `--output` | `-o` | Where to save the converted image or folder |
| `--directory` | `-d` | A folder containing images to convert |
| `--type` | `-t` | Output format (jpg, png, webp, bmp, tiff, gif) |
| `--quality` | `-q` | Image quality (1-100, for JPG and WebP only) |
| `--width` | `-w` | Output width in pixels |
| `--height` | `-h` | Output height in pixels |
| `--recursive` | `-r` | Look through subfolders too |
| `--grayscale` | `-g` | Convert to black and white |
| `--help` | `-h` | Show help message |

## 📦 What You Need

I built this with:
- Pillow - For all the image processing magic
- tqdm - For those nice progress bars
- colorama - To make the terminal output look good

## 📝 License

I'm sharing this under the [MIT license](LICENSE), so feel free to use it however you want!

## 🤝 Want to Help?

Found a bug? Have an idea to make this better? Pull requests are welcome! Just open an issue first so we can discuss it.

## 🙏 Thanks

- [Pillow](https://python-pillow.org/) - Couldn't have done this without it
- Coffee - For keeping me awake while coding this
- You - For checking out my project! 