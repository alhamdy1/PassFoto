# Detailed Installation Guide for PassFoto

## Prerequisites

### Python Installation

1. Download Python from [python.org](https://www.python.org/downloads/)
2. **Important for Windows**: Check "Add Python to PATH" during installation
3. Verify installation:
   ```bash
   python --version
   ```

### For Windows 8 Users

Windows 8 may require additional steps:

1. Install Visual C++ Redistributable:
   - Download from Microsoft's website
   - This is required for OpenCV

2. If you encounter SSL errors:
   - Update pip: `python -m pip install --upgrade pip`
   - Try: `pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org -r requirements.txt`

## Installation Methods

### Method 1: Quick Install (Recommended)

```bash
# Clone repository
git clone https://github.com/alhamdy1/PassFoto.git
cd PassFoto

# Install dependencies
pip install -r requirements.txt

# Run
python main.py
```

### Method 2: Virtual Environment (Recommended for Development)

```bash
# Create virtual environment
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Activate (Linux/Mac)
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run
python main.py
```

### Method 3: Install as Package

```bash
pip install .
passfoto
```

## Troubleshooting

### "DLL load failed" Error

Install Visual C++ Redistributable:
- [VC++ 2015-2022 x64](https://aka.ms/vs/17/release/vc_redist.x64.exe)

### "No module named cv2"

```bash
pip uninstall opencv-python
pip install opencv-python
```

### "tkinter not found"

On Ubuntu/Debian:
```bash
sudo apt-get install python3-tk
```

On Fedora:
```bash
sudo dnf install python3-tkinter
```

### Memory Issues (6GB RAM)

- Close other applications before running
- Process smaller images first
- Disable "Smooth Skin" for faster processing

## Verifying Installation

Run this to verify all dependencies are installed:

```python
python -c "import cv2; import numpy; import PIL; print('All dependencies OK!')"
```

## Updating

To update to the latest version:

```bash
cd PassFoto
git pull
pip install -r requirements.txt --upgrade
```
