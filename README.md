# PassFoto - Passport Photo Enhancement Application

[![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)](https://www.python.org/)
[![Windows](https://img.shields.io/badge/Windows-8%2B-0078D6.svg)](https://www.microsoft.com/windows)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

**PassFoto** is a Windows-compatible desktop application for enhancing formal/passport photos. It features automatic face detection, image straightening, color correction, and many other enhancements to make your passport photos look professional.

![PassFoto Screenshot](docs/screenshot.png)

## ✨ Features

- **🔄 Auto Straighten**: Automatically detects and corrects tilted/rotated photos based on face and eye detection
- **🎨 Auto Enhancement**: Improves overall image quality using advanced histogram equalization
- **⚪ White Balance**: Automatically corrects color cast for natural skin tones
- **🔇 Denoise**: Removes image noise while preserving details
- **✨ Skin Smoothing**: Optional skin softening effect for portrait photos
- **🔪 Sharpen**: Enhances image sharpness for crisp details
- **👁️ Red Eye Removal**: Automatically detects and removes red eye effect
- **✂️ Smart Cropping**: Auto-crops to standard passport photo sizes with proper face positioning
- **🖼️ Background Change**: Replace background with solid colors (white, blue, gray, etc.)
- **💡 Brightness/Contrast**: Manual adjustment controls for fine-tuning

## 📋 System Requirements

- **Operating System**: Windows 8, 8.1, 10, or 11 (64-bit recommended)
- **RAM**: Minimum 4GB, Recommended 6GB or more
- **Python**: 3.7 or higher
- **Disk Space**: 500MB for application and dependencies

## 🚀 Installation

### Option 1: Install from Source

1. **Clone the repository**:
   ```bash
   git clone https://github.com/alhamdy1/PassFoto.git
   cd PassFoto
   ```

2. **Create a virtual environment** (recommended):
   ```bash
   python -m venv venv
   
   # On Windows:
   venv\Scripts\activate
   
   # On Linux/Mac:
   source venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**:
   ```bash
   python main.py
   ```

### Option 2: Install via pip

```bash
pip install passfoto
passfoto
```

## 📖 Usage Guide

### Opening an Image

1. Click **"📂 Open Image"** or press `Ctrl+O`
2. Select your photo file (supports JPG, PNG, BMP, TIFF, GIF)
3. The original image will appear in the left panel

### Applying Enhancements

1. Select the enhancement options you want:
   - ✅ **Auto Straighten** - Fix tilted photos
   - ✅ **Auto Enhance** - Improve overall quality
   - ✅ **White Balance** - Correct colors
   - ✅ **Denoise** - Remove noise
   - ☐ **Smooth Skin** - Soften skin (optional)
   - ✅ **Sharpen** - Increase sharpness
   - ✅ **Remove Red Eyes** - Fix red eye

2. Click **"🔄 Apply Enhancements"**
3. The enhanced image will appear in the right panel

### Cropping to Passport Size

1. Select your target photo size from the dropdown:
   - 2x2 inch (US)
   - 35x45 mm (EU)
   - 35x35 mm
   - 33x48 mm (Indonesia)
   - 51x51 mm

2. Click **"✂️ Crop to Face"**
3. The image will be automatically cropped and resized

### Changing Background

1. Click **"🎨 Change Background"**
2. Select your desired background color
3. Click **"Apply"**

### Manual Adjustments

Use the **Brightness** and **Contrast** sliders for fine-tuning:
- Brightness: -100 to +100
- Contrast: -100 to +100

### Saving Your Photo

1. Click **"💾 Save Image"** or press `Ctrl+S`
2. The enhanced photo is saved with "_enhanced" suffix
3. Or use **"Save As..."** (`Ctrl+Shift+S`) for custom filename

### Reset

Click **"↩️ Reset to Original"** to undo all changes and start over.

## 🖼️ Supported Photo Sizes

| Size Name | Dimensions | Common Use |
|-----------|------------|------------|
| 2x2 inch (US) | 600x600 px | US Passport, Visa |
| 35x45 mm (EU) | 413x531 px | European ID, Passport |
| 35x35 mm | 413x413 px | Various ID cards |
| 33x48 mm (Indonesia) | 390x567 px | Indonesian documents |
| 51x51 mm | 602x602 px | Special visas |

## ⌨️ Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| `Ctrl+O` | Open Image |
| `Ctrl+S` | Save Image |
| `Ctrl+Shift+S` | Save As |

## 🛠️ Technical Details

### Dependencies

- **OpenCV** (`opencv-python`): Image processing and face detection
- **NumPy**: Numerical operations
- **Pillow**: Image display in GUI
- **Tkinter**: GUI framework (included with Python)
- **ttkthemes**: Optional modern UI themes

### Face Detection

PassFoto uses OpenCV's Haar Cascade classifiers for:
- Face detection
- Eye detection (for rotation correction)

### Image Processing Pipeline

1. Load and validate image
2. Detect face and eyes
3. Calculate rotation angle
4. Apply corrections and enhancements
5. Crop and resize to target dimensions
6. Export in high quality

## 🔧 Troubleshooting

### "No face detected"

- Ensure the photo shows a clear frontal view of the face
- The face should not be obscured or too small
- Try a photo with better lighting

### "Could not load image"

- Check if the file is a valid image format
- Ensure the file is not corrupted
- Try converting to JPG or PNG

### Application runs slowly

- Close other resource-intensive applications
- Reduce image resolution before processing
- Disable unnecessary enhancements

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📧 Support

If you encounter any issues or have questions, please:
- Open an issue on GitHub
- Check the troubleshooting section above

## 🙏 Acknowledgments

- OpenCV team for the excellent computer vision library
- Python community for the amazing ecosystem

---

**Made with ❤️ for better passport photos**